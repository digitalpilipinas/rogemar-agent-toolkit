### Session pickup

Apply the [task-handoff method contract](../../workflow-orchestrator/references/method-contract.md).
Restore the last accepted task and unfinished gates; refresh invalidated facts before reusing preparation or advancing.

**You own the resume point. Read the prior trail, don't redo it.** For "take over this", "resume this conversation", "continue from <transcript path>", "you're taking over", "pick up where X left off", a cloud-agent URL handoff, or a pushed branch you're meant to continue.

A pickup reuses relevant prior work while checking freshness. Read the supplied trail first; inspect the current branch, changes, permissions and runtime facts needed to rely on it.

1. Locate the named checkpoint, supplied task history or a verified task-specific transcript mapping via `forge-recall`. Confirm task and workspace identity before reading. Use a bounded read-only extraction through the orchestrator for long history when useful; no broad private transcript scan.

2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. Treat the trail as scoped recovery evidence. Current source, actual side effects and applicable authority determine whether its claims remain valid.
3. Compare done against pending and identify the next dependency-ready unit. Reuse unchanged evidence within its recorded candidate, environment and scope. Refresh changed or uncertain facts and rerun affected checks; do not redo unrelated completed work.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here; the routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (the **forge-principle-prove-it-works** skill). A passing prior self-report is not the proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.
