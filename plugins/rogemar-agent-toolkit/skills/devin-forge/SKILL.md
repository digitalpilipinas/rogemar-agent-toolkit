---
name: devin-forge
description: Run shared Forge engineering methods natively in Devin using Devin's own agent modes, child sessions, and tools. Use for Devin Forge, substantive implementation, diagnosis, refactoring, review, or verification in Devin. codex-forge, cursor-forge, claude-forge and universal-forge are separate entries.
license: MIT
---
# Devin Forge

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

This is the Devin execution entry for the shared Forge methods. Use the
installed `forge-*` skills and the `engineering-playbooks` library. Do not use
`codex-forge` or `forge-setup` here. This entry does not replace Cursor
`/cursor-forge`, `/poteto-mode`, `claude-forge`, or `universal-forge` on other
harnesses. `workflow-orchestrator` remains the only dispatcher.

If this session is not Devin, stop and use the entry for the harness that is
actually running. Naming Devin does not create Devin tools.

Read [the Devin runtime contract](#devin-native-runtime) below before any
worker, model, tool, or publication action. Read [the principle
index](../engineering-playbooks/references/principles.md) for any principle you
apply. Use shared [context guidance](../workflow-orchestrator/references/context-efficiency.md)
for large outputs. Use shared
[sub-agent naming](../workflow-orchestrator/references/subagent-naming.md) for
worker receipts.

## Devin-native runtime

- **Parent model**: Devin does not expose its own runtime model or a self-switch
  control. Report `model unverified` / `effort not exposed` honestly. The user
  switches the session's agent via `!fast`, `!normal`, `!fusion`, `!ultra` or
  the webapp picker. When a mode's desired parent differs from the observed
  session, apply the contract's clarify-a-different-parent step once and record
  the accepted fallback — never claim an unapplied switch.
- **Workers**: `devin_session_create` child sessions. Each gets its own VM and a
  fresh clone of the remote — a child sees only what has been pushed, so push a
  branch/PR first only when the worker needs your uncommitted or local-only
  commits. Give a bounded brief: purpose, scope/files, non-goals, required checks,
  stop conditions, expected evidence. Read-only reviewers must not commit,
  push, comment on PRs or merge.
- **Worker modes** (`devin_mode`): `swe-2-medium`, `swe-2-high`, `swe-2-max`,
  `lite`, `normal`, `fast`, `fusion`, `ultra` — subject to what the org's picker
  allows. Pass the request in the call; the accepted `devin_mode` is visible on
  the child's details but the underlying model stays `effective model
  unverified`.
- **Results**: request `structured_output` for receipts; set
  `notify_on_response=true` and read output via `devin_session_interact` —
  never poll or message "status?" to children.
- **Native routes that beat child sessions** (use these instead of a worker
  when they fit the role):
  - Interactive UI verification (browser/simulator/emulator/device QA, visual
    review of a running app) → the in-session `testing_agent`, which owns its
    own setup and produces annotated recordings. Apply
    [verification efficiency](../workflow-orchestrator/references/verification-efficiency.md):
    request bounded capture when supported, avoid duplicate capture, and report
    provider-controlled recording when no supported off switch exists. Do not
    claim that guidance disabled native capture or that saved media was inspected.
    Use a child session only when
    isolation or concurrency is the point.
  - PR-diff review → `devin_review_manage` (Devin Review) is the native review
    route for an open PR. Child-session reviewers remain for pre-PR artifacts,
    non-PR diffs and independent judgment the native route can't express.
- **Concurrency**: default to at most three workers and one nesting level;
  justify exceptions in the dispatch receipt.

## Choose the work

Select one playbook and read that file in full. The steps there are the shared
method, read from the portable `engineering-playbooks` library — do not copy
them into this adapter. The Devin runtime contract binds workers and tools.

- [Investigation](../engineering-playbooks/playbooks/investigation.md)
- [Bug fix](../engineering-playbooks/playbooks/bug-fix.md)
- [Perf issue](../engineering-playbooks/playbooks/perf-issue.md)
- [Hillclimb](../engineering-playbooks/playbooks/hillclimb.md)
- [Runtime forensics](../engineering-playbooks/playbooks/runtime-forensics.md)
- [Trace forensics](../engineering-playbooks/playbooks/trace-forensics.md)
- [Feature](../engineering-playbooks/playbooks/feature.md)
- [Refactoring](../engineering-playbooks/playbooks/refactoring.md)
- [Prototype](../engineering-playbooks/playbooks/prototype.md)
- [Visual parity](../engineering-playbooks/playbooks/visual-parity.md)
- [Authoring or modifying a skill](../engineering-playbooks/playbooks/authoring-a-skill.md)
- [Eval](../engineering-playbooks/playbooks/eval.md)
- [Babysit](../engineering-playbooks/playbooks/babysit.md)
- [Shipping](../engineering-playbooks/playbooks/shipping.md)
- [Autonomous run](../engineering-playbooks/playbooks/autonomous-run.md)
- [Orchestrate](../engineering-playbooks/playbooks/orchestrate.md)
- [Autopilot-full](../engineering-playbooks/playbooks/autopilot-full.md)
- [Autopilot-stack](../engineering-playbooks/playbooks/autopilot-stack.md)
- [Session pickup](../engineering-playbooks/playbooks/session-pickup.md)
- [Pause safely](../engineering-playbooks/playbooks/pause-safely.md)
- [Multi-phase or multi-PR plan](../engineering-playbooks/playbooks/multi-phase-plan.md)
- [Worktree and simulator cleanup](../engineering-playbooks/playbooks/worktree-cleanup.md)
- [Opening a PR](../engineering-playbooks/playbooks/opening-a-pr.md)

These three shared methods are not part of the 23 PStack playbooks. Read them
from the portable library when the task matches.

- [Knowledge maintenance](../engineering-playbooks/playbooks/knowledge-maintenance.md)
- [Security audit](../engineering-playbooks/playbooks/security-audit.md)
- [External collaboration](../engineering-playbooks/playbooks/external-collaboration.md)

## Saved mode → Devin profile mapping (owner preference)

This table is the saved-preference rung for Devin: it supplies the routing
default when no explicit or task mode resolves. When a mode is resolved
(any source), route per its row here.

| Mode | Desired parent | Workers |
| --- | --- | --- |
| Peak | Fusion | SWE-2 High → SWE-2 Max |
| Balanced | Normal | SWE-2 Medium → SWE-2 High |
| Lean | SWE-2 High | Lite |
| Sprint | unchanged | Lite |

Pick within a band by task fit; modes are routing preferences only and never
lower acceptance standards or widen authority. The owner may revise this table
explicitly — apply the revision and keep a note of it in the task receipt.

## Role → Devin assignment table

Devin analogue of `plan-model-router`'s role mapping — the same portable role
names (see [the shared role inventory](../universal-forge/references/roles.md)),
resolved against Devin's fixed `devin_mode` catalogue. A role is a task
assignment, not a skill command and not a reason to spawn a worker; assignments
apply only when a justified worker is actually dispatched. "Default" = exact
user selection; without a named mode, retain parent inheritance and the
ceilings below.

| Role group | Roles | Peak | Balanced | Lean | Sprint |
| --- | --- | --- | --- | --- | --- |
| Parent-owned (never a worker) | parent-coordinator, workflow-coordinator, integration-owner | desired parent: fusion | desired parent: normal | desired parent: swe-2-high | unchanged |
| Judgment workers (independent-context reviews, judges, synthesis, design) | correctness-reviewer, scope-reviewer, acceptance-auditor, goal-judge, interrogate-reviewers, how-critics, reflect-judgment, judgment-and-prose, why-synthesizer, how-explainer, bug-triager, architect-runners, arena-cross-judge-pool, design-system-reviewer, visual-reviewer, ux-flow-designer, ui-designer, interaction-designer | swe-2-max | swe-2-high | parent-owned (escalate to swe-2-high only when independence is the point) | parent-owned |
| Implementation workers (bounded writes/verification) | feature, refactoring, bug-fix, perf-issue, hillclimb, hardest-tasks, how-explorer, why-investigators, validation-runner, qa-runner, simulator-qa, emulator-qa | swe-2-high (routine) → swe-2-max (hardest slices) | swe-2-medium (routine) → swe-2-high (harder slices) | lite | lite |
| Clerical / monitoring (support receipts, no judgment claims) | findings-consolidator, reflect-synthesizer, reflect-tooling, reflect-divergent, status-monitor, learning-curator, goal-scout, browser-qa, physical-device-qa, accessibility-reviewer | lite | lite | lite | lite |
| Task-fit participants | swarm-workers, arena-runners | resolve each participant's actual function into the rows above | | | |

Rules of application:

- **Judgment vs band**: a judgment worker never runs below the top of its
  mode's worker band — cheap reviewers produce cheap verdicts. Under Lean and
  Sprint the judgment work stays with the parent rather than delegating to a
  Lite worker; flag a named escalation (one bounded worker at the Balanced
  tier) only when a genuinely independent context is required for the record.
- **Inside the implementation band**, route the specific slice, not the whole
  task: routine bounded edits take the band's floor; hardest/least-understood
  slices take the ceiling.
- **Clerical roles never validate**: consolidation, monitoring and support
  receipts do not approve delivery, select scope or fix code.
- **Escalation is named**: any worker exceeding its band (e.g. a Lean
  correctness-reviewer at swe-2-high) is a named exception with a concrete
  reason in the dispatch receipt; it never becomes the new default.
- **Unverified is honest**: record `devin_mode accepted` in receipts; the
  underlying model stays `effective model unverified` and must not be claimed
  otherwise.

## Execution discipline

Proceed through authorized reversible work. Investigate discoverable facts;
ask only for material unresolved owner decisions. A playbook invocation grants
no new external-action authority. Keep an unavailable service or required
runtime check visibly blocked and continue independent authorized work.

Keep scope discipline under [writer isolation](../workflow-orchestrator/references/writer-isolation.md); read-only reviewers stay
read-only, no publication/merge without its own authority. Repository
instructions and the active plan override this file. Reconcile the actual diff,
executable evidence, and independently useful review before acceptance. Never
infer delivery from a worker summary or a green badge.

## Status labels

Entry/resume: `Coordinator · Devin (model unverified) / effort not exposed · <mode> · source: <request|task|saved>`.
Dispatch: `<Role> · <devin_mode> requested · <Forge mode>`; after dispatch note
`devin_mode accepted` vs `effective model unverified`.
Final receipt: roles, assignment modes, requested vs accepted profiles, and
unresolved mismatches.

## Attribution

Devin Forge is inspired by and adapted from Lauren Tan (poteto)'s **PStack**
and **poteto-mode**, published in the [Cursor plugins repository](https://github.com/cursor/plugins/tree/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack).
The original MIT attribution is preserved in `LICENSE.txt`. This is an
independent Devin adaptation; it does not imply endorsement or an unverified
affiliation.
