# Feature

Own the behavior, design and final verification. Use `source tracing` to trace affected flows and `design exploration` when a contested or consequential design needs exploration. Skip formal design machinery for a clear small change.

1. State observable acceptance, compatibility constraints, allowed scope and meaningful checks.
2. Identify blocking prerequisites, independent work and shared mutable state. Prefer one owner for coupled implementation. Request independent workers through the orchestrator only when useful; writers need explicit nonoverlapping scope and isolated worktrees for parallel work. The parent may implement directly.
3. Model the domain before branching logic. Use a state machine, typed model or registry when it removes invalid states or repeated assumptions. Preserve existing contracts and nearby conventions. Use a bounded comparison for materially competing designs, not for every edit.
4. Implement the smallest coherent slice, inspect its diff, then verify the changed behavior on the matching surface. Run focused checks and relevant runtime evidence; a blocked surface stays unverified.
5. Reconcile all consumers of changed shared primitives. Revisit design if repeated workarounds show the model is wrong. Use `assumption critique` where a consequential unresolved assumption needs critique.
6. Record verified increments. Apply `opening-a-pr.md` only when publication is authorized; preparation alone is still a complete local implementation when that is the user's scope.

Report what changed, the chosen design and tradeoff, actual checks, and remaining gaps.
