# Workflow Integration Contract

## Ownership

Project learning is a post-task evidence consumer and curator. It is not a planner, implementer, reviewer, release manager, or orchestrator.

- `workflow-orchestrator` remains the only lifecycle and delegation owner.
- `first-time-right-delivery` and `deliver-approved-programme` may produce evidence that capture summarizes, but they do not persist lessons.
- `create-plan` remains read-only. The Stop hook skips `permission_mode: plan` and explicit no-write requests.
- Capture cannot edit product files, task plans, delivery status, existing skills, global AGENTS.md, or Codex memory.
- A normal task agent may include a task-local `Learning note:` in its own final response when the current task establishes a verified reusable rule. That note is communication only; it does not create, approve, or activate a project lesson.

No existing skill needs a project-learning call. The project Stop hook is only a passive queueing point; capture and review are explicit workflows, optionally performed in a dedicated project-learning task.

## Instruction Precedence

Apply accepted lessons only when relevant. Resolve conflicts in this order:

1. Current system, developer, and user instructions.
2. Current repository contracts, source, tests, and verified runtime evidence.
3. Accepted project lessons.
4. Candidate lessons, which are never instructions.

When an accepted lesson conflicts with current evidence, do not silently apply it. Propose that it be reviewed or superseded.

## Hook Coexistence

Codex runs all matching hook handlers. The project-learning Stop handler therefore:

- Never blocks the current task or emits a model continuation prompt.
- Records only bounded session, turn, signal, milestone, and transcript-path metadata in the ignored queue for a dedicated learning task.
- Immediately allows `stop_hook_active: true`.
- Does not assume it is the only Stop hook.
- Fails open on errors and timeouts.
- Does not use `SessionEnd` for model-assisted synthesis.

The optional dedicated learning task owns source-turn inspection, candidate capture, review, and promotion. A queued signal or task-local note is not itself an accepted lesson and must not change the source task's delivery status.

Project hooks must be reviewed through `/hooks`. Never bypass hook trust.

## Cross-Project Adaptation

Adaptation is target-specific and advisory. Read only accepted source entries, inspect the target, classify applicability, and wait for approval. Preserve source project and lesson IDs. Never copy a source ledger wholesale or create a global catalog automatically.
