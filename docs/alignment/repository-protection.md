# Repository and runtime controls: separate administrative work

No live administrative change was performed. On 2026-09-28 the connected branch
response reported `main` unprotected; the repository rulesets endpoint with inherited
rules included returned an empty list. The connector rejected the effective
branch-rules endpoint as unsupported. Final PR mergeability/check state is still
verified through GitHub; no settings or bypass authority are changed.

The candidate preserves the current CI jobs, Python matrix and read-only workflow
permissions, and replaces two mutable Action refs with connected-source-observed
commit refs. See action-pins.json. This is not a dependency-major-version upgrade
or evidence that the new workflow has run.

Before changing live rules, inspect current branch rules, account permissions,
actual check names, PR review settings, automation identity and bypass authority.
Require the applicable checks on the reviewed candidate, restrict force-push and
branch deletion, and protect acceptance policy, CI and reusable skill updates.
Use the exact required-check contexts actually reported by the resulting CI;
do not invent check names from a matrix label.

Do not create an impossible self-approval gate for a sole maintainer. Select a
review arrangement compatible with real collaborators and repository policy.
A CodeRabbit/Codex result is evidence, not a GitHub permission grant. Any emergency
bypass needs explicit owner authority, limited scope, a reason and retained
verification/recovery evidence. The implementing agent cannot weaken protection
because a check is expensive, red, absent or inconvenient.

Runtime enforcement belongs to the actual host: scoped filesystem and network
permissions, protected identity and secrets, action-intent binding, cancellation,
resource budgets, and an atomic operation/outcome record for side effects.
The optional registered action adapter checks bindings and reserves budgets and
operation IDs in host state. It does not provision host controls or authenticate an
approval; those remain trusted host callback responsibilities. The trusted-execution extension requires a separately protected host
observation and policy; agent-authored hashes are not sufficient.

No live rule change, provider registration, installation, deployment, release,
paid-service enrollment, secret or IAM change follows from applying repository
files. Reconcile uncertain writes before retry and preserve declined access.
