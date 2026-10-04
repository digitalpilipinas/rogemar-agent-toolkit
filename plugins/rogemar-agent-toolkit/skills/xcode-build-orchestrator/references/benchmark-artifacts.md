# Benchmark artifacts (toolkit schema 2.0.0)

Each run owns `.build-benchmark/run-<unique-id>/benchmark.json` and all phase logs.
Use the printed exact path; do not guess a timestamp or pick another run's latest file.
Evidence survives cleanup of the run-owned temporary DerivedData child. The optional
`--derived-data-path` selects an existing parent, never a directory to erase.

`status` is `complete` only after every required phase succeeds. `phases` preserves
settings, warmup, clean preparation and measurement results including failures.
`runs` separates clean, incremental and optional cached-clean measurements. `repeats`
records expected measured runs per type. `incremental_kind` is `edit` when a source
was touched, otherwise `zero-change`. Commands are argument arrays; no shell is used.
Missing measurements have a null median, never a fabricated zero-second success.

Clean means `xcodebuild clean` followed by build; it does not prove a cold system
compilation cache. Cached-clean removes only this run's DerivedData after warming
an enabled cache. Record actual cache conditions before comparisons. Wall time is
elapsed user wait; cumulative parallel task times do not establish the critical path.
Report repetitions, spread, executed work and error counts. Failed/incomplete artifacts
cannot establish a baseline or speedup. Generic upstream performance percentages do
not predict this project's benefit. Use matching inputs and measured justification.

For the field contract see [the schema](../../xcode-build-benchmark/schemas/build-benchmark.schema.json).
