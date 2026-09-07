# Cursor configuration and dispatch contract

## Configuration

Our file is `~/.cursor/cursor-forge.json`, separate from PStack rules and caches.
Use schema version 1 with `active_mode`, `modes` and optional `parent_profiles`.
Each mode contains `groups` and `roles`. Group entries provide defaults; role
entries override a group. Each entry has an ordered `profiles` list of objects
with `model` (exact verified native ID) and `settings` (only fields supported
by the current Cursor tool), plus optional `skills` listing existing skill IDs.
Native defaults can be represented by `inherit: true` instead of `model` and
`settings`; reject contradictory entries. Such inheritance is not evidence
that a requested model or cost preference was enforced.

Validate version, mode names, role/group IDs, setting types, nonempty candidate
lists for configured entries, inheritance exclusivity, and skill ID strings.
Reject unknown fields; preserve unrelated valid modes and settings. Validate
real profiles against the current tool catalogue before saving. Record source
and observation time separately in the setup receipt, not as assumed perpetual
availability. Never overwrite malformed or concurrently changed configuration.
Missing entries are unconfigured rather than implicit permission to use any ID.

The role inventory is model-free. Populate native mappings in Cursor by
qualifying actual available models, using these mode preferences:

| Mode | Native mapping preference |
| --- | --- |
| Peak | Strongest suitable permitted profiles for demanding work |
| Balanced | Strong judgment when needed; efficient bounded execution |
| Lean | Lower-cost sufficient choices where evidenced; selective escalation |
| Sprint | Fast narrow work and minimal coordination |

No portable mode establishes a cross-provider ranking or exact prices. Use
current evidence or disclose heuristic choices. Mode intent never weakens
acceptance requirements. Owner-specified pools and limits remain binding.

## Resolve before dispatch

1. Read the complete configuration. An explicit task mode overrides active_mode
   without persisting it; default to Balanced as a stated task preference only
   when no saved mode or owner choice exists.
2. Select a role for the actual task. Resolve mode → group default → role
   override. Explicit task adaptations require a reason and must remain inside
   owner restrictions; do not silently replace a configured profile.
3. Inspect native role model/settings pins, tool access, scope and independent
   context support. Qualify the exact effective profile and task evidence.
   Required native GoalBuddy contracts cannot be relabeled to escape pins.
4. Return the selected mode, role, source (Cursor mapping or fallback), model,
   supported settings, selected skills, task-fit reason and verification needs.
   The existing orchestrator copies the qualified arguments into the actual
   native worker tool. Do not hard-code another harness's argument names.
5. Keep proposed/requested/accepted/runtime-observed profiles distinct. Record
   missing model identity as Unverified. A configured mapping is not a live test.
   Reuse existing workers only when their verified contract still fits.

Main-owned coordinator/integration roles stay with the parent. Skill hints do
not grant tools or write permissions. Preserve the shared Universal Forge role
contracts for design, QA surfaces, review independence, optional Ponytail/Dream
Team and opt-in learning/recurring monitoring. Panel count is chosen by useful
independent work, not by the number of candidate models.

Fallback applies to absent adapter/configuration/role mappings or genuinely
unavailable optional capabilities, not to validation rejection or permission
failure. Carry all explicit constraints into universal-plan-model-router. If a
required restriction cannot be honored, block only the dependent assignment.

This is a native host-executed procedure, not an API client. Do not claim that
writing this file changes the parent, launches a worker or enforces runtime
behavior without an actual supported call and evidence.
