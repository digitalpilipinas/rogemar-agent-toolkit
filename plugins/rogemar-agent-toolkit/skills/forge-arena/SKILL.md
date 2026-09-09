---
name: forge-arena
description: "Compare independent candidates against a rubric, choose a base, graft useful ideas and verify one synthesis. Request bounded collaboration through workflow-orchestrator."
license: MIT
---
# Arena

## Codex execution contract

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md). `workflow-orchestrator` owns delegation; `plan-model-router` resolves every worker profile under the active Forge mode, or parent defaults and ceilings when no mode is selected. Role preferences are hints, never model IDs or a fanout requirement. Work locally when delegation adds no useful independent work.

Produce independent candidates, choose a base against a declared rubric, graft useful ideas, and verify the synthesis. Use this for contested designs or artifacts where one attempt may lock in the wrong shape.

## A. Frame

State the artifact and shared grounding. Define 3–6 observable rubric criteria before reviewing outputs. Choose the smallest useful number of distinct design directions; two is often enough. Ask the orchestrator for bounded candidate assignments using the `arena-runners` preference pool, with explicit scope, output, acceptance, non-goals, stop condition, and verification. Pools do not specify a worker count. Give candidates the task and constraints; reserve the scoring rubric for the judge where blinding is useful.

## B. Produce independent candidates

The orchestrator schedules within actual concurrency limits and the router-qualified active mode, or parent ceilings when no mode is selected; explicit user and host limits always apply. Candidates return an artifact and rationale naming rejected alternatives. Writing candidates need isolated worktrees and explicit reconciliation; separate branches in one worktree are not isolation. Read-only design candidates may return text. Do useful local work while independent candidates run. A failed candidate is a reported gap, not an implicit pass.

## C. Cross-judge

After candidate outputs are complete, request one read-only judge from `arena-cross-judge-pool` when useful. Prefer an independently framed critique; another Codex model is optional and must be available below the ceiling. Blind labels rather than claiming model-family diversity that the runtime cannot provide. The judge evaluates the declared criteria and recommends a base with evidence while the parent reads all candidates.

## D. Pick a base

Read every candidate and compare criterion by criterion. Reconcile disagreement with the judge by examining the evidence and rubric. Prefer maintainable boundaries and a smaller public surface when candidates are otherwise equivalent. Record the choice and why.

## E. Graft

Inspect each losing candidate for the one or two ideas worth integrating. Adapt each graft to the base's design rather than pasting it mechanically. Record adopted and rejected ideas with their source. Convergence may justify keeping the common shape without grafting. Wide divergence may require reframing; do not average incompatible designs.

## F. Verify

Verify the synthesized artifact against the original acceptance criteria. Candidate success does not prove the combined result. After repeated failures, revise the framing or graft choice instead of rerunning the same approach indefinitely. Return one artifact and a concise synthesis record containing rubric results, base, grafts, rejections, gaps, and actual verification.
