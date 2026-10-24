# Bounded formal verification

Use selectively for a consequential state, retry, locking or synchronization
property when ordinary examples leave important state combinations unexplored.
The existing implementation owner owns the code; `code-review-tests` contributes
evidence to the same review. This method creates no second acceptance authority.

For a new reusable project check, select `formal-verification-create`. For drift in an existing check, select `formal-verification-maintain`. For TLA+ or agreed statechart conversion and understandable counterexamples, select `statechart-verification`. These are optional engineering-pack methods: resolve them through the routing index and report an unavailable method explicitly; the bounded method below remains usable with available tools. Load only the relevant method; this contract remains the common evidence standard.

## Create one useful model

1. Name one observable invariant and the failure it prevents. Separate safety
   (something bad never happens) from liveness (progress eventually happens).
   Name fairness and environment assumptions needed for a liveness claim.
2. Map model state, actions, guards and effects to actual symbols and boundaries.
   Record source revision, content digest for uncommitted inputs, covered symbols,
   model/tool version and the last confirmed synchronization commit. Mark that
   commit unset for an uncommitted new model; do not invent synchronization.
3. Define finite bounds: actors, states, values, sequence depth and environment
   outcomes. Explain exclusions. A statechart can clarify legal transitions and
   forbidden events, but drawing it alone is not verification.
4. Use an available appropriate checker or an exhaustive finite-state explorer.
   Record the command, explored domain/states, result and termination reason.
   Random samples, hand-picked examples and an interrupted search are not an
   exhaustive proof. Missing tools leave the model draft; installation is separate.
5. Confirm sensitivity using the [mutation method](mutation-evidence.md). A relevant
   broken model must violate the property; a broken implementation must be caught
   by the corresponding implementation check before claiming code coverage.
6. Translate each counterexample into an understandable sequence of events and
   replay it against the real implementation where safe. Classify a failed replay
   as a model/code mismatch, unmet assumption or unresolved evidence, not an
   established product bug. Retain all relevant counterexamples.

Completion is a bounded result with executable artifacts, code correspondence,
mutation evidence, replay outcome and limitations. A model result never proves
unmodeled deployment, authorization, UI or external-service behavior.

## Maintain correspondence

On changes to covered symbols, assumptions, bounds or tooling, inspect the actual
diff, update the model only to reflect intended behavior and rerun affected checks
and counterexamples. Distinguish specification drift from an implementation defect;
do not weaken an invariant to make a regression pass. Advance synchronization
metadata only after correspondence and checks are confirmed. Preserve the old
counterexample as regression evidence when relevant.

## Small pilot: polling deadline

A useful first property is: a watcher-owned sleep never exceeds the remaining
positive timeout. States include elapsed time and pending/retry outcomes; the
sleep transition advances elapsed time. Timeout zero is explicitly unbounded.
Map normal and retry actions to the production polling loop, including time spent
reading status. Exclude cancellation of an in-flight network request from this
property; prove it separately if required. Explore a declared finite domain,
demonstrate the original full-interval defect, then replay the counterexample on
the actual runner with a controlled clock. Do not label this a proof that every
wall-clock invocation returns before its deadline.
