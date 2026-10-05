---
name: claude-forge-setup
description: Configure and resolve Claude Forge modes, native model profiles, and role assignments. Use for Claude setup, mode changes, mapping inspection, and automatically before Claude Forge worker dispatch. Universal routing is fallback only.
---
# Claude Forge setup

Follow the shared [Forge mode and status contract](../workflow-orchestrator/references/forge-mode-status.md) at entry,
resume and dispatch: explicit request → task mode → saved preference; ask once
if none exists. Show role, model, effort, mode and evidence status without
repeated introductions. Setup inspection alone does not require a mode choice
or write preferences; apply the prompt when beginning an execution task.

Own Claude profile configuration and resolution. `workflow-orchestrator` alone
dispatches workers. `claude-forge` calls this route without a separate user
invocation.

Read [routing-contract.md](references/routing-contract.md) before configuration
or dispatch. Read `references/roles.json` for role IDs, groups, and skill hints.
These are assignments, not permanent agents and not installed tool claims.

Use Peak, Balanced, Lean, and Sprint. Discover the exact model IDs and accepted
settings from the active Claude worker tool. Do not copy Codex names, Cursor
slugs, or PStack defaults. A family name in conversation becomes a dispatch ID
only after the live catalogue confirms it.

No Claude runtime means model assignment stays unconfigured. Writing this skill
does not prove live switching.

Show current mappings and proposed changes grouped by mode. Persist only an
explicit setup request. Use a backup, a validated temporary file, atomic
replacement, and readback. A mode-only request preserves other modes. A bare
inspection writes nothing.

For ordinary execution, read the saved configuration and qualify the selected
role against task fit, the live catalogue, native pins, and explicit owner
limits. Return exact native arguments to the orchestrator. Do not run the
universal router beside a healthy Claude route.

If this adapter or the relevant mapping is absent, use
`universal-plan-model-router` as a disclosed fallback. Keep the mode, the role,
the permissions, and the required evidence. A malformed configuration or a
rejected profile is not permission to bypass the restriction. Missing optional
routing does not stop the main agent from doing the work directly.

Parent profiles are separate proposals. Apply one only through a supported
current-session control and verify the runtime identity. Existing workers do
not change when setup is saved.
