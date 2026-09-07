#!/usr/bin/env python3
"""Resolve OpenDesign without launching it; run a native command only explicitly.

New toolkit integration, 2026-09-07. Apache-2.0, see ../LICENSE.txt.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Mapping


class ConfigurationError(ValueError):
    pass


def existing_file(value: str, label: str, *, executable: bool = False) -> Path:
    path = Path(value).expanduser()
    try:
        path = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ConfigurationError(f"{label} does not resolve to an existing file") from exc
    if not path.is_file():
        raise ConfigurationError(f"{label} must be a file")
    if executable and not os.access(path, os.X_OK):
        raise ConfigurationError(f"{label} must be executable")
    return path


def source_root(value: str) -> Path:
    try:
        root = Path(value).expanduser().resolve(strict=True)
        package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    except (OSError, RuntimeError, ValueError) as exc:
        raise ConfigurationError("OpenDesign root needs a readable package.json") from exc
    if not isinstance(package, dict) or package.get("name") != "open-design":
        raise ConfigurationError("OpenDesign root package name must be open-design")
    return root


def resolve_command(
    args: argparse.Namespace, env: Mapping[str, str]
) -> tuple[list[str], Path | None, str]:
    selected = args.bin or env.get("OD_BIN") or env.get("OPEN_DESIGN_BIN")
    root_value = args.root or env.get("OPEN_DESIGN_ROOT")
    # A live host's explicit CLI wins over a stale optional checkout hint.
    root = source_root(root_value) if root_value and not selected else None
    if not selected and root:
        selected = str(root / "apps/daemon/bin/od.mjs")
    if not selected:
        raise ConfigurationError(
            "Set OD_BIN, OPEN_DESIGN_BIN, --bin, or --root; bare od is ambiguous"
        )
    cli = existing_file(selected, "OpenDesign CLI")
    blocked = {Path("/usr/bin/od").resolve(), Path("/bin/od").resolve()}
    if cli in blocked:
        raise ConfigurationError("POSIX octal-dump od is not the OpenDesign CLI")

    # Both the npm wrapper and its PATH symlinks resolve to this same structure.
    if cli.name == "od.mjs" and cli.parent.name == "bin":
        if not (cli.parent.parent / "dist/cli.js").is_file():
            raise ConfigurationError("Source launcher requires built daemon dist/cli.js")

    if cli.suffix.lower() in {".js", ".mjs", ".cjs"}:
        node_value = (
            args.node
            or env.get("OD_NODE_BIN")
            or env.get("OPEN_DESIGN_NODE_BIN")
            or shutil.which("node", path=env.get("PATH", ""))
        )
        if not node_value:
            raise ConfigurationError("JavaScript CLI requires a Node-compatible runtime")
        node = existing_file(node_value, "Node-compatible runtime", executable=True)
        is_electron = node.name.lower() in {
            "electron", "electron.exe", "open design", "open design.exe", "open-design", "open-design.exe"
        }
        if is_electron and env.get("ELECTRON_RUN_AS_NODE") != "1":
            raise ConfigurationError("Electron runtime requires generated ELECTRON_RUN_AS_NODE=1")
        if cli.name == "daemon-cli.mjs" or "prebundled" in cli.parts:
            data_dir = env.get("OD_DATA_DIR", "")
            if not data_dir or not Path(data_dir).is_absolute():
                raise ConfigurationError("Packaged CLI requires an explicit absolute OD_DATA_DIR")
        return [str(node), str(cli)], root, "node-script"

    if cli.suffix.lower() in {".cmd", ".bat", ".ps1"}:
        raise ConfigurationError("Use a native executable launcher or JavaScript CLI with --node")
    existing_file(str(cli), "OpenDesign launcher", executable=True)
    return [str(cli)], root, "executable-launcher"


def doctor(args: argparse.Namespace, env: Mapping[str, str]) -> tuple[int, dict]:
    report: dict = {
        "schema_version": 1,
        "status": "unavailable",
        "probe": "filesystem-only; no commands, network, or writes",
        "runtime_verified": False,
        "environment_present": {
            key: bool(env.get(key))
            for key in (
                "OD_BIN", "OPEN_DESIGN_BIN", "OD_NODE_BIN", "OPEN_DESIGN_NODE_BIN",
                "OD_DAEMON_URL", "OD_DATA_DIR", "OD_PROJECT_ID", "OD_PROJECT_DIR",
                "ELECTRON_RUN_AS_NODE",
            )
        },
        "live_dependencies": {
            "daemon": "unverified",
            "node_version_and_native_module_compatibility": "unverified",
            "agent_cli_or_byok_provider_and_auth": "unverified",
            "desktop_renderer_for_pdf_image_pptx": "unverified",
            "browser_media_runtime_for_hyperframes": "unverified",
            "lane_specific_connectors_and_authorization": "unverified",
        },
    }
    try:
        command, root, kind = resolve_command(args, env)
    except (ConfigurationError, OSError) as exc:
        report["error"] = str(exc)
        return 2, report
    report.update(status="configured", launcher_kind=kind, command=command)
    if root:
        package = json.loads((root / "package.json").read_text(encoding="utf-8"))
        report["source_package_version"] = package.get("version")
        report["resources_present"] = {
            path: (root / path).is_dir()
            for path in ("skills", "design-templates", "design-systems", "craft", "plugins/_official")
        }
        report["native_package_directories_present"] = {
            package: (root / "apps/daemon/node_modules" / package).is_dir()
            for package in ("better-sqlite3", "node-pty", "@ffmpeg-installer/ffmpeg", "hyperframes")
        }
    return 0, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin", help="Explicit OpenDesign CLI file; never a shell command")
    parser.add_argument("--node", help="Explicit Node-compatible executable for a JavaScript CLI")
    parser.add_argument("--root", help="Built OpenDesign source checkout")
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("doctor", help="Inspect only local files and configuration presence")
    run_parser = subparsers.add_parser("run", help="Explicitly execute the chosen native command")
    run_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if args.action == "doctor":
        code, report = doctor(args, os.environ)
        print(json.dumps(report, indent=2))
        return code
    arguments = args.arguments
    if arguments[:1] == ["--"]:
        arguments = arguments[1:]
    if not arguments:
        parser.error("run requires native command arguments after --")
    try:
        command, _, _ = resolve_command(args, os.environ)
        # No shell, capture, rewrites, environment dumps or implicit services.
        result = subprocess.run([*command, *arguments], check=False)
        return result.returncode if result.returncode >= 0 else 128 - result.returncode
    except ConfigurationError as exc:
        print(f"OpenDesign adapter: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"OpenDesign launcher could not execute: {exc.strerror}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
