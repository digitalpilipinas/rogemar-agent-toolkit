---
name: bug-triage
description: Use when investigating errors, logs, failed tests, crashes, CI failures, production incidents, bug reports, correlated incoming reports, or confusing runtime behavior that needs hypotheses, reproduction steps, and prioritized fixes.
---

# Bug Triage

## Workflow

1. Gather the exact error, command, environment, recent changes, and reproduction path.
2. Read logs and relevant code before proposing fixes.
   Build the smallest repeatable check that catches the reported symptom, rather
   than merely exiting successfully. Minimize inputs while retaining that failure;
   if reproduction is unavailable, name the missing evidence and keep hypotheses
   provisional. Redact captured credentials and personal data.
3. Form a small ranked set of hypotheses with evidence for and against each.
4. Test the highest-signal hypothesis first using the repo's normal commands.
5. Implement the smallest safe fix when the user wants action, then verify.
   Rerun the original scenario as well as the narrowed regression, and remove
   task-owned diagnostic instrumentation. A performance fix needs measurements.

The focused reproduction method is adapted from Matt Pocock's `diagnosing-bugs`
at `24fe0ef7737efae15c87225755e9f6f5965e4888` ([MIT notice](upstream-notices/mattpocock-LICENSE)).
It adds no mandatory hypothesis count, human checkpoint, or production access.

## Output

- Root cause if known.
- Evidence and reproduction path.
- Fix implemented or proposed.
- Verification run and any remaining gaps.

## Guardrails

- Do not guess from a stack trace alone when code or logs are available.
- Do not erase local state, migrations, caches, or user changes unless explicitly asked.
- Distinguish environment/tooling availability issues from application bugs before changing product code.
- Classify each failed attempt and stop after two similar unexplained failures; see
  [verification efficiency](../workflow-orchestrator/references/verification-efficiency.md).

## Optional delegation guidance

For genuinely independent hypotheses, the orchestrator may assign read-only
workers to inspect code paths, logs, reproduction evidence, or competing root
causes. Give each worker one hypothesis and require evidence for and against
it, reproduction steps, and a confidence/status result. Apply the active harness router
and explicit user limits; this method defines no separate model policy. The main agent owns
hypothesis reconciliation and the final fix decision.

## Correlate related reports before dispatch

When several reports may describe the same failure, use a bounded intake pass
before creating fix assignments. Reuse the project's backlog and current incident
priority; do not delay an urgent mitigation to wait for more reports.

1. Preserve each report's source/ID, affected version, environment, symptom and
   distinct reproduction case. Redact private details in shared records.
2. Check the current baseline where safe. Mark still reproducible, no longer
   reproduced, blocked or unknown; unavailable evidence is not a duplicate.
3. Compare mechanisms, affected paths and timing. Label a suspected relationship
   provisional until evidence supports a common cause. Similar wording alone
   does not establish one defect.
4. Give the orchestrator one investigation for an evidenced cluster, preserving
   links to every report and its separate acceptance case. Keep unrelated or
   conflicting reproductions separate; split a cluster when evidence diverges.
5. Before dispatch, check for an existing investigation or fix. Merge task scope
   only when it preserves ownership, urgency and all distinct regression cases.

Completion is a source-linked grouping with current-baseline status, uncertainty,
owner/next action and retained reproduction cases. Connector subscriptions,
background buffering and external backlog writes need their own actual authority.

## Regression and diagnostic evidence

When testing a deliberately broken variant, follow the shared
[mutation evidence method](../code-review-tests/references/mutation-evidence.md).
An edit command succeeding is not evidence that the intended mutation landed.

After an expensive diagnosis, propose the cheapest useful signal for recurrence:
a metric, structured log, trace field or invariant check. Name the failure it
would distinguish, where it belongs, expected normal/failure values and how to
verify it detects the case. Consider privacy, noise and runtime cost. Add it only
within authorized scope; otherwise return the concrete proposal with the fix.
