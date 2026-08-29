---
name: project-learning
description: Initialize and maintain project-local continuous learning, review captured lesson candidates, or adapt accepted lessons between repositories. Use for project learning setup and curation, not ordinary coding work.
---

# Project Learning

Maintain durable, evidence-backed project lessons without turning unreviewed chat content into instructions.

## Boundaries

- Keep learning project-local. Never write Codex memory, global AGENTS.md, or another project's files unless the user explicitly requests adaptation into that target.
- Treat candidates as inactive. Only user-approved entries in `docs/project-learning/lessons.md` are usable guidance.
- Current user instructions, repository contracts, tests, and verified current evidence override accepted lessons.
- Never persist raw transcripts, hidden reasoning, tool output, secrets, credentials, personal data, or quoted conversation text.
- Do not delegate or invoke workflow skills. `workflow-orchestrator` remains the lifecycle and delegation owner.
- Normal task chats must not be interrupted for learning. The project Stop hook is a passive signal collector; it may queue bounded turn metadata, but it must never block, prompt, or emit a continuation request.
- A normal task may include an optional final `Learning note:` summarizing one verified, reusable rule from that task. This is communication in the source chat, not candidate capture, approval, or accepted project guidance.
- In capture mode, edit only `.codex/project-learning/candidates.jsonl` and `.codex/project-learning/state/`. Never edit product code or the accepted ledger.

## Select a Mode

### Initialize

Use when asked to initialize continuous project learning in a repository.

1. Read [references/operations.md](references/operations.md).
2. Run `scripts/initialize_project.py --check --root <repository-root>`.
3. If the check reports no ambiguity, run it again without `--check`.
4. Run `scripts/validate_project.py --root <repository-root>`.
5. Tell the user that project hooks require review through `/hooks` and a fresh Codex task after installation or hook changes.

### Optional dedicated learning task

Use a dedicated project-learning task/chat only when batch capture, cross-task review, or approval is useful. It is optional and is not required for every task chat. It may process passive signal records under `.codex/project-learning/state/queue/` from other task chats, but a signal or task-local `Learning note` is only a review cue, not proof that a project lesson should be accepted.

1. Review queued source-turn metadata in the dedicated task; select only turns whose repository evidence can be inspected.
2. For each selected turn, inspect the recorded source transcript and current repository evidence without copying raw transcript text into candidates.
3. Capture at most one durable lesson per source turn, or mark it as having no candidate.
4. Present pending candidates in the readable format below and wait for explicit user approval before promotion.
5. Leave the source task's outcome, files, plan, and delivery status unchanged.

The Stop hook does not open or route a new task/chat automatically. The owner starts or continues the optional dedicated learning task when batch review is appropriate.

### Task-local learning note

When the current task produces a verified, durable project rule, the normal task response may end with:

```text
Learning note: <one plain-language sentence derived from this task>
```

Include it only when the rule is genuinely reusable and supported by the task's visible evidence. Omit it for one-off details, unverified suggestions, or when the user opts out. Do not include raw transcript text, internal metadata, candidate IDs, or approval language. The note does not write the candidate store; the passive hook and any later capture/review workflow remain separate.

### Capture

Use in the dedicated learning task or when the user explicitly asks to harvest a specific task. Do not use Capture as an automatic continuation of an ordinary task chat.

1. Read [references/schemas.md](references/schemas.md).
2. Inspect only the completed visible turn and current repository evidence.
3. Decide whether there is one durable, project-relevant lesson. State the lesson as one plain-language sentence describing one reusable decision rule. Keep trigger conditions in `applies_when`, exceptions in `does_not_apply_when`, and proof in `evidence`; do not pack those details into the lesson. One-off task details, unsupported AI suggestions, summaries of work, and facts already covered by an accepted lesson are not candidates.
4. Write a structured capture request under `.codex/project-learning/state/` and run `scripts/candidate_store.py capture`. If nothing qualifies, run `scripts/candidate_store.py mark-no-candidate`.
5. Return the dedicated learning task's outcome with the compact capture receipt described below. Mention a pending review only when the script returns `"review_due": true`, and follow any higher-priority instruction about whether to emit a learning marker.

### Review

Use when asked to review pending lessons or after the user accepts a review cue.

1. Read [references/schemas.md](references/schemas.md) and [references/operations.md](references/operations.md).
2. Run `scripts/candidate_store.py list --status pending`.
3. Present a compact batch using the readable format below. If a proposed lesson is dense or combines multiple rules, show an edited one-sentence lesson and preserve the supporting detail in the boundaries or evidence. Include the recommended action: accept, edit, or dismiss.
4. Do not modify the ledger until the user approves specific candidate IDs or an explicit batch.
5. After approval, use `promote` or `dismiss`, then validate the project.

### Adapt

Use when asked to evaluate accepted lessons from another repository.

1. Read [references/schemas.md](references/schemas.md) and [references/integration.md](references/integration.md).
2. Read only accepted source-ledger entries and inspect the target repository's current contracts and conventions.
3. Classify each source lesson as applicable, adaptable, irrelevant, or conflicting.
4. Present proposals with source provenance. Write nothing until the user approves specific adaptations.
5. After approval, capture each adapted lesson as a target-project candidate and promote it with the recorded source project and lesson ID.

### Status, Enable, or Disable

- Status: run `scripts/validate_project.py` and `scripts/candidate_store.py status`.
- Enable or disable: run `scripts/initialize_project.py --set-enabled true|false`, then validate.
- Disabling is reversible and does not delete candidates or accepted lessons.

## Readable lesson and output format

Every candidate and accepted lesson has one actual lesson: a concise, plain-language sentence that states the reusable rule. Do not combine the rule, its exceptions, evidence, test output, and task summary into that sentence.

Present candidates and capture results in this order:

```text
Candidate: PL-...
Lesson: <one plain-language sentence>
Applies when: <concrete trigger>
Does not apply when: <concrete boundary>
Evidence:
- <kind> — <repository-relative reference and short paraphrase>
Recommended action: Accept | Edit | Dismiss
```

The task-local note is intentionally shorter and separate from this candidate format; use `Learning note:` for source-chat communication and `Lesson:` for a structured candidate or accepted entry.

For capture completion, use `Captured candidate <id>.` followed by `Lesson: <sentence>`. Add `Review: pending` only when the capture result has `review_due: true`. Do not expose raw event JSON, internal fingerprints, or tool logs in user-facing output.

## Project Contract

Read [references/integration.md](references/integration.md) when changing hook behavior, project paths, review triggers, or integration with other skills.
