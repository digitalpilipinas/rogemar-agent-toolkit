#!/usr/bin/env python3
"""Validate and maintain project-learning candidate events and promotions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
EVENT_TYPES = {"captured", "reinforced", "dismissed", "promoted"}
EVIDENCE_LEVELS = {"reported", "observed", "verified", "reinforced"}
EVIDENCE_KINDS = {"file", "test", "commit", "review", "decision", "outcome"}
LEDGER_STATUSES = {"Accepted", "Reinforced", "Superseded"}
CROSS_PROJECT_VALUES = {"No", "Evaluate"}
FORBIDDEN_KEYS = {
    "transcript",
    "raw_transcript",
    "transcript_text",
    "reasoning",
    "hidden_reasoning",
    "tool_output",
    "conversation_quote",
    "quote",
    "credential",
    "secret",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bsb_(?:secret|publishable)_[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
)
LEDGER_MARKER = "<!-- PROJECT-LEARNING:ENTRIES -->"


class StoreError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
        raise StoreError(f"not a Git repository: {cwd}")
    return Path(result.stdout.strip()).resolve()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StoreError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StoreError(f"expected a JSON object in {path}")
    return value


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def config_for(root: Path) -> dict[str, Any]:
    path = root / ".codex/project-learning/config.json"
    config = load_json(path)
    required = {
        "schema_version": SCHEMA_VERSION,
        "capture_policy": "signal-gated",
        "promotion_policy": "review-required",
        "storage_policy": "structured-summaries-only",
    }
    for key, expected in required.items():
        if config.get(key) != expected:
            raise StoreError(f"unsupported {key!r} in {path}")
    if not isinstance(config.get("enabled"), bool):
        raise StoreError(f"`enabled` must be boolean in {path}")
    return config


def project_path(root: Path, config: dict[str, Any], key: str) -> Path:
    raw = config.get(key)
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        raise StoreError(f"config field {key!r} must be a relative path")
    path = (root / raw).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise StoreError(f"config field {key!r} escapes the repository") from exc
    return path


def validate_text(value: Any, field: str, maximum: int = 1200) -> str:
    if not isinstance(value, str):
        raise StoreError(f"{field} must be a string")
    text = " ".join(value.split())
    if not text:
        raise StoreError(f"{field} must not be empty")
    if len(text) > maximum:
        raise StoreError(f"{field} exceeds {maximum} characters")
    if re.search(r"(?:^|\s)(?:/Users/|/home/|[A-Za-z]:\\Users\\)[^\s]+", text):
        raise StoreError(f"{field} must not contain an absolute home-directory path")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise StoreError(f"{field} contains sensitive-looking material")
    return text


def reject_forbidden_keys(value: Any, path: str = "request") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_KEYS:
                raise StoreError(f"forbidden field {path}.{key}")
            reject_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_forbidden_keys(child, f"{path}[{index}]")
    elif isinstance(value, str):
        validate_text(value, path, maximum=4000)


def safe_id(value: Any, field: str) -> str:
    text = validate_text(value, field, maximum=160)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", text).strip("-")
    if not safe:
        raise StoreError(f"{field} does not contain a usable identifier")
    return safe


def validate_capture_request(request: dict[str, Any]) -> dict[str, Any]:
    reject_forbidden_keys(request)
    allowed = {
        "schema_version",
        "session_id",
        "turn_id",
        "lesson",
        "applies_when",
        "does_not_apply_when",
        "evidence_level",
        "evidence",
        "milestone",
        "source_project",
        "source_lesson_id",
    }
    unexpected = set(request) - allowed
    if unexpected:
        raise StoreError("unexpected capture fields: " + ", ".join(sorted(unexpected)))
    if request.get("schema_version") != SCHEMA_VERSION:
        raise StoreError("unsupported capture schema_version")

    evidence_level = request.get("evidence_level")
    if evidence_level not in EVIDENCE_LEVELS:
        raise StoreError("invalid evidence_level")
    evidence_raw = request.get("evidence")
    if not isinstance(evidence_raw, list) or not evidence_raw or len(evidence_raw) > 20:
        raise StoreError("evidence must contain 1 to 20 items")
    evidence: list[dict[str, str]] = []
    for index, item in enumerate(evidence_raw):
        if not isinstance(item, dict) or set(item) != {"kind", "reference", "summary"}:
            raise StoreError(f"evidence[{index}] has invalid fields")
        kind = item.get("kind")
        if kind not in EVIDENCE_KINDS:
            raise StoreError(f"evidence[{index}].kind is invalid")
        evidence.append(
            {
                "kind": kind,
                "reference": validate_text(item.get("reference"), f"evidence[{index}].reference", 500),
                "summary": validate_text(item.get("summary"), f"evidence[{index}].summary", 700),
            }
        )

    milestone = request.get("milestone", False)
    if not isinstance(milestone, bool):
        raise StoreError("milestone must be boolean")
    source_project = request.get("source_project")
    source_lesson_id = request.get("source_lesson_id")
    if source_project is not None:
        source_project = validate_text(source_project, "source_project", 300)
    if source_lesson_id is not None:
        source_lesson_id = safe_id(source_lesson_id, "source_lesson_id")
    if (source_project is None) != (source_lesson_id is None):
        raise StoreError("source_project and source_lesson_id must be provided together")

    return {
        "schema_version": SCHEMA_VERSION,
        "session_id": safe_id(request.get("session_id"), "session_id"),
        "turn_id": safe_id(request.get("turn_id"), "turn_id"),
        "lesson": validate_text(request.get("lesson"), "lesson"),
        "applies_when": validate_text(request.get("applies_when"), "applies_when"),
        "does_not_apply_when": validate_text(
            request.get("does_not_apply_when"), "does_not_apply_when"
        ),
        "evidence_level": evidence_level,
        "evidence": evidence,
        "milestone": milestone,
        "source_project": source_project,
        "source_lesson_id": source_lesson_id,
    }


def fingerprint(request: dict[str, Any]) -> str:
    parts = (
        request["lesson"],
        request["applies_when"],
        request["does_not_apply_when"],
    )
    normalized = "\n".join(" ".join(part.lower().split()) for part in parts)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise StoreError(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(event, dict) or event.get("schema_version") != SCHEMA_VERSION:
                raise StoreError(f"invalid event at {path}:{line_number}")
            if event.get("event_type") not in EVENT_TYPES:
                raise StoreError(f"invalid event type at {path}:{line_number}")
            events.append(event)
    return events


def materialize(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    for event in events:
        candidate_id = event.get("candidate_id")
        if not isinstance(candidate_id, str):
            raise StoreError("candidate event is missing candidate_id")
        event_type = event["event_type"]
        if event_type in {"captured", "reinforced"}:
            payload = event.get("payload")
            if not isinstance(payload, dict):
                raise StoreError(f"{event_type} event is missing payload")
            candidates[candidate_id] = {
                "candidate_id": candidate_id,
                "fingerprint": event.get("fingerprint"),
                "status": "pending",
                "payload": payload,
                "last_event_at": event.get("recorded_at"),
            }
        elif candidate_id in candidates:
            candidates[candidate_id]["status"] = event_type
            candidates[candidate_id]["last_event_at"] = event.get("recorded_at")
    return candidates


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def marker_path(state_dir: Path, session_id: str, turn_id: str) -> Path:
    return state_dir / f"{session_id}-{turn_id}.json"


def review_due(
    state_dir: Path,
    pending_count: int,
    threshold: int,
    milestone: bool,
    source_key: str,
) -> bool:
    state_path = state_dir / "review-reminder.json"
    state = load_json(state_path) if state_path.exists() else {
        "schema_version": SCHEMA_VERSION,
        "last_pending_bucket": 0,
        "milestone_keys": [],
    }
    bucket = pending_count // max(threshold, 1)
    last_bucket = state.get("last_pending_bucket", 0)
    milestone_keys = state.get("milestone_keys", [])
    if not isinstance(last_bucket, int) or not isinstance(milestone_keys, list):
        raise StoreError(f"invalid review reminder state in {state_path}")
    due_for_count = bucket > 0 and bucket > last_bucket
    due_for_milestone = milestone and source_key not in milestone_keys
    state_changed = False
    if bucket < last_bucket:
        state["last_pending_bucket"] = bucket
        state_changed = True
    if due_for_count:
        state["last_pending_bucket"] = bucket
        state_changed = True
    if due_for_milestone:
        milestone_keys.append(source_key)
        state["milestone_keys"] = milestone_keys[-100:]
        state_changed = True
    if state_changed:
        atomic_json(state_path, state)
    return due_for_count or due_for_milestone


def candidate_paths(root: Path, config: dict[str, Any]) -> tuple[Path, Path, Path]:
    return (
        project_path(root, config, "candidate_store"),
        project_path(root, config, "state_directory"),
        project_path(root, config, "accepted_ledger"),
    )


def capture(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    if config.get("enabled") is not True:
        return {"captured": False, "reason": "disabled", "review_due": False}
    request = validate_capture_request(load_json(Path(args.request).resolve()))
    store_path, state_dir, _ = candidate_paths(root, config)
    processed = marker_path(state_dir, request["session_id"], request["turn_id"])
    if processed.exists():
        previous = load_json(processed)
        return {
            "captured": previous.get("outcome") in {"captured", "reinforced"},
            "candidate_id": previous.get("candidate_id"),
            "event_type": previous.get("outcome"),
            "review_due": False,
            "idempotent": True,
        }

    events = load_events(store_path)
    source_key = f"{request['session_id']}:{request['turn_id']}"
    for event in events:
        source = event.get("source")
        if isinstance(source, dict) and f"{source.get('session_id')}:{source.get('turn_id')}" == source_key:
            outcome = event.get("event_type")
            candidate_id = event.get("candidate_id")
            atomic_json(
                processed,
                {
                    "schema_version": SCHEMA_VERSION,
                    "session_id": request["session_id"],
                    "turn_id": request["turn_id"],
                    "outcome": outcome,
                    "candidate_id": candidate_id,
                    "processed_at": now_iso(),
                },
            )
            return {
                "captured": outcome in {"captured", "reinforced"},
                "candidate_id": candidate_id,
                "event_type": outcome,
                "review_due": False,
                "idempotent": True,
            }

    digest = fingerprint(request)
    candidates = materialize(events)
    matching = next(
        (
            item
            for item in candidates.values()
            if item.get("fingerprint") == digest and item.get("status") == "pending"
        ),
        None,
    )
    if matching:
        candidate_id = matching["candidate_id"]
        event_type = "reinforced"
    else:
        candidate_id = "PL-" + digest[:12].upper()
        event_type = "captured"

    payload = {key: value for key, value in request.items() if key not in {"session_id", "turn_id"}}
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": str(uuid.uuid4()),
        "candidate_id": candidate_id,
        "event_type": event_type,
        "recorded_at": now_iso(),
        "fingerprint": digest,
        "source": {"session_id": request["session_id"], "turn_id": request["turn_id"]},
        "payload": payload,
    }
    append_event(store_path, event)
    updated = materialize(events + [event])
    pending_count = sum(1 for item in updated.values() if item["status"] == "pending")
    reminder = config.get("review_reminder")
    if not isinstance(reminder, dict):
        raise StoreError("review_reminder must be an object")
    threshold = reminder.get("pending_count", 5)
    if not isinstance(threshold, int) or threshold < 1:
        raise StoreError("review_reminder.pending_count must be a positive integer")
    milestone_enabled = reminder.get("milestones") is True
    due = review_due(
        state_dir,
        pending_count,
        threshold,
        request["milestone"] and milestone_enabled,
        source_key,
    )
    atomic_json(
        processed,
        {
            "schema_version": SCHEMA_VERSION,
            "session_id": request["session_id"],
            "turn_id": request["turn_id"],
            "outcome": event_type,
            "candidate_id": candidate_id,
            "processed_at": now_iso(),
        },
    )
    return {
        "captured": True,
        "candidate_id": candidate_id,
        "event_type": event_type,
        "pending_count": pending_count,
        "review_due": due,
        "idempotent": False,
    }


def mark_no_candidate(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    _, state_dir, _ = candidate_paths(root, config)
    session_id = safe_id(args.session, "session_id")
    turn_id = safe_id(args.turn, "turn_id")
    processed = marker_path(state_dir, session_id, turn_id)
    if not processed.exists():
        store_path, _, _ = candidate_paths(root, config)
        for event in load_events(store_path):
            source = event.get("source")
            if isinstance(source, dict) and source.get("session_id") == session_id and source.get("turn_id") == turn_id:
                raise StoreError("this session and turn already produced a candidate event")
        atomic_json(
            processed,
            {
                "schema_version": SCHEMA_VERSION,
                "session_id": session_id,
                "turn_id": turn_id,
                "outcome": "no_candidate",
                "candidate_id": None,
                "processed_at": now_iso(),
            },
        )
    return {"captured": False, "reason": "no_candidate", "review_due": False}


def list_candidates(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    store_path, _, _ = candidate_paths(root, config)
    candidates = materialize(load_events(store_path))
    values = sorted(candidates.values(), key=lambda item: item.get("last_event_at") or "")
    if args.status != "all":
        values = [item for item in values if item["status"] == args.status]
    return {"count": len(values), "candidates": values}


def status(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    store_path, _, ledger_path = candidate_paths(root, config)
    candidates = materialize(load_events(store_path))
    counts: dict[str, int] = {}
    for candidate in candidates.values():
        counts[candidate["status"]] = counts.get(candidate["status"], 0) + 1
    return {
        "root": str(root),
        "enabled": config["enabled"],
        "counts": counts,
        "candidate_store_exists": store_path.exists(),
        "ledger_exists": ledger_path.exists(),
    }


def dismiss(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    store_path, _, _ = candidate_paths(root, config)
    events = load_events(store_path)
    candidates = materialize(events)
    candidate = candidates.get(args.candidate_id)
    if candidate is None:
        raise StoreError(f"unknown candidate: {args.candidate_id}")
    if candidate["status"] == "dismissed":
        return {"candidate_id": args.candidate_id, "status": "dismissed", "idempotent": True}
    if candidate["status"] != "pending":
        raise StoreError(f"candidate is not pending: {args.candidate_id}")
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": str(uuid.uuid4()),
        "candidate_id": args.candidate_id,
        "event_type": "dismissed",
        "recorded_at": now_iso(),
        "source": {
            "session_id": safe_id(args.session, "session_id"),
            "turn_id": safe_id(args.turn, "turn_id"),
        },
    }
    append_event(store_path, event)
    return {"candidate_id": args.candidate_id, "status": "dismissed", "idempotent": False}


def validate_promotion_request(request: dict[str, Any]) -> dict[str, Any]:
    reject_forbidden_keys(request)
    allowed = {
        "schema_version",
        "candidate_id",
        "status",
        "lesson",
        "applies_when",
        "does_not_apply_when",
        "evidence_strength",
        "cross_project",
        "approved_by",
        "supersedes",
    }
    unexpected = set(request) - allowed
    if unexpected:
        raise StoreError("unexpected promotion fields: " + ", ".join(sorted(unexpected)))
    if request.get("schema_version") != SCHEMA_VERSION:
        raise StoreError("unsupported promotion schema_version")
    status_value = request.get("status")
    if status_value not in LEDGER_STATUSES:
        raise StoreError("invalid ledger status")
    evidence_strength = request.get("evidence_strength")
    if evidence_strength not in EVIDENCE_LEVELS:
        raise StoreError("invalid evidence_strength")
    cross_project = request.get("cross_project")
    if cross_project not in CROSS_PROJECT_VALUES:
        raise StoreError("invalid cross_project value")
    if request.get("approved_by") != "user":
        raise StoreError("promotion requires approved_by=user")
    supersedes = request.get("supersedes")
    if supersedes is not None:
        supersedes = safe_id(supersedes, "supersedes")
    if status_value == "Superseded" and supersedes is None:
        raise StoreError("Superseded status requires supersedes")
    return {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": safe_id(request.get("candidate_id"), "candidate_id"),
        "status": status_value,
        "lesson": validate_text(request.get("lesson"), "lesson"),
        "applies_when": validate_text(request.get("applies_when"), "applies_when"),
        "does_not_apply_when": validate_text(
            request.get("does_not_apply_when"), "does_not_apply_when"
        ),
        "evidence_strength": evidence_strength,
        "cross_project": cross_project,
        "approved_by": "user",
        "supersedes": supersedes,
    }


def ledger_entry(root: Path, request: dict[str, Any], candidate: dict[str, Any]) -> str:
    payload = candidate["payload"]
    evidence_lines = [
        f"- [{item['kind']}] {item['reference']} — {item['summary']}"
        for item in payload["evidence"]
    ]
    provenance = f"Candidate {request['candidate_id']}"
    if payload.get("source_project"):
        provenance += (
            f"; adapted from {payload['source_project']}#{payload['source_lesson_id']}"
        )
    lines = [
        f"## {request['candidate_id']}",
        "",
        f"Status: {request['status']}",
        f"Lesson: {request['lesson']}",
        f"Applies when: {request['applies_when']}",
        f"Does not apply when: {request['does_not_apply_when']}",
        "Evidence:",
        *evidence_lines,
        f"Evidence strength: {request['evidence_strength']}",
        f"Scope: {root.name}",
        f"Provenance: {provenance}; approved by user",
        f"Last reviewed: {datetime.now(timezone.utc).date().isoformat()}",
        f"Cross-project candidate: {request['cross_project']}",
    ]
    if request.get("supersedes"):
        lines.append(f"Supersedes: {request['supersedes']}")
    return "\n".join(lines) + "\n"


def promote(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    request = validate_promotion_request(load_json(Path(args.request).resolve()))
    store_path, _, ledger_path = candidate_paths(root, config)
    events = load_events(store_path)
    candidates = materialize(events)
    candidate = candidates.get(request["candidate_id"])
    if candidate is None:
        raise StoreError(f"unknown candidate: {request['candidate_id']}")
    if candidate["status"] == "promoted":
        return {"candidate_id": request["candidate_id"], "status": "promoted", "idempotent": True}
    if candidate["status"] != "pending":
        raise StoreError(f"candidate is not pending: {request['candidate_id']}")
    if not ledger_path.exists():
        raise StoreError(f"accepted ledger does not exist: {ledger_path}")
    ledger = ledger_path.read_text(encoding="utf-8")
    if LEDGER_MARKER not in ledger:
        raise StoreError(f"accepted ledger marker is missing: {ledger_path}")
    if re.search(rf"^##\s+{re.escape(request['candidate_id'])}\s*$", ledger, re.M):
        expected_lesson = f"Lesson: {request['lesson']}"
        if expected_lesson not in ledger:
            raise StoreError("ledger entry exists with different approved content")
    else:
        entry = ledger_entry(root, request, candidate)
        separator = "" if not ledger or ledger.endswith("\n\n") else "\n"
        atomic_text(ledger_path, ledger + separator + entry)
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": str(uuid.uuid4()),
        "candidate_id": request["candidate_id"],
        "event_type": "promoted",
        "recorded_at": now_iso(),
        "source": {"session_id": "user-review", "turn_id": str(uuid.uuid4())},
        "payload": {"ledger_status": request["status"]},
    }
    append_event(store_path, event)
    return {"candidate_id": request["candidate_id"], "status": "promoted", "idempotent": False}


def add_root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", help="Repository path; defaults to the current repository")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture_parser = subparsers.add_parser("capture")
    add_root_argument(capture_parser)
    capture_parser.add_argument("--request", required=True)
    capture_parser.set_defaults(handler=capture)

    no_candidate_parser = subparsers.add_parser("mark-no-candidate")
    add_root_argument(no_candidate_parser)
    no_candidate_parser.add_argument("--session", required=True)
    no_candidate_parser.add_argument("--turn", required=True)
    no_candidate_parser.set_defaults(handler=mark_no_candidate)

    list_parser = subparsers.add_parser("list")
    add_root_argument(list_parser)
    list_parser.add_argument(
        "--status", choices=("pending", "dismissed", "promoted", "all"), default="pending"
    )
    list_parser.set_defaults(handler=list_candidates)

    status_parser = subparsers.add_parser("status")
    add_root_argument(status_parser)
    status_parser.set_defaults(handler=status)

    dismiss_parser = subparsers.add_parser("dismiss")
    add_root_argument(dismiss_parser)
    dismiss_parser.add_argument("--candidate-id", required=True)
    dismiss_parser.add_argument("--session", default="user-review")
    dismiss_parser.add_argument("--turn", default="manual")
    dismiss_parser.set_defaults(handler=dismiss)

    promote_parser = subparsers.add_parser("promote")
    add_root_argument(promote_parser)
    promote_parser.add_argument("--request", required=True)
    promote_parser.set_defaults(handler=promote)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = args.handler(args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except StoreError as exc:
        print(f"project-learning store failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
