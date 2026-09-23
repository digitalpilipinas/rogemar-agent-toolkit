# Selecting overlapping provider skills

Use only when more than one installed route provides the requested capability.
The current orchestrator coordinates; a provider keeps its own review or task
procedure. A source review of a skill does not authorize running its service.

## CodeRabbit

When selected by the user or the active acceptance contract, use the namespaced
CodeRabbit plugin's own skill when available. Perform its full review over the
agreed candidate, including all in-scope changes; do not substitute a quick pass,
sampled files or only selected findings. Follow the provider's supported commands,
completion and findings handling. Keep its verdict and full result available even
when the shared review record consolidates duplicates. A standalone CodeRabbit
request need not start a second generic review.

If the plugin skill is unavailable, use the installed standalone CodeRabbit skill
with the same full-review scope. Do not run both installations. Installation,
authentication, code transmission and paid use retain the applicable user
permission; selecting a skill cannot silently grant missing authority. Reuse
existing authorization without asking twice.

## Multiple versions or distributions

Use one established primary for overlapping names, with qualified paths when
needed. Preserve distinct tools, resources and unique skills. Compare full trees
and consumers before disabling duplicate discovery; keep backups and leave
managed caches intact. Retaining a unique method from another distribution does
not authorize duplicate review or parallel execution.

## Convex distributions

When both distributions are present, keep the maintained Convex plugin's shared
expert/authentication contract with its dependent authz methods and native
monitor tools. The curated app binding remains a distinct capability. Same-name
add, update-check, reviewer and domains skills need only one discovery owner.

For a generic new-app request, prefer the installed portable `convex-quickstart`
when available; keep the existing project/deployment identity and execute only
authorized bootstrap steps. Explicit requests for a named plugin quickstart
retain that route. Their differing bootstrap instructions require current-source
inspection: never bypass host security checks, silently rebind an existing
production/persistent deployment to anonymous mode, or enable a monitor/trust
setting without the applicable authority. Do not treat plugin version numbers
from separate distributions as a shared upgrade sequence.

## Review support and decision roles

Apply this separation to authorized local pre-commit/complete-slice reviewers and
ready-PR cloud review. The orchestrator qualifies each assignment; it does not
configure the external provider's own model or start another review cycle.

| Work | Assignment | Authority |
| --- | --- | --- |
| Observe reviewer progress and completion | `status-monitor` | Read-only; record changed state, scope, candidate identity, pending/errors and raw artifact links |
| Consolidate completed feedback | `findings-consolidator` | Read-only; preserve every finding ID/source, group duplicate or related items, retain disagreements and coverage gaps |
| Validate correctness and relevance | `correctness-reviewer`, with `validation-runner` for focused checks | Check source, executable counterexamples, stale/out-of-scope claims and interactions across the whole candidate |
| Assess minimum viable correction | `scope-reviewer`; Ponytail when useful | Recommend the smallest sufficient batch; reject unsupported complexity with evidence |
| Build or fix | Existing qualified implementation role/owner | Apply accepted fixes and rerun affected checks |

In Codex presets, monitoring and consolidation use the router's qualified Luna
profiles. Decision and implementation work must be qualified separately; Peak,
Balanced and Lean use permitted non-Luna decision profiles. Keep exact model tables
in `plan-model-router`. Default preserves the exact user-selected profile. Economy
keeps its existing ceiling unless the owner explicitly changes it; never silently
promote outside the mode pool or disguise a missing qualification. Other harnesses apply the same
role boundary with their own available models, without importing Codex IDs.

Consolidation is preparation, not validation or disposition. Tag apparent duplicates
without deleting provenance, label suspected scope issues as unvalidated, and hand
conflicting evidence to the decision owner. It cannot accept/reject a recommendation,
mark a review passed, resolve a thread, waive a gate, or change code. Requalify at that
boundary; do not continue judgment inside the cheap monitoring assignment. One
suitable qualified agent may cover compatible validation and minimum-scope work;
there is no mandatory new agent for each row. Main retains final reconciliation,
integration and acceptance, including where unavailable support stays direct.

Keep existing cadence and authority: a completed full local slice review need not
repeat at every commit. In an active Integrated Workflow ready-PR wave, collect raw
reports while reviews are pending and consolidate only after all due reviews finish.
A commit alone does not start cloud monitoring; a draft PR needs no monitor. Use
provider/native event waits or bounded changed-only checks, preserve pending/stale
states and stop conditions, and schedule nothing without an explicit request.
