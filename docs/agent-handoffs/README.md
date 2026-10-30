# Toolkit update handoffs

This index tracks toolkit work across sessions. Read repository `AGENTS.md`, the
relevant task record and current Git state before continuing. Records carry
status and evidence; they do not independently grant publication authority.

PR #29 (1.2.0) and PR #31 (1.2.1) are merged on GitHub. The current local
capture follow-up is recorded below; its record distinguishes source files from
protected local Git metadata. Older publication and review-waiver statements
belong to their recorded task, not every future change.

| Task | Record | Dependency |
| --- | --- | --- |
| Findings and evidence handoff | [findings-evidence-handoff](findings-evidence-handoff.md) | Merged capture follow-up; 1.2.2 delivery |
| Verification capture follow-up | [verification-capture-follow-up](verification-capture-follow-up.md) | Merged 1.2.1 source; local source reconciliation |
| Integration and publication | [toolkit-publication](toolkit-publication.md) | Current local work and latest GitHub main |
| Reliability repairs | [toolkit-reliability](toolkit-reliability.md) | None |
| Methods and evidence | [toolkit-methods](toolkit-methods.md) | Reliability repairs |
| Durable handoffs | [toolkit-handoffs](toolkit-handoffs.md) | Methods and evidence |
| Native qualification | [toolkit-host-qualification](toolkit-host-qualification.md) | Local changes and checks |
| Interview and upstream re-audit | [toolkit-upstream-reaudit](toolkit-upstream-reaudit.md) | Current local changes and pinned upstream comparison |
| Upstream adoption review and drift tracking | [toolkit-adoption-review](toolkit-adoption-review.md) | Merged 1.2.2 source |
| Project readiness and method receipts (1.3.0) | [plan](../plans/project-readiness-and-method-receipts.md) | Adoption review (PR #34) |

Read status and next action from each task record rather than maintaining a second
status table here. Retain completed records. Add an approved future task as planned
with acceptance and dependencies; do not invent tasks merely to fill every status.

The project [findings tracker](../quality/findings.md) records in-scope issues,
recommendations and their source/disposition evidence; historical coverage gaps
remain explicit in its linked task receipt.

Required local commands are `python3 -B scripts/toolkit.py lock`, then `verify`,
`python3 -B -m unittest discover -s tests -v`, the Project Learning tests, Forge
verification, watcher tests, and core/full package checks. Exact results belong
in the task records. Historical authentication, provider waivers and delivery authority remain in the
corresponding task records. Reconcile them with the current request rather than
reusing a past PR's exception. After interrupted checks, inspect their actual
outcome or rerun only affected checks.
