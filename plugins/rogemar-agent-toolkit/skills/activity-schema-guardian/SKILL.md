---
name: activity-schema-guardian
description: Use for activity, event, telemetry, logging, or domain schema work involving canonical IDs, category discriminators, sport/activity-specific fields, fixtures, aliases, backward compatibility, JSONB or flexible payload validation, database migrations, and derived insight metrics.
---

# Activity Schema Guardian

## Workflow

1. Inspect canonical IDs, aliases, fixtures, schema definitions, store hydration, generated types, API contracts, and database migrations before editing.
2. Preserve backward-compatible semantics unless the user explicitly asks for a breaking change.
3. Keep universal fields separate from domain-specific payload fields.
4. Validate all canonical variants and legacy aliases through fixtures or targeted tests.
5. For migrations, prefer staged rollout patterns such as backfills, validators, `NOT VALID` constraints, and safe legacy hydration.
6. Reuse existing metric registries or analytics contracts instead of inventing per-screen metrics.

## Guardrails

- Do not silently rename persisted fields.
- Do not weaken validation to make tests pass.
- Do not break historical rows without a migration/backfill story.

## Verification

Run targeted schema tests, TypeScript/type checks, lint, and migration smoke checks when the environment supports them.
