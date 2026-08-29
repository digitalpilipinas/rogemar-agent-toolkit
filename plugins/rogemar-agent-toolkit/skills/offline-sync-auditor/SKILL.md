---
name: offline-sync-auditor
description: Use for any app with offline or poor-network behavior involving local drafts, outbox queues, sync retry logic, conflict handling, user-scoped cache keys, network transitions, foreground/app-start sync, queued UI states, and data integrity across unreliable connectivity.
---

# Offline Sync Auditor

## Workflow

1. Inspect current branch and relevant persistence, cache, sync, and network-state files before assuming behavior.
2. Check draft persistence, outbox storage, sync manager orchestration, network-regain hooks, foreground/app-start hooks, and user-scoped cache boundaries.
3. Verify UI states distinguish draft, queued, syncing, synced, failed, conflict, and unavailable.
4. Review conflict behavior for duplicate submits, edits while queued, deletes while queued, auth changes, logout, user switching, and app restarts.
5. Test or specify tests for offline creation, network restoration, retry failure, idempotent server writes, and data reconciliation.

## Guardrails

- Do not imply server success while offline.
- Do not leak cached data across users.
- Do not drop queued data without explicit user control.
- Prefer honest queued/unavailable states over optimistic fiction when backend state is unknown.

## Output

List data-integrity risks, UX risks, missing tests, and concrete implementation fixes.
