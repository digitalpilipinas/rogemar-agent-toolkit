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
import time
from contextlib import contextmanager
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
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"(?i)\b(?:password|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*[^\s]{8,}"),
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
    if config.get("capture_mode", "explicit") not in {"explicit", "workflow"}:
        raise StoreError(f"unsupported capture_mode in {path}")
    reminder = config.get("review_reminder")
    if not isinstance(reminder, dict) or type(reminder.get("pending_count")) is not int or reminder["pending_count"] < 1:
        raise StoreError("review_reminder.pending_count must be a positive integer")
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
        "proposal",
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

    proposal = request.get("proposal")
    if proposal is not None:
        if not isinstance(proposal, dict) or set(proposal) != {"target_skill", "allowed_files", "validation"}:
            raise StoreError("proposal requires target_skill, allowed_files and validation")
        target = Path(validate_text(proposal["target_skill"], "proposal.target_skill", 500))
        if target.is_absolute() or ".." in target.parts or target.name != "SKILL.md":
            raise StoreError("proposal.target_skill must be a repository-relative SKILL.md")
        allowed_files = proposal["allowed_files"]
        if not isinstance(allowed_files, list) or not 1 <= len(allowed_files) <= 20:
            raise StoreError("proposal.allowed_files requires 1 to 20 paths")
        for raw in allowed_files:
            path = Path(validate_text(raw, "proposal.allowed_files", 500))
            if path.is_absolute() or ".." in path.parts or not path.is_relative_to(target.parent):
                raise StoreError("proposal allowed files must stay inside the target skill")
        proposal = {"target_skill": str(target), "allowed_files": allowed_files,
                    "validation": validate_text(proposal["validation"], "proposal.validation")}
        if source_project is None:
            raise StoreError("global proposal requires accepted source provenance")

    result = {
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
    if proposal is not None:
        result["proposal"] = proposal
    return result


def fingerprint(request: dict[str, Any]) -> str:
    parts = (
        request["lesson"],
        request["applies_when"],
        request["does_not_apply_when"],
    )
    normalized = "\n".join(" ".join(part.lower().split()) for part in parts)
    if request.get("proposal"):
        normalized += "\n" + json.dumps(request["proposal"], sort_keys=True)
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


def review_due(state_dir: Path, candidates: dict[str, Any], threshold: int, milestone: bool) -> bool:
    state_path = state_dir / "review-reminder.json"
    state = load_json(state_path) if state_path.exists() else {}
    pending = {key: item["payload"] for key, item in candidates.items() if item["status"] == "pending"}
    # Only changed pending material earns another reminder, not a new source turn.
    versions = {key: hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                for key, payload in pending.items()}
    notified = state.get("notified_versions", {})
    if not isinstance(notified, dict):
        raise StoreError("invalid notified candidate state")
    new_material = any(notified.get(key) != version for key, version in versions.items())
    bucket = len(pending) // threshold
    last_bucket = state.get("last_pending_bucket", 0)
    if type(last_bucket) is not int:
        raise StoreError("invalid review reminder state")
    due = new_material and (
        bucket > last_bucket or milestone
    )
    if due or bucket < last_bucket:
        state["last_pending_bucket"] = bucket
        if due:
            state["notified_versions"] = versions
        atomic_json(state_path, state)
    return due


def evidence_keys(payload: dict[str, Any]) -> set[tuple[str, str]]:
    return {(item["kind"], item["reference"]) for item in payload.get("evidence", [])}


def accepted_sections(ledger: Path) -> dict[str, str]:
    if not ledger.exists():
        return {}
    parts = re.split(r"^## (PL-[A-F0-9]{12})\s*$", ledger.read_text(encoding="utf-8"), flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)
            if re.search(r"^Status: (?:Accepted|Reinforced)$", parts[i + 1], re.M)}


def ledger_match(ledger: Path, request: dict[str, Any]) -> str | None:
    for candidate_id, section in accepted_sections(ledger).items():
        fields = {}
        for key, label in (("lesson", "Lesson"), ("applies_when", "Applies when"),
                           ("does_not_apply_when", "Does not apply when")):
            match = re.search(rf"^{label}: (.+)$", section, re.M)
            if match:
                fields[key] = match.group(1)
        if len(fields) == 3 and fingerprint(fields) == fingerprint(request):
            return candidate_id
    return None


def validate_proposal_source(args: argparse.Namespace, root: Path, request: dict[str, Any]) -> None:
    proposal = request.get("proposal")
    if proposal is None:
        return
    if not getattr(args, "source_root", None):
        raise StoreError("global proposal requires --source-root for accepted source validation")
    source = resolve_root(args.source_root)
    if source.name != request["source_project"]:
        raise StoreError("source_project must match the selected source repository name")
    source_config = config_for(source)
    if getattr(args, "workflow", False) and (not source_config["enabled"] or source_config.get("capture_mode", "explicit") != "workflow"):
        raise StoreError("automatic global proposals require an enabled, enrolled source project")
    _, _, ledger = candidate_paths(source, source_config)
    section = accepted_sections(ledger).get(request["source_lesson_id"])
    if not section or not re.search(r"^Evidence strength: (?:verified|reinforced)$", section, re.M):
        raise StoreError("global proposal source must be an accepted, verified lesson")
    target = (root / proposal["target_skill"]).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise StoreError("global proposal target skill must exist inside the repository")
    for path in proposal["allowed_files"]:
        if not (root / path).resolve().is_relative_to(target.parent):
            raise StoreError("global proposal allowed path escapes the target skill")


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
    request = validate_capture_request(read_request(args.request))
    if getattr(args, "workflow", False) and request["evidence_level"] not in {"verified", "reinforced"}:
        raise StoreError("workflow capture requires verified or reinforced evidence")
    validate_proposal_source(args, root, request)
    store_path, state_dir, ledger_path = candidate_paths(root, config)
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
    matching = next((item for item in reversed(list(candidates.values()))
                     if item.get("fingerprint") == digest), None)
    revisits = None
    duplicate = False
    if matching:
        candidate_id = matching["candidate_id"]
        prior_evidence = set().union(*(evidence_keys(event.get("payload", {})) for event in events
                                      if event.get("fingerprint") == digest))
        new_evidence = evidence_keys(request) - prior_evidence
        duplicate = not new_evidence or request["evidence_level"] not in {"verified", "reinforced"}
        if matching["status"] != "pending" and not duplicate:
            revisits = candidate_id
            revision = hashlib.sha256((digest + json.dumps(sorted(new_evidence))).encode()).hexdigest()
            candidate_id = "PL-" + revision[:12].upper()
            event_type = "captured"
        else:
            event_type = "reinforced"
    else:
        candidate_id = ledger_match(ledger_path, request) or "PL-" + digest[:12].upper()
        duplicate = candidate_id in accepted_sections(ledger_path)
        event_type = "captured"
    if duplicate:
        atomic_json(processed, {"schema_version": SCHEMA_VERSION, "outcome": "duplicate",
                               "session_id": request["session_id"], "turn_id": request["turn_id"],
                               "candidate_id": candidate_id, "processed_at": now_iso()})
        due = review_due(state_dir, candidates, config["review_reminder"]["pending_count"],
                         request["milestone"] and config["review_reminder"].get("milestones") is True)
        return {"captured": False, "reason": "duplicate", "candidate_id": candidate_id,
                "review_due": due, "idempotent": False}

    payload = {key: value for key, value in request.items() if key not in {"session_id", "turn_id"}}
    if revisits:
        payload["revisits_candidate_id"] = revisits
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
    due = review_due(state_dir, updated, config["review_reminder"]["pending_count"],
                     request["milestone"] and config["review_reminder"].get("milestones") is True)
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
    store_path, _, _ = candidate_paths(root, config)
    due = review_due(state_dir, materialize(load_events(store_path)), config["review_reminder"]["pending_count"],
                     getattr(args, "milestone", False) and config["review_reminder"].get("milestones") is True)
    return {"captured": False, "reason": "no_candidate", "review_due": due}


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
        "capture_mode": config.get("capture_mode", "explicit"),
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
    if payload.get("proposal"):
        lines.extend([
            f"Proposed skill: {payload['proposal']['target_skill']}",
            f"Allowed files: {', '.join(payload['proposal']['allowed_files'])}",
            f"Required validation: {payload['proposal']['validation']}",
            "Proposal approval does not execute or authorize changes outside the recorded scope.",
        ])
    if request.get("supersedes"):
        lines.append(f"Supersedes: {request['supersedes']}")
    return "\n".join(lines) + "\n"


def promote(args: argparse.Namespace) -> dict[str, Any]:
    root = resolve_root(args.root)
    config = config_for(root)
    request = validate_promotion_request(read_request(args.request))
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
    capture_parser.add_argument("--request", required=True, help="JSON request path, or - for stdin")
    capture_parser.add_argument("--source-root", help="Accepted source repository for a global proposal")
    add_capture_guards(capture_parser)
    capture_parser.set_defaults(handler=capture)

    no_candidate_parser = subparsers.add_parser("mark-no-candidate")
    add_root_argument(no_candidate_parser)
    no_candidate_parser.add_argument("--session", required=True)
    no_candidate_parser.add_argument("--turn", required=True)
    no_candidate_parser.add_argument("--milestone", action="store_true")
    add_capture_guards(no_candidate_parser)
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


def read_request(raw: str) -> dict[str, Any]:
    if raw != "-":
        return load_json(Path(raw).resolve())
    try:
        value = json.loads(sys.stdin.read(65537))
    except json.JSONDecodeError as exc:
        raise StoreError("invalid request JSON on stdin") from exc
    if not isinstance(value, dict):
        raise StoreError("request must be a JSON object")
    return value


def add_capture_guards(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workflow", action="store_true", help="Require explicit workflow enrollment")
    parser.add_argument("--permission-mode", choices=("execution", "plan"))
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--no-learning", action="store_true")


@contextmanager
def mutation_lock(state_dir: Path):
    # ponytail: one bounded repository lock; shard only if capture throughput matters.
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / "store.lock").open("a+b") as handle:
        if os.name == "nt":
            import msvcrt
            if handle.tell() == 0:
                handle.write(b"0")
                handle.flush()
            def lock():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            def unlock():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            def lock():
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            def unlock():
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        deadline = time.monotonic() + 2
        while True:
            try:
                lock()
                break
            except OSError as exc:
                if time.monotonic() >= deadline:
                    raise StoreError("learning store busy; skip capture and continue product delivery") from exc
                time.sleep(0.02)
        try:
            yield
        finally:
            unlock()


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command in {"list", "status"}:
        return args.handler(args)
    # These checks must precede reading a request or creating state/lock files.
    if getattr(args, "permission_mode", None) == "plan" or getattr(args, "read_only", False):
        return {"captured": False, "reason": "read_only", "review_due": False}
    if getattr(args, "no_learning", False):
        return {"captured": False, "reason": "no_learning", "review_due": False}
    root = resolve_root(args.root)
    config = config_for(root)
    if args.command in {"capture", "mark-no-candidate"}:
        if config["enabled"] is not True:
            return {"captured": False, "reason": "disabled", "review_due": False}
        if getattr(args, "workflow", False):
            if config.get("capture_mode", "explicit") != "workflow":
                return {"captured": False, "reason": "not_enrolled", "review_due": False}
            if args.permission_mode != "execution":
                raise StoreError("workflow capture requires --permission-mode execution")
    _, state_dir, _ = candidate_paths(root, config)
    with mutation_lock(state_dir):
        return args.handler(args)


def main() -> int:
    args = parse_args()
    try:
        result = run(args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (StoreError, OSError) as exc:
        print(f"project-learning store failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
