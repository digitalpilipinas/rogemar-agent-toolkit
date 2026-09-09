---
name: cursor-forge-setup
description: Configure and resolve Cursor Forge modes, native model profiles, role assignments and supporting skills. Use for Cursor setup, mode changes, mapping inspection, and automatically before Cursor Forge worker dispatch; universal routing is fallback only.
---
# Cursor Forge Setup

Our adaptation of PStack setup, preserving upstream `/setup-pstack` and its
configuration. Own Cursor-specific profile configuration and resolution;
`workflow-orchestrator` alone dispatches workers. The user invokes Cursor Forge
once; it uses this primary route without requiring a separate setup invocation.
Read [routing-contract.md](references/routing-contract.md) before configuration
or dispatch. Read `references/roles.json` for all 45 role IDs, groups and skill
hints. These are assignments, not 45 permanent agents or installed tool claims.

Use Peak, Balanced, Lean and Sprint with explicit Cursor-native per-role model
profiles. Discover the exact IDs and accepted settings from the active Cursor
worker controls; do not copy Codex names or guess availability from upstream
defaults. Existing PStack preferences can seed proposals after validation, but
never rewrite its files. No Cursor runtime means model assignment remains
unconfigured; setup instructions alone do not establish live switching.

Show current role mappings and proposed changes grouped by mode. Preserve valid
owner choices and use group defaults with per-role overrides. Select relevant
installed skills for each role from task needs; hints are optional, not an
activation checklist. Persist only explicitly requested setup changes, using a
backup, validated temporary file, atomic replacement and readback. A mode-only
request preserves other modes and role settings. A bare inspection writes nothing.

For ordinary execution, read the saved configuration and qualify the selected
role against actual task fit, catalogue, native pins and explicit owner limits.
Return exact native profile arguments to the orchestrator. Do not run the
universal router alongside a healthy configured Cursor route.

If this adapter or the relevant mapping is absent, use
`universal-plan-model-router` as a disclosed fallback while preserving mode,
role, permissions and required evidence. A malformed configuration, excluded
profile, unknown mandatory limit or conflicting native pin is not permission
to bypass the primary restriction; resolve that constraint first. Missing
optional routing does not stop independent main-agent work.

Parent profiles are separate proposals. Apply changes only through a supported
current-parent control within authority and verify runtime identity. Existing
workers do not change when setup is saved; requalify each new assignment.
