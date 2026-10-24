# Durable task handoffs across harnesses

Maintain a repository-readable handoff for every task in the approved programme,
including planned, in-progress and completed tasks. Use it on Codex, Cursor, Claude
and other hosts. A chat summary is useful context, but is not the only resume source.

## One record and one owner

Reuse existing versionable task documents and their index if they can hold the
fields below. Otherwise use `docs/agent-handoffs/README.md` as the index and
`docs/agent-handoffs/<stable-task-id>.md` per task. The path is a default, not a
requirement to migrate a working project convention. Link the index from the
existing plan or repository entry instructions within scope.

Reuse accepted task IDs and dependencies. The index links task records and the
authoritative plan/board; it does not become a second scheduler. If GoalBuddy or
another board owns status, the handoff records an as-of snapshot and source
revision, and only that board's authorized owner changes its state. Otherwise
the existing plan/task record owns status. Assign one handoff writer per task;
workers return evidence to that owner. Update a shared index serially.

## Record enough to resume

Use [the task template](../assets/task-handoff-template.md) or equivalent existing
fields. Keep short tasks short, but give every approved task a record.

- Stable ID, outcome, status, dependencies, owner, update time in UTC and source
  of authority. Preserve cancelled/deferred/blocked states instead of dropping work.
- Scope, non-goals, settled decisions with rationale, actual permission and
  delivery boundaries. A handoff describes authorization; it cannot create it.
- Repository-relative source pointers, branch/base/candidate and relevant content
  identity for uncommitted work. List intended changed/new files and preserved
  unrelated changes. A HEAD SHA alone does not identify a dirty candidate.
- Selected methods and instruction identity, meaningful work performed, evidence
  and remaining acceptance gates. Separate local tests, CI, provider review and
  native runtime observations. Link shareable evidence; label unavailable local
  artifacts instead of claiming another host can access them.
- Blockers, pending owner decisions with recommendation/consequence, exact next
  safe action, rollback/recovery and task-owned running operations. Record their
  side-effect status before another agent might repeat them.
- Requested and observed harness/model settings when material, with unverified
  values marked honestly. The receiving harness resolves its own tools/profiles.
- Local/cloud availability: local-only, committed-not-pushed, pushed-and-observed,
  or unknown; verified remote branch/commit and observation time where available.

Planned tasks contain the intended outcome, dependencies and acceptance, with
execution and verification explicitly not started. In-progress tasks retain
partial results and unresolved failures. Completed tasks record acceptance evidence,
delivery boundary and residual limitations; implementation complete is not the
same as required review passed or deployment complete. Keep completed records
discoverable so later tasks can reuse decisions and still-valid evidence.

## Update at meaningful transitions

Create or reconcile records when the approved plan enters execution. Update the
affected record when a task starts, its scope/authority/dependencies change, a
material checkpoint or blocker is reached, it completes, or it is paused/handed
to another harness. Before an intentional switch or context-loss boundary,
checkpoint current work and identify the receiving agent's first action.

Do not rewrite every task after every tool call, copy transcripts, or archive
private reasoning. Update only changed facts; preserve useful examples and
decision rationale. Redact credentials, personal data, machine-specific paths and
private logs from versionable documents. Use repo-relative paths and authorized
durable artifact URLs. Missing accessible evidence remains a resume limitation.

## Git and GitHub are the same document history

Include these sanitized records in the normal authorized commit/PR route, alongside
their task changes. Do not maintain a separately edited GitHub copy or auto-create
issues, comments, branches, hooks or sync services. Do not force-add ignored files.
Repository publication restrictions still govern: without commit/push authority,
write the local records and clearly report that GitHub has not received them.

Before claiming cloud availability, verify the remote branch/commit and the actual
handoff path/content on that revision. A push command or an old PR link alone is
insufficient. Keep the verified remote revision in the receiving handoff/receipt;
do not create an endless series of commits merely to embed a document's own commit
SHA. Content identity or the containing revision supplies that binding.

Before switching machines, unpushed code/evidence must be transferred through an
authorized route or remain explicitly unavailable. A document describing a dirty
patch does not transfer the patch. Continue preparation locally if publication is
blocked; never tell the next harness it can resume absent files.

## Resume and reconcile

Read repository instructions, the index, authoritative task state and the selected
task record first. Fetch/pull only within authority and without overwriting local
work. Compare local/remote revisions, current diffs, evidence identity, running
operations and permission freshness before acting. A newer timestamp alone does
not resolve divergent histories. Merge evidence and decisions against actual source;
raise only a genuine owner-decision conflict and retain both sides until resolved.

Select only relevant skills for the next action. Recheck changed prerequisites and
affected evidence, retain valid completed work, and keep the same task ID and owner
contract. Do not rerun all completed tasks or assume another harness shares tools,
credentials, processes or model settings. Report missing required evidence as a
blocker at its boundary and continue independent authorized work.
