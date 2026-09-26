---
name: forge-setup
description: Configure adaptive per-role Codex model preferences for Forge. Use when setting up Forge, switching Default, Peak, Balanced, Lean, or Economy modes, changing preferred worker models or reasoning hints, or checking routing readiness. Let a selected mode govern parent and worker profiles; verify actual runtime switches separately.
license: MIT
---
# Set up Forge model preferences

Follow the installed orchestrator’s `references/forge-mode-status.md`: explicit
request → task mode → saved preference. Inspection alone never changes settings
or requires an execution-mode choice. A saved mode does not switch the parent.

1. Inspect the actual supported models/reasoning and read the existing `forge.json`
   in the Codex home. Preserve malformed files and explain the error.
2. Use the router’s `--list-modes` and `--role-map` for the single policy catalogue.
   Explain the parent target, actual parent, normal ceilings and any verified
   exceptions. Default is the exact user-selected model AND effort; ask only if
   that profile cannot be established from the explicit choice/current metadata.
3. For an explicit save, run `resolve_profile.py --set-mode MODE --preferences FILE`.
   Default accepts `--default-model MODEL --default-effort EFFORT`; reuse a saved
   Default profile when available. Schema 3 adds `default_profile`; schema 1/2
   remains readable and migrates on an authorized write with backup, atomic
   replacement and readback. Preserve per-role choices; rejected overrides stay
   visible rather than silently escaping policy. Keep exact model generations: a
   preset catalogue update does not rewrite saved Default or role selections.
   Explain an excluded or unavailable preference and offer permitted choices.
4. Read back and validate. Retain the chosen active mode when none was requested.
   `sprint → economy`, `supreme → peak`, `optimize → balanced`, `budget → lean`.
   Never infer mode from parent identity. The accepted new policy changes preset
   meanings; show that once on migration without claiming a runtime switch.
5. Before subsequent execution, resolve any desired/current parent mismatch using
   the existing shared task-level choice. A fallback retains both actual-parent
   and mode ceilings. Default must stay exact: choosing a different current parent
   requires an explicit task Default profile matching that parent.

Read the router’s [runtime routing contract](../plan-model-router/references/runtime-routing.md)
for fields, examples and validation. Setup does not change native GoalBuddy pins,
global Codex defaults, permissions or integrations. Configuration checks and live
worker verification are separate; promotion requires the recorded focused trials.

Routine assignments, including implementation, may use qualified lower profiles.
Keep consequential judgment and coding-evidence checks with `plan-model-router`;
inspect its role ledger for qualification or a provisional parent rationale.
Do not copy its model table here or change saved preferences during inspection.
Explain the qualification scope and any known failure alongside the profile.
Swarm/Arena select each participant by its actual assignment; no fixed worker
model or automatic worker count is implied by the setup table.
