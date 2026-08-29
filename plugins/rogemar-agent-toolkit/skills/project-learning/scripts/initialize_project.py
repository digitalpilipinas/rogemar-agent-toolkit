#!/usr/bin/env python3
"""Idempotently initialize project-local continuous learning."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


BEGIN_MARKER = "<!-- BEGIN PROJECT LEARNING -->"
END_MARKER = "<!-- END PROJECT LEARNING -->"
HOOK_SCRIPT_NAME = "project-learning-stop.py"
HOOK_COMMAND = (
    'python3 -I "$(git rev-parse --show-toplevel)/.codex/hooks/'
    + HOOK_SCRIPT_NAME
    + '"'
)
IGNORE_ENTRIES = (
    ".codex/project-learning/candidates.jsonl",
    ".codex/project-learning/state/",
)


class InitializationError(RuntimeError):
    pass


def resolve_root(raw_root: str | None) -> Path:
    cwd = Path(raw_root).expanduser().resolve() if raw_root else Path.cwd()
    result = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise InitializationError(f"not a Git repository: {cwd}")
    return Path(result.stdout.strip()).resolve()


def atomic_write(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        if mode is not None:
            os.chmod(temp_name, mode)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InitializationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InitializationError(f"expected a JSON object in {path}")
    return value


def hook_commands(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        command = value.get("command")
        if isinstance(command, str):
            found.append(command)
        for child in value.values():
            found.extend(hook_commands(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(hook_commands(child))
    return found


def merged_hooks(path: Path) -> tuple[str | None, str]:
    if path.exists():
        data = load_json(path)
    else:
        data = {"hooks": {}}
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise InitializationError(f"`hooks` must be an object in {path}")

    related = [command for command in hook_commands(data) if HOOK_SCRIPT_NAME in command]
    if related:
        if related == [HOOK_COMMAND]:
            return None, "project-learning Stop hook already present"
        raise InitializationError(
            "an ambiguous project-learning hook already exists: " + ", ".join(related)
        )

    stop_groups = hooks.setdefault("Stop", [])
    if not isinstance(stop_groups, list):
        raise InitializationError(f"`hooks.Stop` must be an array in {path}")
    stop_groups.append(
        {
            "hooks": [
                {
                    "type": "command",
                    "command": HOOK_COMMAND,
                    "timeout": 5,
                    "statusMessage": "Checking project learning signals",
                }
            ]
        }
    )
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n", "add Stop hook"


def merged_agents(existing: str, section: str, path: Path) -> tuple[str | None, str]:
    begin_count = existing.count(BEGIN_MARKER)
    end_count = existing.count(END_MARKER)
    if begin_count != end_count or begin_count > 1:
        raise InitializationError(f"ambiguous Project Learning markers in {path}")
    if begin_count == 1:
        return None, "Project Learning AGENTS block already present"
    prefix = existing
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    if prefix and not prefix.endswith("\n\n"):
        prefix += "\n"
    return prefix + section.rstrip() + "\n", "add AGENTS policy block"


def merged_gitignore(existing: str) -> tuple[str | None, str]:
    lines = existing.splitlines()
    missing = [entry for entry in IGNORE_ENTRIES if entry not in lines]
    if not missing:
        return None, "candidate and state paths already ignored"
    output = existing
    if output and not output.endswith("\n"):
        output += "\n"
    if output and not output.endswith("\n\n"):
        output += "\n"
    output += "# Project-local learning candidates and turn state\n"
    output += "\n".join(missing) + "\n"
    return output, "add project-learning ignore entries"


def validate_existing_config(path: Path) -> None:
    data = load_json(path)
    required = {
        "schema_version": 1,
        "capture_policy": "signal-gated",
        "promotion_policy": "review-required",
        "storage_policy": "structured-summaries-only",
    }
    for key, expected in required.items():
        if data.get(key) != expected:
            raise InitializationError(f"unsupported {key!r} in {path}")
    if not isinstance(data.get("enabled"), bool):
        raise InitializationError(f"`enabled` must be boolean in {path}")


def set_enabled(root: Path, enabled: bool, check: bool) -> list[str]:
    path = root / ".codex/project-learning/config.json"
    if not path.exists():
        raise InitializationError("project learning is not initialized")
    data = load_json(path)
    validate_existing_config(path)
    if data.get("enabled") is enabled:
        return [f"unchanged: learning already {'enabled' if enabled else 'disabled'}"]
    if not check:
        data["enabled"] = enabled
        atomic_write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return [f"{'would ' if check else ''}set enabled={str(enabled).lower()}"]


def initialize(root: Path, check: bool) -> list[str]:
    skill_root = Path(__file__).resolve().parents[1]
    assets = skill_root / "assets"
    changes: list[tuple[Path, str, int | None, str]] = []
    messages: list[str] = []

    agents_path = root / "AGENTS.md"
    agents_existing = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    agents_content, message = merged_agents(
        agents_existing,
        (assets / "agents-section.md").read_text(encoding="utf-8"),
        agents_path,
    )
    messages.append(message)
    if agents_content is not None:
        changes.append((agents_path, agents_content, None, message))

    ignore_path = root / ".gitignore"
    ignore_existing = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
    ignore_content, message = merged_gitignore(ignore_existing)
    messages.append(message)
    if ignore_content is not None:
        changes.append((ignore_path, ignore_content, None, message))

    hooks_path = root / ".codex/hooks.json"
    hooks_content, message = merged_hooks(hooks_path)
    messages.append(message)
    if hooks_content is not None:
        changes.append((hooks_path, hooks_content, None, message))

    managed_assets = (
        (assets / HOOK_SCRIPT_NAME, root / ".codex/hooks" / HOOK_SCRIPT_NAME, 0o755),
        (assets / "config.json", root / ".codex/project-learning/config.json", None),
        (assets / "lessons.md", root / "docs/project-learning/lessons.md", None),
    )
    for source, destination, mode in managed_assets:
        desired = source.read_text(encoding="utf-8")
        if destination.exists():
            if destination.name == "config.json":
                validate_existing_config(destination)
                messages.append("project-learning config already present")
                continue
            current = destination.read_text(encoding="utf-8")
            if current != desired:
                raise InitializationError(f"managed file differs from the skill asset: {destination}")
            messages.append(f"managed file already present: {destination.relative_to(root)}")
            continue
        label = f"add {destination.relative_to(root)}"
        messages.append(label)
        changes.append((destination, desired, mode, label))

    if not check:
        for path, content, mode, _ in changes:
            atomic_write(path, content, mode)
        (root / ".codex/project-learning/state").mkdir(parents=True, exist_ok=True)

    prefix = "would " if check else ""
    changed_labels = {label for _, _, _, label in changes}
    return [prefix + message if message in changed_labels else "unchanged: " + message for message in messages]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Repository path; defaults to the current repository")
    parser.add_argument("--check", action="store_true", help="Report changes without writing")
    parser.add_argument(
        "--set-enabled",
        choices=("true", "false"),
        help="Enable or disable an initialized project without deleting data",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = resolve_root(args.root)
        if args.set_enabled is not None:
            messages = set_enabled(root, args.set_enabled == "true", args.check)
        else:
            messages = initialize(root, args.check)
        print(json.dumps({"root": str(root), "check": args.check, "results": messages}, indent=2))
        return 0
    except InitializationError as exc:
        print(f"project-learning initialization failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
