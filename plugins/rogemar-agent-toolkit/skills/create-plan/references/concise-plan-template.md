# Concise Plan Template

Use this template for one clear, low-risk change. Do not use it for a migration,
security/privacy/authorization change, broad refactor, compatibility work, or
multiple materially different increments.

```markdown
# Plan: <short outcome>

**Status:** Draft

<One to three sentences describing the desired outcome, the repository-grounded
approach, and why this is the smallest safe change.>

## Scope

- **In:** <behaviour, modules, or surfaces included>
- **Out:** <explicit exclusions and adjacent work not being changed>

## Existing context

| Area | Existing pattern or source | How this plan uses it |
| --- | --- | --- |
| <area> | <path, test, or documented contract> | <reuse or preserve> |

## Implementation steps

1. [ ] <Verb-first, concrete discovery or preparation step.>
2. [ ] <Smallest coherent code/configuration/data change and likely path.>
3. [ ] <Update affected tests, types, documentation, or fixtures.>
4. [ ] <Run focused validation.>
5. [ ] <Check the named edge case, failure state, or rollback condition.>

## Acceptance and validation

| Acceptance criterion | Proof | Failure or edge case |
| --- | --- | --- |
| <observable result> | <test, check, or manual smoke> | <negative case> |

## Capability handoff

- **Next entry:** <direct implementation, `goalbuddy:goal-prep`, or
  `deliver-approved-programme`>
- **Applicable specialists:** <smallest justified set, or `None`>
- **Activation reason:** <affected surface or evidence need>
- **Live capability route (when material):** <need; preferred plugin, MCP,
  connector, app, CLI, or local tool; observed availability; smallest installed
  fallback; and authorization still needed, or `None`>

Include model routing below only when the user requests it or the plan has
multiple increments or materially different risk.

### Model routing (when applicable)

| Recommended available model and reasoning | Why this is sufficient | Required validation | Escalate if |
| --- | --- | --- | --- |
| <model and reasoning> | <scope, pattern, and risk rationale> | <focused checks> | <evidence that requires more reasoning or a stronger model> |

## Risks and rollback

- **Risk:** <material risk, or `No material risk beyond normal regression`>
- **Rollback:** <revert, flag/capability action, or `Revert the isolated change`>

## Open questions

- <Only a blocking or material unknown; omit this section when none exist.>
```

Minimum quality: name the affected scope, preserve nearby contracts, state a
testable result, and avoid a vague checklist.
