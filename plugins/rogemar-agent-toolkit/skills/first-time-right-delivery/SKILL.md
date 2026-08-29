---
name: first-time-right-delivery
description: Use for planning, building, reviewing, testing, or shipping any non-trivial coding change when the goal is to avoid missed requirements and rework. Applies project-agnostic evidence gates, cross-functional review lenses, negative testing, staged delivery checks, and honest readiness reporting.
---

# First-Time-Right Delivery

Use this skill as a cross-project delivery-quality discipline. Read the target
repository's instructions, product specification, scripts, and CI workflow
before relying on any checklist below. `workflow-orchestrator` alone owns
delegation and writer selection; this skill defines evidence expectations and
must not be interpreted as a main-agent-only writing policy.

## Planning playbook

1. Inspect current branch, diff, nearby implementation, test conventions, CI,
   deployment constraints, and existing work before proposing a change.
2. Separate locked requirements from assumptions and open decisions. Do not
   silently redesign the product to fill a missing fact.
3. Build a requirement-to-evidence matrix: user behaviour, UI/state, authority
   or backend path, data/compatibility, positive proof, negative proof, and
   rollback/disable path.
4. Divide work into independently deployable increments with real dependency
   order. State what blocks each increment.
5. Select only applicable review lenses: strategy/scope, evidence/research,
   UX/accessibility, copy/truthfulness, technical integration, QA, and
   privacy/security.
6. Invoke `plan-model-router` when the plan has multiple PRs, increments or
   implementation phases, materially different risk levels, or an explicit
   model-routing request. Skip routing overhead for routine, single-track
   changes. Treat profiles as advisory and retain validation and independent
   review; reassess if the actual diff materially exceeds the planned scope or
   risk.

## Execution playbook

1. Implement the complete contract across UI, API, persistence, access control,
   cache/offline state, configuration, observability, and tests as applicable.
2. Keep identity, authorization, ownership, entitlements, quotas, and sensitive
   derived state authoritative on the trusted server boundary.
3. Preserve documented compatibility; test legacy/current inputs and make data
   migrations scoped, retry-safe, and reversible or safely disableable.
4. Treat empty, loading, error, retry, offline, disabled, and unavailable states
   as product behaviour, not late polish. Do not fabricate data.
5. Request an independent counterexample review before delivery. Test whether
   malformed, legacy, unauthorized, concurrent, disabled, or private inputs
   violate the intended contract.

## Delivery playbook

1. Run the target repository's relevant lint, type, test, migration, build,
   security, and smoke checks against final content.
2. Reinspect staged files, run whitespace and secret checks, and preserve
   unrelated/local-only work.
3. Commit only when the change is deployable by itself and the user has
   authorized the commit. Include scope, risk/compatibility, validation, and
   deferred QA in the delivery record.
4. Verify the remote commit and CI after an authorized push. Keep local checks,
   CI, staging/production, and physical-device/manual QA distinct in reports.

## Stop conditions

Stop rather than skipping ahead when the requested work lacks a required prior
contract/migration, an unresolved product decision would change scope, or a
required validation proves the current increment unsafe. A user-approved
deferred manual/device check is a recorded deferral, never a pass.

## Delegation boundary

Defer worker selection and permissions to `workflow-orchestrator`. The main
agent may implement directly, and an approved plan or explicit owner
authorization may assign bounded project-local implementation, tests, or
documentation to Workers. Apply this skill's evidence requirements equally to
every writer. Use read-only explorers, counterexample reviewers, or validation
analysts for independent evidence streams; do not turn those reviewer roles
into implicit write permission. Keep concurrent writers on proven-disjoint
scopes and isolated worktrees, and return scope conflicts, ambiguous product
decisions, or ceiling-constrained work to the main agent.
