#!/usr/bin/env python3
"""Run one native provider with host-owned status, heartbeat, and artifacts.

This wrapper is used by managed background and visible host-owned modes. It
captures provider output, keeps truthful status, and surfaces recognizable
trust, authentication, or approval prompts as explicit manual attention.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import threading
import time


DEFAULT_MAX_OUTPUT = 2 * 1024 * 1024
HEARTBEAT_SECONDS = 15

AUTO_APPROVAL_FLAGS = {
    "grok": ["--always-approve"],
    "antigravity": ["--dangerously-skip-permissions"],
    "junie": ["--brave"],
    "cursor": ["--force"],
    "codex": ["--dangerously-bypass-approvals-and-sandbox"],
}
ATTENTION_PATTERNS = (
    (
        "workspace_trust_required",
        re.compile(
            r"^\s*(?![\"'`>])(?:do you )?trust "
            r"(the contents of )?(this|the) (project|folder|workspace)\b",
            re.I | re.MULTILINE,
        ),
    ),
    (
        "authentication_required",
        re.compile(
            r"^\s*(?![\"'`>])(?:(?:error|warning|fatal)\s*:\s*)?"
            r"(?:not logged in|authentication required|unauthenticated|sign in to continue|"
            r"secitemcopymatching failed -50)\b",
            re.I | re.MULTILINE,
        ),
    ),
    (
        "approval_required",
        re.compile(
            r"^\s*(?![\"'`>])(?:(?:error|warning|fatal)\s*:\s*)?"
            r"(?:requesting permission\b|do you want to proceed\b|"
            r"(?:approval|permission) required\b|"
            r"waiting for (?:user|approval)\b|permission check failed\b[^\n]*"
            r"\buser denied permission\b)",
            re.I | re.MULTILINE,
        ),
    ),
)
MARKDOWN_FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
MARKDOWN_QUOTE_PATTERN = re.compile(r"^(?: {4,}|\t| {0,3}>)")


def attention_reason_for_line(
    line: str,
    active_fence: str | None,
) -> tuple[str | None, str | None]:
    fence = MARKDOWN_FENCE_PATTERN.match(line)
    if fence:
        marker = fence.group(1)[0]
        if active_fence is None:
            return None, marker
        if marker == active_fence:
            return None, None
        return None, active_fence
    if active_fence is not None or MARKDOWN_QUOTE_PATTERN.match(line):
        return None, active_fence
    for reason, pattern in ATTENTION_PATTERNS:
        if pattern.search(line):
            return reason, active_fence
    return None, active_fence


def attention_reason(output: str) -> str | None:
    active_fence: str | None = None
    for line in output.splitlines():
        reason, active_fence = attention_reason_for_line(line, active_fence)
        if reason:
            return reason
    return None


def workspace_authority(manifest: dict[str, object]) -> str | None:
    authority = manifest.get("authority")
    if not isinstance(authority, dict):
        return None
    value = authority.get("workspace")
    return str(value) if value is not None else None


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def provider_entries(manifest: dict[str, object]) -> list[dict[str, object]]:
    raw = manifest.get("providers", [])
    if not isinstance(raw, list):
        return []
    entries: list[dict[str, object]] = []
    for item in raw:
        if isinstance(item, str):
            provider_id = item.lower()
            entries.append({"id": provider_id, "artifact_dir": provider_id, "command": item})
        elif isinstance(item, dict):
            provider_id = str(item.get("id", "provider")).lower()
            entries.append(
                {
                    "id": provider_id,
                    "artifact_dir": str(item.get("artifact_dir", provider_id)),
                    "command": str(item.get("command", provider_id)),
                    "model": item.get("model"),
                    "effort": item.get("effort"),
                }
            )
    return entries


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def write_status(provider_dir: Path, *, state: str, phase: str, started_at: str,
                 progress: str, last_activity: str | None = None,
                 first_output_at: str | None = None, response_at: str | None = None,
                 completed_at: str | None = None,
                 duration_seconds: float | None = None,
                 attention: str | None = None) -> None:
    updated = utc_now()
    activity = last_activity or updated
    content = (
        f"state: {state}\n"
        f"phase: {phase}\n"
        f"started_at: {started_at}\n"
        f"updated_at: {updated}\n"
        f"last_activity: {activity}\n"
        f"progress: {progress.replace(chr(10), ' ')[:240]}\n"
        "artifact_owner: host\n"
    )
    if first_output_at:
        content += f"first_output_at: {first_output_at}\n"
    if response_at:
        content += f"response_at: {response_at}\n"
    if completed_at:
        content += f"completed_at: {completed_at}\n"
    if duration_seconds is not None:
        content += f"duration_seconds: {duration_seconds:.3f}\n"
    if attention:
        content += f"attention: {attention}\n"
    atomic_write(provider_dir / "status.md", content)


def append_event(provider_dir: Path, event: dict[str, object]) -> None:
    event = {"at": utc_now(), **event}
    with (provider_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def build_command(entry: dict[str, object], *, workspace: Path, run_dir: Path,
                  prompt: str, timeout_seconds: int, auto_approve: bool,
                  mode: str | None = None) -> list[str]:
    provider_id = str(entry["id"]).lower()
    if entry.get("entry_command"):
        raise ValueError(
            "provider-native entry commands require visible interactive launch; "
            "the managed runner must not translate them into one-shot prompts"
        )
    command = str(entry.get("command", provider_id))
    model = entry.get("model")
    effort = entry.get("effort")
    args = [command]
    if provider_id == "grok":
        args.extend(["--cwd", str(workspace), "--no-alt-screen"])
        if model:
            args.extend(["--model", str(model)])
        if effort:
            args.extend(["--reasoning-effort", str(effort)])
        args.extend(["--debug-file", str(run_dir / "logs" / "grok.log")])
        if auto_approve:
            args.extend(AUTO_APPROVAL_FLAGS[provider_id])
        # Grok's prompt-file option avoids putting a large prompt in argv.
        args.extend(["--prompt-file", str(run_dir / str(entry["artifact_dir"]) / "prompt.md")])
    elif provider_id == "antigravity":
        args.extend([
            "--print-timeout", f"{timeout_seconds}s",
            "--add-dir", str(run_dir),
        ])
        if model:
            args.extend(["--model", str(model)])
        if effort:
            args.extend(["--effort", str(effort)])
        args.extend(["--log-file", str(run_dir / "logs" / "antigravity.log")])
        if auto_approve:
            args.extend(AUTO_APPROVAL_FLAGS[provider_id])
        # Do not claim that prompt allowlists enforce a filesystem sandbox.
        # Without explicit auto-approval, provider permissions remain
        # fail-closed and unavailable commands must be reported as not run.
        args.extend(["--prompt", prompt])
    elif provider_id == "junie":
        args.extend(["--project", str(workspace), "--skip-update-check"])
        if model:
            args.extend(["--model", str(model)])
        if effort:
            args.extend(["--effort", str(effort)])
        if auto_approve:
            args.extend(AUTO_APPROVAL_FLAGS[provider_id])
        args.extend(["--prompt", prompt])
    elif provider_id == "cursor":
        args.extend([
            "--print",
            "--output-format", "text",
            "--workspace", str(workspace),
            # The manifest already freezes the exact workspace and authority.
            # Confirm that workspace trust non-interactively so a background
            # review does not fail before Cursor reaches its read-only mode.
            "--trust",
        ])
        if mode in {"plan", "review", "validation"}:
            args.extend(["--mode", "plan"])
        if model:
            args.extend(["--model", str(model)])
        if auto_approve:
            args.extend(AUTO_APPROVAL_FLAGS[provider_id])
        # Cursor accepts the initial prompt as a positional argument. MCP
        # approval remains interactive; never add --approve-mcps implicitly.
        args.append(prompt)
    elif provider_id == "codex":
        # Use the non-interactive subcommand for host-owned runs. The prompt
        # is supplied through stdin so a large brief is not exposed in argv.
        args.extend(["exec", "--cd", str(workspace)])
        if model:
            args.extend(["--model", str(model)])
        if auto_approve:
            args.extend(AUTO_APPROVAL_FLAGS[provider_id])
        args.append("-")
    else:
        args.append(prompt)
    return args


def terminate_process(process: subprocess.Popen[str]) -> None:
    try:
        if process.poll() is not None:
            return
        if hasattr(os, "killpg") and process.pid:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
                return
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                return
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    except (OSError, ProcessLookupError):
        pass


def write_result(provider_dir: Path, *, state: str, returncode: int | None,
                 output: str, timed_out: bool = False, cancelled: bool = False,
                 started_at: str | None = None, first_output_at: str | None = None,
                 response_at: str | None = None,
                 completed_at: str | None = None,
                 duration_seconds: float | None = None) -> None:
    if state == "needs_attention":
        summary = "The provider requires visible manual attention before it can continue."
        limitations = "The background attempt is incomplete; use the recorded visible fallback and approve only in-scope actions."
    elif timed_out:
        summary = "The provider exceeded the configured timeout and was terminated by the host runner."
        limitations = "No complete provider report was available before the timeout."
    elif cancelled:
        summary = "The provider was cancelled by the user or host runner."
        limitations = "The report is incomplete because the provider did not reach normal completion."
    elif state == "failed":
        summary = f"The provider exited unsuccessfully (exit code {returncode})."
        limitations = "Treat this as incomplete provider evidence; Codex must not infer a clean result."
    elif state == "completed_with_warnings":
        summary = "The provider exited successfully, but produced no substantive stdout report."
        limitations = "The run is terminal but not sufficient as an independent review."
    else:
        summary = "The host runner captured the provider's completed stdout report."
        limitations = "Provider output is evidence; Codex must independently validate findings."
    body = output.strip() or "(no provider stdout was captured)"
    if len(body.encode("utf-8")) > DEFAULT_MAX_OUTPUT:
        encoded = body.encode("utf-8")[:DEFAULT_MAX_OUTPUT]
        body = encoded.decode("utf-8", "ignore") + "\n<truncated by host runner>"
    content = (
        "# Result\n"
        f"## Summary\n{summary}\n\n"
        f"## Findings\n{body}\n\n"
        f"## Evidence\nHost artifact owner: run_provider.py\nProvider exit code: {returncode}\n"
        f"Terminal state: {state}\n"
        f"Started at: {started_at or 'unknown'}\n"
        f"First output at: {first_output_at or 'no provider output captured'}\n"
        f"Response at: {response_at or 'no provider output captured'}\n"
        f"Completed at: {completed_at or 'unknown'}\n"
        f"Duration seconds: {duration_seconds if duration_seconds is not None else 'unknown'}\n\n"
        "## Changes\nThe host runner did not modify repository files.\n\n"
        "## Validation\nThe host captured stdout and the provider exit state; Codex validation remains required.\n\n"
        f"## Limitations\n{limitations}\n"
    )
    atomic_write(provider_dir / "result.md", content)


def append_owner_completion(run_dir: Path, provider_id: str, *, state: str,
                            started_at: str, first_output_at: str | None,
                            response_at: str | None,
                            completed_at: str, duration_seconds: float) -> None:
    notice = run_dir / "owner_notice.md"
    if not notice.exists():
        return
    with notice.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## Completion benchmark: " + provider_id + "\n"
            f"- state: {state}\n"
            f"- started_at: {started_at}\n"
            f"- first_output_at: {first_output_at or 'no provider output captured'}\n"
            f"- response_at: {response_at or 'no provider output captured'}\n"
            f"- completed_at: {completed_at}\n"
            f"- duration_seconds: {duration_seconds:.3f}\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--timeout-seconds", required=True, type=int)
    parser.add_argument("--approval-policy", choices=("manual", "full-auto"))
    parser.add_argument("--fallback-visible", action="store_true")
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help=(
            "legacy alias for full-auto; this is a breaking safety boundary "
            "and requires explicit owner authorization"
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout-seconds must be positive")
    if args.auto_approve and args.approval_policy is not None:
        parser.error("--auto-approve cannot be combined with explicit --approval-policy")
    run_dir = args.run.expanduser().resolve(strict=True)
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    approval_policy = "full-auto" if args.auto_approve else (args.approval_policy or "manual")
    if approval_policy == "full-auto" and workspace_authority(manifest) != "isolated-worktree":
        parser.error("full-auto requires manifest workspace authority isolated-worktree")
    entries = [entry for entry in provider_entries(manifest) if entry["id"] == args.provider.lower()]
    if not entries:
        parser.error(f"provider is not present in manifest: {args.provider}")
    entry = entries[0]
    provider_dir = run_dir / str(entry["artifact_dir"])
    prompt_path = provider_dir / "prompt.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    workspace = Path(str(manifest["workspace"])).expanduser().resolve(strict=True)
    command = build_command(
        entry,
        workspace=workspace,
        run_dir=run_dir,
        prompt=prompt,
        timeout_seconds=args.timeout_seconds,
        auto_approve=approval_policy == "full-auto",
        mode=str(manifest.get("mode")) if manifest.get("mode") is not None else None,
    )
    if args.dry_run:
        print(json.dumps({"provider": entry["id"], "timeout_seconds": args.timeout_seconds,
                          "approval_policy": approval_policy,
                          "auto_approve": approval_policy == "full-auto",
                          "fallback_visible": args.fallback_visible,
                          "command": command}, indent=2))
        return 0

    provider_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    if approval_policy == "full-auto":
        print("WARNING: provider-native full-auto is enabled only with explicit owner authorization.", flush=True)
        print("WARNING: isolated-worktree and allowed_paths are administrative records, not sandboxes for filesystem, host, network, or external actions.", flush=True)
    started_at = utc_now()
    started_monotonic = time.monotonic()
    write_status(provider_dir, state="running", phase="starting", started_at=started_at,
                 progress="provider process starting")
    append_event(provider_dir, {"type": "host_started", "provider": entry["id"],
                                "timeout_seconds": args.timeout_seconds,
                                "approval_policy": approval_policy,
                                "auto_approve": approval_policy == "full-auto",
                                "fallback_visible": args.fallback_visible})
    print("Host-owned artifact runner starting:", " ".join(command[:4]), "...", flush=True)

    output_queue: queue.Queue[str | None] = queue.Queue()
    captured: list[str] = []
    captured_bytes = 0
    last_activity = started_at
    first_output_at: str | None = None
    last_output_at: str | None = None
    last_activity_lock = threading.Lock()

    prompt_stdin = None
    if str(entry["id"]).lower() == "codex":
        # `codex exec -` reads the prepared brief from stdin. Keep the prompt
        # out of the command line and close the parent descriptor after spawn.
        prompt_stdin = prompt_path.open("r", encoding="utf-8")
    try:
        process = subprocess.Popen(
            command,
            cwd=workspace,
            stdin=prompt_stdin or subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
    except OSError as exc:
        if prompt_stdin is not None:
            prompt_stdin.close()
        completed_at = utc_now()
        duration_seconds = time.monotonic() - started_monotonic
        write_status(provider_dir, state="failed", phase="failed", started_at=started_at,
                     progress=f"provider could not start: {type(exc).__name__}",
                     completed_at=completed_at, duration_seconds=duration_seconds)
        write_result(provider_dir, state="failed", returncode=None, output=str(exc),
                     started_at=started_at, completed_at=completed_at,
                     duration_seconds=duration_seconds)
        append_event(provider_dir, {"type": "host_failed_to_start", "error": type(exc).__name__})
        append_owner_completion(run_dir, str(entry["id"]), state="failed",
                                started_at=started_at, first_output_at=None,
                                response_at=None,
                                completed_at=completed_at, duration_seconds=duration_seconds)
        return 1
    finally:
        if prompt_stdin is not None:
            prompt_stdin.close()

    def read_output() -> None:
        assert process.stdout is not None
        try:
            for line in process.stdout:
                output_queue.put(line)
        finally:
            output_queue.put(None)

    reader = threading.Thread(target=read_output, name="provider-output", daemon=True)
    reader.start()
    deadline = time.monotonic() + args.timeout_seconds
    saw_output = False
    ended = False
    timed_out = False
    cancelled = False
    manual_attention: str | None = None
    attention_fence: str | None = None
    try:
        while not ended:
            remaining = deadline - time.monotonic()
            if remaining <= 0 and process.poll() is None:
                timed_out = True
                terminate_process(process)
                ended = True
                break
            try:
                line = output_queue.get(timeout=min(HEARTBEAT_SECONDS, max(0.1, remaining)))
                if line is None:
                    ended = process.poll() is not None
                    continue
                print(line, end="", flush=True)
                encoded_size = len(line.encode("utf-8", "replace"))
                if captured_bytes < DEFAULT_MAX_OUTPUT:
                    remaining = DEFAULT_MAX_OUTPUT - captured_bytes
                    captured.append(line.encode("utf-8", "replace")[:remaining].decode("utf-8", "ignore"))
                    captured_bytes += min(encoded_size, remaining)
                saw_output = True
                with last_activity_lock:
                    last_activity = utc_now()
                    if first_output_at is None:
                        first_output_at = last_activity
                    last_output_at = last_activity
                write_status(provider_dir, state="running", phase="analysis", started_at=started_at,
                             progress="provider output received", last_activity=last_activity)
                if args.fallback_visible:
                    manual_attention, attention_fence = attention_reason_for_line(
                        line,
                        attention_fence,
                    )
                    if manual_attention:
                        terminate_process(process)
                        ended = True
                        break
            except queue.Empty:
                if process.poll() is None and time.monotonic() < deadline:
                    with last_activity_lock:
                        activity = last_activity
                    write_status(provider_dir, state="running", phase="waiting", started_at=started_at,
                                 progress="provider still running; no new output", last_activity=activity)
                    append_event(provider_dir, {"type": "host_heartbeat"})
            if process.poll() is not None and output_queue.empty():
                ended = True
            if time.monotonic() >= deadline and process.poll() is None:
                timed_out = True
                terminate_process(process)
                ended = True
    except KeyboardInterrupt:
        cancelled = True
        terminate_process(process)
    finally:
        returncode = process.wait(timeout=10) if process.poll() is None else process.returncode
        reader.join(timeout=2)
        if process.stdout is not None:
            process.stdout.close()

    output = "".join(captured)
    completed_at = utc_now()
    duration_seconds = time.monotonic() - started_monotonic
    response_at = last_output_at
    if manual_attention:
        state = "needs_attention"
        phase = "attention"
    elif timed_out:
        state = "timed_out"
        phase = "timeout"
    elif cancelled:
        state = "cancelled"
        phase = "cancelled"
    elif returncode == 0 and saw_output:
        state = "succeeded"
        phase = "done"
    elif returncode == 0:
        state = "completed_with_warnings"
        phase = "done_with_warnings"
    else:
        state = "failed"
        phase = "failed"
    write_result(provider_dir, state=state, returncode=returncode, output=output,
                 timed_out=timed_out, cancelled=cancelled, started_at=started_at,
                 first_output_at=first_output_at, response_at=response_at,
                 completed_at=completed_at,
                 duration_seconds=duration_seconds)
    write_status(provider_dir, state=state, phase=phase, started_at=started_at,
                 progress=f"host runner terminal state: {state}", last_activity=utc_now(),
                 first_output_at=first_output_at, response_at=response_at,
                 completed_at=completed_at,
                 duration_seconds=duration_seconds,
                 attention=manual_attention)
    if manual_attention:
        fallback_command = [
            "python3",
            str(Path(__file__).with_name("launch_terminals.py").resolve()),
            "--run", str(run_dir),
            "--provider", str(entry["id"]),
            "--execution", "visible",
            "--approval-policy", "manual",
        ]
        atomic_write(
            provider_dir / "attention.json",
            json.dumps({
                "at": completed_at,
                "provider": entry["id"],
                "reason": manual_attention,
                "approval_policy": approval_policy,
                "visible_fallback_command": fallback_command,
            }, indent=2) + "\n",
        )
    append_event(provider_dir, {"type": "host_finished", "state": state,
                                "returncode": returncode, "output_bytes": len(output.encode("utf-8"))})
    append_owner_completion(run_dir, str(entry["id"]), state=state,
                            started_at=started_at, first_output_at=first_output_at,
                            response_at=response_at,
                            completed_at=completed_at, duration_seconds=duration_seconds)
    if state == "needs_attention":
        return 2
    return 0 if state in {"succeeded", "completed_with_warnings"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
