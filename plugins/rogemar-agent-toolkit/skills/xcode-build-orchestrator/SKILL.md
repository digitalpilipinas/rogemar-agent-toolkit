---
name: xcode-build-orchestrator
description: Coordinate evidence-based Xcode build analysis as a specialist under the existing workflow owner, reusing approved scope and dispatch.
---

# Xcode build analysis coordination

This is a specialist method under `workflow-orchestrator`, which owns dispatch,
worker scope and delivery. Use only for an actual build-performance question.
Reuse the approved task and acceptance record; do not create a separate programme
or mandatory panel. Do not import harness model names or spawn workers by default.

1. Identify the actual workspace/project, scheme, configuration, compiler/SDK,
   destination and resolved build settings. Verify Xcode is available on this
   Mac or an explicitly configured remote Mac. Source-only analysis on Linux
   remains source analysis; no build pass may be claimed.
2. Use `xcode-build-benchmark` for a baseline with representative repetitions.
   `--derived-data-path` is an existing **parent** for a run-owned child. Evidence
   stays in a separate unique run directory. A failed phase blocks comparisons.
3. Select `xcode-project-analyzer`, `xcode-compilation-analyzer` or
   `spm-build-analysis` only for a supported hypothesis. Task-time sums overlap
   in parallel builds; they do not identify a critical path without trace evidence.
4. Use `scripts/generate_optimization_report.py --benchmark <artifact>` to
   summarize completed data. Raw project settings are hypotheses; inspect resolved
   configuration values before proposing changes. Do not promise generic percentages.
5. Pass justified changes to the existing implementation owner using
   `xcode-build-fixer`. Retest under comparable conditions. Preserve logs and
   retain improvements only with measured benefit or an approved separate purpose.

Baseline failure is a prerequisite defect to diagnose within scope. Do not
cherry-pick unrelated commits, alter dependency repositories, create ignored
package scaffolds or submit community feedback automatically. New authority is
needed only for actions outside the approved task. Refer to the cooperating
skills' references for the selected diagnostic, not a compulsory full audit.
