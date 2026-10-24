# Tooling lens

Read [the reflection review contract](review-contract.md), then inspect the
supplied task, authorized transcript or digest. Look for recurring tooling
friction, broken or unwired checks, missing diagnostic signals and manual work
that an available authorized tool could have done.

Ground each suggestion in the actual tool or code path. Identify the missing
mechanism, command convention or capability handoff; preserve version-specific
facts as source evidence rather than universal instructions. An unavailable or
unauthorized integration is a limitation, not an agent failure to use it.

## Agent self-sufficiency examples

Look for manual transfers of context that an available, authorized tool could
have supplied. For example:

- A user pastes a ticket title after the agent failed to read the linked ticket.
- A user describes a flaky test whose named trace was accessible through the
  existing observability connector.
- A user copies a linked discussion that the agent could have retrieved itself.

Inspect availability and task authority before treating the handoff as avoidable.
A helpful user contribution is not automatically an agent failure. Route the
repair to the existing workflow owner, with the precise lookup and evidence
needed, rather than prescribing one provider for every project. Preserve durable
command conventions, debugging entry points and non-obvious flags; keep pinned
versions and paths in the evidence instead of making them universal policy.

## Inspection prompts

Use these prompts where the supplied evidence supports them:

- Tool invocations and command flags the agent had to discover
- Library / framework quirks (config, lockfiles, env-var behavior, version-specific gotchas)
- File or path conventions that aren't obvious from a glance at the code
- Test commands, CI flags, and how to reproduce a failing run locally
- Debugging entry points: how to capture a trace, where logs land, which RPC to hit
- Build / package-manager / sandbox surprises that cost minutes the first time


For each supported finding, return:

- Principle: the reusable tool or workflow rule.
- Evidence: the source turn or artifact and the observed friction.
- Routing: the existing owner and section or a justified missed-trigger route.
- Proposal: the smallest repair, reusable helper or diagnostic improvement.

Return no findings when no evidenced improvement earns its cost.

<AUTHORIZED TRANSCRIPT PATH OR TASK DIGEST>
