---
name: workflow-orchestrator
description: Use for non-trivial coding work that spans brainstorming, research, planning, UX or system design, implementation, debugging, review, testing, release, or monitoring and needs the smallest effective capability set, explicit handoffs, risk-based validation, and honest evidence reporting.
---

# Workflow Orchestrator

Coordinate a coding task across its lifecycle without duplicating specialist
skills. Use this skill to decide what kind of work is needed, what evidence is
required, which installed capabilities apply, and when the task should pause.

## Core routing

1. Classify the request as answering, research, brainstorming, planning,
   design, implementation, diagnosis, review, release, or monitoring.
2. Inspect repository instructions, current state, relevant files, constraints,
   and available tools before making repository-specific claims.
3. Identify the affected surfaces and risk lenses: UX, data, authorization,
   privacy, security, compatibility, performance, accessibility, operations,
   or documentation.
4. Select the smallest effective specialist set. Use sub-agents for independent,
   naturally parallel work and for bounded implementation slices when the task,
   approved plan, or Rogemar explicitly authorizes delegation. Do not force the
   main agent to repeat work that an authorized worker can complete safely.
5. Separate facts, assumptions, decisions, open questions, and evidence.

## Capability preflight

For non-trivial work—and always before choosing a manual, CLI, or other
workaround—derive the capabilities needed from the task, repository, affected
surfaces, and risk. Inspect the capability catalog exposed in the current
environment for relevant skills and surfaced plugin, MCP, connector, app, or
tool routes. The user does not need to name ordinary helpful capabilities.

- Discover in layers: inspect skill names and descriptions, expand only the
  relevant members of any namespaced or specialist family, and inspect the
  surfaced live tool/MCP/app/connector registry separately. A live tool may be
  available without a matching skill, while an installed plugin may expose no
  callable tool. Do not load an entire family or activate overlapping routes.
- Limit automatic discovery to capabilities already installed or surfaced in
  the current Codex environment. Installed marketplace plugins participate like
  any other installed plugin; do not search the external marketplace or suggest
  a new installation unless the owner separately asks for that discovery.
- Distinguish installed or advertised from usable. Before relying on a live
  route, verify that its underlying tool is surfaced and, when material,
  enabled and authenticated. A skill or plugin name alone is not proof of
  callable access.
- Choose one primary route and only the fallback needed if that route is
  unavailable, unsuitable, or outside the approved evidence boundary. Do not
  run a fallback alongside a healthy primary unless independent evidence is
  required or the owner asks for both.
- Discovery does not grant authority. Do not install, enable, authenticate,
  spend credits, access private connector data, expose new files, or perform an
  external mutation unless the task or owner authorizes that action.
- If an installed capability layer cannot be inspected, record that layer as
  Unverified and use the smallest safe repository-local fallback. State the
  resulting evidence limitation instead of implying integration success.

Skip broad capability discovery for a simple known-file task whose existing
local route is sufficient. Re-run the targeted preflight at a phase boundary
when the next phase needs materially different live capabilities.

## Delegation policy

The main agent owns the goal, final decisions, synthesis, and validation. This
skill owns delegation policy and should be the only orchestration layer that
decides whether a worker is needed.

The main agent is also an implementation-capable worker. In the default hybrid
shape, it owns integration-heavy, ambiguous, highest-risk, or shared-surface
implementation while bounded Workers own disjoint packages. Reconciliation is
an additional responsibility, not a supervisor-only restriction.

Before delegating, decide whether a fresh context materially earns its cost.
Delegate only when independent investigation, a bounded specialist lens, an
independent counterexample, or a safely partitioned package will improve the
outcome more than its coordination, context, and validation cost. Keep
synthesis, requirements, integration, and final judgment with the main agent.

Choose a surfaced custom-agent type for its behavioral and permission contract,
not as a permanent model assignment. Role intent may be explorer, investigator,
implementation worker, debugger, reviewer, architect, or bounded experiment
worker; the main agent normally synthesizes. Use the role guidance in
`plan-model-router` when a profile is needed.

- Automatically delegate safe, independent, read-heavy work when it justifies
  its overhead. Treat an approved plan or explicit user instruction to use
  workers for implementation as authorization for bounded project-local writes.
- Require main-agent or user authorization for implementation, external
  actions, destructive operations, and shared-state writes. Authorization does
  not expand the worker's assigned scope or permit irreversible actions.
- Limit default concurrency to three workers and nested delegation to one
  level. Use zero workers for trivial or serial work, one for one independent
  stream, and two or three only for proven-disjoint evidence or write scopes.
- Give each worker one bounded role, one owned surface or file set, explicit
  non-goals, acceptance criteria, required verification, stop conditions, and a
  structured evidence contract. Include `allowed_files` (or an equivalent
  exact scope) for write workers.
- Keep discovery workers read-only by default, but allow authorized workers to
  implement, edit, test, document, or run scoped validation. Isolate writers,
  permit sequential workers when dependencies require them, and never allow
  multiple workers to edit the same file or surface concurrently.
- Workers share the worktree: preserve unrelated dirty or untracked work, do
  not revert another worker's changes, and report conflicts or out-of-scope
  findings instead of guessing. The main agent must inspect the resulting diff,
  reconcile it with the approved plan, and perform or direct final validation.
- Capture the parent model and reasoning effort before spawning. No worker may
  use a stronger model or higher reasoning effort than the parent.
- Treat a role's stated model or effort as a desired profile, never a bypass of
  either parent ceiling. Record the requested and effective profile; clamp to
  the strongest permitted profile or mark the work `ceiling-constrained`.
- If a worker needs more capability than the parent ceiling permits, mark the
  handoff `ceiling-constrained` and return the unresolved work to the main
  agent or Rogemar.
- If worker model or effort cannot be verified, report it as Unverified and do
  not claim the ceiling was enforced.
- Gather concise worker receipts rather than raw intermediate output. Preserve
  independent evidence long enough for reconciliation, then make one main-agent
  decision against the actual diff and validation.

Specialist skills may declare delegation hints, recommended roles, evidence,
and escalation conditions. They must not create unrestricted or recursive
spawning rules.

Use [skill-collaboration.md](references/skill-collaboration.md) as the shared
contract for specialist-to-orchestrator handoffs. A specialist skill may
describe a collaboration hint using that contract, but the hint is advisory;
the orchestrator decides whether and when to activate it.

For work that moves through planning, GoalBuddy preparation, implementation,
and pull-request delivery, read
[stage-routing.md](references/stage-routing.md). The user should normally need
only the entry skill for the current stage; specialists remain independently
invocable and are activated only when their evidence or implementation surface
is actually present.

Do not assume a language, framework, database, hosting provider, deployment
system, test runner, or integration. Derive those from the repository or the
user's explicit constraints.

## Lifecycle

### 1. Discover and define

Record:

- User goal, audience, and desired outcome.
- In scope, out of scope, constraints, and success criteria.
- Relevant evidence and source boundary.
- Locked decisions, assumptions, and open decisions.

If an unresolved decision would materially change the implementation, pause and
ask one focused question or produce bounded options.

### 2. Design the contract

As applicable, define:

- User journey and complete state set: initial, loading, empty, success, error,
  retry, disabled, permission-denied, offline, and destructive states.
- Public interfaces, data ownership, authorization, validation, and error
  behavior.
- Compatibility with existing inputs, persisted data, APIs, and clients.
- Accessibility, privacy, performance, observability, and rollback needs.

Use `create-plan` for the plan artifact. Use `plan-model-router` only for
multi-PR, sprint, phased, materially mixed-risk work, or an explicit routing
request. Planning remains read-only.

### 3. Implement in increments

Use `first-time-right-delivery` for non-trivial implementation. Preserve
repository-native abstractions and keep each increment small enough to verify.
Use the relevant specialist skills for the actual repository technology or
domain, rather than adding generic stack assumptions here. After the plan is
approved, assign each increment to the main agent or an authorized worker with
an explicit scope. Sequence dependent increments and parallelize only disjoint
ones; do not duplicate implementation that an assigned worker is completing.

### 4. Verify with risk-based evidence

Use the cheapest check that can fail for the right reason. Route to:

- `bug-triage` for ranked hypotheses and reproduction.
- `code-review-tests` for diff or pull-request review.
- `test-architecture-engineer` when deciding sufficient test layers.
- `accessibility-auditor`, `visual-qa`, or `performance-profiler` when those
  risks are applicable.
- `privacy-safety-review` or `security-best-practices` for relevant sensitive
  behavior.

Include positive and negative cases as applicable: malformed, unauthorized,
legacy, duplicate, concurrent, offline, disabled, private, boundary, and
rollback inputs. Do not treat automated checks as proof of manual or device QA.

### 5. Release and operate

Use `deploy-checklist` and any target-specific release skill only when release
is in scope. Confirm:

- Validation against the actual final diff or commit.
- Migration, compatibility, rollout, and rollback posture.
- Environment and secret requirements without exposing values.
- Monitoring, alerts, support, and post-release checks.
- Local, CI, staging, production, simulator, device, and deferred evidence as
  separate statuses.

Do not claim deployment, CI, monitoring, or external-tool success unless it was
actually observed.

## Handoff contract

Every phase handoff should carry:

- Goal and user behavior.
- Evidence and source boundary.
- Decisions, invariants, and non-goals.
- Affected surfaces and dependencies.
- Acceptance criteria and required validation.
- Risks, rollback or disable path, and unresolved questions.
- Next action and owner or responsible capability.
- Required capability, preferred route, observed availability, fallback, and
  any authorization still needed when a live integration affects the next
  phase.

Every worker handoff must additionally carry:

- Parent model and reasoning ceilings.
- Assigned model and reasoning effort.
- Permissions, tools, isolation, and budget.
- Owned files or surfaces and explicit non-goals.
- Required output, evidence, stop conditions, and escalation triggers.

## Output

Lead with the current recommendation or result. Keep the response proportional
to the task. Use these evidence statuses:

- **Verified:** directly observed through the named check or source.
- **Partial:** some required evidence exists, but coverage is incomplete.
- **Unverified:** a recommendation or inference without direct proof.
- **Blocked:** progress depends on a failed or unavailable prerequisite.
- **Deferred:** intentionally left for a later environment or manual check.

Never invent quality scores, progress percentages, costs, timelines,
performance results, test results, CI status, deployment status, or tool access.
