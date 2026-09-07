---
name: forge-swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for $forge-swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
license: MIT
---
# Swarm

## Codex execution contract

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md). `workflow-orchestrator` owns delegation; `plan-model-router` resolves every worker profile under the active Forge mode, or parent defaults and ceilings when no mode is selected. Role preferences are hints, never model IDs or a fanout requirement. Work locally when delegation adds no useful independent work.

Coordinate bounded coverage, races, or mixed exploration and return one report.

1. **Frame.** State the done predicate, deliverable, independent slices, and worker budget. For a race declare first-pass, rank-all, or best-of before dispatch. A requested total number is a coverage target, not permission to exceed concurrency.
2. **Request assignments.** Give `workflow-orchestrator` each slice, role hint `swarm-workers`, scope, acceptance, non-goals, stop condition, and verification. Default to the selected parent; resolve justified alternatives through the router. Read-only workers may share a checkout. Writers need isolated worktrees or sequential ownership. Do not assume cloud agents, background flags, or remote branches exist as tool parameters.
3. **Run and drain.** The orchestrator schedules the smallest useful rolling window within exposed limits. Use actual status tools; do not invent wakeups. Track every assignment to a terminal receipt. On failure, reassign a narrower slice or absorb it locally and record the coverage change.
4. **Aggregate.** Coverage requires evidence for every required slice. A race follows its declared selection rule. Missing slices remain gaps even when other workers pass. Inspect artifacts and reconcile overlapping findings.
5. **Report.** Return one compact table of slice, owner, result, evidence, and gaps. Use Verified, Partial, Blocked, or Unverified without fabricated scores or costs. A selected candidate still requires final integration verification.
