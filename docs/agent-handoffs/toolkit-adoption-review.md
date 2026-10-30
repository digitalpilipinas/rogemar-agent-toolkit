# Upstream adoption review and drift tracking

Date: 2026-10-30. Owner: current toolkit maintainer (Claude Forge, Balanced).
Worktree branch: `claude/skills-plugin-review-508af3` from `76fea71`.
This record grants no commit, push, merge or installation authority.

## Decisions (owner-approved 2026-10-30)

- **Statechart: intentional fork.** Upstream PStack `34b1b7c` (#977) replaced
  the `.mjs` scripts with a TypeScript compiler (Node >=22.18) and no longer
  documents from-chart, `--against`/`--fixed`, PNG, cover or readerActions.
  Local keeps them. The matching `create-formal-verification-skill` sentence is
  deliberately not synced. Recorded as `divergence` plus `reviewed: 4dd1d05` on
  the cursor/plugins adaptation in `catalog/imported-sources.json`.
- **Drift detection, not auto-update.** `scripts/upstream_compare.py` now
  compares each adapted path from its own pin and falls back to Git tree diffs
  when GitHub's 300-file compare cap hides the paths. New `--all` flag and
  weekly `.github/workflows/upstream-drift.yml` (read-only; opens or updates one
  `Upstream drift` issue). Nothing repins or vendors automatically.

## Evidence

- Live `--all` run: 19 sources, 0 unavailable (argent, pstack and
  tester-army/e2e previously hit the cap). Drift in adapted paths: argent,
  diagram-design, coderabbit, convex, expo, mattpocock/skills, ponytail, pstack,
  tester-army/e2e, twostraws/SwiftUI. Not reviewed in this task.
- Passed locally on 2026-10-30: `toolkit.py lock` (no skill content changed),
  `verify` (131 skills), README inventory check, full suite (281 tests OK), core
  package (6 skills) and full package (126 skills). Workflow YAML parsed; the
  workflow itself has not run on GitHub yet.

## Researched, not yet implemented (proposals)

- Matt Pocock: PR #1342 merged (`a496f55`); adopt "fresh implementer per
  ticket" only if local delegation guidance reuses implementers; then set
  `reviewed` for mattpocock adaptations.
- tla-ts (MIT, 0.0.3, created 2026-10-26): optional TLC backend after a corpus
  trial; not a dependency.
- Appllama: already adapted from `dd5caae` (still upstream HEAD). Remaining gap:
  the numeric UI slop pre-flight count. Appllama is not in
  `imported-sources.json`, so drift checking cannot see it.
- Video: optional thin `programmatic-video` method skill citing
  JohnHeibel/ClaudeAnimationBase and lemomo-ai/lemo-opuscar (both MIT); prompt
  lists are reference-only (one has no license).
- Local install: 124 toolkit skills are duplicated in `~/.claude/skills` and
  the Claude plugin; removal needs owner approval.

## Next action

Owner decides commit/PR, the proposals above, and the local duplicate cleanup.
