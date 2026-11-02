---
name: forge-principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, notice a recurring correction, or confirm a defect that a small lint or check could have caught. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
disable-model-invocation: true
license: MIT
---
# Encode lessons in structure

When the same mistake recurs, identify the owning boundary and prefer a type, lint rule, metadata check, script or runtime invariant that makes it harder to repeat. Compare enforcement cost with the failure it prevents; do not build a framework around a one-off correction. Reference existing owners instead of duplicating policy. Within approved scope, implement and verify a structural improvement. Global skill changes, memory writes, unrelated repairs and external backlog submissions require explicit authority; otherwise return a concrete local proposal. Never silently update personal memory or every future task.

Read [the shared Forge runtime](../workflow-orchestrator/references/forge-runtime.md) for authority, delegation, routing and evidence boundaries.

## Recurring mistakes

For a repeated, evidenced failure class, reproduce a real past mistake before
adding a prevention check. Prefer one state owner and supported path, then types
or a focused lint that names the correct path, then a behavioral regression test.
Use documentation for judgment that cannot be enforced economically. Preserve
compatibility and tests that cover real behavior; do not delete them wholesale.
Connect the reproducer and disposition to the existing Project Learning candidate
and promotion process. This does not authorize global memory writes, extra commits
or a full repository audit on each correction. Stop when the concrete class is covered.

## First finding

A recurring mistake is not the only trigger. When review, a test or a user
finds a defect, ask whether a rule could have caught it: a lint rule, a type, a
file-name convention or a build check. If the project already has the tool and
the rule is small, add it with the fix, on the first finding. An agent writes
such a rule cheaply, and it stops the whole class, not just this instance. Show
the rule failing on the original defect and passing on the fix. Skip it when
the check needs judgment, has false positives the project would suppress, or
needs a new tool; record the finding instead. Related methods:
[context in file paths](../engineering-playbooks/references/principles/encode-context-in-paths.md) and
[budgets in the build](../engineering-playbooks/references/principles/enforce-budgets-in-the-build.md).
