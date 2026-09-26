# Automatic delivery checkpoints

The orchestrator selects these actions without requiring the user to name skills.
Integrated Workflow owns an explicitly approved delivery; these triggers grant no
new editing, provider, publication or scheduling authority. Reuse its gate record.

Navigation may be skipped for known-file work; a required acceptance checkpoint
may not. This also applies to read-only readiness questions: run the read-only
helper, or report the specific missing base, policy or capability as blocked.
Preserve failing checks' nonzero exit status; do not swallow assertion failures
or turn them into a successful shell result. Read-only runs must avoid caches
and other incidental writes (for example, use Python's `-B` option).

| Event | Next action |
| --- | --- |
| Start/resume | Restore scope, candidate and unfinished gates. Read relevant accepted lessons and feature-map entries before diagnosing a vague report. |
| Unfamiliar subsystem, multi-file impact, callers | Use an existing agent-map after its freshness check; one bounded query, then current source/tests. Missing, stale, unsupported or ambiguous results fall back to direct search. Missing edges never prove absence. Skip known-file work. |
| Mapped behavior | Select affected journeys and meaningful failure cases before editing. Shared-code changes require all affected features, not just the reported screen. |
| Missing recipe | Record a coverage gap. Discover and reuse an existing verifier; use forge-create-verification-skill only to create/extend within authorized scope. |
| Draft verifier | Attempt its initial proof when prerequisites and authority permit; keep draft/blocked until observed success. One successful journey does not prove the map. |
| Behavior/driver drift | Record updated, unchanged with reason, or coverage gap. Re-prove affected recipes; use forge-maintain-verification-skill for a full map audit when warranted. A partial repair is not completed maintenance. |
| Acceptance/readiness | Run selected checks; validate their receipt against current candidate, required features/platforms and surviving artifacts. |
| Verified completion | In enrolled projects, assess one evidenced candidate per native source turn through project-learning. Capture remains inactive; show only its due review reminder. |

A feature map describes expected behavior; a navigation index locates code; a
verifier drives it; accepted lessons guide future work. Keep one maintained feature
map with stable IDs, entry points, source paths, prerequisites, recipes and observable
outcomes. Path matches trigger review; they cannot prove semantic completeness.
Investigate regressions instead of rewriting expected behavior to match a defect.

## Checkpoint command

Use the installed Integrated Workflow `scripts/checkpoint.py` with `--root ROOT
--base COMMIT --phase start|accept|close --receipt ABSOLUTE_RECEIPT.json`. It prints
JSON and writes nothing. Start can use a missing receipt; read its selected recipes
and coverage gaps. Planning/no-write starts persist nothing. On acceptance, extend
the existing gate record with these machine-readable fields (do not create a board):

- `schema_version: 1`, `candidate` from the current start result (base/head/content),
  `scope: {features: [additional IDs], assessment: source-grounded impact rationale}`.
- `map_review: {disposition, reason, expected_behavior_preserved: true}` when affected.
  A false value or coverage gap blocks acceptance; evidence must resolve the issue.
- `gates`: existing requirement/source/trigger/owner/boundary/state/candidate/evidence
  fields, with `gate: feature-ID:platform`, `feature`, `platform` for each selected
  feature/platform. Required gates cannot be downgraded in the receipt.
- Each passed gate supplies nonempty artifacts with absolute `path`, `sha256` and
  `candidate`. Runtime artifacts also supply `kind: runtime`, exact `platform`, and
  gate `runtime: {target, fixture, actions, observed, cleanup}`. Keep private artifacts
  local; no credentials or raw personal data in shared receipts.
- Deferrals include `owner_decision`; they remain deferred and suppress verified
  completion capture (exit 2, never a passed shell gate). Failed/blocked gates reject
  their named acceptance boundary with exit 1.

The project `.agents/verification.json` contains schema_version 1, runtime_paths,
shared_paths, nonruntime_paths and features with id, paths, recipe and platforms.
Paths are repository-relative glob patterns. Shared paths select all mapped features;
unmapped runtime paths are coverage gaps. Nonruntime exceptions must be narrowly
reviewed. Additional feature IDs cover semantic relationships missed by globs.
Do not claim unlisted platforms are verified. Runtime inputs and generated metadata
freeze during attested QA; refresh indexes before launch or use source reads.

## Trusted policy and proportional enforcement

Accept/close require `--trusted-policy FILE --policy-sha256 SHA --validator-sha256 SHA`.
Use a separately reviewed validator and policy snapshot outside the candidate
checkout; the policy contains its resolved `repository`, exact `mapping` and
`boundary` (default `accept`) and `required_gates` IDs for other gates due there.
Outstanding required receipt gates at that boundary are also enforced; future
boundaries remain pending without blocking a different authorized boundary. Carry the pins in the
existing approved acceptance record or trusted CI configuration, never derive them
from candidate-controlled values at acceptance. Policy changes require their own
review; do not refresh pins merely to make a product candidate pass.

Existing acceptance commands invoke this helper. CI uses its protected baseline
copy/pins and available artifacts. When runtime artifacts exist only locally, CI
records structural evidence only and the runtime gate stays local/unverified there.
Never infer simulator execution from a filename or invent evidence in CI. A pin
checks integrity, not who approved it. Agent instructions and wrappers cannot
sandbox unrestricted shell access; enforced harness permissions remain separate.

Changed source, dependency or runtime inputs invalidate affected proof. Bug fixes
need a before/after reproduction; comparisons use equivalent baseline scenarios,
with absence explicitly recorded for new features. Material repair rounds rerun
affected checks and a relevant shared-cause regression; no fixed lane count. Refresh
current-head CI before its required readiness/merge boundary. Preserve the existing
provider completion barrier and per-provider allowances.

Keep handoffs to scope, candidate, selected checks, evidence/blockers and next action.
Read accepted lessons, never pending candidates, as guidance. Learning failures do
not block delivery. No background collector, automatic promotion, new hook or
native model policy follows from these checkpoints.
