# Autopilot stack

Build and verify a linear PR chain for the user to review and land. `integrated-workflow` owns the approved delivery contract; the orchestrator owns delegation.

1. Verify implementation and publication authority separately. If publication is outside scope, prepare the local changes and proposed topology. Preserve user-owned review and merge decisions. Do not create a goal or monitor unless requested.
2. Assign coherent slices with `feature.md`, `bug-fix.md` or `refactoring.md`. Parallel writers use isolated worktrees; the parent can own coupled work. Use live task profiles below both parent ceilings and explicit verification responsibilities.
3. Capture decisions and exact base/head evidence as work progresses. Review the actual diff, meaningful checks and applicable runtime behavior. Request independent verification where its risk justifies it, with bounded coverage and one reconciled verdict.
4. Publish only under existing authority. Draft PRs are valid when evidence or review is pending. A timeline or checkpoint never forces a push or ready-state claim.
5. Keep one writer for stack topology. Confirm each child is based on the intended parent's tip and targets its branch. Record an explicit bottom-to-top order. Do not infer dependency from PR numbers or require Graphite.
6. Reconcile trunk drift from the bottom. Any head/base change requires reviewing the new integration context and rerunning affected checks; a matching patch ID is useful comparison evidence, not preservation of an old verdict. History rewrites or force pushes need specific authority and fresh remote evidence.
7. Use an exposed watcher only for authorized monitoring. GitHub readiness is evidence for review, not programme acceptance. Missing or stale evidence blocks readiness.
8. Deliver the chain with per-link head, base, verdict, checks and gaps. Do not merge, arm auto-merge or close links. User review and landing remain the terminal boundary of this playbook.
