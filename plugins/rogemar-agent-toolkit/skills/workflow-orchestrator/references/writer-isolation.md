# Writer isolation

This is the shared writer policy for the orchestrator and harness adapters.
Repository instructions, host restrictions and explicit assignment limits may
require stronger isolation. State such a restriction in the assignment.

Multiple writers may share a worktree only when the implementation owner has
established independent write scopes. Two writers must not edit the same file at
the same time. Account for shared generated outputs, interfaces, dependency files,
Git index/branch operations, databases and mutable runtime resources; different
source filenames alone do not establish independence. The main agent is a writer.

Use isolated worktrees for competing implementations, overlapping changes, branch
operations or uncertain separation. Separate worktrees do not isolate databases,
devices or external services: isolate or serialize those resources too. If the
needed isolation is unavailable, sequence the affected work. Do not fabricate a
worktree or claim a role label enforces read-only access.

Assign exact ownership and stop conditions before concurrent work. Keep Git
operations and integrated validation with the implementation owner. On conflict,
pause affected writers, preserve all work and reconcile; continue independent
work. Inspect integrated diffs and rerun checks invalidated by integration. For a
read-only reviewer compare the post-review state with its actual starting state,
including existing dirty and untracked work, rather than requiring a clean tree.

The assignment validator defaults to rejecting concurrent writers in one worktree
unless every writer supplies `independence_evidence` naming the owner's scope and
resource review. Overlapping paths remain forbidden there. Competing changes in
different worktrees require the same explicit `integration_plan` reference. Shared
exclusive runtime resources remain forbidden in either case. These fields record
review evidence; nonempty strings do not prove independence or authorize dispatch.
