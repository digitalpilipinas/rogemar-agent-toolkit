# Workflow Integration Contract

## Ownership

Project learning is a post-task evidence consumer and curator. It is not a planner, implementer, reviewer, release manager, or orchestrator.

- `workflow-orchestrator` remains the dispatcher and delegation owner; explicitly invoked `integrated-workflow` owns the approved delivery lifecycle.
- `first-time-right-delivery` and `integrated-workflow` produce evidence and invoke candidate-only capture at explicitly enrolled workflow checkpoints; they never approve or activate lessons.
- `create-plan` remains read-only. The Stop hook skips `permission_mode: plan` and explicit no-write requests.
- Capture cannot edit product files, task plans, delivery status, existing skills, global AGENTS.md, or harness memory.
- A normal task agent may include a task-local `Learning note:` in its own final response when the current task establishes a verified reusable rule. That note is communication only; it does not create, approve, or activate a project lesson.

Explicit-capture projects retain their current behavior. Enrolled workflows call the existing candidate store at completion, using native-neutral source IDs and explicit permission/no-write guards. The Stop hook remains an optional passive queue; workflow enrollment does not install it. Review and promotion always require approval. Capture errors cannot change the source task's delivery status.

## Instruction Precedence

Apply accepted lessons only when relevant. Resolve conflicts in this order:

1. Current system, developer, and user instructions.
2. Current repository contracts, source, tests, and verified runtime evidence.
3. Accepted project lessons.
4. Candidate lessons, which are never instructions.

When an accepted lesson conflicts with current evidence, do not silently apply it. Propose that it be reviewed or superseded.

## Hook Coexistence

The passive Stop handler is a Codex hook; other harnesses use enrolled workflow capture and install no hook. Codex runs all matching hook handlers. The project-learning Stop handler therefore:

- Never blocks the current task or emits a model continuation prompt.
- Records only bounded session, turn, signal, milestone, and transcript-path metadata in the ignored queue for a dedicated learning task.
- Immediately allows `stop_hook_active: true`.
- Does not assume it is the only Stop hook.
- Fails open on errors and timeouts.
- Does not use `SessionEnd` for model-assisted synthesis.

An enrolled source workflow may capture candidates; a user-requested dedicated learning task may inspect queued turns and curate them. Promotion remains user-controlled. A queued signal or task-local note is not itself an accepted lesson and must not change the source task's delivery status.

Project hooks must be reviewed through `/hooks`. Never bypass hook trust.

## Cross-Project Adaptation

Adaptation is target-specific and advisory. Read only accepted source entries, inspect the target, classify applicability, and wait for approval. Preserve source project and lesson IDs. Never copy a source ledger wholesale or create a global catalog automatically.

## Checkpoint integration

The dispatcher selects the skill; this skill never calls back into the workflow. At a verified completion use `capture --workflow --permission-mode execution --request -`, or `mark-no-candidate` with the same guards and native session/turn IDs. Planning, read-only, no-learning, disabled and unenrolled cases return before writing even a lock or state directory. Do not write a request file before checking these conditions. Store mutations share a two-second bounded OS lock; timeout/error is nonblocking for delivery.

Use accepted lessons as evidence for a proposed canonical skill improvement, never as permission to apply it. The `proposal` fields record target and allowed scope. `--source-root` verifies an accepted/reinforced source-ledger entry with verified/reinforced evidence; the owner must additionally inspect the actual evidence and target applicability. The CLI cannot infer either from an evidence label. Proposals remain inactive until reviewed and do not modify skills.
