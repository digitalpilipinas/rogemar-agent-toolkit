# Bounded dynamic workflows

Select this method for an authorized broad audit, a real migration with independent
packages, or an existing backlog of failing checks. Use it only when repeatable
coordination earns its cost. A small correction, coupled change, or empty backlog
stays with ordinary execution. Do not invent a migration or audit to use agents.

`workflow-orchestrator` remains the single selection and dispatch owner. A native
workflow script executes its approved assignments; it is not another coordinator.
Integrated Workflow retains delivery and review gates. Other harnesses may use
bounded native workers under this same method, but must not claim Claude workflow
execution. If the required runtime is absent, report it and use only an authorized
fallback; missing required independent evidence remains blocked.

## Prepare the bounded run

Reuse the existing plan and receipt. Before dispatch record:

- Candidate commit/tree, plus hashes of included uncommitted files; selected
  directory and complete file/package inventory, exclusions and allowed evidence
  reads outside it. Preserve unrelated changes.
- Named phases, package owner and independent reviewer, dependencies, tools,
  permission and model qualification, acceptance evidence and stop conditions.
- Total agent-attempt budget, concurrent limit, round limit and any enforceable
  time/usage budget. State whether the parent counts. Reserve review and validation
  capacity before scheduling producers; retries and replacements consume capacity.
- Progress measure and baseline: verified coverage/independently confirmed new
  root causes for audits; integrated, checked packages for migrations; original
  failing checks resolved without new regressions for repair work.

Start with one directory for an unfamiliar route. Size to useful packages, not a
fixed roster or one agent per line/file. Keep default concurrency at three or less
and honor a tighter owner/runtime limit. No nested spawning by workers. Count all
attempts across resume/relaunch; do not reset the task budget with a new run ID.

Use supported runtime restrictions, exact ownership and isolated fixtures. Read-only
instructions alone are not sandbox enforcement. For concurrent writers use isolated
worktrees, inspect shared resources and serialize integration. Tests must not target
real installations, credentials or production state without separate authority.

## Produce, review, challenge

Give each independent package one producer and a different reviewer. The reviewer
inspects the entire assigned package, including areas reported clean, for omissions
and incorrect conclusions. Carry the selected methods, source identity, scope,
authority and evidence requirements in both briefs. The parent accepts the result.

For audits, every candidate finding from either producer or reviewer goes to another
agent to attempt to disprove it. Each finding records a stable root-cause key,
candidate, location, trigger, expected/actual behavior, impact, evidence and author.
The challenger must not be the author. A reviewer may challenge producer findings
within its review; use another agent for the reviewer's own new findings. Cross-check
new challenger findings too, or leave them unverified when capacity is exhausted.
Do not require a third review of an already adequately challenged finding.

Use these separate dispositions in the existing receipt:

- `confirmed`: independent challenge completed with a reproduction or decisive
  source/contract evidence supporting the claim; parent validated the disposition.
- `rejected`: contrary evidence disproves the claim; retain the reason.
- `unverified`: evidence is insufficient, disputed, stale or challenge failed.
- `uncovered`: required package, file or review has no completed evidence.

Count only confirmed unique root causes as findings. Deduplicate without losing
distinct failure cases or author/reviewer provenance. A vote, severity label,
repetition, successful command or self-reported completion is not proof.

## Continue, stop and recover

Catch failures at assignment boundaries. Null, malformed, cancelled, timed-out and
failed results retain their package identity and coverage gap. Do not filter them
out of the inventory or label them clean. Continue independent assignments; block
dependents whose evidence is missing. Record actual runtime/profile substitutions.

A round is one bounded work-and-validation wave against the recorded candidate.
Compare its verified result with the previous wave before scheduling another.
Stop after two consecutive rounds without meaningful progress under the recorded
measure; reset the streak only on evidence-backed progress. Renaming issues,
retrying a command, deleting a failing test or reducing coverage is not progress.
Stop earlier on completion, cancellation, exhausted budget or an unresolved required
prerequisite. A pause for authority/authentication is not an invitation to retry.

The existing `workflow_contracts.py retry` helper accepts optional
`no_progress_rounds` for this method; two or more returns `stop-no-progress`.
The host computes that count from evidence. The helper neither measures progress
nor dispatches agents. Scripted routes must check their cumulative budgets before
every spawn and preserve counters during recovery. A size preference is not a cap.

Reconcile actual worker state before resuming. Invalidate evidence affected by a
changed candidate, preserve unaffected results and never create duplicate active
writers. Report covered inventory, all dispositions, failed assignments, remaining
gaps, attempts used, stop reason and next safe action. Partial success is not full
coverage. Audit completion does not authorize fixes or publication.

## Harness binding and sources

In Claude Code, use the installed `claude-forge` reference
`references/dynamic-workflows.md` when that adapter is available. In Codex, Cursor
and portable routes, use the active adapter's observed native worker controls and
model policy; do not copy Claude commands, model IDs or persistence assumptions.
No global instruction expansion, always-on mode, new scheduler or default login
is required. Static skill installation and live workflow qualification are separate.

Sources reviewed 2026-10-11: [Claude Code workflows](https://code.claude.com/docs/en/workflows)
for native execution; [Managed Agents orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)
only for decomposition, independent package review and failure/coverage handling.
Managed Agents hosting, API configuration and budgets are not Claude Code controls.
