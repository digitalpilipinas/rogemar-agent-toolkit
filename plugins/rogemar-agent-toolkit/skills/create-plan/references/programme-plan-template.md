# Programme Plan Template

Use this shape when dependencies, compatibility, risk, or a handoff need more
detail than the concise plan. Omit irrelevant sections. Extend an existing
approved plan or board in its own format; do not create a second source of truth.

```markdown
# Plan: <programme outcome>

**Status and authority:** <proposed or approved; current delivery boundary>
**Done when:** <observable proof of the complete requested outcome>
**Scope:** <affected systems and meaningful non-goals>

## Context and decisions

- <Source path or specification, current behavior, and contract to preserve.>
- <Chosen approach and why; material alternatives considered.>
- <Verified fact, explicit assumption, or unresolved owner decision.>

## Acceptance

| Requirement | Observable behavior | Evidence needed |
| --- | --- | --- |
| <requirement> | <success and relevant failure behavior> | <focused check or artifact> |

## Sequence

| Increment | Scope and outcome | Depends on | Acceptance evidence |
| --- | --- | --- | --- |
| <existing ID or short name> | <paths/interfaces and coherent result> | <predecessor or none> | <check tied to acceptance above> |

<For a handoff, identify the owner, allowed files or symbols, consumed/produced
contracts, and stop condition. Add these to the existing task records when used.>

## Material risk and rollout

- <Supported old/new inputs, clients, or persisted shapes and transition rule.>
- <Authority, privacy, concurrency, or operational invariant affected.>
- <Relevant denial, legacy, retry, concurrency, or rollback counterexample.>
- <Rollout prerequisite, recovery/disable action, and required environment proof.>

## Next action

<First authorized increment, required evidence or unresolved prerequisite, and
the selected execution owner. Add a capability requirement only if material.>
```

Validate dependency order, missing references, contradictory interfaces, and
requirement coverage. A dependency graph is useful for branching work; a list
is enough for a linear sequence. Independent writers need disjoint scope,
isolation, and a named integration owner before parallel execution is selected.

Keep validation proportional. Bugs need the original reproduction; compatibility
changes need supported old/new cases; interaction changes need the relevant
runtime evidence; performance claims need a measured comparable baseline. Do not
require unit, live, and performance suites for every increment. Record required
but unavailable evidence as blocked, and owner-approved omissions as deferred.

The active harness supplies model availability, agent roles, tool bindings, and
delegation policy. Add a routing recommendation only when requested or materially
useful under that policy. This template neither selects a model family nor
requires a board, scheduler, external provider, PR stack, or commit per step.

Modified by Rogemar Agent Toolkit on 2026-09-07 for portable, proportionate planning.
