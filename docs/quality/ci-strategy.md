# CI strategy

Status: applied 2026-11-01 after two independent reviews (DevOps lens, then a
fresh-context final review). Where implementation differed from the review,
the "As applied" notes say why. Project-agnostic: project-specific findings
stay in that project's own records.

## Policy (one rule for every project)

Hosted CI confirms; the local gate decides.

1. Every project has one CI entrypoint (`scripts/ci`, `make ci`, or the
   project's equivalent) that runs every gate. Hosted CI, any runner vendor,
   and local agents all call that same command.
2. Merge evidence is the entrypoint passing on the exact candidate SHA, from
   a clean worktree with frozen lockfiles. The receipt records the SHA,
   command, exit code, toolchain versions, OS and log path, written by the
   script rather than narrated by the agent.
3. When hosted CI is unavailable (quota, billing, outage), the slice
   continues on that local evidence. Hosted CI is recorded as
   `unavailable_by_quota` (or the actual reason), never as passed.
4. Excluded from local-only merge: database migrations and access rules,
   authentication, backend stacks the local gate does not run (for example a
   Supabase job), and release, tag or store builds. These wait for a clean
   hosted or self-hosted run.
5. Backfill: when hosted CI returns, run it on the main branch head. A
   failure there is fixed forward or reverted before new work merges.
6. Hosted CI runs on PRs marked ready, pushes to main, tags, and a nightly
   schedule. Draft PRs do not run it. Non-hermetic checks (live advisory
   databases, network-dependent audits) run nightly, not per PR.

This is the original continuous-integration practice: a private build
before integrating, with the server as confirmation. Rails 8.1 ships the same
shape as `bin/ci` plus an optional signoff commit status from the local run.

## Toolkit repository: `validate.yml`

Measured: four matrix jobs per run, 130-227 s each; queue 1-2 s; the unit
suite is 110-167 s of each job. Locally the suite is 350 s, and
`test_selection_install` is 206 s of that because six tests each build
release archives or rewrite the lock from scratch.

| # | Change | Why |
| --- | --- | --- |
| 1 | `concurrency: validate-${{ github.ref }}` with `cancel-in-progress` for PRs | A new push replaces the running job |
| 2 | `pull_request` types include `ready_for_review`; jobs skip drafts | Drafts stop spending runs |
| 3 | PRs: ubuntu-24.04 on 3.9 and 3.11. Main pushes, tags, nightly and manual: add macos-latest | PRs get fast feedback; main pushes keep macOS because direct commits are the usual route and post-push CI blocks nobody (restored 2026-11-01 after first applying ubuntu-only to main) |
| 4 | `timeout-minutes: 15` per job | A hung test cannot hold a runner for six hours |
| 5 | Remove `paths-ignore` | As applied: release archives package all of `docs/` and `CHANGELOG.md`, and the archive tests run inside them, so no docs path is safe to skip. A docs PR costs one free ubuntu run |
| 6 | Workflow steps call `scripts/ci.py` instead of listing commands | One entrypoint for every vendor and for local agents |

## Toolkit repository: test speed

As applied: the planned shared archive fixture did not fit. Each slow test
builds a different artifact (core package with a nested suite, per-harness
packages, full package, an install, two lock runs), so there was no repeated
build to share. The manifest-drift test now runs one lock for all five
manifests instead of five (23 s to 5 s). The suite is still over two minutes;
splitting it across jobs stays the next option if PR time matters.

## Toolkit guidance

1. `integrated-workflow/references/execution-loop.md`: add the policy rules
   2-5 under the gate contract. `capability-fallbacks.md` already says what
   to record; this adds that the slice continues, the exclusions, and the
   backfill.
2. `project-readiness`: the plan reports the single CI entrypoint, or
   recommends one when a project has none. As applied, this is an
   observation like the review route, not a needs-owner item, so existing
   approved plans stay valid. `readiness.py ci` stays the method-receipt job.
3. Forge setup: offer an opt-in pre-push hook that runs the entrypoint's
   fast subset (verify, inventory, tests excluding `test_selection_install`),
   with the owner's consent, beside the existing readiness hooks.
4. Optional: a script that posts a `local-gate` commit status after a
   passing local run. Visibility only; it does not replace hosted CI.

## Vendor portability

Only GitHub-Actions-compatible runner vendors (Blacksmith, Namespace, Depot,
self-hosted runners) accept a workflow file with a `runs-on` change.
CircleCI, GitLab and Buildkite need their own config. The single entrypoint
keeps each vendor file to three steps: check out, set up toolchains, run
the entrypoint. Environment such as feature flags lives in one checked-in
file both vendors load, so the vendors test the same thing.

## Not adopted

- Failing a run when `select_checks.py` selects nothing: most changes are
  covered by the root suite and correctly select nothing.
- A four-value `ci_policy` setting: the single rule above covers it.
- Ignoring `README.md` in Validate: Validate runs the README inventory check.
- The article's TypeScript-specific swaps (Oxlint, Bun typecheck, Vitest
  isolation, sharding) and paid runner vendors.
