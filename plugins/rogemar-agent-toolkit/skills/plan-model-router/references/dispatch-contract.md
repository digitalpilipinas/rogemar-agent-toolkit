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
   For an explicit no-mode choice, use a request-local validated preference copy
   with `active_mode: null` and `parent_policy: suggest-at-phase-boundaries`;
   never let the saved active mode reappear through resolver fallback or write
   this temporary choice to disk.
   Read `${CODEX_HOME:-$HOME/.codex}/forge.json` if present. Pass its complete
   validated object as `preferences`; do not reconstruct it from a remembered
   mode. A task-only `mode` overrides the saved mode without writing it. Re-read
   before new assignments after a switch. Keep aliases supreme → peak,
   optimize → balanced, budget → lean readable; authorized writes canonicalize.
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
   Without a named mode, use qualified candidates or exact parent inheritance.
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
   Before the native call, construct `task_name` from the qualified assignment
   using the installed orchestrator's `references/subagent-naming.md`. Keep mode
   out of the name and retain exact model IDs in arguments and receipts.
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

`parent-coordinator`, `workflow-coordinator`, and `integration-owner` are
main-owned. Resolve them with `target: parent` for a desired profile only.
`runtime_switch_performed: false` remains true until a separate supported
current-task control is used and its outcome verified. Do not use a follow-up
message, global configuration edit, or worker spawn to simulate that control.

## Preference operations

Setup uses `--set-mode MODE --preferences FILE` for an explicitly requested
saved switch. The helper validates first, backs up bytes, preserves role
preferences, atomically writes schema version 2, and verifies readback. A bare
setup inspection preserves the current mode. `--validate-preferences FILE`
checks structure only. Availability and actual dispatch require separate proof.

Schema example (model choices still require current runtime checks):

```json
{"schema_version":2,"policy":"adaptive","parent_policy":"mode-adaptive",
 "active_mode":"balanced","roles":{}}
```

No active mode uses `active_mode: null` and
`parent_policy: "suggest-at-phase-boundaries"`. Version 1 files remain readable.
Role preferences use `preferred_models` and optional normalized `effort_hint`.
`inherit-parent`/`auto` inherit both settings and cannot accompany an effort hint.
