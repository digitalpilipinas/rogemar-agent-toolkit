# Execution routing and Forge preferences

Read this at a materially different execution package, before worker dispatch,
after a parent-profile change, or when a documented escalation fires.
`workflow-orchestrator` owns dispatch; this reference resolves its profile input.

## Parent selection

The manually selected active main model and reasoning effort are the defaults
and independent ceilings. A global configuration default is not proof of the
active turn. Do not change that selection automatically, including during
formal planning. Suggest a different parent at a major phase boundary only
with a concrete task-fit reason; the owner makes any change. Continue safely
with the selected parent when a suggested change is optional.

Known profile order for the exposed named families is Luna, Terra, Sol, Astra.
The model IDs are `gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`, and
`gpt-6-astra`. This order is a capability constraint, not a price table.
Do not infer ranks for unknown IDs, aliases, other providers, or future models
from their spelling. For an unranked model, inherit the exact parent or obtain
current capability evidence before comparing it. Never infer availability
from this list. Use the current dispatch catalog; a different CLI/backend's
model listing does not prove availability in this task.

## Preference file

Forge setup owns `${CODEX_HOME:-$HOME/.codex}/forge.json`, separate from Codex's
global model configuration. Schema version 1:

```json
{
  "schema_version": 1,
  "policy": "adaptive",
  "parent_policy": "suggest-at-phase-boundaries",
  "roles": {
    "feature": {"preferred_models": ["inherit-parent"]},
    "how explorer": {"preferred_models": ["gpt-5.6-luna", "gpt-5.6-terra"], "effort_hint": "medium"}
  }
}
```

The example's explicit IDs are examples, not entitlement claims. Missing file
or role means parent inheritance. `auto` and `inherit-parent` both mean omit
profile overrides and inherit the current parent; never pass an alias as a
model ID. Preferred lists do not determine fan-out or override a ceiling.
Effort hints are advisory and must pass the runtime/parent checks. Accept only
the documented fields and normalized efforts. Malformed configuration produces
a visible configuration error and leaves the parent/default route usable;
do not silently overwrite or repair the owner's file.

Role keys preserve the upstream setup vocabulary: feature, refactoring,
bug-fix, perf-issue, hillclimb, judgment and prose, hardest tasks, how explorer,
how explainer, how critics, why investigators, why synthesizer, reflect tooling,
reflect judgment, reflect divergent, reflect synthesizer, arena runners, arena
cross-judge pool, swarm workers, architect runners, and interrogate reviewers.
The same keys identify task classes, not permanent agent instances.

## Resolve and dispatch

1. Capture active parent evidence and the currently exposed models/efforts.
2. Assess the bounded task against `routing-profiles.md`. Start with parent
   inheritance. Propose lower sufficient candidates only with a task-fit reason;
   use preferences to choose among sufficient candidates, not to guess a design.
3. Inspect the selected role configuration. Its fixed model or effort can take
   precedence over spawn arguments. Reject an unsafe override; use an unpinned
   equivalent or keep the work with the main agent.
4. Filter both ceilings and model-specific effort support independently. Ultra
   also requires a deliberately independent-work profile and a parent using
   Ultra. Lack of a sufficient permitted profile returns unresolved work to the
   parent; a clamped weak profile does not make a critical task safe.
5. Use `scripts/resolve_profile.py` with observed inputs to check a proposed
   assignment. It is a pure preflight helper and never discovers entitlement,
   configures models, spawns agents, or proves what model actually ran.
6. The orchestrator sends the requested profile through the surfaced tool.
   Explicit overrides require a bounded-context fork when full-history forks
   force inheritance. Reuse only profile-compatible workers; reassess before
   sending more work after an escalation or parent change.
7. Inspect runtime metadata if surfaced and reconcile the result and checks.

Record: task/package, role/owner, desired profile, requested profile, observed
effective profile or Unverified, parent ceilings and evidence source,
selection reason, permissions/isolation, validation, and escalation condition.
Record this in the existing task receipt or programme evidence. Do not create
a new global log or save user memory automatically.

The helper reads one JSON object from stdin or a named file. Input fields are
`parent` (model, effort), `catalog` (model, efforts), `candidates` (model, effort,
reason), optional `role_config` (model, effort), and `parallel` (boolean).
Output distinguishes `ready`, `inherit-unverified`, and `blocked`, reports
rejected candidates, and leaves `observed_effective` null until the runtime
provides that evidence. Invoke `--help` for a read-only usage summary.

The family order is a local routing policy, not measured price or benchmark evidence. The live catalogue establishes availability and supported efforts. Unknown families are incomparable unless authoritative capability evidence establishes a ceiling relationship.
