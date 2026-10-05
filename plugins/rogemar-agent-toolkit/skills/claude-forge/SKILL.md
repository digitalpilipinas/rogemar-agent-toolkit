---
name: claude-forge
description: Run Forge engineering methods on Claude with Claude's own models, subagents, and tools. Use for Claude Forge, substantive implementation, diagnosis, refactoring, review, or verification. Preserve Cursor poteto-mode and Codex Forge as separate entries.
---
# Claude Forge

Follow the [applicable method contract](../workflow-orchestrator/references/method-contract.md) at entry, every task handoff and delegation,
material changes, resume and acceptance. Select relevant methods automatically; preserve one owner,
required evidence and the original working fallback. Query the routing index only
for the current task; do not load or activate the whole catalog.

For an approved task, preserve the current plan and effective delivery route.
Selecting this execution entry does not restart planning or authorize publication.
When Integrated Workflow owns delivery, contribute methods through its existing
orchestrator; use the shared operating contract when present.

At task start/resume, before acceptance and at verified completion, apply the shared
[automatic checkpoints](../engineering-playbooks/references/agent-friendly-workflow.md) when a project verification map or learning enrollment exists. Select the actions without waiting for skill names; preserve task authority and required evidence.

Follow the shared [Forge mode and status contract](../workflow-orchestrator/references/forge-mode-status.md) at entry,
resume and dispatch: explicit request → task mode → saved preference; ask once
if none exists. Show role, model, effort, mode and evidence status without
repeated introductions. Setup inspection alone does not require a mode choice
or write preferences; apply the prompt when beginning an execution task.

This is the Claude execution entry for the shared Forge methods. Use the
installed `forge-*` skills and the `engineering-playbooks` library. Do not use
`codex-forge` or `forge-setup` here. This entry does not replace Cursor
`/cursor-forge` or `/poteto-mode`. `claude-forge-setup` qualifies Claude
profiles. `workflow-orchestrator` remains the only dispatcher.

If this session is not Claude, stop and use the entry for the harness that is
actually running. Naming Claude does not create Claude tools.

Read [the Claude runtime contract](references/claude-runtime.md) before any
worker, model, tool, or publication action. Read
[the companion index](references/companions.md) when a playbook names a companion.
Read [the principle index](../engineering-playbooks/references/principles.md)
for any principle you apply.

Use shared [context guidance](../workflow-orchestrator/references/context-efficiency.md)
for large outputs. Use shared
[sub-agent naming](../workflow-orchestrator/references/subagent-naming.md) after
setup qualifies the profile.

## Choose the work

Select one playbook and read that file in full. The steps there are the shared
method. The Claude runtime contract binds workers and tools.

- [Investigation](playbooks/investigation.md)
- [Bug fix](playbooks/bug-fix.md)
- [Perf issue](playbooks/perf-issue.md)
- [Hillclimb](playbooks/hillclimb.md)
- [Runtime forensics](playbooks/runtime-forensics.md)
- [Trace forensics](playbooks/trace-forensics.md)
- [Feature](playbooks/feature.md)
- [Refactoring](playbooks/refactoring.md)
- [Prototype](playbooks/prototype.md)
- [Visual parity](playbooks/visual-parity.md)
- [Authoring or modifying a skill](playbooks/authoring-a-skill.md)
- [Eval](playbooks/eval.md)
- [Babysit](playbooks/babysit.md)
- [Shipping](playbooks/shipping.md)
- [Autonomous run](playbooks/autonomous-run.md)
- [Orchestrate](playbooks/orchestrate.md)
- [Autopilot-full](playbooks/autopilot-full.md)
- [Autopilot-stack](playbooks/autopilot-stack.md)
- [Session pickup](playbooks/session-pickup.md)
- [Pause safely](playbooks/pause-safely.md)
- [Multi-phase or multi-PR plan](playbooks/multi-phase-plan.md)
- [Worktree and simulator cleanup](playbooks/worktree-cleanup.md)
- [Opening a PR](playbooks/opening-a-pr.md)

These three shared methods are not part of the 23 PStack playbooks. Read them
from the portable library when the task matches.

- [Knowledge maintenance](../engineering-playbooks/playbooks/knowledge-maintenance.md)
- [Security audit](../engineering-playbooks/playbooks/security-audit.md)
- [External collaboration](../engineering-playbooks/playbooks/external-collaboration.md)

When no bundled playbook fits, use the Figure it out section of the companion
index. A standing approved programme stays inside `integrated-workflow`.

## Attribution

Claude Forge is inspired by Lauren Tan's PStack and poteto-mode. The shared
playbooks preserve that MIT notice. This package is the Claude binding. Cursor
keeps `/cursor-forge` and upstream `/poteto-mode`. Codex keeps `codex-forge`.

## Affected capability maintenance

For changed skill dependencies, broken recipes, or an explicit update, route
through `workflow-orchestrator` to `codex-capability-maintainer` and the
applicable verification-skill companion. Scope the check to the behavior that
changed. Do not start a new delivery owner.
