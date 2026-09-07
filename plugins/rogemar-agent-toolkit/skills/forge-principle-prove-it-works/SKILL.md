---
name: forge-principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles."
license: MIT
---
# Prove it works

Define what would demonstrate the requested behavior, then obtain evidence on the matching artifact and surface. Tests, static checks, runtime observations, image comparisons and performance probes answer different questions; choose those required by the actual change. Reuse meaningful checks and avoid tests that merely mirror trivial edits. For a bug, compare the original reproduction before and after. For performance, use comparable measured workloads. For a visible interaction, inspect the relevant runtime when available. A worker report is evidence to reconcile with the actual diff, not final acceptance. Label passed, failed, skipped, blocked and unverified separately; never substitute a plan, command invocation or unrelated green check for proof. Do not invent live results when the surface is unavailable.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) for authority, delegation, routing and evidence boundaries.
