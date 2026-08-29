#!/usr/bin/env python3
"""Launch prepared native-agent prompts in managed PTYs, background runs, or a physical fallback."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from datetime import datetime, timezone


DEFAULT_TIMEOUTS = {
    "grok": 20 * 60,
    "antigravity": 30 * 60,
    "junie": 30 * 60,
    "cursor": 30 * 60,
    "codex": 30 * 60,
}

INTERACTIVE_COMMANDS = {
    "grok": "grok",
    "antigravity": "agy",
    "cursor": "agent",
    "codex": "codex",
}
APPROVAL_POLICIES = {"manual", "full-auto"}
EXECUTION_MODES = {"visible", "background", "managed-pty"}


def _read_launch_receipt(path: Path) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _prior_launch_receipts(path: Path) -> list[dict[str, object]]:
    """Keep prior launch evidence when a run is relaunched for fallback.

    ``launch.json`` remains the current receipt.  The small ``launch_attempts``
    list carries receipts written by an earlier invocation so a visible
    fallback cannot erase the original background launch evidence.
    """
    receipt = _read_launch_receipt(path)
    if receipt is None:
        return []
    attempts = receipt.get("launch_attempts")
    current = dict(receipt)
    current.pop("launch_attempts", None)
    if isinstance(attempts, list):
        return [item for item in attempts if isinstance(item, dict)] + [current]
    return [receipt]


def _receipt_timestamps(receipt: dict[str, object]) -> list[str]:
    values: list[str] = []
    monitor_started = receipt.get("monitor_started_at")
    if isinstance(monitor_started, str) and monitor_started:
        values.append(monitor_started)
    providers = receipt.get("providers")
    if isinstance(providers, list):
        for provider in providers:
            if not isinstance(provider, dict):
                continue
            for key in ("started_at", "opened_at"):
                value = provider.get(key)
                if isinstance(value, str) and value:
                    values.append(value)
    return values


def _earliest_timestamp(values: list[str]) -> str | None:
    parsed: list[tuple[datetime, str]] = []
    for value in values:
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            continue
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        parsed.append((timestamp, value))
    return min(parsed, key=lambda item: item[0])[1] if parsed else None


def _append_owner_notice(path: Path, section: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        has_content = path.stat().st_size > 0
    except OSError:
        has_content = False
    prefix = "\n---\n\n" if has_content else ""
    payload = (prefix + section.rstrip() + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, payload)
    finally:
        os.close(descriptor)


def prompt_submission_mode(execution_mode: str) -> str:
    return (
        "host_runner_at_launch"
        if execution_mode in {"background", "visible_hosted"}
        else "manual_after_provider_ready"
    )


def manifest_policy(manifest: dict[str, object]) -> tuple[str, str, bool]:
    execution = manifest.get("execution")
    if not isinstance(execution, dict):
        return "visible", "manual", False
    mode = str(execution.get("mode", "visible"))
    legacy_unattended = mode == "unattended"
    if legacy_unattended:
        mode = "background"
    return (
        mode,
        str(execution.get("approval_policy", "manual")),
        bool(execution.get("fallback_visible", False)) or legacy_unattended,
    )


def workspace_authority(manifest: dict[str, object]) -> str | None:
    authority = manifest.get("authority")
    if not isinstance(authority, dict):
        return None
    value = authority.get("workspace")
    return str(value) if value is not None else None


def validate_launch_policy(
    *, execution: str, approval_policy: str, fallback_visible: bool,
    authority: str | None,
) -> None:
    if execution not in EXECUTION_MODES:
        raise ValueError(f"unsupported execution mode: {execution}")
    if approval_policy not in APPROVAL_POLICIES:
        raise ValueError(f"unsupported approval policy: {approval_policy}")
    if approval_policy == "full-auto" and authority != "isolated-worktree":
        raise ValueError("full-auto requires manifest workspace authority isolated-worktree")
    if execution == "managed-pty" and approval_policy != "manual":
        raise ValueError("managed-pty requires manual approval")
    if execution == "background" and approval_policy == "manual" and not fallback_visible:
        raise ValueError("background manual approval requires visible fallback")


def validate_native_entry_policy(
    *, entries: list[dict[str, object]], execution_mode: str,
) -> None:
    native_entries = [str(entry["id"]) for entry in entries if entry.get("entry_command")]
    if native_entries and execution_mode not in {"interactive", "managed_pty"}:
        raise ValueError(
            "native entry commands require managed PTY or visible interactive execution: "
            + ", ".join(native_entries)
        )


def provider_entries(manifest: dict[str, object]) -> list[dict[str, object]]:
    raw = manifest.get("providers")
    if not isinstance(raw, list):
        return []
    entries: list[dict[str, object]] = []
    for item in raw:
        if isinstance(item, str):
            provider_id = item.lower()
            entries.append(
                {
                    "id": provider_id,
                    "artifact_dir": provider_id,
                    "command": item,
                    "model": None,
                    "effort": None,
                    "timeout_seconds": None,
                }
            )
        elif isinstance(item, dict):
            provider_id = str(item.get("id", "provider")).lower()
            entries.append(
                {
                    "id": provider_id,
                    "artifact_dir": str(item.get("artifact_dir", provider_id)),
                    "command": str(item.get("command", provider_id)),
                    "model": item.get("model"),
                    "effort": item.get("effort"),
                    "timeout_seconds": item.get("timeout_seconds"),
                    "entry_command": item.get("entry_command"),
                }
            )
    return entries


def shell_script(
    *,
    provider: dict[str, object],
    workspace: Path,
    run_dir: Path,
    approval_policy: str,
    fallback_visible: bool,
    timeout_seconds: int,
    manifest_mode: str | None,
    execution_mode: str,
) -> tuple[str, str]:
    provider_id = str(provider["id"])
    configured_command = str(provider["command"])
    prompt_path = run_dir / str(provider["artifact_dir"]) / "prompt.md"
    if execution_mode in {"background", "visible_hosted"}:
        runner_path = Path(__file__).with_name("run_provider.py").resolve()
        runner_args = [
            "python3",
            str(runner_path),
            "--run", str(run_dir),
            "--provider", provider_id,
            "--timeout-seconds", str(timeout_seconds),
        ]
        runner_args.extend(["--approval-policy", approval_policy])
        if fallback_visible:
            runner_args.append("--fallback-visible")
        command_line = " ".join(shlex.quote(value) for value in runner_args)
        warning_line = (
            "printf '%s\\n' 'WARNING: full-auto requires explicit owner authorization "
            "and is not bounded by allowed paths.'\n"
            if approval_policy == "full-auto"
            else ""
        )
        script = f"""#!/bin/zsh
set -u
cd -- {shlex.quote(str(workspace))}
printf '%s\\n' 'Agent Collaboration Terminal: {provider_id}'
printf '%s\\n' 'Execution mode: host-owned {execution_mode} runner'
printf '%s\\n' 'Approval policy: {approval_policy}'
{warning_line}printf '%s\\n' 'Prompt: {prompt_path}'
exec {command_line}
"""
        approval_note = f"host-owned runner with {approval_policy} approval"
        if approval_policy == "full-auto":
            approval_note += "; explicit owner authorization required"
        return script, approval_note

    # Visible and Codex-managed interactive modes deliberately start only the
    # native CLI. Prompt submission is a second, operator-observed step after
    # the provider shows that it is ready for input.
    command = INTERACTIVE_COMMANDS.get(provider_id, configured_command)
    command_line = shlex.quote(command)
    managed_pty = execution_mode == "managed_pty"
    approval_note = (
        "manual approvals remain visible in the Codex-managed PTY"
        if managed_pty
        else "interactive approvals remain visible in Terminal"
    )
    entry_command = provider.get("entry_command")
    entry_line = (
        f"printf '%s\\n' {shlex.quote('Native entry command: ' + str(entry_command))}\n"
        if entry_command
        else ""
    )
    startup_note = (
        "Starting the provider CLI in the Codex-managed PTY without submitting the task prompt."
        if managed_pty
        else "Starting the provider CLI without submitting the task prompt."
    )
    ready_note = (
        "Wait until the native CLI is ready; Codex will submit the standalone entry command "
        "and then the prepared follow-up."
        if managed_pty
        else "Wait until the native CLI is ready, then paste and submit the prepared prompt above."
    )
    script = f"""#!/bin/zsh
set -u
cd -- {shlex.quote(str(workspace))}
printf '%s\\n' 'Agent Collaboration Terminal: {provider_id}'
printf '%s\\n' 'Approval policy: {approval_note}'
printf '%s\\n' 'Prompt: {prompt_path}'
{entry_line}printf '%s\\n' {shlex.quote(startup_note)}
printf '%s\\n' {shlex.quote(ready_note)}
exec {command_line}
"""
    return script, approval_note


def launch_background(script_path: Path, diagnostics_path: Path) -> int:
    """Start one host-owned provider runner without opening Terminal.app."""
    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    with diagnostics_path.open("ab", buffering=0) as diagnostics:
        process = subprocess.Popen(
            ["/bin/zsh", str(script_path)],
            stdin=subprocess.DEVNULL,
            stdout=diagnostics,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    return process.pid


def open_terminal(script_path: Path) -> str:
    """Open a real Terminal.app window and return its window identifier.

    A successful `osascript` exit alone is not enough: the command can be
    accepted while the GUI launch is unavailable to the calling task.  Returning
    the Terminal window id lets the receipt prove that a visible terminal was
    requested and created.  Callers must treat an empty id as a launch failure.
    """
    if sys.platform != "darwin":
        raise RuntimeError("visible Terminal.app launch is supported only on macOS")
    command = f"/bin/zsh {shlex.quote(str(script_path))}"
    applescript = (
        "tell application \"Terminal\"\n"
        "activate\n"
        "do script " + json.dumps(command) + "\n"
        "set terminalWindowId to id of front window\n"
        "delay 1\n"
        "activate\n"
        "return terminalWindowId as text\n"
        "end tell"
    )
    result = subprocess.run(
        ["osascript", "-e", applescript],
        check=True,
        capture_output=True,
        text=True,
    )
    window_id = result.stdout.strip()
    if not window_id:
        raise RuntimeError(
            "Terminal.app accepted the launch request but returned no window id; "
            "the provider was not considered visibly launched"
        )
    return window_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--provider", action="append", default=[])
    parser.add_argument("--execution", choices=sorted(EXECUTION_MODES))
    parser.add_argument("--approval-policy", choices=sorted(APPROVAL_POLICIES))
    parser.add_argument("--fallback-visible", action="store_true")
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help=(
            "legacy alias for --approval-policy full-auto; this is a breaking "
            "safety boundary and requires explicit owner authorization"
        ),
    )
    parser.add_argument("--timeout-seconds", type=int)
    parser.add_argument(
        "--unattended",
        action="store_true",
        help="legacy alias for --execution background",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.timeout_seconds is not None and args.timeout_seconds < 1:
        parser.error("timeout-seconds must be positive")
    if args.auto_approve and args.approval_policy is not None:
        parser.error("--auto-approve cannot be combined with explicit --approval-policy")

    run_dir = args.run.expanduser().resolve(strict=True)
    manifest_path = run_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        parser.error(f"missing manifest: {manifest_path}")
    except json.JSONDecodeError as exc:
        parser.error(f"invalid manifest: {exc}")
    if not isinstance(manifest, dict):
        parser.error("manifest must be an object")
    configured_execution, configured_approval, configured_fallback = manifest_policy(manifest)
    execution = args.execution or ("background" if args.unattended else configured_execution)
    approval_policy = args.approval_policy or (
        "full-auto" if args.auto_approve else configured_approval
    )
    # Schema-2 callers used --unattended as the one-shot background mode.  Keep
    # its safe visible fallback even when the newer execution block is absent.
    fallback_visible = args.fallback_visible or configured_fallback or args.unattended
    try:
        validate_launch_policy(
            execution=execution,
            approval_policy=approval_policy,
            fallback_visible=fallback_visible,
            authority=workspace_authority(manifest),
        )
    except ValueError as exc:
        parser.error(str(exc))
    execution_mode = (
        "background"
        if execution == "background"
        else "managed_pty"
        if execution == "managed-pty"
        else "visible_hosted" if approval_policy == "full-auto" else "interactive"
    )
    workspace_value = manifest.get("workspace")
    if not isinstance(workspace_value, str):
        parser.error("manifest workspace is missing")
    workspace = Path(workspace_value).expanduser().resolve(strict=True)
    manifest_mode = manifest.get("mode")
    if manifest_mode is not None and not isinstance(manifest_mode, str):
        parser.error("manifest mode must be a string when present")
    entries = provider_entries(manifest)
    selected = {value.strip().lower() for value in args.provider if value.strip()}
    if selected:
        entries = [entry for entry in entries if str(entry["id"]).lower() in selected]
    if not entries:
        parser.error("no matching providers in manifest")
    if execution == "managed-pty" and len(entries) != 1:
        parser.error("managed-pty launches exactly one provider; select one --provider")
    try:
        validate_native_entry_policy(entries=entries, execution_mode=execution_mode)
    except ValueError as exc:
        parser.error(str(exc))

    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    launch_records: list[dict[str, object]] = []
    failures: list[str] = []
    managed_script_path: Path | None = None
    if approval_policy == "full-auto":
        print("WARNING: provider-native full-auto is enabled only with explicit owner authorization.")
        print("WARNING: isolated-worktree and allowed_paths are administrative records, not sandboxes for filesystem, host, network, or external actions.")
    elif execution == "background":
        print("Managed background mode is fail-closed and will surface manual attention.")
    elif execution == "managed-pty":
        print("Codex-managed PTY mode requires this launcher to run with tty=true.")

    launch_path = run_dir / "launch.json"
    prior_launches = _prior_launch_receipts(launch_path)

    for provider in entries:
        provider_id = str(provider["id"])
        timeout_seconds = args.timeout_seconds or int(
            provider.get("timeout_seconds") or DEFAULT_TIMEOUTS.get(provider_id, 30 * 60)
        )
        script, approval_note = shell_script(
            provider=provider,
            workspace=workspace,
            run_dir=run_dir,
            approval_policy=approval_policy,
            fallback_visible=fallback_visible,
            timeout_seconds=timeout_seconds,
            manifest_mode=manifest_mode,
            execution_mode=execution_mode,
        )
        script_path = run_dir / "logs" / f"launch-{provider_id}.sh"
        script_path.write_text(script, encoding="utf-8")
        os.chmod(script_path, 0o700)
        record: dict[str, object] = {
            "provider": provider_id,
            "script": str(script_path),
            "prompt": str(run_dir / str(provider["artifact_dir"]) / "prompt.md"),
            "status": str(run_dir / str(provider["artifact_dir"]) / "status.md"),
            "events": str(run_dir / str(provider["artifact_dir"]) / "events.jsonl"),
            "result": str(run_dir / str(provider["artifact_dir"]) / "result.md"),
            "diagnostics": str(run_dir / "logs" / f"{provider_id}.log"),
            "approval": approval_note,
            "approval_policy": approval_policy,
            "execution_mode": execution_mode,
            "timeout_seconds": timeout_seconds,
            "started": False,
            "opened": False,
            "visibility": (
                "background_process"
                if execution == "background"
                else "codex_managed_pty"
                if execution == "managed-pty"
                else "physical_terminal_required"
            ),
            "prompt_submission": prompt_submission_mode(execution_mode),
            "entry_command": provider.get("entry_command"),
        }
        if fallback_visible:
            record["visible_fallback"] = (
                f"python3 {Path(__file__).resolve()} --run {run_dir} "
                f"--provider {provider_id} --execution visible --approval-policy manual"
            )
        if args.dry_run:
            record["command_preview"] = script
        else:
            try:
                if execution == "background":
                    background_log = run_dir / "logs" / f"background-{provider_id}.log"
                    record["pid"] = launch_background(script_path, background_log)
                    record["background_log"] = str(background_log)
                    record["started"] = True
                    record["started_at"] = datetime.now(timezone.utc).isoformat()
                elif execution == "managed-pty":
                    if not (sys.stdin.isatty() and sys.stdout.isatty()):
                        raise RuntimeError(
                            "managed-pty requires a Codex-managed terminal session with tty=true"
                        )
                    managed_script_path = script_path
                    record["managed_pty_command"] = [
                        "/bin/zsh",
                        str(script_path),
                    ]
                    record["started"] = True
                    record["started_at"] = datetime.now(timezone.utc).isoformat()
                else:
                    window_id = open_terminal(script_path)
                    record["started"] = True
                    record["opened"] = True
                    record["window_id"] = window_id
                    record["opened_at"] = datetime.now(timezone.utc).isoformat()
            except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
                failures.append(f"{provider_id}: {type(exc).__name__}: {exc}")
                record["error"] = str(exc)
        launch_records.append(record)

    started_times = [
        str(record.get("started_at") or record.get("opened_at"))
        for record in launch_records
        if record.get("started") and (record.get("started_at") or record.get("opened_at"))
    ]
    prior_times = [
        timestamp
        for prior in prior_launches
        for timestamp in _receipt_timestamps(prior)
    ]
    launch_receipt = {
        "run_id": manifest.get("run_id"),
        "run": str(run_dir),
        "mode": "dry_run" if args.dry_run else execution,
        "execution_mode": "dry_run" if args.dry_run else execution_mode,
        "visibility": "not_launched" if args.dry_run else (
            "background_process"
            if execution == "background"
            else "codex_managed_pty"
            if execution == "managed-pty"
            else "physical_terminal_required"
        ),
        "approval_policy": approval_policy,
        "auto_approve": approval_policy == "full-auto",
        "fallback_visible": fallback_visible,
        "timeout_seconds": args.timeout_seconds,
        "monitor_started_at": _earliest_timestamp(prior_times + started_times),
        "providers": launch_records,
        "errors": failures,
    }
    if prior_launches:
        launch_receipt["launch_attempts"] = prior_launches
    launch_path.write_text(json.dumps(launch_receipt, indent=2) + "\n", encoding="utf-8")
    notice_lines = [
        "# Agent Collaboration Terminal launch",
        "",
        f"Run: {run_dir}",
        f"Workspace: {workspace}",
        f"Mode: {manifest_mode or 'unspecified'}",
        f"Execution mode: {'dry_run' if args.dry_run else execution_mode}",
        f"Approval policy: {approval_policy}",
        f"Monitoring starts: {launch_receipt['monitor_started_at'] or 'when provider start is confirmed'}",
        "",
        "The exact provider instructions are in each prompt file below. Codex should read these files before summarizing provider work.",
        "",
    ]
    if approval_policy == "full-auto":
        notice_lines.extend(
            [
                "WARNING: provider-native full-auto requires explicit owner authorization and crosses a breaking safety boundary.",
                "WARNING: isolated-worktree, allowed_paths, and excluded_paths are administrative records only; they are not filesystem, host, network, or external-action sandboxes.",
                "",
            ]
        )
    elif prior_launches:
        notice_lines.extend(
            [
                "This launch is a fallback/relaunch attempt. Prior launch receipt(s) and owner evidence are preserved above and in launch.json.",
                "",
            ]
        )
    for record in launch_records:
        notice_lines.extend(
            [
                f"## {record['provider']}",
                f"- launch script: {record['script']}",
                f"- prompt: {record['prompt']}",
                f"- status: {record['status']}",
                f"- events: {record['events']}",
                f"- result: {record['result']}",
                f"- diagnostics: {record['diagnostics']}",
                f"- timeout: {record['timeout_seconds']} seconds",
                f"- started: {record['started']} ({record.get('pid', 'no background pid')})",
                f"- opened: {record['opened']} ({record.get('window_id', 'not confirmed')})",
                f"- prompt submission: {record['prompt_submission']}",
                f"- managed PTY command: {record.get('managed_pty_command', 'not applicable')}",
                f"- visible fallback: {record.get('visible_fallback', 'not configured')}",
                "",
            ]
        )
    _append_owner_notice(run_dir / "owner_notice.md", "\n".join(notice_lines))
    print(json.dumps(launch_receipt, indent=2, ensure_ascii=False))
    print("\nOwner handoff: " + str(run_dir / "owner_notice.md"))
    for record in launch_records:
        print(
            f"{record['provider']}: prompt={record['prompt']} "
            f"result={record['result']} status={record['status']}"
        )
    if execution == "managed-pty" and not args.dry_run and not failures:
        if managed_script_path is None:
            failures.append("managed-pty: launcher did not prepare a provider script")
            launch_receipt["errors"] = failures
            launch_path.write_text(
                json.dumps(launch_receipt, indent=2) + "\n",
                encoding="utf-8",
            )
            _append_owner_notice(
                run_dir / "owner_notice.md",
                "## Managed PTY launch failure\n\n" + failures[-1],
            )
        else:
            print(
                "Codex-managed PTY handoff: retain this session id and submit the "
                "standalone native command before the command-free follow-up."
            )
            try:
                os.execv("/bin/zsh", ["/bin/zsh", str(managed_script_path)])
            except OSError as exc:
                failures.append(f"managed-pty: {type(exc).__name__}: {exc}")
                launch_records[0]["started"] = False
                launch_records[0]["error"] = str(exc)
                launch_receipt["errors"] = failures
                launch_path.write_text(
                    json.dumps(launch_receipt, indent=2) + "\n",
                    encoding="utf-8",
                )
                _append_owner_notice(
                    run_dir / "owner_notice.md",
                    "## Managed PTY launch failure\n\n" + failures[-1],
                )
                return 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
