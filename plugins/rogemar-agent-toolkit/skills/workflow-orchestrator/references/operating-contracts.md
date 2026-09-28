# Proportional operating contract

The current main agent remains the only dispatcher and integrator. This reference
adds checks within existing task state; it creates no board, scheduler, model router,
provider session or authorization system. Native model qualification and the existing
review contracts remain unchanged.

## Act within the approved scope

Investigate discoverable facts, implement, test, diagnose and correct without asking
again for permission already granted. Pause only when a consequential choice or
necessary authority is missing. Scope knowledge by data source and recipient as
well as filesystem path: read-only access can still disclose private information.
Successful trials qualify a bounded capability; only the owner or an explicitly
approved policy may broaden authority. An agent never awards itself permissions.

A disproportionate control is a redesign candidate, not permission to bypass a
required gate. Prefer a direct check for a known-file, reversible correction.
Sensitive changes need appropriate evidence even when the diff is small.

## Assignment and recovery records

For material delegation, reuse existing task IDs and append the necessary fields:
owner, acceptance, dependencies, owned paths, workspace, shared exclusive resources,
state, candidate and evidence references. Do not collect these for every thought or
routine helper call. A prefix such as `src/auth` owns that directory and descendants;
a single filename owns that file. Use exact paths, not ambiguous globs.

The optional read-only helper is:

```sh
python3 -B <orchestrator-skill>/scripts/workflow_contracts.py assignments < record.json
python3 -B <orchestrator-skill>/scripts/workflow_contracts.py affected --changed task-a < record.json
```

It validates the declared dependency graph and overlapping running writers. It does
not discover omitted dependencies, resolve aliases to physical worktrees, attest
execution or isolate processes. Use actual host/worktree identity and inspect shared
contracts, databases, generated output, credentials and runtime resources before
parallel dispatch. Serialize writers in a shared worktree; separate worktrees alone
do not isolate a shared service.

Before changing a completed producer, compute its affected descendants from the
current record, invalidate their proof, and return those units to the appropriate
state in one owner-controlled update. Preserve unaffected work. Run the relevant
integrated regression checks after reconciliation. A missing or timed-out worker
remains unfinished; no result is not a clean result.

## Bounded corrections

Classify the failure before retry: implementation, environment, verifier, context,
routing, authority, or unknown. Attempt, time, cost and tool budgets belong in the
existing acceptance/assignment contract. No universal three-retry rule applies.
Reserve capacity for validation and integration instead of spending it all on work
production. Do not retry declined authority or blindly repeat uncertain side effects.

```sh
python3 -B <orchestrator-skill>/scripts/workflow_contracts.py retry < retry.json
```

The helper reports eligibility or a diagnosis/stop condition; it does not launch a
retry or reset a provider's existing review allowance. Preserve failed evidence.
Cancellation stops affected work and preserves recoverable progress. A stalled
optional learning operation must not keep product delivery alive indefinitely.

## Consequential-action binding

Permissions and intentional requests are different. A principal may be authorized
to delete a resource without having requested this deletion. Bind the actual tool,
authenticated connection, requester, target, operation ID, and complete normalized
arguments to the authorized action. Preserve exact values; do not coerce, drop
fields, or use a vague free-text approval as a blank cheque.

`action_digest` and `check_action_binding` are comparison helpers only. The host must
supply an authenticated, unexpired approval and atomically reserve operation IDs,
reconcile uncertain outcomes, recheck resource authorization and enforce runtime
isolation. A self-generated matching hash is not approval. Changes to arguments,
recipient, amount, target, connection or scope invalidate the binding. Checks must
occur after final argument normalization and before each side effect.

## Existing delivery remains authoritative

For scoped qualification, a registered host action adapter, controlled external
updates and bounded effectiveness observations, follow
[capability lifecycle](capability-lifecycle.md). Keep these within the existing
dispatcher and maintainer records; select them when those capabilities are needed.

Use the recorded delivery route. Selecting an execution skill or planning alone
does not grant publication. Explicit Integrated Workflow invocation retains its
native default only where the current repository and task permit it. No-push,
local-only and stop-before-merge instructions take precedence. Keep complete-slice
local review, required cloud-provider completion barriers and per-provider counts.
No extra control in this reference may reset or silently reduce them.

For task framing, reuse the installed create-plan reference when it is needed; if
that optional route is absent, apply the task's existing brief directly. Missing
optional helpers never manufacture required evidence or block unrelated work.
