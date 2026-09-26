# Codex routing policy and preferences

Use `scripts/resolve_profile.py` as the single qualifier. A resolution is not a
worker launch or proof of effective identity. Other harnesses use native routers.

## Modes

| Mode | Desired parent | Normal worker policy |
| --- | --- | --- |
| Default | Exact user-selected model and effort | Same exact profile for all ordinary roles |
| Peak | GPT-6 Astra / xhigh | GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol, GPT-6 Luna |
| Balanced | GPT-6 Sol / xhigh | GPT-6 Sol, GPT-5.6 Sol, GPT-6 Luna |
| Lean | GPT-5.6 Sol / xhigh | GPT-5.6 Sol, GPT-6 Luna |
| Economy | GPT-6 Luna / medium | GPT-6 Luna only |

Normal efforts are low through xhigh for Peak/Balanced/Lean, low/medium for Economy.
These pools permit qualified candidates; availability alone is not qualification.
The catalogue owns exact-generation IDs, supported efforts and the support profile.
GPT-6 Luna supports low through max, not ultra. Retired preset models remain valid
explicit Default choices when available; never translate a user pin or its evidence
to a successor. Historical GPT-5.6 results do not qualify GPT-6 assignments.

Model tier and effort are independent ceilings. Use the stricter mode target and
accepted actual parent for normal workers. A lower family at higher effort still
needs an exception. Tier ordering is owner policy, not a measured intelligence
ranking. Default permits any actually supported exact user profile, including
Ultra, without automatic escalation or per-role optimization.

Only `hillclimb` and `hardest-tasks` can use a verified exact cross-family or higher-reasoning
exception. Provisional records cannot dispatch. Required quality checks do not
change by mode. A parent fallback does not satisfy an independent review gate.

Aliases: `supreme → peak`, `optimize → balanced`, `budget → lean`, `sprint → economy`.
Existing `budget` keeps its historical meaning. No new Auto mode or automatic
mode choice from the parent is introduced.

## Requests

Provide `parent: {model, effort}`, the live `catalog: [{model, efforts}]`, `role`,
`mode` and a concrete `task_reason`. `target` defaults to `worker`; `parent` returns
only the desired profile and whether it differs. Explicit `mode: null` means the
legacy no-mode route and overrides saved preferences; omitted mode may use them.

Optional fields:

- `consequential: true`: require the actual parent's exact model generation for security or architecture
  judgment within any role. False cannot relax the catalogue-protected roles.
- `implementation: true`: require paired executable coding evidence for any alternate
  profile doing implementation. Catalogue coding roles, including ui-designer,
  enforce this automatically. Inspect `qualification_scope`: SQLite evidence does
  not qualify UI implementation, and browser checks do not qualify a native device.
- `evidence_contract`: identify the matching tested contract, currently `notes-store`
  or `note-editor-ui`, after checking the actual task. Alternate implementation
  profiles and every above-ceiling exception require this match. UI implementation
  roles bind it to `note-editor-ui`; a hard-task label cannot turn database proof
  into UI proof. The dispatcher supplies the field; do not ask the user to memorize
  fixture identifiers. A declared ID alone never establishes broader task fit.

- `preferences`: validated saved schema below.
- `default_profile: {model, effort}`: explicit task Default profile; otherwise use
  its saved profile or the explicitly selected, verified current parent.
- `parent_fallback: {mode, desired, actual, accepted: true}`: the existing affirmative
  task-local decision, bound to exact profiles. A changed profile invalidates it.
- `candidates: [{model, effort, reason}]`: explicit task-fit candidates. They still
  obey ceilings, consequential-family restrictions, paired quality evidence, role pins and explicit limits.
- `limits: {model?, effort?}`: additional hard ceilings, including on exceptions.
- `role_config: {model?, effort?}`: observed native pins, never invented hints.
- `goalbuddy_required: true`: requires the role’s native GoalBuddy contract and
  observed Scout/Low or Judge/High pin. Omitted/false means an ordinary unpinned
  read-only Forge assignment; its receipt is not native GoalBuddy evidence.
- `difficult_task: true`, `exception_evidence_id`, `exception_reason`: request the
  exact verified exception for a justified assignment. Naming a role is insufficient.

Here, retaining the parent family means the exact model ID, including generation;
GPT-5.6 Sol is not interchangeable with a GPT-6 Sol parent for consequential work.

Routine implementation, refactoring, synthesis, design and ordinary reviews may
use evidence-qualified lower profiles. Consequential defaults and main-owned
responsibilities remain in the catalogue. Hardest-tasks/hillclimb inherit the actual
parent normally; a higher accepted fallback never expands a mode worker pool.
A blocked hard worker may remain direct parent work, with its limitation disclosed.

Only `status: ready`, `target: worker` can dispatch. Copy `requested` settings exactly
into supported native controls, use `dispatch_agent_type` when present, and pass
`task_requirements` in the bounded handoff. `parent-choice-required` means reuse
or obtain the shared decision once. `blocked` means requalify within policy, keep
ordinary work with the parent, or report missing required independent evidence.
Unknown metadata stays unverified; do not simulate a parent switch with a worker.

## Preferences and migration

Schema 3 retains `policy: adaptive`, `parent_policy`, `roles`, `active_mode` and adds
`default_profile` (null unless selected/configured). The legacy `parent_policy`
string `mode-adaptive` remains a compatibility field; it does not authorize an
unbounded worker pool. Use `suggest-at-phase-boundaries` when active_mode is null.

Each role preference retains `preferred_models` and optional normalized
`effort_hint`. Inheritance aliases inherit both model and effort and cannot be
combined with an effort hint. Default rejects conflicting role preferences;
other presets reject out-of-policy preferences rather than silently ignoring them.

Read versions 1/2 without changing their files. On an authorized write, migrate
spaced role IDs, aliases and schema; preserve choices; back up exact prior bytes;
write atomically and validate readback. Refuse malformed/colliding preferences,
symlink replacements and detected concurrent changes. Setup never changes global
Codex defaults or native agent configuration.

Examples (supply the actual preference path):

```sh
python3 scripts/resolve_profile.py --set-mode economy --preferences FORGE_JSON
python3 scripts/resolve_profile.py --set-mode default --default-model gpt-5.6-sol --default-effort xhigh --preferences FORGE_JSON
python3 scripts/resolve_profile.py --validate-preferences FORGE_JSON
python3 scripts/resolve_profile.py --role-map
```

The role map marks Swarm/Arena as `assignment_role_required`, rather than showing
a blanket worker model. Their participant still resolves through the actual role.

## Evidence and fallback

`role-evidence.json` preserves all 225 role/mode decisions. The historical record
supports candidate selection, not general intelligence or parent coordination
claims. Native cases and main-owned roles lack comparable isolated measurements.
New focused validation is separate and candidates need two successful repetitions
before promotion. Verify output quality independently from runtime model identity.

Economy reduces unnecessary context, workers and duplicated evidence. Estimate
account credits from actual usage telemetry and dated rates; report raw tokens,
API-equivalent dollars and duration separately. Never infer current quota or a
bill from a mode name. Missing required checks remain blocked, regardless of cost.

`known_quality_failures` must remain visible in the handoff. A provisional parent
may repair a demonstrated defect, but its default selection never marks that defect
resolved. Native pins exempt only their fixed effort within the actual parent family;
Scout/Judge are read-only and reject implementation assignments.
