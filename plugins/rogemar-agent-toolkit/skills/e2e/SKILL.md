---
name: e2e
description: TesterArmy end-to-end journeys for supported browser, iOS and Android projects, with deterministic assertions and actual run evidence.
license: Apache-2.0
---

# TesterArmy E2E

Prefer this runner for suitable new browser/mobile journeys. Preserve existing
coverage and project conventions; adapt the relevant journey within the active
task, never perform a wholesale migration automatically. Unsupported capabilities
use the existing project runner or remain blocked when required.

## Readiness and setup

- Read the project test configuration, required journey and environment first.
  Node.js 22.12+ is required. Inspect current dependency/provider configuration.
- Use exact compatible project dependency versions: `e2e@0.17.0`,
  `@e2e-dev/web@0.12.0` for browser and `@e2e-dev/mobile@0.9.2` for mobile.
  Install only the engine needed. Preserve the project package manager and lockfile.
- Use the release-bundled `references/` here. Upstream main may describe APIs that
  differ from this published set. Do not run `init --yes`: it can select providers,
  install skills and register MCP without an explicit project decision.
- Set `E2E_TELEMETRY_DISABLED=1` and `DO_NOT_TRACK=1` in toolkit-created run
  commands/configuration. Do not submit upstream feedback or enable paid features.
- Deterministic journeys require no model or provider login. Agent-driven steps
  require an already approved configured provider, actual authentication and bounded
  time/token/cost settings supported by that provider. Never infer auth from a key name.
- Browser engine needs a compatible installed browser. iOS needs a reachable Mac,
  build and simulator/device; Android needs its SDK/device/emulator. Skill installation
  alone establishes none of these. Keep mobile and AI readiness separate.

## Execution and acceptance

Use deterministic actions and explicit assertions first. Select stable locators,
known fixtures and owned browser/device resources. Keep retries/timeouts finite;
do not weaken assertions to make a test pass. Preserve the project's test data and
cleanup contract. See the appropriate engine and assertion references only as needed.

Run the pinned local CLI through the project's package manager. Inspect the actual
`report.json`, traces/screenshots and exit status. Confirm selected and executed
counts, required assertions and no silently skipped required journey. Exit zero alone
is insufficient: skipped or flaky coverage is not proof of the required outcome.
A failing assertion must remain failed; missing device/authentication/capabilities
or exhausted budgets remain blocked, never successful. Keep deterministic browser,
mobile, AI-driven, accessibility and physical-device evidence distinct.

Integrated Workflow owns acceptance and `workflow-orchestrator` selects methods.
This skill adds no second owner, monitor, provider purchase or new approval cycle.
