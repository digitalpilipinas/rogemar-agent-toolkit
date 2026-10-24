# Toolkit update handoffs

This is the resume index for the current authorized toolkit improvement and publication task.
Read repository `AGENTS.md`, the selected task record, and actual Git state before
continuing. These records own this local task status; they do not replace a future
GoalBuddy board or independently grant publication authority. The latest operator request explicitly authorizes committing all intended changes and aligning GitHub; see the publication record for current blockers. The current PR publication status and cloud location are recorded in `toolkit-publication.md`.

| Task | Record | Dependency |
| --- | --- | --- |
| Integration and publication | [toolkit-publication](toolkit-publication.md) | Current local work and latest GitHub main |
| Reliability repairs | [toolkit-reliability](toolkit-reliability.md) | None |
| Methods and evidence | [toolkit-methods](toolkit-methods.md) | Reliability repairs |
| Durable handoffs | [toolkit-handoffs](toolkit-handoffs.md) | Methods and evidence |
| Native qualification | [toolkit-host-qualification](toolkit-host-qualification.md) | Local changes and checks |
| Interview and upstream re-audit | [toolkit-upstream-reaudit](toolkit-upstream-reaudit.md) | Current local changes and pinned upstream comparison |

Read status and next action from each task record rather than maintaining a second
status table here. Retain completed records. Add an approved future task as planned
with acceptance and dependencies; do not invent tasks merely to fill every status.

Required local commands are `python3 -B scripts/toolkit.py lock`, then `verify`,
`python3 -B -m unittest discover -s tests -v`, the Project Learning tests, Forge
verification, watcher tests, and core/full package checks. Exact results belong
in the task records. The operator reports host-terminal authentication is complete; CodeRabbit review
is temporarily waived for this PR by the operator. Authentication/network diagnosis remains in the qualification record; do not retry local CLI review for this delivery.

PR publication is authorized through the GitHub connector; verify remote revision and file contents before
claiming another machine can read them. Resume after interrupted local tests by
inspecting their actual outcome or rerunning only affected checks.
