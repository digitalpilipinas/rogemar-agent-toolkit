---
name: project-readiness
description: Use at the start or resume of every task in a repository, before planning or execution. Detects the project's technologies, checks the paths toolkit skills will need, and produces one setup plan for a single owner approval plus a situation map of which skills apply. Read-only.
---

# Project Readiness

Run this at the start or resume of every task, before planning or execution. It is
cheap and read-only, and it does nothing visible when the project is already ready.

1. Run `python3 -B <this skill folder>/scripts/readiness.py plan --root <repository root>`. Exit 0 means
   ready (or a declined plan that has not changed); exit 2 means the plan has items
   for the owner; exit 3 means the owner approved items you still need to apply;
   exit 1 means readiness is unavailable. Report unavailable as unavailable, never as ready.
2. If the status is `needs-owner`, show the owner the `needs-owner` items once, as one
   plan: unignore or ignore rules for paths skills write, and the one-line project
   instruction. Never apply them without approval; the plan grants no authority.
   After approval, apply them with your normal tools and record the approved
   `plan_id` in the readiness record (default `.agents/readiness.json`, or the
   project's declared location); the status is then `approved` until the items are
   applied, and `ready` once nothing is pending. Record `declined_plan_id` instead
   when the owner declines; either one stops repeat prompts until the plan changes.
3. Run `python3 -B <this skill folder>/scripts/readiness.py map --root <repository root>` and keep the
   situation map for this task. At slice start, name the matching rows in the
   one-line announcement the [method contract](../workflow-orchestrator/references/method-contract.md)
   requires. The map is a filtered view of the routing index: `workflow-orchestrator`
   still selects methods, and an applicable skill missing from the map is still
   applicable.
4. Continue with the entry skill that invoked you: task-handoff discovery, then
   planning or execution.

The readiness record may also declare `locations` that override a footprint's default
path, such as an agent-map output folder outside the repository. Declared locations
win. Connection state for MCP servers and plugins is observed by the agent at runtime
and never written to the record or the map.

Opt-in hooks run these checks automatically: `scripts/hooks.py` provides session
start, prompt and finish hooks, and each harness's Forge setup explains how to
install them with the owner's consent (on Claude, `claude-forge-setup`'s
`references/readiness-hooks.md`).

To enforce the method receipt on pull requests, `readiness.py ci` prints a GitHub
Actions job for the owner to review and adopt; it reads the validator and policy
from the protected base branch, never the pull request. It writes nothing.

For acceptance pins, `python3 -B <this skill folder>/scripts/readiness.py pins --policy FILE --validator FILE`
prints the sha256 values and the exact accept command for the owner's acceptance
record or trusted CI. It writes nothing.
