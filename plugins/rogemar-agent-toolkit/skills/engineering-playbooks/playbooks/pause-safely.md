# Pause safely

Create a durable checkpoint when the user explicitly asks to pause. Compaction alone does not end active work; keep going requests remain active.

1. Stop new assignments and finish or safely suspend the current bounded operation. Ask the orchestrator to interrupt workers when appropriate and reconcile partial changes. Preserve the real state even if tests are currently failing; do not hide it with an unrelated rewrite.
2. Save a concise task-local checkpoint: original goal, approved scope, current branch/head and diff, owners, completed evidence, blockers, active processes, next action, and relevant paths. Reuse an existing decision trail.
3. Do not commit, push, publish, delete or alter credentials merely to pause. If a specific durable commit is already authorized, stage only reviewed task paths and report its actual result.
4. Verify the checkpoint and artifacts exist. Report what is saved, what remains unverified, and the first resume action. `session-pickup.md` uses this evidence at restart rather than assuming agent persistence.
