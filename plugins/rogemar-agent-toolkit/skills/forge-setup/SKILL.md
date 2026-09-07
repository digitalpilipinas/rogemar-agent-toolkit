---
name: forge-setup
description: Configure adaptive per-role Codex model preferences for Forge. Use when setting up Forge, switching Peak, Balanced, Lean, or Sprint modes, changing preferred worker models or reasoning hints, or checking routing readiness. Let a selected mode govern parent and worker profiles; verify actual runtime switches separately.
license: MIT
---
# Set up Forge model preferences

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md).
Route the configuration assessment through `workflow-orchestrator` and read
`plan-model-router/references/runtime-routing.md` for the single shared schema.
Setup writes only the explicitly requested preference file; it does not alter
Codex's main model, global defaults, agent pins, permissions, or integrations.

1. Inspect the current dispatch catalog and supported reasoning levels. Include
   Astra, Sol, Terra, and Luna only when those exact IDs are surfaced. Distinguish
   active parent evidence from configuration defaults. No catalog means keep
   parent inheritance available and report model choices as Unverified.
2. Read `${CODEX_HOME:-$HOME/.codex}/forge.json` if present. Preserve valid
   existing choices. Show missing/retired choices without treating them as
   usable. Never overwrite a malformed file or silently change an owner choice.
3. Read the named modes in `plan-model-router/references/runtime-routing.md`.
   Use `resolve_profile.py --list-modes` for their exact model/effort pools.
   Accept `$forge-setup Use peak`, `Use balanced`, `Use lean`, or
   `Use sprint`. Preserve the active mode if none is selected;
   recommend Balanced for everyday work without silently changing an owner choice.
   Modes supersede parent defaults for future profile assessments; the file write
   alone does not switch the running parent. No
   eligible worker means report the constraint; do not invent an eligible profile. Ultra is outside all
   four presets by the owner's specification. Use only hyphenated role keys.
   Show the executable role mapping with `resolve_profile.py --role-map`,
   including every role across Peak, Balanced, Lean, and Sprint. Read
   `plan-model-router/references/role-mapping.md` for task-fit rules. Distinguish
   these defaults from saved per-role overrides and actual dispatched profiles.
   Offer the available Codex models plus `inherit-parent`/`auto`. Lists are
   candidate pools; they neither pin a role nor create a worker per entry.
   Use group defaults with individual role overrides and justified task adaptations.
   Accept the owner's batch choices rather than requiring a configuration form
   before ordinary programme execution.
4. Validate the version, policy, role keys, model IDs, and effort hints using
   `plan-model-router/scripts/resolve_profile.py --validate-preferences FILE`.
   This validates structure; verify selected real IDs against the live catalog
   separately. Apply the mode pool; retain parent ceilings only on the legacy no-mode route.
5. For a requested mode switch, run the router helper with `--set-mode MODE
   --preferences FILE`. It validates before mutation, backs up prior bytes,
   migrates legacy spaced role keys, atomically writes schema version 2, and
   reads it back. It preserves per-role choices. Old mode names remain aliases (supreme → peak,
   optimize → balanced, budget → lean); authorized writes use canonical names. For other explicitly requested
   preference updates, preserve the same validation/backup/atomic-write contract.
   Version 2 retains policy, parent_policy and roles, and adds active_mode.
   Existing version 1 files remain readable until an authorized write.

6. Read back and validate the file. Report configured preferences separately
   from a verified worker dispatch. Profile changes apply at the next package
   assessment; do not claim existing workers changed models.
7. If the project lacks reusable runtime proof, recommend
   `forge-create-verification-skill` through the orchestrator when useful. This
   is optional and grants no device, service, installation, or publication access.

## Switching verification

Run fixture tests for all four mode transitions, inheritance exclusions,
unknown metadata, pinned profiles, and mode precedence and legacy parent ceilings. When live
worker tests are requested, assign a useful bounded read-only task to permitted
profiles through the orchestrator, keeping requested and runtime-observed
settings separate. Reassess after any user-applied parent change. Without a
surfaced control for switching the current parent, report that portion pending
an owner-applied change; do not imply a preference update switched the parent.
