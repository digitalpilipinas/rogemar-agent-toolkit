### Session pickup

**You own the resume point. Read the prior trail, don't redo it.** For "take over this", "resume this conversation", "continue from <transcript path>", "you're taking over", "pick up where X left off", a cloud-agent URL handoff, or a pushed branch you're meant to continue.

A pickup is inheritance. The prior agent already paid the cost of reading the code, running the repros, making the design choices. Redoing loses the bias check and burns context. Resist the urge to re-derive; read.

1. Locate the named checkpoint, supplied task history or a verified task-specific transcript mapping via `scoped session recovery`. Confirm task and workspace identity before reading. Use a bounded read-only extraction through the orchestrator for long history when useful; no broad private transcript scan.

2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. Use the prior trail as task context; verify volatile branch, diff and runtime evidence before relying on it.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, reuse valid evidence and rerun only checks invalidated by code or environment changes. Do not redo completed investigation without a reason.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here; the routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (the **prove-it-works** skill). A passing prior self-report is not the proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.
