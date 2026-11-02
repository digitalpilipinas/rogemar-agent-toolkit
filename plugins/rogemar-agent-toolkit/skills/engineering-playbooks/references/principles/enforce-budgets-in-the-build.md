# Budgets in the build

A performance or size goal that only lives in a document drifts. Make the build
or the local CI entrypoint fail when it is exceeded: bundle or download size,
startup time, frame time under a fixed load, query count per request, or binary
size. Measure it the same way on every run and print the measured value and the
limit.

Set the limit from a measured baseline plus a stated margin, not a guess, and
record who may raise it. A budget check that is flaky under load belongs in a
controlled run, not in every pre-push. Raising a limit is a decision the owner
records, not a fix. Use [Explain the Number](explain-the-number.md) when a
result is close to the limit.
