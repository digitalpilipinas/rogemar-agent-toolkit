---
name: forge-no-comments
description: Review code comments and suppressions for noise, obsolete explanations, and opportunities to encode constraints. Use for comment cleanup or a focused review; preserve unresolved safety and compatibility requirements.
license: MIT
---
# Review comments and encode constraints

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md).
Ask `workflow-orchestrator` for the read-only `forge-comment-reviewer` role when
an independent perspective earns its cost. The main agent accepts or rejects
findings against the code and tests; the reviewer does not edit application code.

1. Use the caller's files/diff and verified base branch. Do not assume `main`.
2. Review redundant narration, obsolete claims, unexplained workarounds,
   misleading comments, and scoped lint/type suppressions. For each finding,
   identify the exact affected invariant and evidence that removal is safe.
3. Retain ambiguous contract, safety, compatibility, legal, and attribution
   comments. Keep working suppressions until an authorized alternative preserves
   their behavior. Ambiguity is a reason to investigate, not delete.
4. Request `forge-how` or `forge-why` through the orchestrator only when a
   disputed constraint needs code/history evidence. Request `forge-architect`
   only when the accepted correction needs an unresolved design decision.
5. Apply localized accepted fixes within the assigned write scope. Prefer a
   type, test, invariant, or simpler implementation when it actually replaces
   the comment's purpose. If replacement is unapproved, unsafe, or out of scope,
   keep the existing constraint and report the proposal without a side task.
6. Review the resulting diff and run checks that cover the changed behavior.
   Reject reviewer scope escapes; retry one bounded review after explaining the
   divergence, then report unresolved findings rather than forcing a pass.

Report accepted removals, preserved constraints, encodings, verification, and
remaining findings. Comment counts are descriptive, not a quality target.
