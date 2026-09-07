---
name: forge-principle-sequence-verifiable-units
description: "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer."
license: MIT
---
# Sequence verifiable units

Order work so each coherent risk-bearing unit can be reviewed and verified before a dependent unit relies on it. Group related mechanical edits when that is the smallest useful slice; avoid artificial micro-tasking or rerunning an entire suite after every line. Define dependencies and evidence before implementation. Keep each unit within explicit ownership and preserve unrelated changes. Use test-first sequencing when it meaningfully demonstrates a regression. Commits, rebases, branch changes and publication require the corresponding authority; verification does not depend on rewriting history. Recheck the actual integration context after base/head changes.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) for authority, delegation, routing and evidence boundaries.
