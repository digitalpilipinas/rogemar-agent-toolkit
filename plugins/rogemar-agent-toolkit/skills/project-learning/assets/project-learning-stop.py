#!/usr/bin/env python3
"""Passive signal collector for project-local learning.

The hook records only bounded turn metadata for a separate project-learning
task. It never blocks the current task, emits a model prompt, or persists
conversation text. All failures are intentionally fail-open.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


CONFIG_RELATIVE = Path(".codex/project-learning/config.json")
STATE_RELATIVE = Path(".codex/project-learning/state")
QUEUE_RELATIVE = STATE_RELATIVE / "queue"
MAX_TEXT_CHARS = 80_000

NO_LEARNING_PATTERNS = (
    re.compile(r"^\s*(?:please\s+)?(?:do not|don't|no)\s+(?:write|learn|remember)\b", re.I),
    re.compile(
        r"\b(?:for this task|this task|this turn)\b.{0,50}\b(?:do not|don't)\s+(?:write|learn|remember)\b",
        re.I | re.S,
    ),
)

USER_SIGNALS = {
    "correction": re.compile(
        r"\b(?:instead|not what|that's wrong|that is wrong|should have|must not|do not|don't)\b",
        re.I,
    ),
    "preference": re.compile(r"\b(?:i|we)\s+(?:want|prefer|need|expect)\b", re.I),
    "durable-rule": re.compile(
        r"\b(?:from now on|going forward|always|never|remember this|lesson learned|we learned)\b",
        re.I,
    ),
    "approval-change": re.compile(
        r"\b(?:approved|accepted|rejected|reject this|adapt this|supersede)\b", re.I
    ),
}

ASSISTANT_SIGNALS = {
    "verified-outcome": re.compile(
        r"\b(?:verified|validation passed|tests? passed|implemented|fixed|delivered)\b", re.I
    ),
    "failure-or-regression": re.compile(
        r"\b(?:root cause|failed because|regression|broke|incorrect assumption|conflict)\b", re.I
    ),
    "decision": re.compile(
        r"\b(?:decision|trade-?off|architecture|invariant|superseded|deferred)\b", re.I
    ),
}

MILESTONE_PATTERN = re.compile(
    r"\b(?:sprint|release|programme|program|milestone|phase)\s+(?:is\s+)?(?:complete|completed|done|delivered)\b",
    re.I,
)


def emit_allow() -> None:
    return


def safe_component(value: Any) -> str:
    text = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value or "unknown"))
    return text[:120] or "unknown"


def extract_text(content: Any) -> str:
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") not in {"input_text", "output_text", "text"}:
            continue
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts)


def visible_current_turn(transcript_path: Path) -> tuple[str, str] | None:
    user_messages: list[str] = []
    assistant_messages: list[str] = []
    saw_task_start = False

    with transcript_path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict):
                continue
            payload = record.get("payload")
            if record.get("type") == "event_msg" and isinstance(payload, dict):
                if payload.get("type") == "task_started":
                    saw_task_start = True
                    user_messages.clear()
                    assistant_messages.clear()
                continue
            if not saw_task_start or record.get("type") != "response_item":
                continue
            if not isinstance(payload, dict) or payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role not in {"user", "assistant"}:
                continue
            text = extract_text(payload.get("content")).strip()
            if not text:
                continue
            if role == "user" and text.startswith("<skill>") and text.endswith("</skill>"):
                continue
            if role == "user":
                user_messages.append(text)
            else:
                assistant_messages.append(text)

    if not saw_task_start:
        return None
    return (
        "\n".join(user_messages)[-MAX_TEXT_CHARS:],
        "\n".join(assistant_messages)[-MAX_TEXT_CHARS:],
    )


def find_signals(user_text: str, assistant_text: str) -> list[str]:
    signals: list[str] = []
    for label, pattern in USER_SIGNALS.items():
        if pattern.search(user_text):
            signals.append(label)
    for label, pattern in ASSISTANT_SIGNALS.items():
        if pattern.search(assistant_text):
            signals.append(label)
    return signals


def enqueue_signal(
    project_root: Path,
    *,
    session_id: str,
    turn_id: str,
    transcript_path: Path,
    signals: list[str],
    milestone: bool,
) -> None:
    queue_dir = project_root / QUEUE_RELATIVE
    queue_dir.mkdir(parents=True, exist_ok=True)
    queue_path = queue_dir / f"{session_id}-{turn_id}.json"
    if queue_path.exists():
        return
    event = {
        "schema_version": 1,
        "event_type": "turn_signal",
        "session_id": session_id,
        "turn_id": turn_id,
        "transcript_path": str(transcript_path),
        "signals": signals[:6],
        "milestone": milestone,
    }
    temporary_path = queue_dir / f".{queue_path.name}.{os.getpid()}.tmp"
    try:
        temporary_path.write_text(
            json.dumps(event, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        temporary_path.replace(queue_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        if payload.get("hook_event_name") != "Stop":
            return 0
        if payload.get("stop_hook_active") is True:
            return 0
        if payload.get("permission_mode") == "plan":
            return 0

        script_path = Path(__file__).resolve()
        project_root = script_path.parents[2]
        config_path = project_root / CONFIG_RELATIVE
        if not config_path.is_file():
            return 0
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict) or config.get("enabled") is not True:
            return 0
        if config.get("capture_policy") != "signal-gated":
            return 0

        session_id = safe_component(payload.get("session_id"))
        turn_id = safe_component(payload.get("turn_id"))
        queue_path = project_root / QUEUE_RELATIVE / f"{session_id}-{turn_id}.json"
        if queue_path.exists():
            return 0

        transcript_raw = payload.get("transcript_path")
        if not isinstance(transcript_raw, str) or not transcript_raw:
            return 0
        transcript_path = Path(transcript_raw)
        if not transcript_path.is_file():
            return 0
        visible = visible_current_turn(transcript_path)
        if visible is None:
            return 0
        user_text, transcript_assistant = visible
        last_assistant = payload.get("last_assistant_message")
        assistant_text = last_assistant if isinstance(last_assistant, str) else transcript_assistant

        if any(pattern.search(user_text) for pattern in NO_LEARNING_PATTERNS):
            return 0

        signals = find_signals(user_text, assistant_text)
        if not signals:
            return 0

        milestone = bool(MILESTONE_PATTERN.search(f"{user_text}\n{assistant_text}"))
        enqueue_signal(
            project_root,
            session_id=session_id,
            turn_id=turn_id,
            transcript_path=transcript_path,
            signals=signals,
            milestone=milestone,
        )
        return 0
    except Exception:
        emit_allow()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
