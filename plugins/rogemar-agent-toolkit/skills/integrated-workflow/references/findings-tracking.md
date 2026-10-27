# Findings tracking and human handoff

Keep one canonical findings record for the authorized task. Reuse the project's
existing tracker and IDs when suitable. Otherwise maintain the project-local
`docs/quality/findings.md` using the [template](../assets/findings-template.md),
when repository writes are authorized; with no write authority, use an existing
authorized task receipt and report the durable-record gap. Link the record from
the existing task handoff. The implementation owner reconciles worker reports.
Do not create issues, post comments, install services or start monitoring merely
to track a finding; existing external records remain source references.

Record every distinct finding and recommendation encountered within the agreed
scope, including test and CI failures, local tooling or environment problems,
human and provider feedback, and optional improvements. Separate defects from
recommendations, hypotheses and missing prerequisites. Track rejected and deferred
items too. Tracking does not establish validity, priority, authority to fix, or a
new review gate. Validate each finding against its actual candidate and evidence.
During a ready-PR cloud review wave, collect raw reports while either required
initial review is pending; wait for the existing completion barrier before
consolidation, validation or reviewer-driven fixes. Local and pre-ready work keeps
its existing cadence.

## Record and reconcile

Use the template's fields or equivalent existing project fields: stable ID,
title, category, priority, affected behavior, first/last observation, task/PR,
candidate/environment, source IDs and links, reproduction/evidence, limitations,
status, proposed correction, disposition and next action. Include fix and
verification references when available; deferred work also needs a reason, revisit
trigger and owner when known. Preserve source-specific recommendations and their
dispositions without copying private logs, credentials or personal data.

Preserve project status names when equivalent. Fallback states are untriaged,
open, in progress, blocked, awaiting publication, fixed, deferred, rejected,
false positive and reopened; retain a useful `rejected-overengineering` distinction.
Mark a local fix awaiting publication when delivery is required. A resolved review
thread or merged PR is not proof of a fix. Separate a historical reported resolution
from verification of the relevant candidate and behavior.

Group reports only when evidence establishes the same cause, contract and failure
scenario. Preserve distinct reproduction cases, source IDs, recommendations and
disagreements; a similar symptom alone establishes only a provisional relation.
Reprocessing an existing source or test attempt must not create another finding
or increase counts. Keep distinct source reports, observed failing attempts and
verified recurrences after a fix separate: two reviewers are two reports, not two
runtime failures. Count only identifiable observations; where coverage is incomplete
say `at least N observed`, not zero. Never report a rate without its denominator.
Do not reopen for another report or wording alone; new evidence of a current defect
or invalidated fix can reopen it. Preserve the original disposition history.

## Checkpoints and evidence

At completion, pause, a blocked handoff or an owner decision, summarize newly
found, fixed, deferred, blocked and recurring items with a clickable tracker link
when accessible. If no tracker is available, link the authorized task receipt when
possible and name the durable-record gap; never invent a link. Use the existing
receipt rather than dumping the full record. For relevant media,
follow [verification efficiency](../../workflow-orchestrator/references/verification-efficiency.md#human-evidence-handoff).
Keep finding history when eligible evidence is removed; record the unavailable
artifact and cleanup receipt without deleting its finding or resolution.

Freeze versioned tracker contents with the review candidate. Later observations
belong in the existing authorized task or PR receipt and are reconciled in the next
permitted tracker update; they do not alter the frozen candidate retroactively.
Project Learning remains the owner of reviewed reusable lessons: a finding is not
automatically a lesson. Normal task startup reads relevant records; it does not
automatically rescan the project's historical PRs.
