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

## Outcome (2026-10-30)

- PR #34 (drift checker, statechart fork) and PR #35 (1.3.0 plan and slice 1
  docs) merged after GitHub CodeRabbit and Codex reviews; PR #36 (slice 2:
  footprints, tags, argent repin, Appllama tracking) merged with local
  substitute evidence for a second cloud review, by owner choice.
- Slices 3-9 committed directly to `main` under the owner's direct-commit
  authorization: `320eb00`..`4e5d6f8`. Gate: one full local CodeRabbit review
  (four minor findings, fixed), full local suite on Python 3.9 plus structural
  checks on 3.11, owner suites, both packages and `claude plugin validate`;
  then GitHub CI on `main` at `4e5d6f8`: 4/4 jobs passed (run 41058627184).

- 1.3.0 docs and review gate (2026-10-30, direct to `main`): provider-neutral
  review route (`readiness.py` reports `review_route`), the cloud barrier waits only
  for configured reviewers, CHANGELOG tidy, README rewrite, `docs/user-guide.md` and
  `docs/assets/readme/v13` infographics. Two local CodeRabbit runs (5 findings, all
  fixed); full local suite 323 tests, verify, packages and `claude plugin validate`.
- Claude marketplace entry reverted to the plugin-folder source (version kept):
  Claude Desktop could not check for updates after slice 5's root source with a
  skill list. Owner to confirm the Desktop update; seven other-assistant adapters
  are now visible in the Claude plugin, and the managed installer still filters.

## Still open

- Slice 9 runs: the compliance protocol (`docs/quality/method-compliance-protocol.md`)
  in installed Claude, Codex and Cursor sessions, plus one EVERSO pilot slice.
  These gate the 1.3.0 tag, which the owner applies.
- tla-ts parity trial: needs the owner's authorization to download and run
  `tla-ts@0.0.3`; TLC remains the default until then.
- Owner's local Claude install: keep the plugin, then run
  `upgrade --convert-external-only` for `~/.claude` only, with consent.
- Installed-plugin overlap audit (read-only), approved as a separate task.

## Next action

Owner confirms the Claude Desktop update to 1.3.0, then runs the compliance
protocol and EVERSO pilot before tagging 1.3.0.
