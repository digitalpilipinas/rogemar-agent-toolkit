#!/usr/bin/env python3
"""Validate native-agent collaboration receipts without contacting a broker."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

try:
    from prepare_run import git_snapshot
except ImportError:  # pragma: no cover - direct use from an unusual loader
    git_snapshot = None


VALID_STATES = {
    "pending",
    "running",
    "succeeded",
    "completed",
    "completed_with_warnings",
    "failed",
    "incomplete",
    "timed_out",
    "cancelled",
    "needs_attention",
}
REQUIRED_HEADINGS = (
    "# Result",
    "## Summary",
    "## Findings",
    "## Evidence",
    "## Changes",
    "## Validation",
    "## Limitations",
)
SUCCESS_STATES = {"succeeded", "completed"}


def read_status(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:100]:
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def provider_entries(manifest: dict[str, object]) -> list[dict[str, object]]:
    raw = manifest.get("providers")
    if not isinstance(raw, list):
        return []
    entries: list[dict[str, object]] = []
    for item in raw:
        if isinstance(item, str):
            entries.append({"id": item, "artifact_dir": item, "command": item})
        elif isinstance(item, dict):
            provider_id = str(item.get("id", "provider"))
            entries.append(
                {
                    "id": provider_id,
                    "artifact_dir": str(item.get("artifact_dir", provider_id)),
                    "command": item.get("command"),
                    "model": item.get("model"),
                    "effort": item.get("effort"),
                    "timeout_seconds": item.get("timeout_seconds"),
                }
            )
    return entries


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    # Providers and Markdown/YAML serializers sometimes quote scalar values.
    # Normalize the harmless representation difference before parsing.
    value = value.strip().strip('"').strip("'").strip()
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def check_events(events_path: Path) -> tuple[int, list[str]]:
    if not events_path.exists():
        return 0, []
    errors: list[str] = []
    count = 0
    try:
        with events_path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                count += 1
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    errors.append(f"events.jsonl line {line_number} is not JSON")
                    continue
                if not isinstance(value, dict):
                    errors.append(f"events.jsonl line {line_number} is not an object")
    except OSError as exc:
        errors.append(f"events.jsonl unreadable: {exc}")
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--max-bytes", type=int, default=8 * 1024 * 1024)
    parser.add_argument("--require-headings", action="store_true")
    parser.add_argument("--require-unchanged", action="store_true")
    args = parser.parse_args()
    if args.max_bytes < 1:
        parser.error("max-bytes must be positive")
    run_dir = args.run.expanduser().resolve(strict=True)
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        parser.error(f"missing manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"invalid manifest: {exc}")

    entries = provider_entries(manifest)
    if not entries:
        parser.error("manifest providers must be a non-empty list")

    receipts: list[dict[str, object]] = []
    hard_errors = 0
    warnings: list[str] = []
    for entry in entries:
        provider_id = str(entry["id"])
        provider_dir = run_dir / str(entry["artifact_dir"])
        status_path = provider_dir / "status.md"
        events_path = provider_dir / "events.jsonl"
        result_path = provider_dir / "result.md"
        status = read_status(status_path)
        state = status.get("state", "missing")
        errors: list[str] = []
        if state not in VALID_STATES:
            errors.append(f"invalid state: {state}")
        elif state not in SUCCESS_STATES:
            errors.append(f"run is not complete: {state}")
        if not status_path.is_file():
            errors.append("missing status.md")
        if state in {
            "running",
            "succeeded",
            "completed_with_warnings",
            "failed",
            "incomplete",
            "timed_out",
            "cancelled",
            "needs_attention",
        }:
            for key in ("started_at", "updated_at"):
                if key not in status:
                    errors.append(f"status.md missing {key}")
                elif parse_timestamp(status[key]) is None:
                    errors.append(f"status.md has invalid {key}")
            for key in ("first_output_at", "response_at", "completed_at"):
                if key in status and parse_timestamp(status[key]) is None:
                    errors.append(f"status.md has invalid {key}")
        try:
            result_size = result_path.stat().st_size
            result_mtime = datetime.fromtimestamp(result_path.stat().st_mtime, timezone.utc)
        except OSError:
            result_size = 0
            result_mtime = None
        if state in {"succeeded", "completed_with_warnings", "timed_out", "cancelled", "needs_attention"} and result_size == 0:
            errors.append(f"{state} without result.md")
        if result_size > args.max_bytes:
            errors.append(f"result.md exceeds {args.max_bytes} bytes")
        if args.require_headings and state in SUCCESS_STATES:
            try:
                result_text = result_path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                errors.append(f"result.md unreadable: {exc}")
            else:
                for heading in REQUIRED_HEADINGS:
                    if heading not in result_text:
                        errors.append(f"result.md missing heading: {heading}")
        started_at = parse_timestamp(status.get("started_at"))
        if state in SUCCESS_STATES and result_mtime and started_at and result_mtime < started_at:
            errors.append("result.md predates provider started_at")
        event_count, event_errors = check_events(events_path)
        errors.extend(event_errors)
        if errors:
            hard_errors += len(errors)
        receipts.append(
            {
                "provider": provider_id,
                "command": entry.get("command"),
                "model": entry.get("model"),
                "effort": entry.get("effort"),
                "timeout_seconds": entry.get("timeout_seconds"),
                "state": state,
                "phase": status.get("phase"),
                "started_at": status.get("started_at"),
                "first_output_at": status.get("first_output_at"),
                "response_at": status.get("response_at"),
                "completed_at": status.get("completed_at"),
                "duration_seconds": status.get("duration_seconds"),
                "progress": status.get("progress"),
                "last_activity": status.get("last_activity"),
                "artifact_owner": status.get("artifact_owner"),
                "result_bytes": result_size,
                "event_count": event_count,
                "errors": errors,
                "status_path": str(status_path),
                "result_path": str(result_path),
            }
        )

    if args.require_unchanged:
        workspace = manifest.get("workspace")
        expected = manifest.get("snapshot")
        if not isinstance(workspace, str) or not isinstance(expected, dict) or git_snapshot is None:
            hard_errors += 1
            warnings.append("cannot compare current workspace fingerprint")
        else:
            current = git_snapshot(Path(workspace).expanduser().resolve())
            if current.get("snapshot_sha256") != expected.get("snapshot_sha256"):
                hard_errors += 1
                warnings.append("workspace fingerprint changed since preparation")

    handoff_dir = run_dir / "handoff"
    if handoff_dir.is_dir():
        for handoff in sorted(handoff_dir.glob("to-*.md")):
            content = handoff.read_text(encoding="utf-8", errors="replace")
            if re.search(r"^state:\s*ready\s*$", content, re.MULTILINE):
                if "source_artifacts:" not in content or "source_snapshot_sha256:" not in content:
                    hard_errors += 1
                    warnings.append(f"ready handoff is missing provenance: {handoff.name}")

    output = {
        "run_id": manifest.get("run_id"),
        "workspace": manifest.get("workspace"),
        "mode": manifest.get("mode"),
        "workflow": manifest.get("workflow"),
        "manifest_state": manifest.get("state"),
        "providers": receipts,
        "warnings": warnings,
        "complete": all(
            item["state"] in SUCCESS_STATES and not item["errors"]
            for item in receipts
        ),
        "hard_errors": hard_errors,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 1 if hard_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
