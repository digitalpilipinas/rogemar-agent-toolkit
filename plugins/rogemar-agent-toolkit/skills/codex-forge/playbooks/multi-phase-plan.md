# Multi-phase plan

Use `create-plan` and `workflow-orchestrator` to turn a cross-cutting outcome into verifiable increments. `plan-model-router` supplies profile proposals under the active Forge mode; without a mode, parent defaults and ceilings apply. Explicit user and host limits always apply. Planning is not implementation.

1. Inspect instructions, source, current changes, dependencies and existing plan state. Name the observable goal, assumptions, constraints, non-goals, affected systems and authority. Reuse an approved programme or GoalBuddy record rather than starting a competing board.
2. Resolve only material user decisions. A prototype may answer an empirical question when scratch implementation is authorized; in planning mode describe the experiment without writing production code, scaffolding, branches or jobs.
3. Decompose into the largest safe useful increments. Each names owner, allowed files/symbols, dependency IDs, acceptance, non-goals, stop conditions, validation and expected evidence. Shared writers serialize unless isolated worktrees and reconciliation are explicit. No compulsory panel size or worker for a routine increment.
4. Choose validation from the actual risk: focused checks for small edits; characterization/equivalence for risky refactors; original repro for bugs; runtime/visual checks for interactions; measured baseline and comparable workload for performance. Record justified omissions and blocked checks. Do not require unit, live and performance tests on every change or exact wording in prose.
5. Keep one concise machine-readable contract alongside the human plan when structural checking is useful. Run `node <codex-forge>/scripts/check-plan.mjs <plan.md>`. It checks shape and dependency consistency only; it cannot verify consent, task sufficiency, runtime availability or completed work.

```forge-contract
{
  "schema_version": 1,
  "goal": "Deliver the agreed behavior",
  "done_when": "Named acceptance evidence exists for each increment",
  "authority": {"source": "Current user-approved implementation request", "allowed_actions": ["edit scoped files", "run local checks"]},
  "tasks": [{
    "id": "T1", "owner": "main agent", "scope": ["explicit/path"],
    "depends_on": [], "acceptance": ["Observable behavior and compatibility condition"],
    "profile": "inherit-parent", "stop_when": "Scope or required evidence cannot be established",
    "validation": [{"check": "Repository-native scoped check", "evidence": "Saved result and actual diff"}]
  }]
}
```

6. Record worker profile hints separately with task-fit reasons, validation and escalation triggers. Re-resolve at dispatch using the live catalogue and actual role overrides. Parent-model suggestions at major boundaries are advisory and user-applied.
7. After approval, hand the existing contract to `integrated-workflow` where applicable. It retains lifecycle and external-action authority; Forge activates the matched implementation, diagnosis, refactoring or verification method inside each package. Create a goal, recurring monitor, PR or deployment only with the corresponding user authority.
8. Close against the actual diff and evidence. State implemented, verified, blocked and deferred separately. Do not mark an unchecked requirement complete because the plan validator passes.
