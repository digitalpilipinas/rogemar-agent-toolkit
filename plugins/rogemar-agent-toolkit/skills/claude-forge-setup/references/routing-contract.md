# Claude configuration and dispatch contract

## Configuration

Our file is `~/.claude/claude-forge.json`. Leave Claude settings, permissions,
hooks, and `CLAUDE.md` alone unless the task explicitly edits that file.

Use schema version 1 with `active_mode`, `modes`, and optional `parent_profiles`.
Each mode contains `groups` and `roles`. Group entries provide defaults. Role
entries override a group. Each entry has an ordered `profiles` list of objects
with `model` set to an exact native ID confirmed in this session, and `settings`
limited to fields the current Claude worker tool accepts. Optional `skills`
lists skill IDs that are already installed. Native inheritance is `inherit: true`
instead of `model` and `settings`. Reject an entry that sets both.

Validate version, mode names, role and group IDs, setting types, nonempty
candidate lists, inheritance exclusivity, and skill ID strings. Reject unknown
fields. Preserve unrelated valid modes. Validate profiles against the current
tool catalogue before saving. Record the catalogue source and observation time
in the setup receipt, not as a permanent availability claim. Never overwrite a
malformed or concurrently changed file. A missing entry is unconfigured. It is
not permission to use any ID.

The role inventory is model-free. Populate mappings by qualifying models that
are actually available.

| Mode | Native mapping preference |
| --- | --- |
| Peak | Strongest suitable permitted profile for demanding work |
| Balanced | Strong judgment when the task needs it, and a cheaper profile for bounded execution |
| Lean | A lower-cost profile where the task evidence supports it, with room to escalate |
| Sprint | Fast narrow work and little coordination |

No mode establishes a cross-provider ranking or a price. Owner-specified pools
and limits remain binding. Mode intent does not weaken acceptance.

## Resolve before dispatch

1. Read the whole configuration. Apply explicit request, then the established
   task mode, then saved `active_mode`. Ask once when none exists. Do not
   silently select Balanced.
2. Select a role for the actual task. Resolve mode, then group default, then
   role override. An explicit task adaptation needs a reason and must stay
   inside owner restrictions.
3. Inspect native pins, tool access, scope, and whether the worker gets an
   independent context. Qualify the exact profile.
4. Return mode, role, source, model, supported settings, selected skills,
   task-fit reason, and verification needs to the orchestrator. The orchestrator
   copies those arguments into the live Claude worker tool. Do not reuse Codex
   or Cursor argument names. Then apply shared
   [sub-agent naming](../../workflow-orchestrator/references/subagent-naming.md)
   through a naming field the tool actually has.
5. Keep proposed, requested, accepted, and runtime-observed profiles distinct.
   A saved mapping is not a live test.

Main-owned coordinator and integration roles stay with the parent. Skill hints
do not grant tools. Panel size follows useful independent questions, not the
number of configured models.

Fallback applies when the adapter, configuration, or role mapping is absent, or
when an optional capability is genuinely unavailable. It does not apply to a
validation rejection or a missing permission. Carry explicit constraints into
`universal-plan-model-router`. If a required restriction cannot be honored,
block only the dependent assignment.

This procedure runs in the host session. Writing the JSON file does not launch
a worker or switch the parent.
