# Forge resolution and native dispatch

This is the shared contract for Forge, setup, and workflow-orchestrator.
The router computes a profile; the orchestrator performs the native tool call.

1. Decide whether independent work is useful and authorized. Keep zero workers
   for serial or simple work. Identify the smallest bounded role, skill hints,
   exact scope, permissions, acceptance evidence, and stop condition. Read only
   relevant installed skills. A hint is neither tool availability nor permission.
2. Resolve task mode and status using `references/forge-mode-status.md`
   from the installed `workflow-orchestrator` skill.
   Pass the established task mode as explicit `mode` on every resolver request
   so saved preferences cannot override it on later assignments. When mode is
   pending, continue direct work and do not dispatch mode-dependent workers.
   For an explicit no-mode choice, pass `mode: null`; it overrides saved
   preferences without writing them. Never let a saved mode reappear on resume.
   Read `${CODEX_HOME:-$HOME/.codex}/forge.json` if present. Pass its complete
   validated object as `preferences`; do not reconstruct it from a remembered
   mode. A task-only `mode` overrides the saved mode without writing it. Re-read
   before new assignments after a switch. Keep aliases supreme → peak,
   optimize → balanced, budget → lean, sprint → economy readable; authorized writes canonicalize.
3. Observe the active parent model/effort and current native dispatch catalogue.
   Pass `parent: {model, effort}`, `catalog: [{model, efforts}]`, `role`, and a
   concrete `task_reason`. Inspect the selected native agent's fixed settings
   and pass them as `role_config: {model, effort}` when present. Do not use a
   different backend's catalogue or infer runtime identity from global defaults.
4. Run `python3 <router-skill>/scripts/resolve_profile.py REQUEST.json` (or JSON
   through stdin). The request contains the saved preferences above. With a
   named mode, omit `candidates` to use group → role override → saved role
   preferences. Explicit candidates require task-fit reasons and undergo the
   same checks. Apply separately requested user limits before proposing them.
   Without a named mode, declared roles and implementation/consequential work still
   require qualified candidates, exact parent inheritance or a compatible mandatory
   native pin in the parent family. Legacy role-less, unflagged assessments may
   propose an alternate within both ceilings, labeled `alternate-profile-provisional`;
   they do not qualify that profile for a Forge role or implementation contract.
5. Dispatch only authorized independent assignments with `status: ready`,
   `target: worker`. A ready resolver result does not waive explicit user or host
   hard limits: check both model and effort against them before dispatch, even
   in a named mode. If incompatible, requalify within those limits or retain the
   work with the main agent. `target: parent` is proposal-only and must never
   be submitted to `spawn_agent`. Inspect the live dispatch schema before
   applying overrides; model/effort controls differ across Codex runtimes.
   When `collaboration.spawn_agent` exposes both `model` and `reasoning_effort`,
   copy the corresponding `requested` values exactly into those arguments.
   Use only supported `fork_turns` values; full-history forks may forbid
   overrides. Otherwise use an observed supported profile-selection control
   and verify its effect. If none can apply the qualified profile, mark it
   unapplied and retain the work with the main agent; never send unsupported
   fields or silently substitute inheritance for a nonempty request. Include
   the role's bounded task contract in `message`. For `requested: {}`, omit
   both overrides and use a confirmed compatible inheritance path. Do not
   submit a role ID or the string `auto` as a model ID.
6. A blocked resolution is not a license to drop the arguments or silently
   inherit an excluded profile. Requalify an available permitted profile, retain
   direct work with the main agent while disclosing its mode status, or report
   the missing capability. Do not weaken acceptance requirements. Mandatory
   native contracts (such as GoalBuddy) cannot be replaced just to evade pins.
7. Record mode, role, reason, requested and expected profile, tool acceptance,
   and observed runtime profile. Accepted spawn and worker self-report do not
   prove the effective model. Use authoritative runtime metadata when exposed;
   otherwise label it Unverified. Reconcile the worker's evidence with the
   actual result before main-agent acceptance.

A mode change affects future assignments. Reuse an existing worker only when
its verified profile and contract still fit; otherwise create a fresh bounded
assignment after resolving again. Do not claim an existing worker changed.

Before mode-dependent execution, follow the installed `workflow-orchestrator`
shared Forge mode/status contract's parent clarification: compare desired and
observed profiles, obtain a task-local fallback or manual-switch choice for a
mismatch, and preserve an already accepted choice while those profiles match.

`parent-coordinator`, `workflow-coordinator`, and `integration-owner` are
main-owned. Resolve them with `target: parent` for a desired profile only.
`runtime_switch_performed: false` remains true until a separate supported
current-task control is used and its outcome verified. Do not use a follow-up
message, global configuration edit, or worker spawn to simulate that control.

## Preference operations

Setup uses `--set-mode MODE --preferences FILE` for an explicitly requested
saved switch. The helper validates first, backs up bytes, preserves role
preferences, atomically writes schema version 3, and verifies readback. A bare
setup inspection preserves the current mode. `--validate-preferences FILE`
checks structure only. Availability and actual dispatch require separate proof.

Schema example (model choices still require current runtime checks):

```json
{"schema_version":3,"policy":"adaptive","parent_policy":"mode-adaptive",
 "active_mode":"balanced","roles":{},"default_profile":null}
```

No active mode uses `active_mode: null` and
`parent_policy: "suggest-at-phase-boundaries"`. Version 1/2 files remain readable.
Role preferences use `preferred_models` and optional normalized `effort_hint`.
`inherit-parent`/`auto` inherit both settings and cannot accompany an effort hint.

## Five-mode qualification fields

Use the current request schema in [runtime-routing.md](runtime-routing.md).
Pass the actual parent, observed catalogue, mode, role and task-fit reason.
If the resolver returns `parent-choice-required`, carry the existing bound choice
or obtain it once; never fabricate acceptance. Only `ready` worker results dispatch.

For Default, supply the exact task/saved `default_profile`. For ordinary Scout/Judge
use the returned unpinned read-only `dispatch_agent_type`; required GoalBuddy roles
must set `goalbuddy_required: true` and supply observed pins as `role_config`.

An exception needs `difficult_task: true`, `exception_evidence_id`, the matching
`evidence_contract` and a concrete `exception_reason`, all matching the catalogue’s
verified role/profile record and the actual task. Alternate code-producing work
also requires matching contract evidence. The dispatcher supplies this field;
never ask the user to memorize fixture IDs or substitute database proof for UI work.
Explicit limits apply even to an exception. Naming a difficult role alone is not
qualification. Include `task_requirements` returned by the router in its handoff.

Normal ceilings may be exceeded only for a practical need: the parent cannot
adequately perform the bounded work, or a higher-profile consultation has a
concrete expected advantage for that work. Identify the unresolved requirement,
capability gap or decision, the consultant's deliverable, and why its expected
quality or avoided rework justifies the extra usage. A higher score, effort
label, role name or available budget alone is not a reason. A clear capability
gap can justify consultation before a failed attempt; do not manufacture retries.

Keep a consultant read-only and narrowly scoped unless implementation is separately
authorized and qualified. The parent retains coordination, integration and final
acceptance. Keep the original playbook/function, independence and evidence needs
in the handoff; calling an assignment a consultation cannot bypass the exact
hard-role exception checks above. Choose the lowest sufficient qualified higher
profile, state the stop condition, verify its effective profile and evaluate its
actual contribution. No automatic Max/Ultra upgrade, parent switch or external
provider selection follows. Default remains exact unless the user changes it.

Follow the orchestrator’s `references/subagent-naming.md` after qualification.
Copy supported model/effort arguments exactly, use a fresh minimal-context worker
when changing profile, then verify native metadata. Preserve required independent
review when no candidate is available. No parent or worker switch is inferred.

Before qualification, set `consequential` for architectural/security decisions
inside other roles and `implementation` for code-producing work. The catalogue
protects consequential and coding defaults even when these flags are omitted.
Check that the actual task matches the qualification packet and executable
contract; another task needs its own evidence. Carry `qualification_id` and
`quality_status` in the receipt. Parent-profile-provisional is a fallback, not
a measured optimum. Cross-family exceptions are permitted only for the two
hard roles with exact paired proof and concrete need; user hard limits still win.

For external-review follow-through, use the orchestrator's
[review support/decision roles](../../workflow-orchestrator/references/provider-routing.md#review-support-and-decision-roles).
`status-monitor` and `findings-consolidator` are read-only preparation roles; attempts
to combine them with `implementation` or `consequential` work are blocked. Route
finding judgment to `correctness-reviewer`, checks to `validation-runner`, minimum
scope to `scope-reviewer`, and accepted code changes to the appropriate coding role.
The catalogue owns preset model separation; preferences and native pins cannot
bypass it. Preserve Default exactness and Economy limits unless explicitly changed.

## Playbook-step qualification before dispatch

Read the selected playbook step before resolving a worker. Identify its actual
function, authority, required tools/surface and observable result. A role name
or a fixture pass alone is not sufficient task fit. Preserve a compact task-fit
reason in the existing handoff; no additional board or reviewer is required.

For `swarm-workers` or `arena-runners`, supply `assignment_role` naming the actual
bounded function (for example `how-explorer`, `refactoring`, or
`correctness-reviewer`). The resolver returns `assignment-required` without it;
this asks the dispatcher to classify discoverable work, not the user to approve.
Alternatively send that role directly with `arrangement: swarm` or `arena`.
Each participant follows its own role policy. Do not copy the swarm profile to
all participants or recursively launch another coordinator.

Set `implementation: true` whenever the assignment produces code, including UI,
motion, performance experiments and arena candidates. Set `consequential: true`
for architectural/security decisions under any role. `how-critics` is always
architectural judgment and cannot opt out. Test strategy, source-weighted
synthesis and minimum viability are analytical decisions, not clerical collection.
Keep simple scripted checks separate from deciding whether their evidence suffices.

Treat historical/paired qualification as limited to its actual supplied contract.
A prose readiness answer does not qualify browser/device operation, rendered
visual judgment or implementation. Required task-fit and live evidence stay
unresolved until inspected; retain direct ordinary work or a suitable qualified
assignment without replacing required independence. Missing evidence is not proof
that a frontier fallback is necessary, nor permission to claim it optimized.
Default still uses the exact user-selected profile; these authority and evidence
requirements apply independently of model selection.

Budget the complete useful job: participants, context, experiments/retries,
consolidation, judgment and main integration. Use measured telemetry when present;
otherwise report cost as unknown. Do not divide multi-focus batch costs into
invented per-role estimates. Limit fan-out and reuse valid evidence before
increasing model effort. No new benchmark or escalation is implied by this check.
