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

`--capture-mode workflow` enrolls checkpoint capture without creating or changing hooks. Omit the flag to preserve an existing capture mode; new default installations use explicit capture. A mode change updates only the marked policy block and mode field. Never overwrite a nonempty accepted ledger.

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
- At a milestone only when pending material has changed since the last reminder. New turns alone do not earn repeated reminders.

Mention the review availability in one sentence. Do not start review or activate lessons automatically.

## Failure and Rollback

Learning is fail-open. A hook parse error, missing transcript, disabled config, or failed validation must allow the task to finish. Report persistent setup failures, but do not retry indefinitely.

Disable learning by setting `enabled` to false through the initializer. Do not delete hooks, candidates, or lessons unless the user separately authorizes deletion.

## Enrolled checkpoint commands

Use the absolute bundled script path while running from the target repository. Enrollment:

```sh
python3 -I <skill-dir>/scripts/initialize_project.py --root <repo> --capture-mode workflow --check
python3 -I <skill-dir>/scripts/initialize_project.py --root <repo> --capture-mode workflow
python3 -I <skill-dir>/scripts/validate_project.py --root <repo>
```

Capture structured JSON through stdin (no shell interpolation of lesson content):

```sh
python3 -I <skill-dir>/scripts/candidate_store.py capture --root <repo> --workflow --permission-mode execution --request -
python3 -I <skill-dir>/scripts/candidate_store.py mark-no-candidate --root <repo> --workflow --permission-mode execution --session <native-id> --turn <native-id> --milestone
```

Add `--read-only` or `--no-learning`, or use `--permission-mode plan`, to skip persistence. Disabled or unenrolled workflow calls also skip. Omitted permission mode on workflow calls is an error. Capture failures return nonzero for diagnosis; the caller records a learning failure and continues delivery. Never chain capture success to product acceptance.

For global proposals, run capture against the canonical toolkit repository with `--source-root <source-repo>` and the schema's proposal fields. Read the accepted source entry and current target skill before composing the proposal. The CLI checks source status and bounded paths; it does not execute the validation description. Approval is still required before promotion or any skill edit.
