# Method compliance measurement (1.3.0 release acceptance)

Purpose: measure whether agents use the skills a task calls for, per harness, before
and after 1.3.0's readiness entry, enforced receipt and hooks. It follows the Forge
Eval playbook (`claude-forge/playbooks/eval.md`): blind candidates, organic prompts,
scoring from observed behavior, never from self-report. This file stays out of every
candidate's workspace.

Status: protocol ready; runs pending. They need installed builds in real Claude,
Codex and Cursor sessions, so they happen after 1.3.0 is pushed and installed, and
before the owner tags 1.3.0.

## Fixture

A small, sanitized iOS project with a SwiftUI screen, a local save queue with retry,
and a Supabase migration folder. Use project-shaped names only. Commit it to a
scratch repository the candidate can clone; never to this repository.

## Task prompt (identical for every run)

> On the notes screen, when saving fails, show a banner that lets me retry or keep
> both versions. Keep the existing retry queue working, and add the database column
> we need to remember which version I kept.

Expected required methods (from `receipt_tags`): the SwiftUI group
(`swiftui-expert-skill` / `swiftui-pro`), `supabase-guardian`, and, because the retry
queue is state-heavy, the statechart and formal-verification sequence when the
agent models it. Process expectations: readiness at start, the slice-start
announcement, and a complete method receipt.

## Arms

| Arm | Toolkit | Hooks |
| --- | --- | --- |
| Baseline | 1.2.2 (`036243c` or the last pre-1.3.0 commit) | none |
| 1.3.0 | the pushed 1.3.0 candidate | none |
| 1.3.0 + hooks | the pushed 1.3.0 candidate | Claude readiness hooks installed |

Run each arm three times per harness (Claude, Codex, Cursor; hooks arm on Claude
only), each in a fresh session with the same model settings the owner normally uses.

## Scoring (from transcripts and artifacts)

For each expected method group, record exactly one outcome:

- **used**: the transcript shows the skill opened and its method applied, and an
  artifact (review notes, test, commit) reflects it;
- **reasoned**: recorded as unavailable, blocked or not applicable, with a reason;
- **skipped**: neither. This is the failure the release targets.

Also record: readiness ran (yes/no), announcement made (yes/no), receipt complete
(yes/no), defects later found by an independent review, and wall-clock time.

Compliance rate per run = (used + reasoned) / expected groups. Report each arm's
median and range; three runs show direction, not statistical significance.

## Record

| Harness | Arm | Run | Expected | Used | Reasoned | Skipped | Readiness | Announced | Receipt | Review defects | Minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Acceptance

- Results are recorded here with transcripts kept as evidence outside the repository.
- One real EVERSO slice runs on 1.3.0 as a pilot, with its receipt and findings.
- Release notes state the measured rates and their limits; nothing is claimed that
  was not measured. If Claude still skips methods more than other harnesses, the
  owner decides whether the hooks become the recommended Claude default.
