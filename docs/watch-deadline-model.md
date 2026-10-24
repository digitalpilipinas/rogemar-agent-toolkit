# Polling deadline verification pilot

This pilot checks one property: a watcher-owned sleep does not exceed the
remaining positive timeout. It does not prove wall-clock completion by the
deadline, since in-flight GitHub reads and scheduling delays are outside the model.

## Correspondence and source identity

- Implementation: `plugins/rogemar-agent-toolkit/skills/codex-forge/scripts/watch-pr/policy.ts`, `pollUntilTerminal`, normal sleep and query-retry sleep.
- Source baseline: `3cdfb485dd8d9bbfd0caeff3c8f091c0479dda16` with uncommitted changes.
- Reviewed implementation SHA-256: `02bd52cbb63e666fe7b8ec0db34e7aa0646e9f89b2e0d8c1cfb8429b1f686593`.
- Model: `tests/test_watch_deadline_model.py`, `sleep_transition`.
- Implementation replay: `deadline.test.ts` beside the production loop.
- Last confirmed synchronization commit: unset; this model and fix are uncommitted.
  The content digest above identifies the reviewed implementation. Recheck it and
  the mappings after relevant edits; a future commit alone does not prove sync.

## Finite domain and assumptions

Exhaust 1,764 one-step transitions: timeout 1..7 seconds, elapsed 0..timeout+2,
query duration 0..3, requested sleep 1..9. Time is monotonic and modeled in whole
seconds; requests finish and clocks advance deterministically. Retry and ordinary
polling both choose a requested sleep before applying the same remaining-time cap.
The property constrains the sleep, not elapsed time already consumed by a query.
Timeout zero is tested separately as intentionally unbounded.

This is exhaustive finite transition exploration, not an unbounded proof or
concurrency/liveness qualification. It excludes fractional clocks, wall-clock
jumps, network cancellation, GitHub correctness and deployed scheduling behavior.
No external model-checker installation is needed.

## Counterexample and executable checks

The original defect has the trace: start at 0, remain pending, request a 60-second
sleep with timeout 5, resume at 60. The corrected trace sleeps 5. The abstract
mutant also produces bounded-domain counterexamples, including timeout 5 and
requested sleep 9 ending at 9.

Run:

```sh
python3 -B -m unittest discover -s tests -p test_watch_deadline_model.py
bun test plugins/rogemar-agent-toolkit/skills/codex-forge/scripts/watch-pr/deadline.test.ts
```

The production runner tests cover single PR, stack, queued stack and query retry
across three timeouts and three intervals, plus unlimited timeout and time spent
reading status. They assert the remaining budget at each sleep and final timeout.
The baseline run failed all 36 bounded cases. In an isolated copy, removing only
the two production sleep caps reproduced 36 behavioral failures while the
unlimited-timeout case passed; the mutation diff was inspected before the run.
The original working candidate was not mutated. This demonstrates sensitivity
to this defect, not broad watcher correctness or hosted-service qualification.
