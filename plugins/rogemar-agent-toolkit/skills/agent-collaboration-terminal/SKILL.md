---
name: agent-collaboration-terminal
description: Coordinate native Grok, Antigravity/Gemini, Cursor Agent, Junie, and Codex CLI sessions from Codex for research, planning, implementation, review, validation, or other bounded external-agent work. Prepare exact worktree prompts, Codex-managed PTY or background execution with physical fallback, frozen repository fingerprints, Markdown artifacts, monitoring, handoffs, and Codex synthesis without routing through the Agent Collaboration MCP broker.
---

# Agent Collaboration Terminal

Use this skill when the native provider CLIs are the desired execution surface. Codex prepares the run manifest and prompts, the provider keeps its normal CLI capabilities, and Codex monitors local files. This is a file-backed coordination workflow, not another broker or Supervisor MCP.

## Core contract

- Use the exact workspace path supplied by the user. Never silently substitute committed `HEAD`, a sanitized patch, an attachment, or a stale worktree.
- Freeze and record branch, `HEAD`, `origin/main`, refs, status, staged diff, unstaged diff, tracked index, and ignored/untracked status fingerprints before launch.
- Record explicit `allowed_paths` and `excluded_paths`. A user-authorized current-worktree scope may include modified, staged, untracked, and ignored files. Do not narrow it without a new scope decision.
- Use separate artifact directories and prompts for each provider. Keep provider evidence separate from Codex synthesis.
- Preserve provider-native behavior within the workspace and external authority recorded in the manifest. Provider-local skills or helpers may operate inside the authorized workspace when they cause no data egress or external action. MCPs, plugins, extensions, memory/web capabilities, native sub-agents, or other tools that send data or act externally require compatible recorded external authority and explicit user scope. Do not translate the invoking Codex model into a provider model ceiling or silently remove a capability that is authorized for the run. Do not route recursively through Agent Collaboration or Supervisor MCPs.
- Before using a workaround, each provider performs a targeted preflight of its
  own installed or currently surfaced skills, namespaced skill families, MCPs,
  plugins, extensions, helpers, and native tools. Skills and callable tools are
  separate discovery surfaces. Select only the smallest relevant set and one
  installed fallback; do not load an entire family, search an external
  marketplace, install or enable capabilities, authenticate a new service, or
  expand the objective or manifest authority.
- Treat the objective and authority fields as the required outcome and hard
  boundaries, not the prompt's named tools or suggested procedure as an
  exhaustive method list. Within those boundaries, the provider may exercise
  native judgment, use additional installed capabilities, choose a better
  approach, inspect necessary adjacent evidence, and surface useful alternatives
  or out-of-scope leads without implementing them.
- Provider authentication, credits, model availability, and CLI updates remain provider-owned. Check the command and version/status before launch, but never request or persist tokens.
- Prefer Codex-managed execution: use the host-owned background runner for
  non-interactive provider CLIs, and use a Codex-managed PTY through
  `exec_command` with `tty: true` plus `write_stdin` for native interactive
  entry commands. A physical Terminal.app window is a fallback for a managed
  PTY that cannot authenticate, render, or accept input, or when the owner
  explicitly requests a visible external window.
- Keep run artifacts outside the source repository unless the user explicitly requests repository-local artifacts. Do not clean a run automatically.
- For a bounded implementation handoff, the provider prompt must begin with the ordinary-language task brief: the requested implementation, first direct action, acceptance boundary, and stop condition. Keep the immutable manifest as the exhaustive record of the full path inventory and fingerprints; do not make the provider enumerate that inventory before beginning work. Capability preflight is conditional for implementation: inspect a provider-native capability only when normal editing and focused validation cannot complete the known task or a concrete blocker requires it. Review, research, and diagnosis prompts retain their independent discovery contract.

## Completion evidence versus progress telemetry

Treat provider progress displays consistently across Grok, Antigravity, Cursor, Junie, and Codex CLI. A context-window or token-use percentage, activity spinner, task count, elapsed time, or number of files read/edited is progress telemetry only; it is never proof that the task is complete. Do not use a percentage to estimate completion or to terminate a moving provider.

For a direct interactive run, completion requires the provider to reach a terminal success state, emit the required `result.md` headings and a substantive report, and stop processing or visibly return to its follow-up prompt. For a host-owned run, use the host's terminal status and captured result. Codex must still inspect the actual worktree and run the required verification before accepting the result. A provider's final report is evidence, not final approval. A native provider may write `state: completed` or `state: succeeded`; both mean terminal success only when the result and independent validation requirements are satisfied. `completed_with_warnings`, `failed`, `incomplete`, `timed_out`, `cancelled`, and `needs_attention` are not successful completion.

## Prepare a run

Run commands from this skill directory (the folder containing `SKILL.md`) so
the bundled `scripts/...` paths resolve portably. Provider names are
case-insensitive; the user-facing keyword `Codex` resolves to the verified
native lowercase `codex` executable. Generated commands preserve the verified
native CLI entrypoints: `grok`, `agy`, `agent`, `junie`, and `codex`.

```bash
python3 scripts/prepare_run.py \
  --workspace /path/to/worktree \
  --objective "Review the current Sprint 1 worktree" \
  --provider Grok \
  --provider agy \
  --provider cursor \
  --provider-model 'grok=Grok 4.6' \
  --provider-effort 'grok=high' \
  --provider-model 'antigravity=gemini-3.7-flash-high' \
  --provider-effort 'antigravity=high' \
  --provider-model 'cursor=claude-sonnet-5-high' \
  --role-model 'main=GPT-5.6 Sol High' \
  --role-model 'monitor=GPT-5.6 Luna Max' \
  --role-model 'review=GPT-5.6 Sol Medium' \
  --role-model 'validation=GPT-5.6 Sol Medium' \
  --mode review \
  --review-profile code \
  --intent "independent code and architecture review" \
  --workspace-authority read-only \
  --external-authority none \
  --workflow parallel \
  --monitor-minutes 20 \
  --poll-seconds 60 \
  --allowed-path src \
  --allowed-path tests \
  --exclude-path node_modules \
  --exclude-path .env \
  --execution background \
  --approval-policy manual \
  --fallback-visible
```

Use `--intent` for the task purpose and `--mode` for its mutation rule. The intent may describe research, architecture, debugging, documentation, implementation, review, validation, or another bounded assignment. Record `--workspace-authority` as `read-only`, `allowed-paths`, or `isolated-worktree`, and `--external-authority` as `none`, `read-only`, or `authorized-write`. Task purpose never grants authority. Use a project-specific `--run-root` when artifacts must survive temporary-directory cleanup. The script never stages, commits, fetches, resets, copies, or edits the repository.

Provider model values must use the exact identifiers exposed by the live CLI. For Antigravity, check `agy models` immediately before preparing a run; do not pass a display label when the installed CLI requires an ID. For Cursor, verify `agent status` and `agent models`; this installation defaults prepared Cursor runs to the verified `claude-sonnet-5-high` ID unless `--provider-model cursor=<id>` overrides it. Cursor encodes the reasoning profile in the model ID, so do not invent a separate Cursor effort flag. For Codex CLI, verify `codex --version` and `codex exec --help` immediately before relying on a model or approval flag; do not assume the supervising Codex desktop model or settings are inherited by the CLI process.

### Review runs

This skill is not a review-only wrapper. The objective and intent define the provider's job; `--mode` defines repository mutation behavior; workspace and external authority define permitted scope; execution and approval policy define how the native CLI runs. Provider-native capabilities remain available within those recorded boundaries.

Only when the task explicitly asks the provider to review code, a diff, branch, or PR—including a security review of that code—pass `--review-profile code` together with the appropriate mutation mode. `--mode review` alone never activates code-review skills, while a bounded review-and-fix objective may combine the code profile with `--mode implementation`. Do not select the code profile for research, planning, general security research, documentation review, implementation that contains no review step, or ordinary validation. For an authorized independent code-review task, prefer managed background execution with manual approval and visible fallback unless the owner explicitly requests visible interaction or the run requires a provider-native entry command.

With `--review-profile code`, `prepare_run.py` adds this normalized contract:

- Antigravity explicitly invokes `$code-review-and-quality`; it invokes `$code-review-tests` only when changed behavior, tests, or material regression risk makes that analysis relevant. If native skill expansion is unavailable, it reads and applies the exact installed skill file and discloses the fallback.
- Grok applies the same five-axis quality standard with additional security, privacy, trust-boundary, authorization, data-integrity, architecture, and minimality focus. It applies the focused test contract only when relevant.
- Cursor applies the same base standard with an independent pragmatic codebase-navigation and implementation-quality perspective: correctness, maintainability, developer ergonomics, user-visible reliability, focused tests, and the smallest feasible correction.
- Junie uses the same base standard with a runtime, reproduction, and test-evidence focus when that lane is useful.
- CodeRabbit remains a separate Codex-owned review layer. No provider may invoke CodeRabbit, a CodeRabbit skill, or another external reviewer recursively.

Every actionable provider finding uses one semantic root cause and reports severity, a stable `root cause | file or symbol | requested outcome` key, exact evidence, impact, the smallest valid correction, and focused validation. This common evidence shape supports Codex reconciliation; it does not require every provider to perform the same analysis.

The run contains:

- `manifest.json`: immutable objective, intent, authority, execution policy, provider commands/models, Codex role models, scope, monitor policy, and repository fingerprints.
- `grok/`, `agy/`, `cursor/`, `junie/`, or `codex/`: provider prompt, status, events, and final result.
- `owner_notice.md`: owner-facing map of the exact prompts, launch scripts, status/events/result paths, logs, windows, and timeouts. The launcher also prints this map in its Codex task output.
- `comparison.md`: reserved for Codex synthesis; provider reports remain unchanged.
- `handoff/to-<provider>.md`: placeholder until Codex reviews source artifacts and prepares a sequential handoff.
- `logs/`: provider diagnostics supplied by the terminal workflow.

## Launch the providers

Visible interactive launch and prompt submission are two separate steps. First open each provider terminal and invoke its native CLI:

```text
grok
agy
agent
junie
codex
```

Wait until the provider's own interactive prompt is visibly ready. Only then paste each generated provider prompt verbatim:

```text
Terminal A: /path/to/run/<id>/grok/prompt.md
Terminal B: /path/to/run/<id>/agy/prompt.md
Terminal C: /path/to/run/<id>/cursor/prompt.md
Terminal D: /path/to/run/<id>/codex/prompt.md
```

Do not combine CLI startup and prompt submission into one visible-interactive command. An opened shell is not a running review, and a provider that exits before showing its prompt is a failed launch.

The default path is managed execution inside the Codex harness: host-owned
background for ordinary non-interactive runs and one independent Codex PTY per
native interactive provider. Use the bundled Terminal.app launcher only when a
managed PTY is unavailable or the owner explicitly asks for a physical window.
Never silently replace a requested managed run with an external window. When a
physical fallback is used, the launcher records a Terminal window identifier in
`launch.json`; a provider is not considered visibly launched unless its record
has `opened: true` and a non-empty `window_id`. If Terminal.app automation is
unavailable, stop and report the exact launch error so the user can grant
macOS Automation access or run the generated script in Terminal.app themselves.
If Codex is managing PTYs, use one independent PTY per provider and never reuse
a process or terminate a completed provider to start another.

Each prompt includes the exact repository path, phase, workflow, model, effort, snapshot fingerprints, allowed/excluded paths, artifact locations, monitoring policy, and the task objective. `external-authority none` removes authorization for data egress and actions against external services; provider-local skills or helpers remain usable only when they stay within the recorded workspace authority and do not send data or take an external action. The generated prompt tells the provider to report any external check or action as not run. If the user provides additional detailed instructions, preserve them verbatim in the generated objective or prompt file.

When the provider is Codex CLI, the native `codex` process is a separate
agent from the supervising Codex desktop task. Its model, session, approvals,
MCPs, plugins, and authentication are not implicitly inherited from the
supervisor. Do not launch another Agent Collaboration or Supervisor MCP
coordinator recursively; return the CLI result through this run's terminal and
artifact protocol for independent Codex validation.

### Implementation-first prompt shape

For an implementation provider, place the actual task immediately after the
native command header. Write it as a normal direct implementation prompt, not
as a coordination summary: what to build or fix, the first bounded action,
the completion boundary, and the exact stop conditions. Put run-artifact
protocol, model metadata, full fingerprints, and the exhaustive allowed-path
inventory after that brief or in `manifest.json`.

The implementation prompt must say that only targeted reading of the exact
file or nearby existing pattern is permitted before the first edit. It must
not require skills/MCP/plugin/registry discovery unless a non-default
capability is actually needed. A provider may still inspect a minimal relevant
capability when blocked, and must retain every manifest authority and
exclusion. This is not a relaxation of safety boundaries.

For Cursor implementation, use the configured native entry command as the
first route with the same executable brief and frozen authority. Submit that
command as a standalone first message with no task text or arguments. After
the provider visibly enters the native mode, send the generated command-free
follow-up brief as a second message. It is the default engineering path, not a
substitute for a precise task. Pstack's native `/poteto-mode` is a
playbook dispatcher and may legitimately perform planning, context discovery,
or delegated specialist work before producing a product-file diff. Do not
interpret an early no-diff interval as a stalled run or substitute normal Cursor
mode merely to force a direct edit. Preserve provider artifacts and permit the
selected playbook to reach a stated completion, pause, terminal failure,
manifest-boundary conflict, or configured timeout. Use normal interactive
Cursor mode only when the owner requests it, the native mode is unavailable or
terminally failed, or the Pstack run explicitly declines the bounded task.
Normal Cursor mode is otherwise optional and is generally the leaner route for
code reviews; `/poteto-mode` may also be selected for a code-review task when
its deeper structured reasoning is materially useful. Do not add more metadata
or broaden the source map to compensate.

The generated prompt also requires the provider to inspect its own installed
capability surface. Codex must not assume that Grok, Antigravity, Cursor, and Junie have
the same skills, MCPs, or plugins, and a provider must not claim a capability
was available or used without observing it in its native CLI. If the provider
cannot inspect a capability layer, it records that layer as Unverified and
continues with the smallest permitted native route.

Do not reduce provider autonomy to a Codex-authored command checklist. Named
skills and methods are requirements only when the task contract explicitly says
so; otherwise they are useful routing hints. Providers may independently select
better installed methods while remaining accountable for evidence and the
manifest's scope and authority.

### Physical Terminal.app fallback

Use the bundled launcher with `--execution visible` only when the Codex-managed PTY cannot authenticate, render, or accept input, or when the owner explicitly requests a physical window:

```bash
python3 scripts/launch_terminals.py \
  --run /path/to/run/<id> \
  --provider cursor \
  --execution visible \
  --approval-policy manual
```

On macOS this opens one Terminal.app window per provider. It writes an inspectable `logs/launch-<provider>.sh`, `launch.json`, and `owner_notice.md` before opening the windows. The launcher output names each exact prompt and result path so the owner can see what was supplied and where the response will appear. If GUI access is unavailable, it prints the exact scripts and reports the launch error instead of claiming that a terminal opened.

The launcher starts only the native CLI, prints the exact prompt path, and leaves prompt submission to a second explicit action after the provider is visibly ready. For Antigravity, start `agy`, wait for its input prompt, and then paste `agy/prompt.md`; for Grok, do the same with `grok` and `grok/prompt.md`; for Cursor, start bare `agent`, wait for its native input prompt, confirm the configured model is Claude Sonnet 5 High, and then paste `cursor/prompt.md`; for Codex CLI, start bare `codex`, wait for its native input prompt, and then paste `codex/prompt.md`. Do not use a launch-time prompt flag or blind delay as a shortcut for this workflow. Provider flags change across releases, so verify model IDs and argument syntax against the installed executable rather than relying on display labels or stale examples.

### Codex-managed PTY sessions

Use a Codex-managed PTY when a provider needs a native interactive command or
approval prompt. Prepare the run with `--execution managed-pty` and one
provider, then execute the generated launch script with Codex's terminal tool
using `tty: true`. Keep the returned session identifier; use `write_stdin` to
submit input and poll output, and stop steering when the provider is still
active. Record the managed session identifier and prompt-submission checkpoints
in the run's owner evidence. Do not run the same provider through both a
managed PTY and Terminal.app.

```bash
python3 scripts/prepare_run.py \
  --workspace /exact/worktree \
  --objective "Detailed bounded implementation task" \
  --provider cursor \
  --cursor-entry-command /poteto-mode \
  --mode implementation \
  --workspace-authority allowed-paths \
  --execution managed-pty \
  --approval-policy manual \
  --fallback-visible
```

Run the resulting `launch_terminals.py` command from a Codex-managed PTY, not
from a normal noninteractive shell. Managed PTY launch is deliberately
single-provider so each native CLI has one independently controllable session.

The PTY sequence is:

1. Start the bare native CLI through the generated launch script.
2. Wait for the provider's actual input prompt, not a fixed sleep or a context percentage.
3. Submit any native entry command as its own standalone message.
4. Wait for the provider's native mode banner and task indicator.
5. Submit the command-free generated brief as a separate follow-up.
6. Monitor the provider artifacts and PTY until the provider stops or requires attention.

For a Codex CLI PTY, the launch keyword is the user-facing `Codex` (the
launcher executes the case-sensitive shell command `codex`). Submit only the
bare command first, wait for the CLI's own prompt, then submit the generated
brief as a separate message. Keep approvals visible and do not append the
brief to `codex`.

If the Codex terminal tool cannot allocate or control the PTY, use the recorded
Terminal.app fallback once. The fallback is an execution change that must be
visible in the launch receipt; it is not silent substitution.

### Cursor native slash-command sessions

When Cursor must enter a native mode such as `/poteto-mode`, prepare it explicitly:

```bash
python3 scripts/prepare_run.py \
  --workspace /exact/worktree \
  --objective "Detailed bounded implementation task" \
  --provider cursor \
  --cursor-entry-command /poteto-mode \
  --mode implementation \
  --workspace-authority allowed-paths \
  --execution managed-pty \
  --approval-policy manual
```

The generated `cursor/prompt.md` is a command-free follow-up brief; it must never concatenate the native command with task text. The launcher starts bare `agent`. Type and submit the exact entry command alone, with no goal, arguments, or appended text. Some Cursor terminal builds render a pasted first message as chat text (`[Pasted text ...]`) before the native slash-command parser runs, which is why the command and task brief are separate submissions. Wait until the terminal visibly shows the `Potato Mode` title and `1 task`, then paste or type `cursor/prompt.md` as the normal follow-up. Do not treat the visible model label, a renamed task, or a command prefix inside pasted text as proof of activation. If `Potato Mode` and `1 task` do not appear before work begins, stop before any repository edit and record the native mode as unavailable or unverified; do not silently substitute ordinary Cursor mode.

Native entry commands are fail-closed to one-shot `agent --print` runs. Use a
Codex-managed PTY for the native interaction, or the explicit physical
Terminal.app fallback. Ordinary Cursor tasks that do not require a native
slash command may use the managed background runner.

### CodeRabbit local CLI

CodeRabbit is a separate Codex-owned review layer, not a provider in this
skill's Grok/Antigravity/Cursor/Junie/Codex CLI roster. The CodeRabbit plugin invokes the
local `coderabbit` CLI; when that CLI is installed and authenticated, Codex can
run `coderabbit review --agent` through a managed non-interactive
`exec_command` process, capture its NDJSON output in a review artifact, and
poll a returned session with `write_stdin` until it exits. A PTY is normally
unnecessary for this CLI. Do not add CodeRabbit as a provider, route it through
`run_provider.py`, or describe its output as a native-agent result.

Before the approved review gate, check `coderabbit --version`,
`coderabbit review --help`, and `coderabbit auth status --agent`. Run only the
narrowest authorized scope, do not pass `--use-credits` implicitly, and do not
send a worktree containing secrets. CodeRabbit sends the selected diff to its
service; preserve that external-data boundary in the review receipt. If auth
or an interactive prerequisite requires a physical terminal, use the explicit
fallback and record it.

Visible interaction proves prompt order and keeps trust or approval requests observable; it does not disable Cursor's configured MCPs or plugins. Before a strict `external-authority none` run, inspect the live Cursor CLI for a supported per-run isolation control. If none exists, do not mutate persistent Cursor configuration implicitly and do not claim MCP/plugin isolation; either use an owner-approved isolated Cursor profile/configuration or record that boundary as Blocked.

Do not use a fixed sleep as proof of readiness. A short Terminal settle delay may help window bookkeeping, but the prompt-submission gate is the provider's actual native input prompt.

### Managed background execution

For a host-owned background run that submits the prompt, captures output, and
falls back to a visible session when trust, authentication, or command approval
is required, prepare the run with:

```bash
python3 scripts/prepare_run.py \
  --workspace /exact/worktree \
  --objective "Research the requested topic" \
  --provider agy \
  --mode review \
  --intent research \
  --workspace-authority read-only \
  --execution background \
  --approval-policy manual \
  --fallback-visible

python3 scripts/launch_terminals.py \
  --run /path/to/run/<id>
```

`run_provider.py` owns heartbeat, timeout, stdout capture, and final Markdown
receipt. If recognizable attention is required, it stops the background
attempt, records `state: needs_attention` plus `attention.json`, and supplies
the exact visible manual fallback command. The background runner does not open
a GUI by itself. When the existing run authority covers the fallback, the
supervising Codex task executes that recorded command once, confirms the native
CLI is visibly ready, and then submits the already frozen prompt. Do not hand
ordinary in-scope Terminal operation back to the owner; ask only when new
authority, credentials, or an owner-only operating-system permission is
required. Codex may confirm the already authorized workspace and choose a
one-time Yes only for an in-scope action; deny or escalate anything broader. It
must not choose a persistent Always allow rule merely for convenience.

`--approval-policy full-auto` maps to provider-native flags: Grok
`--always-approve`, Antigravity `--dangerously-skip-permissions`, Cursor
`--force`, Junie `--brave`, and Codex CLI
`--dangerously-bypass-approvals-and-sandbox`. Cursor's `--approve-mcps` is never added
implicitly because MCP authority remains separately governed. These full-auto
flags are all-or-nothing and do not enforce `allowed_paths`, so
full auto is accepted only when the manifest explicitly records
`--workspace-authority isolated-worktree`. The legacy `--auto-approve` flag is
an alias for this policy and is a breaking safety-boundary choice: it requires
explicit owner authorization and cannot be combined with an explicit
`--approval-policy`. `isolated-worktree`, `allowed_paths`, and `excluded_paths`
remain administrative records; they are not filesystem, host, network, or
external-action sandboxes. Do not label prompt instructions or after-the-fact
diff checks as bounded auto-approval.

For schema-2 runs, the legacy `--unattended` alias still selects managed
background execution with a visible manual fallback by default. Existing
top-level `approval_policy` and `auto_approve` fields remain in `launch.json`;
when a run is relaunched for fallback, prior launch receipt(s) are retained in
`launch_attempts`, and `monitor_started_at` remains the earliest observed launch
time. `owner_notice.md` is appended so the original background evidence is not
replaced by the visible fallback notice.

Inspect `launch.json` and require each selected provider to show `started: true`,
its execution and approval policies, prompt-submission mode, and timeout. A
managed PTY run additionally requires `visibility: codex_managed_pty` and the
returned Codex session identifier in owner evidence. A physical visible run
additionally requires `opened: true` and a non-empty `window_id`. For
interactive runs, confirm that the provider prompt appeared and that the
prepared prompt was submitted; `opened: true` proves only Terminal creation.

Default host timeouts are 20 minutes for Grok and 30 minutes for Antigravity,
Cursor, Junie, or Codex CLI. Override a run with `--timeout-seconds`, or record a per-provider value
during preparation with `--provider-timeout antigravity=1800`.

## Mode rules

- **Plan:** inspect and design; do not edit the repository. Report commands that would mutate state as not run.
- **Review:** independently inspect the requested worktree and return evidence-backed findings. Read-only unless the objective explicitly authorizes a change.
- **Implementation:** one provider edits an authorized workspace at a time. Parallel implementation requires separate worktrees and an explicit reconciliation choice; never silently combine edits.
- **Validation:** inspect the resulting worktree, run the requested checks, and report changed files and validation evidence. Do not rewrite provider findings.

Parallel review/research is recommended for independent opinions. Sequential implementation is recommended after Codex selects findings and prepares a handoff. A completed provider is never terminated merely to advance the next stage.

## Provider artifact protocol

When `run_provider.py` is used, the host owns `status.md`, `events.jsonl`, and
`result.md`. Providers return their final Markdown through stdout and must not
use native file tools or Bash to write those paths; this avoids Antigravity's
native artifact-root restriction (`.gemini/antigravity-cli/brain/...`). The
host writes the files atomically and keeps native diagnostics in `logs/`.

The host status uses these states:

```text
pending → running → succeeded
                  ↘ completed_with_warnings
                  ↘ needs_attention → visible manual fallback
                  ↘ failed | timed_out | cancelled
```

`needs_attention` is an incomplete background attempt requiring trust,
authentication, or an in-scope manual approval. `completed_with_warnings` means the process exited successfully but produced no
substantive stdout report; it is a terminal receipt, not a completed independent review, and validation remains nonzero. `timed_out` and `cancelled` are terminal evidence,
not successful reviews. A result file is required for every terminal state.
For host-owned runs, `status.md`, `result.md`, monitor receipts, and the
completion section appended to `owner_notice.md` record `started_at`,
`first_output_at`, `response_at` (last captured provider output),
`completed_at`, and `duration_seconds` for benchmarking.

For direct interactive runs, each provider updates its own `status.md`:

```text
state: pending|running|succeeded|completed|completed_with_warnings|failed|incomplete|timed_out|cancelled
phase: prepared|starting|analysis|implementation|validation|writing_artifact|done
started_at: <UTC timestamp>
updated_at: <UTC timestamp>
last_activity: <UTC timestamp>
progress: <short human-readable update>
```

Append bounded JSON records to `events.jsonl` when useful. Before setting `state: succeeded`, atomically write `result.md` with:

```markdown
# Result
## Summary
## Findings
## Evidence
## Changes
## Validation
## Limitations
```

For implementation work, list every changed path. For review work, include exact file/line evidence and distinguish provider findings from checks not performed. Never put API keys, cookies, authorization headers, private keys, or a raw transcript in artifacts.

For review work, keep one entry per semantic root cause. Use the normalized finding key from the generated prompt so Codex can match agreements, duplicates, prior dispositions, and genuinely new evidence without turning repeated wording into another remediation cycle.

## Standby monitoring

Run the bundled monitor from the Codex main task or a read-only monitor sub-agent:

```bash
python3 scripts/monitor_run.py \
  --run /path/to/run/<id> \
  --interval 60 \
  --timeout-minutes 30
```

The monitor reads only `manifest.json`, provider `status.md`, `events.jsonl`, and
`result.md`. It reports new file activity, phase, heartbeat, result size, and
terminal state. The monitor reads once per minute by default, and emits only
when the receipt changes. The active window begins at the earliest `opened_at` recorded in
`launch.json`, not when a later Codex task happens to start polling. The window
must be between 5 and 30 minutes (30 by default); pass `--timeout-minutes` to
choose another value. It never launches, relaunches, steers, approves, edits
the repository, changes scope, or declares a provider result valid.

Use the role assignments in `manifest.json` when available:

- `monitor`: Luna or another explicitly selected Codex model watches files and reports provider activity.
- `review`: Codex independently compares provider findings and evidence.
- `validation`: Codex runs local checks and verifies claims against the worktree.
- `implementation`: only the explicitly selected implementation provider edits the authorized workspace.
- `main`: the main Codex agent decides whether to accept findings and plan changes.

Standby can last several minutes. A quiet provider is not automatically failed; use `last_activity`, process status, and the configured timeout. If one provider fails, retain the other provider's artifacts and report a partial result.

## Sequential handoffs

Do not send raw transcripts to a later provider. After reviewing a completed artifact, Codex populates `handoff/to-<provider>.md` with:

- source provider and artifact paths;
- reviewed summary and selected findings;
- source snapshot SHA-256;
- target phase and objective;
- allowed files and mutation authority;
- required validation and unresolved limitations.

The receiving provider must use the same workspace fingerprint or an explicitly refreshed one. If the worktree changed between stages, stop and prepare a new manifest or explicit rebase decision.

## Reconcile and validate

Keep each provider's `result.md` unchanged. Write Codex conclusions only to `comparison.md`, clearly labeled as Codex synthesis. For review, compare agreements, disagreements, unique findings, evidence, false positives, and missing checks; deduplicate semantic finding keys before creating tasks or PR comments. For implementation, validate the resulting worktree with the project's own tests/build/lint commands and review the diff independently. Provider artifacts are evidence, not final approval.

Use the validator after results arrive:

```bash
python3 scripts/validate_run.py \
  --run /path/to/run/<id> \
  --require-headings
```

The validator checks provider metadata, states, required headings, result size, event JSON, artifact timestamps, and handoff references. Use `--require-unchanged` for read-only plan/review validation when the provider was not authorized to edit.

## Failure handling

- Missing `grok`, `agy`, `agent`, `junie`, or `codex`: report the exact command and let other providers continue.
- Authentication, workspace trust, or command approval in managed background mode: preserve `attention.json`, use the recorded visible fallback, and approve only the already authorized scope.
- Cursor macOS Keychain error `SecItemCopyMatching failed -50` in a sandboxed
  background attempt is classified as authentication attention, not proof that
  the account is signed out; retry once through the recorded visible `agent`
  fallback where host Keychain access is available.
- Authentication, subscription, or model failure: preserve the provider error without secrets; do not fabricate success or retry indefinitely.
- Provider crash: retain existing artifacts and mark the provider incomplete; do not claim process cleanup that was not observed.
- Missing or stale status/result: report incomplete evidence, not a clean review.
- `completed_with_warnings`, `timed_out`, and `cancelled`: preserve the result and classify it explicitly; never upgrade it to `succeeded`.
- Changed repository fingerprint: stop the affected review and refresh the manifest; never compare against a different worktree silently.
- Codex task reload: rediscover the run through `manifest.json`; file artifacts do not depend on an in-memory job registry.
- One parallel provider fails: keep healthy peers running and synthesize `partial` evidence.
- Cleanup: delete a run only after the user explicitly requests cleanup and the exact run path is confirmed.

## Non-goals

This skill does not emulate a Codex model picker, own a broker, negotiate ACP sessions, run a persistent daemon, automate arbitrary GUI Terminal.app keystrokes, impose a second provider shell allowlist, merge worktrees, commit/push code, or guarantee provider availability. It may use the Codex-managed PTY input surface for the explicit native-command and prompt-submission sequence described above. It coordinates native CLIs and preserves their normal capabilities while making their inputs and outputs reviewable.
