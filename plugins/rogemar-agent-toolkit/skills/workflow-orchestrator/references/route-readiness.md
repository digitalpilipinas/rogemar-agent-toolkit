# Selected route, readiness and evidence

The current agent selects methods from the task, changed files, project conventions
and the routing index. Integrated Workflow invokes that selection through this
orchestrator at entry and material phase changes. The resolver validates a selected
route; it does not infer relevance, launch workers or make a model obey instructions.
Use the smallest sufficient selection and retain the active delivery owner.

## Choose from overlapping methods

- SwiftUI implementation: `swiftui-expert-skill`; focused review: `swiftui-pro`.
- Concurrency implementation/migration/diagnostics: `swift-concurrency`; focused
  review: `swift-concurrency-pro`.
- Select `swiftdata-pro` only for SwiftData work and `swift-testing-pro` for Swift
  Testing. Do not migrate persistence or test frameworks just because a skill exists.
- Xcode performance: select only the applicable analysis, benchmark or fix method
  from the six-skill family. The specialist orchestrator remains subordinate to this
  dispatcher. Retain optimization changes only with a measured, explained benefit.
- Architecture/module/interface reasoning: `codebase-design` when useful, without
  imposing its vocabulary or launching an automatic panel.
- Supported browser/iOS/Android E2E: prefer `e2e` for relevant new journeys, retaining
  existing coverage and conventions. Static guidance works anywhere; builds, devices
  and actual journey evidence have their own platform requirements.

A primary and review alternative can cooperate for a concrete coverage gap. Record
that reason; don't load both routinely. PStack's explicit invocation flags still
apply to its raw native skills. Portable Forge uses adapted shared methods.

## Check only the selected route

The installed `scripts/select_methods.py` accepts repeated `--method ID` and one
optional `--entry`. Source-only resolution verifies files/resources and hard skill
dependencies. Supply additional installation roots with `--additional-skills-root`;
Codex's standard shared/native roots are understood. Different physical copies in
those roots are conflicts; symlink aliases to one copy are not duplicate sources.

For material runtime work, use `--context receipt.json --candidate ID --runtime`.
Context is an object containing `harness`, `task_tags`, `platform` and `readiness`.
Tags are declared task applicability (for example `swiftui`, `swift-concurrency`,
`swiftdata`, `swift-testing`, `xcode-performance`, `e2e`, `architecture`), not keyword
scores. `overlap_reason` explains any selected primary/review pair.

The toolkit checkout's `scripts/toolkit.py doctor` can provide scoped readiness:

```sh
python3 scripts/toolkit.py doctor --harness cursor --target user \
  --method swiftui-expert-skill --capability xcode --exercise --candidate ID --json
```

`--exercise` performs selected public version probes; it never establishes feature
correctness. `--auth-check` runs only known selected authentication-status commands;
it never logs in or reveals their output. Without it, authentication stays unverified.
Missing tools, unsupported checks and failed authentication remain explicit. Static
skill reads require no authentication. Harness UI/tool discovery must be inspected
through the actual host; PATH and files cannot prove that registry.

Place the returned doctor object under `readiness` in the existing receipt. Its
candidate must match, its observation time must be valid, and the owner must mark
`invalidated: true` after a material tool/environment change. Reuse unaffected facts;
do not expire valid evidence on an arbitrary timer. Candidate identity includes
relevant dirty content, dependencies and runtime, not merely the Git HEAD label.
External service/device observations use the same per-capability shape: `installed`,
`discoverable`, `exercised`, and `authenticated` where needed. Inspect the real result;
a handwritten success value does not establish readiness.

For E2E, context also has `execution.surface` (`browser`, `ios`, `android`) and
`execution.mode` (`deterministic`, `agent-driven`). Doctor checks exact project package
versions, Node 22.12+ and the CLI; engines and devices need separate evidence. Mobile
requires a successful `device` observation from the real selected device route.
Agent-driven mode additionally needs an explicitly approved named `provider`,
`provider_authorized: true`, finite positive `max_steps`, `timeout_seconds`, `max_cost`,
and a live authenticated `model-provider` observation. Deterministic mode needs none
of those provider settings. The receipt records existing authority, never creates it.
Keep telemetry disabled and do not submit upstream feedback automatically.

## Maintenance and acceptance

Select `forge-create-verification-skill` for a meaningful missing reusable recipe;
select `forge-maintain-verification-skill` for affected behavior/recipe/dependency
drift. Both retain their entry names and work across harnesses. Select portable
`codex-capability-maintainer` for capability dependency or instruction changes.
Do not start a full audit, new verifier, background monitor or login on every task.

For delegated work, `--worker-brief` validates the existing brief's owner, role,
allowed_files, non_goals, authority, instructions, methods, candidate and required_evidence.
List-valued fields contain concrete strings. Authority is `read-only` or an existing
`approved-task-write` grant. The helper cannot verify dispatch, enforce filesystem
boundaries or replace native sandbox/permissions. Pass essential instructions and
observed capability limitations to the worker, not just the skill names.

At acceptance, optional `--acceptance` checks each route's required evidence in
`context.evidence`: status, candidate, artifact path and SHA-256. These are integrity
checks only. The main owner still inspects deterministic assertions, actual execution
counts, logs and counterexamples against the task. Preserve failure/blocked/deferred
states and separate unit/UI/accessibility/device evidence. Unsupported completion
claims are rejected even if a receipt says passed. Refresh only invalidated checks.
