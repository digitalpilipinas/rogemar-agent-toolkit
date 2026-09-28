# Qualification, controlled updates and observations

Use the existing task, router qualification and maintainer records. This method
creates no agent, monitor, background updater, trust score or permission grant.
Keep ordinary work on its working route when an optional enhancement is absent.

## AQ-01: qualification is separate from permission

Record the capability, eligible task types/actions, actual environment, relevant
versions, observed successes and unresolved failures, bounded operating limits and
expiry. Reuse matching evidence. A changed environment, version, scope or revoked
grant invalidates affected use, not every unrelated method. Do not equate a model
name or reasoning preference with executed behavior.

The owner grant has its own authenticated source, scope, expiry and limits. A
successful trial never broadens it. `scripts/capability_lifecycle.py qualification
--input record.json` compares `qualification`, `task` and `owner_grant` records.
It does not authenticate the supplied objects. Native router contracts still own
model and reasoning qualification; this contract adds capability/action scope.

For an explicitly enrolled host, import `scripts/execution_boundary.py` at its
existing action boundary. The host supplies a live authenticated decision lookup
and registered native tool callbacks. The adapter binds the complete action,
checks qualification and grant, atomically reserves operation IDs and cumulative
budgets in the host's existing protected state location, then invokes the callback.
Only actual observed success marks completion. Uncertain operations remain reserved
after interruption; inspect their actual outcome before creating another action.
Cancellation or revocation must be reflected by the live host lookup. The host must
stop running processes and enforce filesystem/network privileges itself.

`transition` and `invalidate` operate on the existing coordination record. The
dispatcher must persist their results under its existing lock/transaction, using
actual workspace/resource identities. They reject incomplete prerequisites,
overlapping active writers and missing completion evidence, and invalidate affected
descendants. They do not discover semantic dependencies or create process isolation.

## UP-01: controlled external updates

For a relevant external change, the existing maintainer records its authoritative
URI, version and digest, checks duplicate consideration, and assesses applicability
and conflicts. Keep project-derived proposals with Project Learning. External
updates use these transitions in the existing maintenance record:

1. `detected` → `assessed`: concrete affected paths, benefit, acceptance and rollback.
2. `assessed` → `qualified`: observed regression and scoped qualification evidence.
3. `qualified` → `approved`: actual owner decision bound to the exact proposal digest.
4. `approved` → `piloted`: an authorized bounded pilot and its observed result.
5. `piloted` → `promoted`: observed promotion and usable rollback evidence.
6. `promoted` → `rolled-back`: observed rollback when needed.

`capability_lifecycle.py update` accepts the existing `record`, `event`, live
`observed_source`, and `owner_decision` when needed, returning the proposed next
record. The maintainer performs authorized real actions and persists observations;
the validator does not install updates. Changed proposals require a new linked
record. Failed/rejected/rolled-back records cannot be relabeled as successes.
Reject source drift and failed pilots; preserve their evidence and reasons.

## ME-01: proportionate effectiveness evidence

Collect only useful observations for comparable eligible tasks and versions in an
explicit observation window. `capability_lifecycle.py measures` takes `observations`
with task ID, version, eligibility and optional observed metrics. Keep absent values
null, distinct from zero. Distinguish prohibited attempts, blocked attempts and
completed unauthorized actions. Record verified success, false completion, recurring
defects, stale/inappropriate lesson use and demonstrated useful knowledge reuse.
Retrieval alone is not a prevented defect. Cost units cover latency, tokens, money,
review, retrieval, ingestion, storage and recovery. Include unsuccessful attempts.

The bounded output supplies denominators and missing observations, not a composite
score or causal conclusion. Do not collect raw transcripts or private content. No
production improvement is claimed from synthetic tests or a single task.

## Evidence tier

Unit fixtures exercise adapter behavior with controlled callbacks and real local
side effects. They do not prove independently protected policy, native Codex/Cursor
dispatch, model quality, owner identity or deployed sandbox behavior. Enroll that
stronger tier only after the actual host protects its callbacks, state, producer,
policy and verifier from candidate writes and passes its own boundary trials.
