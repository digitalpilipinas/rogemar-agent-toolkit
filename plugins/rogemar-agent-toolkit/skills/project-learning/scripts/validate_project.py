#!/usr/bin/env python3
"""Validate an initialized project-learning installation and its local data."""

from __future__ import annotations

import argparse
import importlib.util
import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path


_STORE_PATH = Path(__file__).resolve().with_name("candidate_store.py")
_STORE_SPEC = importlib.util.spec_from_file_location("project_learning_candidate_store", _STORE_PATH)
if _STORE_SPEC is None or _STORE_SPEC.loader is None:
    raise RuntimeError(f"unable to load candidate store from {_STORE_PATH}")
candidate_store = importlib.util.module_from_spec(_STORE_SPEC)
_STORE_SPEC.loader.exec_module(candidate_store)


BEGIN_MARKER = "<!-- BEGIN PROJECT LEARNING -->"
END_MARKER = "<!-- END PROJECT LEARNING -->"
LEDGER_MARKER = "<!-- PROJECT-LEARNING:ENTRIES -->"
HOOK_SCRIPT_NAME = "project-learning-stop.py"
EXPECTED_IGNORE = (
    ".codex/project-learning/candidates.jsonl",
    ".codex/project-learning/state/",
)


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Repository path; defaults to the current repository")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = candidate_store.resolve_root(args.root)
        config = candidate_store.config_for(root)
        store_path, state_dir, ledger_path = candidate_store.candidate_paths(root, config)

        agents_path = root / "AGENTS.md"
        require(agents_path.is_file(), f"missing {agents_path}")
        agents = agents_path.read_text(encoding="utf-8")
        require(agents.count(BEGIN_MARKER) == 1, "AGENTS begin marker must appear once")
        require(agents.count(END_MARKER) == 1, "AGENTS end marker must appear once")

        ignore_path = root / ".gitignore"
        require(ignore_path.is_file(), f"missing {ignore_path}")
        ignore_lines = ignore_path.read_text(encoding="utf-8").splitlines()
        for entry in EXPECTED_IGNORE:
            require(ignore_lines.count(entry) == 1, f"ignore entry must appear once: {entry}")

        hooks_path = root / ".codex/hooks.json"
        hooks = candidate_store.load_json(hooks_path)
        commands = []
        stack = [hooks]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                command = value.get("command")
                if isinstance(command, str) and HOOK_SCRIPT_NAME in command:
                    commands.append(command)
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
        require(len(commands) == 1, "exactly one project-learning hook command is required")

        hook_path = root / ".codex/hooks" / HOOK_SCRIPT_NAME
        require(hook_path.is_file(), f"missing {hook_path}")
        with tempfile.TemporaryDirectory(prefix="project-learning-pycache-") as cache_dir:
            py_compile.compile(
                str(hook_path),
                cfile=str(Path(cache_dir) / "project-learning-stop.pyc"),
                doraise=True,
            )

        require(ledger_path.is_file(), f"missing {ledger_path}")
        ledger = ledger_path.read_text(encoding="utf-8")
        require(ledger.count(LEDGER_MARKER) == 1, "ledger marker must appear once")
        for match in re.finditer(r"^##\s+(PL-[A-F0-9]{12})\s*$", ledger, re.M):
            section = ledger[match.start() :]
            next_heading = re.search(r"^##\s+PL-[A-F0-9]{12}\s*$", section[match.end() - match.start() :], re.M)
            if next_heading:
                section = section[: match.end() - match.start() + next_heading.start()]
            require(
                re.search(r"^Status: (?:Accepted|Reinforced|Superseded)$", section, re.M)
                is not None,
                f"ledger entry {match.group(1)} has invalid status",
            )

        events = candidate_store.load_events(store_path)
        candidate_store.materialize(events)
        for event in events:
            candidate_store.reject_forbidden_keys(event, "event")

        result = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", str(store_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        require(result.returncode == 0, "candidate store is not ignored by Git")
        state_probe = state_dir / "probe.json"
        result = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", str(state_probe)],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        require(result.returncode == 0, "state directory is not ignored by Git")

        print(
            json.dumps(
                {
                    "valid": True,
                    "root": str(root),
                    "enabled": config["enabled"],
                    "candidate_events": len(events),
                    "accepted_entries": len(
                        re.findall(r"^##\s+PL-[A-F0-9]{12}\s*$", ledger, re.M)
                    ),
                },
                indent=2,
            )
        )
        return 0
    except (
        ValidationFailure,
        candidate_store.StoreError,
        OSError,
        py_compile.PyCompileError,
    ) as exc:
        print(f"project-learning validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
