---
name: workflow-orchestrator
description: Use for non-trivial coding work that spans brainstorming, research, planning, UX or system design, implementation, debugging, review, testing, release, or monitoring and needs the smallest effective capability set, explicit handoffs, risk-based validation, and honest evidence reporting.
---

# Workflow Orchestrator

Only when a Codex, Cursor or Universal Forge route is active, follow the shared [Forge mode and status contract](references/forge-mode-status.md) at entry,
resume and dispatch: explicit request → task mode → saved preference; ask once
if none exists. Show role, model, effort, mode and evidence status without
repeated introductions. Setup inspection alone does not require a mode choice
or write preferences; apply the prompt when beginning a Forge execution task.
Generic/core-only workflows do not prompt for a Forge mode or emit Forge labels.


Coordinate a coding task across its lifecycle without duplicating specialist
skills. Use this skill to decide what kind of work is needed, what evidence is
required, which installed capabilities apply, and when the task should pause.

## Automatic Codex Forge dispatch

When Codex Forge is active, automatically use the installed `plan-model-router` for
EVERY justified new worker assignment. Follow its
`plan-model-router/references/dispatch-contract.md` contract:
read saved preferences and current runtime capabilities, select the task role,
run the resolver, and copy its qualified model/effort into the actual native
spawn arguments. Do not stop at a mapping table or recommendation. Re-resolve
after mode changes; a changed profile requires a fresh compatible assignment.

Peak, Balanced, Lean, and Sprint share one executable catalogue owned by the
router. Old names remain compatibility aliases. Named modes supersede inherited
parent defaults for workers; the no-mode route retains parent ceilings.
Main-owned coordination and integration remain with the current main agent.
A desired parent profile is advisory unless a supported live control applies it.
Never recursively activate Forge or start a second coordinator when one is active.

## Cursor Forge dispatch

Cursor Forge uses `cursor-forge-setup` as the primary role/profile resolver.
Read its saved native mappings, qualify task fit and pins, then apply exact
supported settings to the native worker call. The universal router is fallback
only for unavailable adapter/mappings; it cannot bypass owner limits, rejected
configuration or required evidence. Keep this same orchestrator as sole dispatcher.

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

## Shared methods and native harness bindings

Use the shared `engineering-playbooks` method for substantive engineering work when installed. In Codex, prefer the complete installed `codex-forge` implementation of that method. In Cursor, prefer installed `cursor-forge`, otherwise native PStack with reconciled dispatch ownership. Elsewhere prefer `universal-forge` with `universal-plan-model-router`, falling back to the shared method if absent. Honor an explicit compatible entry choice and a declared `Harness: <name>`; a name does not prove live capabilities. Other harnesses use their own exposed models and tools. Select one execution owner; do not run the native and portable workflows twice.

This orchestrator alone dispatches specialists and workers. Each playbook supplies methods and bounded hints. For Codex workers, use installed `plan-model-router` at materially different packages or dispatch boundaries, preserving its runtime contract: selected Forge modes supersede default parent ceilings; the no-mode route retains them. Other harnesses use their actual model controls and inherit the parent when controls or identity are unavailable. Never import Codex or Cursor model names into another harness or invent a selector. Record requested and observed profiles only when delegation is material; unavailable identity remains Unverified.

`create-plan` owns planning. `code-review-and-quality` owns the independent review and may request focused `code-review-tests` evidence. CodeRabbit and harness-native reviewers are separate evidence providers; consolidate findings by root cause without relabeling their verdicts. They are required only when the approved acceptance contract requires them.
When CodeRabbit is selected, invoke its own installed skill for a full review of
the agreed candidate. Keep its procedure and verdict independent; do not replace
it with a shortened shared review or a sample of the diff. See
[provider routing](references/provider-routing.md) for overlapping installations.

When Integrated Workflow is installed and owns an active ready-PR cloud review
wave, carry existing per-provider counts, candidate coverage and pending states
through handoffs. Follow [delivery review routing](references/provider-routing.md#delivery-review-cadence)
before consolidating, validating cloud findings or dispatching cloud-review fixes;
do not create a second review loop. Selected local providers retain full agreed
coverage and local reconciliation at the existing cadence. Outside that lifecycle, retain the task's
own acceptance requirements rather than mandating both cloud providers.

For a programme, use `integrated-workflow` if installed; otherwise preserve the approved plan and gates directly. Missing optional packs do not block adequate in-scope work. Keep trivial direct work proportional.

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
  the active harness environment. Installed marketplace plugins participate like
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

For every justified new sub-agent, in default operation or any Forge route,
follow [sub-agent naming](references/subagent-naming.md) after native profile
qualification: role, task, model and native reasoning in the supported naming
field, or the ordinary handoff when unavailable; keep mode in status and receipts.

The main agent owns the goal, final decisions, synthesis, and validation. This
skill owns delegation policy and should be the only orchestration layer that
decides whether a worker is needed.

The current main agent performs the orchestrator role and remains an
implementation-capable owner of integration, synthesis and final validation.
This skill has no separate default AI model and does not spawn a coordinator.
The selected harness's Forge adapter and router qualify worker profiles; any
requested parent-model change requires supported controls and verified effect.

Before delegating, decide whether a fresh context materially earns its cost.
Delegate only when independent investigation, a bounded specialist lens, an
independent counterexample, or a safely partitioned package will improve the
outcome more than its coordination, context, and validation cost. Keep
synthesis, requirements, integration, and final judgment with the main agent.

For large outputs, repeated reads or long handoffs, apply
[context efficiency](references/context-efficiency.md). Preserve decisive evidence
and freshness while reducing repeated work; do not add another acceptance cycle.

Choose a surfaced custom-agent type for its behavioral and permission contract,
not as a permanent model assignment. Role intent may be explorer, investigator,
implementation worker, debugger, reviewer, architect, or bounded experiment
worker; the main agent normally synthesizes. Use the role guidance in
the active harness's profile controls when a profile is needed; Codex uses installed `plan-model-router`.

- Delegate safe, independent, read-heavy work when authorized and useful.
  Delegated writes require existing user-authorized execution and a bounded
  worker scope; approval of a planning-only artifact does not authorize writes.
- The main agent may delegate only authority already granted by the user.
  External actions, destructive operations and shared-state writes retain their
  applicable user authorization; a worker assignment cannot expand it.
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
- In a shared worktree, serialize writers, including the main agent. Parallel
  implementation uses separate worktrees with explicit ownership; separation
  does not isolate shared databases, generated outputs or runtime resources.
  Preserve unrelated work in every lane. Report conflicts rather than reverting
  others' edits. The main agent inspects and reconciles the combined diff and
  performs or directs final integrated validation.
- Capture the parent model and reasoning effort before spawning. In a named
  Forge mode, qualify the worker against its pool and the backend; it may exceed
  parent defaults. Without a mode, enforce both parent ceilings.
- Treat a role's stated model or effort as a desired profile, never a bypass of
  mode membership or an applicable legacy parent ceiling. Record requested and observed profiles. Requalify a sufficient permitted
  profile or report the constraint; never silently clamp or drop overrides.
- Without a named mode, if a worker needs more capability than the parent ceiling permits, mark the
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

## Automatic execution strategy

Default to `AGILE_FOCUSED`. At a new implementation package or a material change
in dependencies, scope or available isolation, assess the actual repository and
approved authority; do not continuously poll or create a detector/scoring system.
Explicit user strategy, one-writer limits and repository restrictions take precedence.

Select `AGILE_CONTROLLED_PARALLEL` automatically only when delegation is already
permitted, independent packages have exact owners/files or symbols, separate
branches/worktrees are available, and parallel work is likely to justify its
coordination and integration cost. Check shared contracts, dependency ordering,
generated outputs, databases and runtime resources; different filenames alone
are insufficient. Assign acceptance checks, stop conditions and the main-agent
integration owner before dispatch. Selection grants no additional authority.

If evidence is insufficient or isolation unavailable, continue focused; useful
read-only investigation/review may still run concurrently. Briefly record the
chosen strategy and reason in the existing receipt, without a new board or a
routine owner confirmation. Ask only when a material scope/authority decision is
missing and cannot be resolved within the approved task.

If overlap or a shared dependency emerges, pause affected writers at a safe
checkpoint, retain their edits and receipts, reconcile ownership and continue
those packages sequentially. Keep unaffected lanes running only while their
independence remains established. Do not reset, discard work or switch strategy
merely because a task is taking longer than expected. Reassess parallel eligibility
when the dependency is resolved; validate the final integrated candidate.

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

Use `create-plan` for the plan artifact. In Codex, use installed `plan-model-router` only for
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
- `code-review-and-quality` for diff or pull-request review; add `code-review-tests` only for focused test evidence.
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

- Observed parent profile, selected mode, and applicable limits.
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
