---
name: test-architecture-engineer
description: Use when designing or reviewing a test strategy for a feature, PR, sprint, bug fix, migration, or release. Routes work between unit, integration, contract, E2E, visual regression, accessibility, native emulator/device, smoke, and flaky-test diagnosis based on risk.
---

# Test Architecture Engineer

Use this skill when the question is not merely "write a test", but "what
evidence is enough for this change?"

## Workflow

1. Identify the behavior, risk, blast radius, and failure cost of the change.
2. Build a small risk-based matrix across layers: pure logic, component/UI,
   service/API, database/schema, auth/permissions, migration/backfill, offline
   or concurrency, accessibility, visual layout, native platform, and deploy.
3. Choose the cheapest test that can fail for the right reason. Prefer
   repo-native test patterns and existing helpers.
4. Include negative cases for sensitive behavior: unauthorized, malformed,
   legacy, duplicate, concurrent, offline, disabled, private, rollback, and
   boundary values as applicable.
5. Diagnose flaky tests by isolating time, randomness, network, shared state,
   async waits, order dependence, and environment assumptions.
6. Report deferred manual or physical-device QA honestly; do not treat it as
   passed.

## Guardrails

- Do not add broad E2E tests when a contract or unit test proves the invariant.
- Do not accept snapshot-only coverage for behavior with security, privacy, or
  data consequences.
- Do not delete or loosen failing tests unless the intended behavior changed and
  the new contract is explicit.
- Keep tests deterministic and scoped to the behavior under review.

## Output

Provide a matrix with risk, chosen test type, files or commands, required
negative cases, and what remains manual or deferred.

## Optional delegation guidance

The orchestrator may assign a read-only test-design or test-log analyst when
the evidence streams are independent. Give the worker the affected behavior,
risk matrix, repository test conventions, parent model and reasoning ceilings,
and required output format. Require exact proposed checks and evidence gaps.
Keep the worker below the parent ceilings; return unresolved test sufficiency,
security, migration, or concurrency judgments to the main agent.
