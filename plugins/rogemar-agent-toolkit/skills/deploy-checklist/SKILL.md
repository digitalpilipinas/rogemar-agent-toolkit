---
name: deploy-checklist
description: Use when preparing releases, deploys, preview builds, production pushes, branch summaries, release notes, rollback plans, QA checklists, or risk reviews before shipping a web, mobile, backend, or Supabase change.
---

# Deploy Checklist

## Workflow

1. Inspect branch state, changed files, recent commits, and deployment target.
2. Summarize user-facing changes, backend/schema changes, config/env changes, and operational risks.
3. Run or recommend repo-native validation: lint, typecheck, tests, build, migrations, smoke tests.
4. Produce release notes, manual QA steps, rollback notes, and any required secrets/env checklist.
5. If asked to deploy, use the relevant deployment skill or MCP and verify the deployed URL/status.
6. Tie each acceptance result to the reviewed commit SHA; keep automated,
   staging/production, and manual/device evidence distinct.

## Output Shape

Use short sections: Scope, Validation, Risk, Manual QA, Release Notes, Rollback.
