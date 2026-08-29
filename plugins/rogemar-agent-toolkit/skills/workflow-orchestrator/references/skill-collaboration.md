# Specialist skill collaboration contract

This contract defines how a specialist skill recommends collaboration to
`workflow-orchestrator`. It does not give a specialist permission to invoke
another skill, spawn a worker, change model ceilings, or make final readiness
claims.

## Collaboration hint

Each optional hint should provide:

- `use_when`: the task shape and evidence conditions that justify collaboration.
- `role`: the specialist or bounded worker role being recommended.
- `preferred_agent_type`: a surfaced custom-agent type when one is useful, or
  `None`. This is a behavior and permission preference, not authority to create
  or configure an agent.
- `desired_profile`: the role's lowest useful model and effort shape when a
  profile matters, or `None` for ordinary local work.
- `effective_profile_evidence`: the observed runtime availability plus the
  parent-ceiling result. Record `ceiling-constrained` or `Unverified` rather
  than implying a desired profile was used.
- `inputs`: the minimum context, files, artifacts, or prior findings required.
- `required_capabilities`: the capability need, not an exhaustive tool list.
- `preferred_route`: the selected skill plus its underlying plugin, MCP,
  connector, app, CLI, or local tool when one is required.
- `fallback_route`: the smallest safe alternative if the preferred route is
  unavailable or unsuitable.
- `availability_evidence`: what was actually observed about surfacing,
  enablement, authentication, or the absence of a discovery mechanism.
- `owned_scope`: the exact behavior, surface, hypothesis, or evidence stream.
- `non_goals`: what the collaborator must not redesign, edit, or decide.
- `permissions`: read-only, isolated write, tool, connector, and external-action limits.
- `expected_evidence`: files, lines, sources, measurements, screenshots, tests, or reproduction steps.
- `output_format`: the concise result and status fields returned to the orchestrator.
- `independence_requirement`: why a fresh context is worth its coordination
  cost, or why the work should remain with the main agent.
- `synthesis_owner`: normally the main agent; name another owner only when the
  task explicitly assigns one.
- `escalation_condition`: evidence that returns the work to the main agent or Rogemar.

## Ownership and sequencing

1. `AGENTS.md` directs non-trivial work to `workflow-orchestrator`.
2. The orchestrator classifies the lifecycle phase, affected surfaces, and risks.
3. The orchestrator selects applicable specialist skills.
4. Specialist skills run sequentially when they require shared context.
5. The orchestrator may run independent evidence streams in parallel and may
   assign bounded implementation packages when the task, approved plan, or
   owner authorizes project-local writes. Concurrent writers require
   proven-disjoint scopes and isolated worktrees.
6. The main agent reconciles findings and Worker diffs and owns the final
   decision and integrated validation.

Specialist skills should not invoke one another directly. A specialist may
recommend a follow-up skill or worker by returning a collaboration hint, but
the orchestrator remains responsible for ordering, deduplication, permissions,
budgets, model ceilings, and reconciliation.

A role profile is a desired routing input, not a fixed override. The
orchestrator selects a surfaced agent type, then `plan-model-router` computes
an effective profile no stronger than the parent model or effort. If that
profile cannot meet the evidence burden, the work returns to the main agent.

A capability hint is not permission to install, authenticate, spend credits,
read private connector data, expose additional files, or mutate an external
system. The orchestrator must confirm that authority separately.

## Worker result

Every delegated result should state:

- Status: Verified, Partial, Unverified, Blocked, or Deferred.
- Findings and evidence within the assigned scope.
- Files, surfaces, sources, or measurements inspected.
- Checks performed and their actual results.
- Assumptions, conflicts, and remaining risks.
- Recommendation and the next owner.

Workers must not claim overall readiness, authorize release, expand scope, or
silently continue after a ceiling, permission, or evidence boundary is hit.
