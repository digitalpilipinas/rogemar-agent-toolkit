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

Read exact model IDs, supported efforts and policy tiers from
`scripts/routing_catalog.json`; use the intersection with the observed native
catalogue. Tier ordering is a routing boundary, not an intelligence or price claim.
Distinguish generations in every receipt. An old family member's qualification
cannot transfer to its successor, even when the label or assigned role is similar.

Low/medium are candidates for narrow established tasks; high/xhigh/max/ultra need
matching evidence and supported controls, not a presumed quality advantage.
Light maps to `low`, Extra High to `xhigh`. Neither reasoning effort nor generation
establishes superiority or lower total delivered-task cost.

Normal presets stop at their explicit effort ceiling. Default may use any exact
supported selection; higher preset effort requires a verified, practically needed
hard-role exception. Never infer native effort support from a remembered label.

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
