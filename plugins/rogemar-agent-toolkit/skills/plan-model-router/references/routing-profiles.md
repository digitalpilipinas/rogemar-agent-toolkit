# Task-fit assessment

Use the shared [dispatch contract](dispatch-contract.md) for execution and
[role mapping](role-mapping.md) for current Forge pools. This reference guides
qualification; it is not another model table or dispatch implementation.

## Qualification

Before assigning implementation, establish the intended behavior, exact scope,
ownership, invariants, acceptance evidence, dependencies, and rollback posture.
If those are materially unclear, perform bounded triage or planning first.
A role default is only a starting candidate. Do not infer sufficiency from a
role name, patch size, urgency, or the effort label alone.

For materially risky or multi-increment plans, assess these dimensions:
blast radius and reversibility; security/privacy/authorization; cross-layer
coupling; novelty and ambiguity; verification difficulty; rollback difficulty.
Record the dimensions that actually affect the profile, rather than scoring
routine tasks for ceremony. Reassess against the real diff before execution.

## Family and effort hints

These are local task-fit heuristics, not measured prices or benchmark claims.
Use only model IDs and efforts exposed by the current dispatch tool:

| Family | Candidate ID | Task-fit hint |
| --- | --- | --- |
| Astra | `gpt-6-astra` | Most demanding unresolved reasoning when available and permitted |
| Sol | `gpt-5.6-sol` | Substantial ambiguity, coupled design, or consequential review |
| Terra | `gpt-5.6-terra` | Bounded implementation requiring engineering judgment |
| Luna | `gpt-5.6-luna` | Narrow investigation, established execution, or bounded checking |

Low/medium are candidates for narrow established tasks; high/xhigh for deeper
investigation or checking; max for assignments needing sustained reasoning.
These are choices to qualify, not guarantees. Light maps to `low`, Extra High
to `xhigh`. Reasoning effort does not establish model-family equivalence.
Do not claim Luna/max outperforms Terra/medium or necessarily finishes faster.

The four Forge pools exclude Ultra. If the runtime exposes Ultra for another
explicitly authorized no-mode assignment, validate it through the helper's
applicable parent ceiling and independent-work condition. Do not infer supported
efforts or automatic parallel execution from a remembered model description.

## Adaptation and evidence

1. Begin with the mode/group/role candidate and saved preferences.
2. Explain why it is sufficient for this actual package and its evidence needs.
3. If unavailable or insufficient, propose a qualified alternate within the
   same mode and explicit user limits. Do not silently fall back or weaken tests.
4. Escalate within the pool when unresolved ambiguity, repeated reasoning
   failure, or a failed counterexample makes that necessary. If no eligible
   profile suffices, report the constraint and recommend a mode change.
5. Use independent review when it resolves material uncertainty. Keep it
   read-only and bounded; the implementation owner reconciles defects. A second
   pass is unnecessary when targeted checks already provide adequate evidence.

For each meaningful increment, record the exact model and effort, task-fit
reason, required specialist methods, acceptance evidence, invariants, non-goals,
dependencies, and escalation trigger in the existing plan or handoff. Do not
create a second board or duplicate the delivery workflow. The main agent owns
integration and final acceptance; model selection never replaces either.
