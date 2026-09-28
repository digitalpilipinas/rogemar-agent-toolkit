# Everyday workflow

Plan once. Use one execution entry. Let the existing Integrated Workflow owner select
supporting methods and manage the recorded delivery boundary. You do not need to
memorize the skill catalog or invoke a separate agent for each discipline.

## The two-entry path

**Planning:** use `create-plan` for a new substantive change. Describe the result,
constraints and important checks. It reads the repository, resolves meaningful
uncertainty and returns one proportionate plan. For an obvious safe correction,
formal planning is optional unless requested or required by the project.

**Execution:** invoke Integrated Workflow with the approved plan, or invoke the
appropriate Forge entry and explicitly ask it to follow Integrated Workflow. State
the delivery route once. The existing single orchestrator then selects useful
supporting methods and qualified native tools without restarting the plan.

Codex's example syntax is `$skill-name`. Cursor and other harnesses use their actual
picker/command syntax or natural language; this document does not install slash
aliases. Replace example paths with the real approved plan.

```text
$create-plan Plan the requested change using the current repository.
Include the expected outcome, affected contracts, focused checks and recovery.
Do not implement yet.
```

```text
$integrated-workflow Implement the approved plan at docs/plans/current-change.md.
Harness: Codex
Use codex-forge for execution.
Delivery to main: BRANCH + PR, STOP BEFORE MERGE
Continue through the authorized boundary without reconfirming routine actions.
```

For Cursor, name Cursor and cursor-forge. For another supported environment use
universal-forge with its actual capabilities. When you prefer native `/poteto-mode`,
preserve that externally managed PStack entry and reconcile its handoff with the
existing owner; do not run native and portable coordinators in parallel.

For fully authorized repository delivery, replace the route with
`BRANCH + PR + MERGE AUTHORIZED`. For local work, use `LOCAL ONLY`. Stricter task or
repository rules always prevail. An implementation approval is not by itself a
permission to deploy, change protection, spend on new providers, or publish releases.

## What happens automatically

The owner restores the original request, accepted plan, current candidate, effective
authority and unfinished gates. It selects only the required design, data, security,
accessibility, testing and review methods. Model selection stays with the active
native router; no static model table is duplicated here. A required absent Forge
mode is resolved once under its existing contract, not guessed from the parent.

Work proceeds in coherent vertical slices. Tests run as behavior changes. Precommit
checks verify the staged candidate and preserve unrelated work. Local full-slice
review occurs before ready-PR handoff, not automatically after every intermediate
commit. Early diagnosis and useful domain review may happen during implementation.

For substantive delivery, preserve local CodeRabbit and the active quality review.
An explicit owner exception is recorded for that task as waived, never as passed;
it does not waive unrelated repository checks or change the default policy.
At the ready PR, obtain both required full initial GitHub CodeRabbit and Codex reviews.
Wait for both to finish before consolidating, validating findings or assigning their
fixes. Later waves wait for every due provider in that wave. Each cloud provider keeps
its initial review plus at most one justified follow-up unless the owner explicitly
extends the allowance. Equivalent automatic reviews count; commits and resumed
sessions do not reset it. Do not infer that every push triggers a bot.

Consolidate by root cause into one existing finding record. Validate findings before
fixing, preserve rejected/deferred decisions, and make the smallest sufficient batch
of accepted corrections. Recheck affected behavior and shared causes. Unsupported
suggestions and harmless style preferences do not become mandatory work. A clean
merge does not mean zero bot comments.

## Four task sizes, one owner

| Work | Proportionate path |
| --- | --- |
| Small understood reversible correction | Relevant direct checks; no programme or mandatory external panel unless existing policy requires it. |
| Substantive feature or fix | Coherent slice, implementation evidence, complete local review, ready-PR cloud barrier and current-candidate validation. |
| Sensitive change | Add boundary-specific independence, negative cases, migration/concurrency/recovery evidence as warranted; size alone does not reduce risk. |
| Resume | Restore exact candidate, authority, source/version context, review counters and outstanding gates; invalidate only affected proof. |

A tiny authorization edit can be sensitive. A documentation edit needs proof of its
own outcome, not an unrelated mobile build. Learning and knowledge housekeeping
stay nonblocking except where a missing source fact is decisive to the task.

## Review names are not interchangeable

`code-review-and-quality` owns general quality review. `code-review-tests` contributes
testing/counterexample evidence to that same record. `/code-tests` is not assumed to
be an installed alias. CodeRabbit's external `code-review` route is a separate
provider; `/code-rabbit` is not assumed to be its command in every host.

`agent-collaboration-terminal` keeps its existing Codex-managed execution route.
Its file-backed coordination method also works in other harnesses with equivalent
controls; preserve working routes and use the native/portable handoff when needed. Do not start every external CLI by default or let external reviewers
recursively invoke additional reviewers.

## Publication and completion

A draft PR is already published work, but not the ready-review boundary. Do not start
an active PR-review monitor while draft. Existing CI/bots may still run; draft status
does not disable them. Inspect actual automation before publishing any change.

Before merge: verify current candidate and target compatibility, required checks,
provider coverage, accepted/rejected/deferred findings, actual repository approvals
and merge authority. Do not weaken a gate for green CI. After an authorized merge,
verify target contents and required post-merge results. Merged is not deployed.

Stop at the named route boundary. A permanent watcher requires a separate scheduling
request. A blocked reviewer, missing runtime or exhausted review allowance produces
an actionable partial report; it does not erase valid independent work.

## Learning and knowledge

In enrolled projects, assess at most the allowed evidenced learning candidate at the
verified checkpoint. Capture is inactive; review can be a compact batch. Accepted
rules remain scoped, revisable and revocable. Useful research may be retained through
a separately enrolled ingest/query/lint method, with original-source lineage and
privacy. Neither route changes permissions or shared policy automatically.

See [workflow diagram source](diagrams/everyday-workflow.mmd) and
[implementation status](alignment/implementation-spec.md). Diagram rendering and
live host qualification are distinct validation steps, not implied by this document.
