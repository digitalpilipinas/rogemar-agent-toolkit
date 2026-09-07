---
name: forge-setup
description: Configure adaptive per-role Codex model preferences for Forge. Use when setting up Forge, changing preferred worker models or reasoning hints, or checking routing readiness. Preserve the manually selected main model and effort as the inherited defaults and ceilings.
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
3. Show one compact table of upstream-equivalent roles and current preferences.
   Offer the available Codex models plus `inherit-parent`/`auto`. Lists are
   candidate pools; they neither pin a role nor create a worker per entry.
   Recommend inherited defaults and bounded cheaper candidates where justified.
   Accept the owner's batch choices rather than requiring a configuration form
   before ordinary programme execution.
4. Validate the version, policy, role keys, model IDs, and effort hints using
   `plan-model-router/scripts/resolve_profile.py --validate-preferences FILE`.
   This validates structure; verify selected real IDs against the live catalog
   separately. Keep the owner's selected parent and both ceilings in force.
5. For an authorized setup/update, back up an existing file and atomically write
   the chosen preferences. An initial default needs no model assumptions:

```json
{
  "schema_version": 1,
  "policy": "adaptive",
  "parent_policy": "suggest-at-phase-boundaries",
  "roles": {}
}
```

6. Read back and validate the file. Report configured preferences separately
   from a verified worker dispatch. Profile changes apply at the next package
   assessment; do not claim existing workers changed models.
7. If the project lacks reusable runtime proof, recommend
   `forge-create-verification-skill` through the orchestrator when useful. This
   is optional and grants no device, service, installation, or publication access.
