# Evidence-Based Response Standards

Keep the response proportional to the request. Do not emit every section by
default.

## Recommended structure

1. Result or recommendation.
2. Context and assumptions.
3. Relevant risks, dependencies, and open decisions.
4. Evidence and validation status.
5. Two to six prioritized next actions.
6. Plain-language recap or diagram when it materially helps.

## Evidence statuses

- **Verified:** directly observed through the named check or source.
- **Partial:** some evidence exists, but a required surface remains unchecked.
- **Unverified:** plausible recommendation without observed proof.
- **Blocked:** evidence cannot be gathered because of a dependency or failure.
- **Deferred:** intentionally left for a later environment or manual check.

## Progress

Track acceptance items or milestones, not invented percentages. Distinguish
planned, in progress, verified, blocked, and deferred work.

## Risks

When relevant, list Critical, Medium, and Low risks with impact, evidence,
mitigation, owner, and whether the risk blocks the next step.

## Repository and release status

Include branch, diff, CI, staging, production, simulator, device, or
deployment status only when inspected in the current task. Never infer status
from an intended command or a sample template.
