# Verification efficiency

Select verification by the claim, changed behavior and acceptance boundary.
Project records own runtime versions, destinations and retention durations.
This method changes neither review providers nor required acceptance gates.

## Cadence

- A commit or review comment alone is not a full simulator, device, UI or
  compatibility-matrix trigger. Keep all explicit commit-time static, unit,
  hook and CI requirements.
- During edits, use the cheapest check that can fail for the changed behavior:
  static or compile checks, focused unit or contract tests, and interaction or
  runtime checks when needed.
- A fix first runs its discriminating regression, then affected adjacent
  checks. A text-only or non-runtime correction does not automatically trigger
  UI QA. Do not weaken a meaningful failing regression to reduce work.
- Batch coupled corrections before expanding coverage. Reserve complete-candidate
  gates for a complete candidate, not an increment still awaiting approved work.
- At that boundary, run affected integrated regressions and changed user journeys
  on the project's primary target, plus every applicable explicit gate.
  Compatibility follows changed risk, known failures and project requirements;
  do not postpone all compatibility concerns until product completion.
- Honor task-specific destinations and valid evidence. Do not rerun accepted
  work solely to relabel it under a new default runtime.

## Repeated failures

Classify each failed attempt as application behavior, fixture or prerequisite,
automation, runner infrastructure, or unclear. A launch that never starts the
test runner is infrastructure-blocked, not an application result.

- Verify the fixture's starting account, data and route before repeating a
  whole journey. Isolate selector, focus or gesture failures before expanding.
- Reproduce data-integrity and authorization defects at the cheapest valid
  boundary, retain the regression, then verify the affected real journey.
- After a second similar unexplained failure, stop repeating that invocation.
  Record what changed, the hypothesis and the discriminating observation the
  next attempt must obtain in the existing task receipt.
- No automatic retry, OS rotation, longer waits or resets without a reasoned
  discriminating purpose. This stops repetition, not the approved task; the
  failed gate remains failed or blocked while safe independent work continues.

## Evidence selection and inspection

- Logic and data: executed assertions, relevant outputs and observed side effects.
- Interaction: executed actions and observed behavior, not just a final image.
- Appearance: targeted inspected screenshots of the affected required states.
- Motion, gestures, flicker or timing: a short deliberately selected recording
  or trace answering a named question.

For configurable capture, explicitly set screen video and diagnostic traces off
during routine iterations. Opt in for a required claim or focused diagnosis.
Document actual SDK defaults truthfully; a usage override does not change them.
Some tools return screenshots automatically. Avoid duplicate requests rather
than claiming that an instruction disables the tool's response format.

Preserve useful failure attachments. Retain-on-failure may still record every
attempt before discarding passing media; it does not eliminate capture overhead.
Keep replayable action caches separate from screen video and diagnostic traces.

Record capture state separately from inspection state. A screenshot, log, trace
or video file existing does not mean it was inspected. Describe the actual
observation and its limitations. Pixels do not prove data integrity; text and
accessibility assertions do not prove every visual property.

## Human evidence handoff

At completion, pause, a blocked handoff or an owner decision, include only
relevant screenshots and recordings in the existing human-facing report. Give a
descriptive clickable file or authorized artifact link, the claim or question,
and the feature, platform, state and candidate/build when needed. Label each
`inspected`, `partially inspected` or `captured but not inspected`; state the
actual observation and limitation. Name the retention disposition and relevant
finding ID where applicable. A saved file is not an inspected observation.

Check that a local file exists before linking it; use the host's supported link
format. Report missing, expired or inaccessible artifacts, including those not
accessible to a receiving host. Do not claim a link is usable without checking
what the current environment can verify. Do not upload, capture extra media, or
share private paths, credentials or sensitive logs merely for a handoff. Prefer
authorized durable links in versionable records; use local links only in an
appropriate private report. An inline preview is optional, not a substitute for an
accessible link where supported.

## Safe reuse and invalidation

Reuse only within valid source and dirty-snapshot, test, fixture, toolchain,
artifact, configuration, destination and prerequisite bindings. Changed inputs
invalidate associated evidence even when application source is unchanged.
Historical results inform selection, not a pass for changed source. Refresh
exact-candidate gates under their existing identity and freshness rules.

Preserve incremental build state and reserved destinations when valid. Reuse
build-for-testing artifacts only after verifying source, configuration,
toolchain, test artifact and destination compatibility. No routine clean,
dependency resolution, reset or blind cross-runtime reuse.

## Capture, teardown and retention

Keep full logs private and model-facing summaries bounded. A child exit code,
saved artifact or selected command is not acceptance; inspect actual executed
cases, failures, skips and required observations.

For selected recording, name the owned capture handle/process and its stop
operation. Stop only owned capture/test resources on success, failure or
interruption; preserve evidence through teardown. Never kill by process name
or stop another session's services.

Assign retention ownership, disposable intermediates, protected pins and the
owner who may release a pin. Required final proof, unresolved failures and audit
or legal evidence remain pinned. Project policy decides eligibility duration;
missing acceptance or delivery facts do not make an artifact disposable.

Cleanup may run within an existing explicit owner-approved policy covering the
artifact paths, eligibility and pins; do not request approval again for each
covered batch. Without that authority, preview candidates and obtain scoped
approval before deletion. Use the [project retention template](evidence-retention-template.md)
when a project has no policy. A template alone grants no deletion authority.
Verify an accessible replacement
archive before retiring a needed local copy; a hash cannot replace the artifact.
Never prune inside opaque result bundles blindly. Replay caches have their own
validity/privacy lifecycle and are not media cleanup.
Human review does not release a protected pin. Before an authorized cleanup,
recheck ownership, active writes and pins, then report deleted, retained and
failed items. Mark deleted evidence unavailable in its finding/receipt, preserving
its description, resolution history and cleanup receipt. Missing authority or
uncertain eligibility means retain and report.

## Instruction scenarios to check

- A narrow logic fix: focused unit or contract checks, no UI media.
- A visual layout correction: targeted screenshots, actually inspected.
- A motion or failure diagnosis: a short recording or trace selected for the
  question, followed by owned teardown.
- An infrastructure launch blocker: blocked, not application failure or pass.
- A changed source or fixture that invalidates a previously green result.
