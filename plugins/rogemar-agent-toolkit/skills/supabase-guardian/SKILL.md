---
name: supabase-guardian
description: Use for any project with Supabase work involving RLS audits, migrations, SECURITY DEFINER RPCs, storage policies, auth/session handling, database functions, logs, or sensitive state where client-supplied identity, permissions, counters, rewards, tiers, credits, or ownership must not be trusted.
---

# Supabase Guardian

## Workflow

1. Inspect current repo state, Supabase config, migrations, functions, generated types, and client access paths before judging.
2. Review RLS policies for user isolation, role boundaries, write constraints, ownership checks, and least-privilege anon/authenticated access.
3. Review `SECURITY DEFINER` functions for explicit authorization checks, stable `search_path`, safe inputs, idempotency, and denial of direct raw table writes when sensitive state is involved.
4. Check storage bucket policies, signed URL behavior, upload paths, content ownership, and deletion/reconciliation.
5. Trace auth/session handling from client to server. Identity should come from Supabase auth or trusted server context, not request body fields.
6. Validate migrations locally when available. If Docker/Postgres is unavailable, run code/type tests and clearly state the migration-validation gap.

## Security Biases

- Treat rewards, credits, billing, roles, ownership, profile state, moderation state, and counters as server-authoritative.
- Prefer typed RPCs/functions for sensitive writes.
- Keep secrets local and uncommitted; never echo service role keys into outputs.
- Review delete/rewrite paths as carefully as create/finalize paths.

## Output

Lead with risks and fixes. Include files/migrations reviewed, validation run, and any production safety gaps.
