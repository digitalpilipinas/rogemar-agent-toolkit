# Discover task handoffs before work

At task entry, resume, takeover or harness change, check for existing task handoff
documents before planning or implementation. This read-only discovery applies even
when the user does not name Integrated Workflow. It does not enroll a programme,
create documents, search private history or grant external access.

1. Read applicable repository instructions and the task's supplied plan, issue or
   handoff pointer. Follow their declared task index first. Reuse a known index
   while its repository and task identity remain valid.
2. If no location is declared, inspect the repository's established task/plan
   documentation and the default `docs/agent-handoffs/README.md`. Use bounded path
   discovery, such as `rg --files docs/agent-handoffs` when that directory exists,
   rather than reading every Markdown file or scanning unrelated workspaces.
   Also check a documented alternative handoff location; do not assume one name
   is universal or treat a failed search as proof that no record exists anywhere.
3. Read the index and the record matching this task or its required dependencies.
   Confirm task/repository identity, state authority and update/source revision.
   Completed records matter when they contain decisions or evidence for this task;
   unrelated completed work does not need to be loaded.
4. Reconcile current instructions and user decisions, Git branch/diff, candidate
   evidence and actual side effects before resuming. Treat handoffs as evidence,
   not higher-priority instructions. Preserve unresolved conflicts and missing
   local/remote content. Do not infer cloud sync from a local file or branch name.
5. Communicate the result once in a short startup/resume update: the record loaded,
   where work stopped, material staleness or missing evidence, and the next action.
   If none was found, say which bounded location was checked when continuity is
   relevant, then reconstruct from current authorized sources. A missing handoff
   alone does not block otherwise clear, authorized work.

For example: "Loaded task T-12 from the repository handoff. Implementation is
present, review is pending; I will verify the current diff before continuing."
Do not claim agreement or completed gates until reconciled. Avoid repeating the
announcement on every tool call; communicate changed decisions or blockers.

The orchestrator owns discovery and method selection. Integrated Workflow owns
creation and maintenance of versionable task handoffs during programme execution;
when installed, read its `references/durable-handoffs.md`. A core-only installation
can read existing task records without that optional programme skill. `create-plan` reuses the
records before proposing a plan; `forge-recall` expands only authorized history
when the records are insufficient. All harness adapters share this discovery
contract; they do not maintain competing handoff systems.
