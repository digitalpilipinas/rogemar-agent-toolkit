#!/usr/bin/env python3
"""Prepare a local, file-backed native-agent collaboration run."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid


PROVIDER_SPECS = {
    "grok": {"command": "grok", "artifact_dir": "grok"},
    "antigravity": {"command": "agy", "artifact_dir": "agy"},
    "gemini": {"command": "agy", "artifact_dir": "agy"},
    "agy": {"command": "agy", "artifact_dir": "agy"},
    "junie": {"command": "junie", "artifact_dir": "junie"},
    "codex": {"command": "codex", "artifact_dir": "codex"},
    "cursor": {
        "command": "agent",
        "artifact_dir": "cursor",
        "default_model": "claude-sonnet-5-high",
    },
    "cursor-agent": {
        "command": "agent",
        "artifact_dir": "cursor",
        "default_model": "claude-sonnet-5-high",
    },
    "agent": {
        "command": "agent",
        "artifact_dir": "cursor",
        "default_model": "claude-sonnet-5-high",
    },
}
ROLE_NAMES = {"main", "monitor", "review", "validation", "implementation"}
MODE_NAMES = {"plan", "review", "implementation", "validation"}
WORKFLOW_NAMES = {"parallel", "sequential"}
WORKSPACE_AUTHORITY_NAMES = {"read-only", "allowed-paths", "isolated-worktree"}
EXTERNAL_AUTHORITY_NAMES = {"none", "read-only", "authorized-write"}
EXECUTION_NAMES = {"visible", "background", "managed-pty"}
APPROVAL_POLICY_NAMES = {"manual", "full-auto"}
REVIEW_PROFILE_NAMES = {"none", "code"}


def canonical_provider(value: str, parser: argparse.ArgumentParser) -> str:
    normalized = value.strip().lower()
    if normalized not in PROVIDER_SPECS:
        parser.error(f"unsupported provider: {value}")
    if normalized in {"gemini", "agy"}:
        return "antigravity"
    if normalized in {"cursor-agent", "agent"}:
        return "cursor"
    return normalized


def parse_pairs(values: list[str], *, name: str, parser: argparse.ArgumentParser) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key.strip() or not item.strip():
            parser.error(f"{name} must use KEY=VALUE: {value}")
        result[key.strip().lower()] = item.strip()
    return result


def normalize_cursor_entry_command(value: str) -> str:
    """Validate a Cursor-native slash command without accepting prompt text."""
    command = value.strip()
    if not command.startswith("/") or len(command) == 1:
        raise ValueError("cursor entry command must be a native slash command such as /poteto-mode")
    if any(character.isspace() for character in command):
        raise ValueError("cursor entry command must contain only the slash-command token")
    return command


def parse_timeout_pairs(values: list[str], *, parser: argparse.ArgumentParser) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key.strip() or not item.strip():
            parser.error(f"provider-timeout must use PROVIDER=SECONDS: {value}")
        try:
            seconds = int(item.strip())
        except ValueError:
            parser.error(f"provider-timeout seconds must be an integer: {value}")
        if seconds < 1:
            parser.error(f"provider-timeout seconds must be positive: {value}")
        result[key.strip().lower()] = seconds
    return result


def run_git_raw(workspace: Path, *args: str) -> tuple[bytes | None, str | None]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=workspace,
            text=False,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, type(exc).__name__
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).decode("utf-8", "replace").strip().splitlines()
        return None, f"exit {result.returncode}{(': ' + detail[0]) if detail else ''}"
    return result.stdout, None


def text_value(data: bytes | None, error: str | None) -> str:
    if data is None:
        return f"<unavailable: {error or 'unknown error'}>"
    return data.decode("utf-8", "replace").strip()


def digest(data: bytes | None, error: str | None) -> dict[str, object]:
    if data is None:
        return {"sha256": None, "bytes": None, "error": error or "unavailable"}
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def short_text(value: str, limit: int = 12000) -> str:
    if len(value) <= limit:
        return value
    return f"{value[:limit]}\n<truncated; see digest in manifest>"


def git_snapshot(workspace: Path) -> dict[str, object]:
    commands: dict[str, tuple[str, ...]] = {
        "repo_root": ("rev-parse", "--show-toplevel"),
        "branch": ("branch", "--show-current"),
        "head": ("rev-parse", "HEAD"),
        "origin_main": ("rev-parse", "origin/main"),
        "status": ("status", "--short", "--branch"),
        "refs": (
            "for-each-ref",
            "--format=%(refname:short) %(objectname)",
            "refs/heads",
            "refs/remotes",
            "refs/tags",
        ),
    }
    values: dict[str, str] = {}
    for name, command in commands.items():
        data, error = run_git_raw(workspace, *command)
        values[name] = short_text(text_value(data, error))

    fingerprints: dict[str, object] = {}
    fingerprint_commands = {
        "status_porcelain_v2": ("status", "--porcelain=v2", "--untracked-files=all"),
        "status_with_ignored": (
            "status",
            "--porcelain=v2",
            "--untracked-files=all",
            "--ignored=matching",
        ),
        "unstaged_diff": ("diff", "--no-ext-diff", "--binary"),
        "staged_diff": ("diff", "--cached", "--no-ext-diff", "--binary"),
        "tracked_index": ("ls-files", "--stage"),
    }
    for name, command in fingerprint_commands.items():
        data, error = run_git_raw(workspace, *command)
        fingerprints[name] = digest(data, error)

    snapshot: dict[str, object] = {
        "workspace": str(workspace),
        **values,
        "fingerprints": fingerprints,
    }
    snapshot_payload = json.dumps(snapshot, sort_keys=True, ensure_ascii=False).encode("utf-8")
    snapshot["snapshot_sha256"] = hashlib.sha256(snapshot_payload).hexdigest()
    return snapshot


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def review_contract_for(provider_id: str, review_profile: str) -> str:
    """Return an explicitly selected, provider-specific review contract."""
    if review_profile != "code":
        return ""

    quality_skill = Path.home() / ".agents" / "skills" / "code-review-and-quality" / "SKILL.md"
    tests_skill = Path.home() / ".agents" / "skills" / "code-review-tests" / "SKILL.md"
    if provider_id == "antigravity":
        provider_guidance = f"""- Invoke `$code-review-and-quality` from `{quality_skill}` in addition to the task objective. If native skill expansion is unavailable, read and apply that exact file and disclose the fallback.
- When the candidate changes tests or behavior, or carries material regression risk, also invoke `$code-review-tests` from `{tests_skill}`. Do not invoke it mechanically when it adds no relevant test analysis."""
    elif provider_id == "grok":
        provider_guidance = f"""- Apply the five-axis standard in `{quality_skill}`, with additional focus on security, privacy, trust boundaries, authorization, data integrity, architecture, and unnecessary complexity.
- Apply the focused test and counterexample standard in `{tests_skill}` only when the candidate changes behavior or carries material regression risk. Do not claim native skill invocation unless it actually occurred."""
    elif provider_id == "junie":
        provider_guidance = f"""- Apply the five-axis standard in `{quality_skill}` and focus on reproducible runtime, test, and regression evidence.
- Apply `{tests_skill}` only when focused test analysis is relevant. Do not duplicate another provider's review merely to fill the report."""
    elif provider_id == "cursor":
        provider_guidance = f"""- Apply the five-axis standard in `{quality_skill}` with a pragmatic codebase-navigation and implementation-quality perspective: correctness, maintainability, developer ergonomics, user-visible reliability, and the smallest feasible correction.
- Apply the focused test and counterexample standard in `{tests_skill}` only when the candidate changes behavior or carries material regression risk. Preserve an independent perspective rather than imitating another provider's emphasis."""
    elif provider_id == "codex":
        provider_guidance = f"""- Apply the five-axis standard in `{quality_skill}` with an independent correctness, security, privacy, trust-boundary, data-integrity, and minimality focus.
- Apply the focused test and counterexample standard in `{tests_skill}` only when the candidate changes behavior or carries material regression risk.
- This is a separate Codex CLI process, not the supervising Codex desktop task. Do not launch Agent Collaboration or Supervisor MCP recursively, and do not treat the supervisor's conclusions as your own review evidence."""
    else:
        provider_guidance = (
            "- Apply the five-axis correctness, readability, architecture, security, and "
            "performance standard, plus focused test analysis when it is relevant."
        )

    return f"""## Review contract

{provider_guidance}
- CodeRabbit is a separate Codex-owned review layer. Do not invoke CodeRabbit, a CodeRabbit skill, or another external reviewer from this provider session.
- Keep one finding per semantic root cause. Do not repeat the same issue under different wording.
- Reject speculative future-proofing and optional complexity that lacks meaningful current-scope value. Identify genuinely easy, localized, low-risk improvements separately from required defects.
- Under `## Findings`, order actionable items by severity. For each item include `Severity`, `Finding key` (`root cause | file or symbol | requested outcome`), exact file/line evidence when available, impact, smallest valid correction, and focused test or validation evidence. If no actionable issue remains, state that explicitly.
"""


def prompt_for(
    *,
    provider: dict[str, object],
    workspace: Path,
    run_dir: Path,
    objective: str,
    intent: str,
    mode: str,
    workflow: str,
    scope: str,
    workspace_authority: str,
    external_authority: str,
    allowed_paths: list[str],
    excluded_paths: list[str],
    monitor_minutes: int,
    poll_seconds: int,
    codex_roles: dict[str, dict[str, str | None]],
    review_profile: str = "none",
) -> str:
    provider_id = str(provider["id"])
    provider_dir = run_dir / str(provider["artifact_dir"])
    model = provider.get("model") or "the model selected in this native CLI"
    effort = provider.get("effort") or "the reasoning/effort selected in this native CLI"
    snapshot = run_dir / "manifest.json"
    allowed = ", ".join(allowed_paths) if allowed_paths else "all paths permitted by the objective"
    excluded = ", ".join(excluded_paths) if excluded_paths else "none"
    role_lines = "\n".join(
        f"- {role}: {details.get('model') or 'Codex-selected model'}"
        f" ({details.get('effort') or 'default effort'})"
        for role, details in codex_roles.items()
    )
    if mode in {"plan", "review", "validation"}:
        mutation_rule = "Do not modify the repository; report any check that would mutate state as not run."
    else:
        mutation_rule = "Edit or execute only within the authorized workspace and paths; list every changed file and command."
    if external_authority == "none":
        capability_rule = (
            "- External authority is **none**. Do not send data to or take actions against external "
            "services through MCPs, plugins, extensions, web capabilities, native sub-agents, or "
            "other tools. Provider-local skills or helpers may be used only when they remain inside "
            "the recorded workspace authority and cause no data egress or external action; report "
            "any required external check or action as not run."
        )
    else:
        capability_rule = (
            "- Use provider capabilities only within the authority recorded above. Do not silently "
            "expand scope, send data, or take an external action beyond that authority."
        )
    capability_preflight = """## Provider-native capability preflight

- Before using a workaround, infer the capabilities needed for this objective and inspect your own CLI's installed or currently surfaced skill names and descriptions, relevant members of namespaced skill families, and live MCP, plugin, extension, helper, native sub-agent, or tool registry. Skills and callable tools are separate discovery surfaces: a tool may exist without a matching skill, while an installed plugin may expose no callable tool.
- Limit discovery to capabilities already installed or surfaced in this provider CLI, including installed marketplace plugins. Do not search an external marketplace, install, enable, update, or authenticate a capability.
- Treat the objective and authority fields as the required outcome and hard boundaries; treat named tools and procedural suggestions as non-exhaustive unless the task contract explicitly marks them required. Within those boundaries, exercise provider-native judgment, select better installed methods when useful, inspect necessary adjacent evidence, and report useful alternatives or out-of-scope leads without implementing them.
- Select only the smallest relevant capability set, with one primary route and an installed fallback only when the primary is unavailable or unsuitable. Do not load an entire family or activate overlapping routes by default.
- Every selected capability remains bounded by the objective, workspace authority, external authority, allowed paths, and excluded paths in this manifest. Capability discovery never expands those boundaries.
- Under `## Evidence`, name the provider-native capabilities actually used and their observed availability. Under `## Limitations`, record any required capability layer that could not be inspected or used as Unverified or not run.
"""
    if mode == "implementation":
        capability_preflight = """## Implementation-first execution

- The Objective above is the actual assignment. Start the smallest direct implementation action after reading only the exact target file or nearby repository pattern that action requires.
- Do not enumerate skills, plugins, MCPs, extensions, tool registries, unrelated sports, or broad repository directories before editing. Inspect a provider-native capability only if normal edit and focused-validation tools cannot complete the stated task, or if a concrete blocker requires it.
- The immutable manifest contains the exhaustive path inventory and snapshot evidence. Treat it as a guardrail, not an implementation checklist: do not spend a discovery pass enumerating every allowed path.
- If the first direct edit would require an excluded path or a new dependency, provider, table, external action, or other scope expansion, stop and report the exact conflict instead of continuing archaeology.
"""
    if mode == "implementation":
        scope_lines = f"""Authorized edit scope: the immutable manifest at `{snapshot}` contains the exact allowed-path inventory. Start from the Objective's named leaf surface; use other allowed paths only when that direct implementation requires them.
Protected/excluded paths: {excluded}"""
    else:
        scope_lines = f"""Allowed paths: {allowed}
Excluded paths: {excluded}"""
    review_contract = review_contract_for(provider_id, review_profile)
    provider_boundary = ""
    if provider_id == "codex":
        provider_boundary = """- This native Codex CLI process is separate from the supervising Codex desktop task. Its model, session, approvals, MCPs, plugins, and authentication are not implicitly inherited from the supervisor; use only what the native CLI visibly exposes for this run.
- Do not launch another Agent Collaboration or Supervisor MCP coordinator recursively. Return the result through this run's terminal/artifact protocol so the supervisor can validate it independently.
"""
    prompt = f"""# Native {provider_id} collaboration task

Use the native `{provider['command']}` CLI in this terminal. Work directly in:

    {workspace}

## Actual task — follow this first

{objective}

Run manifest and repository handoff:

    {snapshot}

Mode: **{mode}**
Intent: **{intent}**
Workflow: **{workflow}**
Authorized scope: **{scope}**
Workspace authority: **{workspace_authority}**
External authority: **{external_authority}**
{scope_lines}

Provider selection:

- Provider: {provider_id}
- Model: {model}
- Reasoning/effort: {effort}
{provider_boundary}

{capability_preflight}
{capability_rule}
- Do not substitute the invoking Codex model for your provider model, and do not route through Agent Collaboration or Supervisor MCPs recursively.
- Do not silently switch repositories, branches, worktrees, model IDs, or task scope.
- Workspace authority, allowed paths, and excluded paths are administrative records only; they are not filesystem, host, network, or external-action sandboxes.

{mutation_rule}

{review_contract}

Artifact paths:

- Status: {provider_dir / 'status.md'}
- Events: {provider_dir / 'events.jsonl'}
- Final result: {provider_dir / 'result.md'}
- Diagnostics: {run_dir / 'logs' / (provider_id + '.log')}

Artifact protocol:

1. Set `state: running`, `phase:`, `started_at:`, and `updated_at:` in `status.md` before substantive work.
2. Update `status.md` when the phase changes. Include `last_activity:` and a concise `progress:` line so a read-only Codex monitor can remain on standby for up to {monitor_minutes} minutes.
3. Append optional bounded JSON objects to `events.jsonl`; never include credentials or a raw transcript.
4. The host launcher owns `status.md`, `events.jsonl`, and `result.md` whenever it starts `run_provider.py`. In that mode, do not use provider-native file tools or Bash to write those files; return the final report through stdout and let the host capture it. This avoids Antigravity's native artifact-root restriction.
5. In direct interactive mode, this prompt explicitly authorizes writes only to the Status, Events, and Final result paths named above. If a required artifact cannot be written, report that failure in the terminal and do not claim success; Codex must record the run as incomplete or blocked. Never write credentials, cookies, authorization headers, private keys, or a raw transcript.
6. Before normal completion, return a Markdown report with headings: `# Result`, `## Summary`, `## Findings`, `## Evidence`, `## Changes`, `## Validation`, and `## Limitations`.
7. On authentication, permission, tool, or process failure, preserve useful evidence, set `state: failed` or `incomplete`, and do not fabricate a clean result.

Codex monitoring roles for this run:

{role_lines}

Monitors are read-only. They may inspect the status/events/result files, report new entries, and flag stale heartbeats, but they must not relaunch you, change the prompt, change scope, edit the repository, or declare your result valid. Codex will independently consolidate and validate your evidence.

Keep provider output separate from Codex synthesis. If a later sequential stage is requested, Codex will create a hash-bound handoff file containing selected artifact paths, a reviewed summary, the repository fingerprint, allowed changes, and validation requirements.

Do not store API keys, cookies, authorization headers, private keys, or full transcripts in the artifact directory.
"""
    entry_command = provider.get("entry_command")
    if entry_command:
        # Native Cursor commands are submitted as a standalone first message.
        # The generated artifact is the command-free follow-up brief sent only
        # after the provider visibly enters the requested native mode.
        return f"# Follow-up after standalone native mode activation\n\n{prompt}"
    return prompt


def handoff_template(target: str, run_dir: Path) -> str:
    return f"""state: not_ready
target_provider: {target}
source_artifacts: []
source_snapshot_sha256: {json_placeholder(run_dir)}

# Handoff to {target}

This file is populated only after Codex reviews the source provider's artifacts.
Do not launch from this placeholder.

## Reviewed summary

## Selected findings

## Allowed changes

## Validation requirements
"""


def json_placeholder(run_dir: Path) -> str:
    return f"see {run_dir / 'manifest.json'}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--provider", action="append", required=True)
    parser.add_argument("--run-root", type=Path)
    parser.add_argument("--scope", default="current-worktree")
    parser.add_argument("--mode", choices=sorted(MODE_NAMES), default="review")
    parser.add_argument("--intent", help="free-form task purpose; defaults to --mode")
    parser.add_argument(
        "--review-profile",
        choices=sorted(REVIEW_PROFILE_NAMES),
        default="none",
        help="opt-in contract for an explicit code/diff/branch/PR review; mode and intent remain independent",
    )
    parser.add_argument("--workflow", choices=sorted(WORKFLOW_NAMES), default="parallel")
    parser.add_argument("--workspace-authority", choices=sorted(WORKSPACE_AUTHORITY_NAMES))
    parser.add_argument(
        "--external-authority",
        choices=sorted(EXTERNAL_AUTHORITY_NAMES),
        default="none",
    )
    parser.add_argument(
        "--execution",
        choices=sorted(EXECUTION_NAMES),
        default=None,
        help=(
            "execution surface; defaults to managed-pty for a native entry command "
            "and managed background otherwise"
        ),
    )
    parser.add_argument(
        "--approval-policy",
        choices=sorted(APPROVAL_POLICY_NAMES),
        default="manual",
    )
    parser.add_argument("--fallback-visible", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--provider-model", action="append", default=[])
    parser.add_argument("--provider-effort", action="append", default=[])
    parser.add_argument(
        "--cursor-entry-command",
        help=(
            "Cursor-native slash command such as /poteto-mode; requires "
            "managed-pty or explicit visible fallback with manual approval"
        ),
    )
    parser.add_argument(
        "--provider-timeout",
        action="append",
        default=[],
        help="provider=seconds; defaults to Grok 1200s and Antigravity/Junie/Cursor/Codex 1800s",
    )
    parser.add_argument("--role-model", action="append", default=[])
    parser.add_argument("--role-effort", action="append", default=[])
    parser.add_argument("--allowed-path", action="append", default=[])
    parser.add_argument("--exclude-path", action="append", default=[])
    parser.add_argument(
        "--monitor-minutes",
        type=int,
        default=30,
        help="active monitoring window from terminal launch, between 5 and 30 minutes",
    )
    parser.add_argument("--poll-seconds", type=int, default=60)
    args = parser.parse_args()

    if not 5 <= args.monitor_minutes <= 30 or args.poll_seconds < 1:
        parser.error("monitor-minutes must be between 5 and 30; poll-seconds must be positive")
    providers: list[str] = []
    for value in args.provider:
        provider = canonical_provider(value, parser)
        if provider not in providers:
            providers.append(provider)
    if args.execution is None:
        # Native Cursor slash commands and the interactive Codex CLI use a
        # managed PTY by default. Multiple providers still use the background
        # runner unless the owner selects a single managed provider explicitly.
        args.execution = (
            "managed-pty"
            if args.cursor_entry_command or providers == ["codex"]
            else "background"
        )
        # Keep a manual fallback available without changing the approval policy.
        args.fallback_visible = True
    workspace = args.workspace.expanduser().resolve(strict=True)
    if not workspace.is_dir():
        parser.error(f"workspace is not a directory: {workspace}")
    workspace_authority = args.workspace_authority or (
        "read-only" if args.mode in {"plan", "review", "validation"} else "allowed-paths"
    )
    if args.approval_policy == "full-auto" and workspace_authority != "isolated-worktree":
        parser.error("full-auto requires --workspace-authority isolated-worktree")
    if args.execution == "background" and args.approval_policy == "manual" and not args.fallback_visible:
        parser.error("background manual approval requires --fallback-visible")

    cursor_entry_command: str | None = None
    if args.cursor_entry_command:
        try:
            cursor_entry_command = normalize_cursor_entry_command(args.cursor_entry_command)
        except ValueError as exc:
            parser.error(str(exc))
        if "cursor" not in providers:
            parser.error("--cursor-entry-command requires --provider cursor")
        if args.execution not in {"managed-pty", "visible"} or args.approval_policy != "manual":
            parser.error(
                "Cursor native entry commands require managed-pty or visible execution "
                "with manual approval"
            )
    provider_models = parse_pairs(args.provider_model, name="provider-model", parser=parser)
    provider_efforts = parse_pairs(args.provider_effort, name="provider-effort", parser=parser)
    provider_timeouts = parse_timeout_pairs(args.provider_timeout, parser=parser)
    role_models = parse_pairs(args.role_model, name="role-model", parser=parser)
    role_efforts = parse_pairs(args.role_effort, name="role-effort", parser=parser)
    unknown_roles = (set(role_models) | set(role_efforts)) - ROLE_NAMES
    if unknown_roles:
        parser.error(f"unsupported Codex role(s): {', '.join(sorted(unknown_roles))}")
    codex_roles = {
        role: {"model": role_models.get(role), "effort": role_efforts.get(role)}
        for role in sorted(ROLE_NAMES)
    }

    root = args.run_root or Path(os.environ.get("AGENT_COLLABORATION_TERMINAL_ROOT", tempfile.gettempdir())) / "agent-collaboration-terminal"
    root = root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    run_id = f"run-{dt.datetime.now().strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:10]}"
    run_dir = root / run_id
    run_dir.mkdir(mode=0o700)

    snapshot = git_snapshot(workspace)
    provider_entries: list[dict[str, object]] = []
    for provider_id in providers:
        spec = PROVIDER_SPECS[provider_id]
        provider_model = provider_models.get(provider_id, args.model)
        if provider_model is None:
            provider_model = spec.get("default_model")
        provider_entries.append(
            {
                "id": provider_id,
                "command": spec["command"],
                "artifact_dir": spec["artifact_dir"],
                "model": provider_model,
                "effort": provider_efforts.get(provider_id, args.effort),
                "timeout_seconds": provider_timeouts.get(provider_id),
                "entry_command": cursor_entry_command if provider_id == "cursor" else None,
            }
        )

    manifest: dict[str, object] = {
        "schema": 3,
        "run_id": run_id,
        "created_at": utc_now(),
        "workspace": str(workspace),
        "objective": args.objective,
        "intent": args.intent or args.mode,
        "mode": args.mode,
        "review_profile": args.review_profile,
        "workflow": args.workflow,
        "scope": args.scope,
        "allowed_paths": args.allowed_path,
        "excluded_paths": args.exclude_path,
        "authority": {
            "workspace": workspace_authority,
            "external": args.external_authority,
        },
        "execution": {
            "mode": args.execution,
            "approval_policy": args.approval_policy,
            "fallback_visible": args.fallback_visible,
        },
        "providers": provider_entries,
        "codex_roles": codex_roles,
        "monitor": {
            "standby_minutes": args.monitor_minutes,
            "poll_seconds": args.poll_seconds,
            "provider_timeouts_seconds": provider_timeouts,
        },
        "artifact_protocol": "host-owned-v1",
        "snapshot": snapshot,
        "state": "prepared",
    }
    atomic_write(run_dir / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    atomic_write(
        run_dir / "comparison.md",
        "# Codex comparison\n\nState: waiting_for_provider_results\n\nKeep provider reports unchanged. Record Codex synthesis here after independent validation.\n",
    )
    (run_dir / "handoff").mkdir(mode=0o700)
    (run_dir / "logs").mkdir(mode=0o700)

    for provider in provider_entries:
        provider_id = str(provider["id"])
        provider_dir = run_dir / str(provider["artifact_dir"])
        provider_dir.mkdir(mode=0o700)
        atomic_write(provider_dir / "status.md", f"state: pending\nphase: prepared\nupdated_at: {utc_now()}\n")
        atomic_write(provider_dir / "result.md", "")
        atomic_write(provider_dir / "events.jsonl", "")
        atomic_write(
            provider_dir / "prompt.md",
            prompt_for(
                provider=provider,
                workspace=workspace,
                run_dir=run_dir,
                objective=args.objective,
                intent=args.intent or args.mode,
                mode=args.mode,
                workflow=args.workflow,
                scope=args.scope,
                workspace_authority=workspace_authority,
                external_authority=args.external_authority,
                allowed_paths=args.allowed_path,
                excluded_paths=args.exclude_path,
                monitor_minutes=args.monitor_minutes,
                poll_seconds=args.poll_seconds,
                codex_roles=codex_roles,
                review_profile=args.review_profile,
            ),
        )
        atomic_write(run_dir / "handoff" / f"to-{provider_id}.md", handoff_template(provider_id, run_dir))

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
