---
name: xcode-build-fixer
description: Apply approved Xcode build optimization changes following best practices, then re-benchmark to verify improvement. Use when a developer has an approved optimization plan from xcode-build-orchestrator, wants to apply specific build fixes, needs help implementing build setting changes, script phase guards, source-level compilation fixes, or SPM restructuring that was recommended by an analysis skill.
---

# Apply measured Xcode build improvements

Use the existing workflow owner and approved scope. Load this method only after a
concrete diagnosis; a settings recommendation alone is not a proven improvement.

- Confirm baseline artifact status `complete`, successful phases and all expected
  repetitions. Record actual scheme, destination, SDK/compiler, configuration and
  cache conditions. Preserve source and build logs.
- Apply the smallest supported change. Reuse existing approval; ask only for an
  unresolved scope or authority decision. Never apply all suggested settings as
  a blanket best-practice rewrite.
- Run `scripts/benchmark_builds.py` with the same settings and representative
  repetitions; alternate baseline/candidate runs where noise warrants it.
  `--derived-data-path` is an existing parent for a temporary child, never a
  directory to delete. Arbitrary output-overriding arguments are rejected.
- Retain a performance change only when the measured benefit justifies it. A
  correctness/compatibility change can be retained for its separately approved
  purpose without inventing a speedup. Revert only this task's unsuccessful changes.
- Report baseline/candidate values, spread, executed work and failures. Zero-change
  builds are different from edit/rebuild loops. Never convert incomplete or failed
  measurements into a successful optimization report.

Use upstream references for applicable diagnostics, subject to the project’s
actual toolchain and conventions. Do not submit telemetry or community benchmark
data without explicit authorization.
