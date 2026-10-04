---
name: bug-triage
description: Use when investigating errors, logs, failed tests, crashes, CI failures, production incidents, bug reports, or confusing runtime behavior that needs hypotheses, reproduction steps, and prioritized fixes.
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

## Optional delegation guidance

For genuinely independent hypotheses, the orchestrator may assign read-only
workers to inspect code paths, logs, reproduction evidence, or competing root
causes. Give each worker one hypothesis and require evidence for and against
it, reproduction steps, and a confidence/status result. Pass the parent model
and reasoning ceilings; never let a worker exceed them. The main agent owns
hypothesis reconciliation and the final fix decision.
