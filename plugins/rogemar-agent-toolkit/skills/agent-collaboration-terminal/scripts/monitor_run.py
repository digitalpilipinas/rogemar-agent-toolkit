#!/usr/bin/env python3
"""Read-only standby monitor for a native-agent collaboration run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import time
from datetime import datetime, timezone


TERMINAL_STATES = {
    "succeeded",
    "completed_with_warnings",
    "failed",
    "incomplete",
    "timed_out",
    "cancelled",
    "needs_attention",
}
ATTENTION_PATTERNS = (
    (re.compile(r"tool[_ ]confirmation|permission[_ ](check|request|prompt)|waiting for (user|approval)", re.I), "waiting_for_user_approval"),
    (re.compile(r"quota|usage limit|rate limit|too many requests", re.I), "provider_quota_or_rate_limit"),
    (re.compile(r"not logged in|authentication required|unauthenticated", re.I), "provider_authentication_required"),
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip().strip('"').strip("'").strip()
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def launch_started_at(run_dir: Path) -> datetime | None:
    """Return the first physical-terminal launch time, when recorded."""
    try:
        launch = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(launch, dict):
        return None
    started = parse_timestamp(launch.get("monitor_started_at"))
    if started:
        return started
    values: list[datetime] = []
    providers = launch.get("providers")
    if isinstance(providers, list):
        for provider in providers:
            if isinstance(provider, dict):
                value = parse_timestamp(provider.get("opened_at"))
                if value:
                    values.append(value)
    return min(values) if values else None


def read_status(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return values
    for line in content.splitlines()[:80]:
        key, separator, value = line.partition(":")
        if separator and key.strip():
            values[key.strip()] = value.strip()
    return values


def provider_entries(manifest: dict[str, object]) -> list[dict[str, str]]:
    raw = manifest.get("providers", [])
    entries: list[dict[str, str]] = []
    if not isinstance(raw, list):
        return entries
    for item in raw:
        if isinstance(item, str):
            entries.append({"id": item, "artifact_dir": item})
        elif isinstance(item, dict):
            provider_id = str(item.get("id", "provider"))
            entries.append(
                {
                    "id": provider_id,
                    "artifact_dir": str(item.get("artifact_dir", provider_id)),
                    "timeout_seconds": str(item.get("timeout_seconds", "")),
                }
            )
    return entries


def log_attention(path: Path) -> str | None:
    try:
        with path.open("rb") as handle:
            handle.seek(0, 2)
            size = handle.tell()
            handle.seek(max(0, size - 64 * 1024))
            text = handle.read().decode("utf-8", "replace")
    except OSError:
        return None
    matches = [label for pattern, label in ATTENTION_PATTERNS if pattern.search(text)]
    return matches[-1] if matches else None


def receipt(run_dir: Path, entry: dict[str, str]) -> dict[str, object]:
    provider_dir = run_dir / entry["artifact_dir"]
    status_path = provider_dir / "status.md"
    events_path = provider_dir / "events.jsonl"
    result_path = provider_dir / "result.md"
    log_path = run_dir / "logs" / f"{entry['id']}.log"
    status = read_status(status_path)
    try:
        status_stat = status_path.stat()
        status_signature = [status_stat.st_mtime_ns, status_stat.st_size]
    except OSError:
        status_signature = None
    try:
        result_stat = result_path.stat()
        result_signature = [result_stat.st_mtime_ns, result_stat.st_size]
        result_bytes = result_stat.st_size
    except OSError:
        result_signature = None
        result_bytes = 0
    try:
        event_stat = events_path.stat()
        event_signature = [event_stat.st_mtime_ns, event_stat.st_size]
    except OSError:
        event_signature = None
    return {
        "provider": entry["id"],
        "state": status.get("state", "missing"),
        "phase": status.get("phase"),
        "started_at": status.get("started_at"),
        "updated_at": status.get("updated_at"),
        "last_activity": status.get("last_activity"),
        "first_output_at": status.get("first_output_at"),
        "response_at": status.get("response_at"),
        "completed_at": status.get("completed_at"),
        "duration_seconds": status.get("duration_seconds"),
        "progress": status.get("progress"),
        "artifact_owner": status.get("artifact_owner"),
        "timeout_seconds": entry.get("timeout_seconds"),
        "attention": status.get("attention") or log_attention(log_path),
        "result_bytes": result_bytes,
        "status_signature": status_signature,
        "events_signature": event_signature,
        "result_signature": result_signature,
        "status_path": str(status_path),
        "prompt_path": str(provider_dir / "prompt.md"),
        "events_path": str(events_path),
        "result_path": str(result_path),
    }


def emit(run_dir: Path, manifest: dict[str, object]) -> tuple[bool, list[dict[str, object]]]:
    receipts = [receipt(run_dir, entry) for entry in provider_entries(manifest)]
    public_receipts = []
    for item in receipts:
        public_receipts.append({key: value for key, value in item.items() if not key.endswith("_signature")})
    print(json.dumps({"at": now(), "run_id": manifest.get("run_id"), "providers": public_receipts}, ensure_ascii=False))
    complete = bool(receipts) and all(item["state"] in TERMINAL_STATES for item in receipts)
    return complete, receipts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument(
        "--timeout-minutes",
        type=int,
        help="active monitoring window from terminal launch, between 5 and 30 minutes",
    )
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if args.interval < 1:
        parser.error("interval must be positive")
    run_dir = args.run.expanduser().resolve(strict=True)
    manifest_path = run_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        parser.error(f"missing manifest: {manifest_path}")
    except json.JSONDecodeError as exc:
        parser.error(f"invalid manifest: {exc}")

    monitor_config = manifest.get("monitor")
    configured_minutes = 30
    if isinstance(monitor_config, dict):
        configured_value = monitor_config.get("standby_minutes")
        if isinstance(configured_value, int):
            configured_minutes = configured_value
    timeout_minutes = args.timeout_minutes if args.timeout_minutes is not None else configured_minutes
    if not 5 <= timeout_minutes <= 30:
        parser.error("timeout-minutes must be between 5 and 30")

    previous: object = None
    started_at = launch_started_at(run_dir)
    if started_at is None:
        # A monitor can be started before launch.json exists. In that case the
        # monitor window starts now and remains honest about the limitation.
        started_at = datetime.now(timezone.utc)
    elapsed = max(0.0, (datetime.now(timezone.utc) - started_at).total_seconds())
    deadline = time.monotonic() + max(0.0, timeout_minutes * 60 - elapsed)
    while True:
        receipts = [receipt(run_dir, entry) for entry in provider_entries(manifest)]
        signature = [(item["provider"], item["state"], item["phase"], item["attention"], item["status_signature"], item["events_signature"], item["result_signature"]) for item in receipts]
        if signature != previous:
            previous = signature
            complete, _ = emit(run_dir, manifest)
            if complete or args.once:
                return 0
        if time.monotonic() >= deadline:
            print(json.dumps({
                "at": now(),
                "run_id": manifest.get("run_id"),
                "state": "monitor_timeout",
                "timeout_minutes": timeout_minutes,
                "monitor_started_at": started_at.isoformat(),
            }))
            return 2
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
