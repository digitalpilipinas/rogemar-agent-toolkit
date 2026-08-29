# Project Learning Operations

## Initialization

Resolve the target with `git rev-parse --show-toplevel`. Before writing, inspect `AGENTS.md`, `.gitignore`, `.codex/hooks.json`, and any existing project-learning files.

The initializer owns only:

- The bounded Project Learning block in root `AGENTS.md`.
- The project-learning Stop handler inside `.codex/hooks.json`.
- `.codex/hooks/project-learning-stop.py`.
- `.codex/project-learning/config.json`.
- The passive project-learning queue directory configuration.
- `docs/project-learning/lessons.md` when absent.
- Two exact `.gitignore` entries for candidate and state data.

It must preserve every unrelated byte where practical. It may append a missing JSON handler but must not replace existing hook groups. Partial markers, invalid JSON, or a different handler that already names `project-learning-stop.py` are conflicts: stop and report them.

The project-learning Stop handler is passive. It may queue bounded source-turn metadata for a dedicated learning task, but it must never block the active task or request model-assisted capture inline.

Run initialization twice during validation. The second run must report no changes.

## Capture Requests

Create a JSON request in `.codex/project-learning/state/<session>-<turn>-capture.json`. Use only the fields defined in `schemas.md`. Then run:

Run these commands from the `project-learning` skill directory so the bundled
script path resolves on every supported machine.

```bash
python3 -I scripts/candidate_store.py capture \
  --root "$(git rev-parse --show-toplevel)" \
  --request <request-path>
```

If the signal was a false positive, run:

```bash
python3 -I scripts/candidate_store.py mark-no-candidate \
  --root "$(git rev-parse --show-toplevel)" \
  --session <session-id> --turn <turn-id>
```

Never put transcript text or quotes in the request. Evidence summaries describe the observed result; they do not reproduce chat or tool output.

Queued source-turn metadata is a review cue only. A dedicated learning task must inspect the source turn and current repository evidence before creating a capture request.

## Review and Promotion

List materialized pending candidates as JSON. Propose a batch and wait for approval. For each approved candidate, create a promotion request following `schemas.md`, then run `candidate_store.py promote`. For rejected candidates, run `dismiss` with the approved candidate ID.

Promotion appends one bounded Markdown entry and one `promoted` event. Re-running the same promotion is idempotent. A candidate cannot be promoted when its evidence does not exist, its record fails validation, or it contains sensitive-looking material.

## Review Reminders

A capture result may return `review_due: true`:

- Once when the pending count enters each group of five.
- Once for each distinct milestone turn.

Mention the review availability in one sentence. Do not start review or activate lessons automatically.

## Failure and Rollback

Learning is fail-open. A hook parse error, missing transcript, disabled config, or failed validation must allow the task to finish. Report persistent setup failures, but do not retry indefinitely.

Disable learning by setting `enabled` to false through the initializer. Do not delete hooks, candidates, or lessons unless the user separately authorizes deletion.
