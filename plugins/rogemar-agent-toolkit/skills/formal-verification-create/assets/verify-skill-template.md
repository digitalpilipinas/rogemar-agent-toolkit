---
name: verify-<project-property>
description: Verify <property> when <guarded state, callers or behavior> changes.
---

# Verify <property>

This is an authoring template. Replace all placeholders before qualification.

## Promise and correspondence

- Property and harm prevented: <observable promise and consequence>.
- Technique: <model checking, code verifier, proof, or generated testing>.
- Covered files/symbols and every writer of guarded state: <source pointers>.
- Atomic actions and actual implementation boundaries: <mapping>.
- Bounds, fairness/environment assumptions, omissions: <explicit domain>.
- Tool/version and prerequisites: <reproducible dependency identity>.
- Last confirmed synchronization commit: <real checked commit or unset>.
- Dirty source identity: <base commit and content digests, if applicable>.

## Execute

1. Compare current source, callers and new guarded-state writers with the record.
   Use `formal-verification-maintain` for drift; an old pass is not current proof.
2. Run <actual one-command check> from <actual working directory>.
3. Inspect <actual result artifacts>. State whether exploration completed and
   what was checked; an interrupted search is incomplete.
4. For TLA+ results use `statechart-verification` through its current help and
   instructions. Preserve counterexamples and distinguish reachability goals
   from violated safety rules.
5. Replay counterexamples through <actual implementation entry points> and
   inspect observable outcomes. Classify model drift, product defect or blocker.
6. For a model-only route, confirm checker sensitivity with <isolated model or
   property mutation and expected violation>. This does not establish implementation
   coverage; preserve the separate correspondence and replay evidence from step 5.
   If an implementation-level verifier or harness is included, also require
   <isolated real-code mutation and expected failure> through that layer.
   Inspect each mutation against its pristine baseline, restore only that mutation,
   and confirm the original verdict. Record the layer exercised and any limits.

## Record and maintain

Keep commands/results, covered state writers, replay, mutation evidence and
limitations in <existing evidence record>. Change a property only for an intended
promise change backed by evidence. Advance synchronization only after checking
correspondence at that exact source. Missing execution leaves this skill draft.
