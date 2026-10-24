# Claude Forge runtime contract

Use this contract for the Claude counterparts of PStack and poteto-mode workflows.
The engineering method stays in the selected playbook. This file only binds that
method to a Claude session.

## One workflow owner

`workflow-orchestrator` alone decides specialist activation and subagent dispatch.
A playbook request to investigate, compare designs, run a panel, or delegate is a
bounded hint, not a second coordinator. If the orchestrator is already active,
return the hint to that owner. Do not restart the lifecycle or call `claude-forge`
again.

`claude-forge-setup` qualifies role profiles before a new worker. Use
`universal-plan-model-router` only when this setup skill or the relevant mapping
is unavailable. An explicit Universal Forge request stays on `universal-forge`.
Do not run Claude Forge and Universal Forge as two execution owners.

Each hint carries objective, exact owned scope, non-goals, read and write limits,
isolation, evidence, the reason independence is useful, and a stop condition.
The main agent remains an implementer and integrator. It keeps coupled work and
may execute a package directly. Default to no worker for serial work. Concurrent
writes follow [writer isolation](../../workflow-orchestrator/references/writer-isolation.md). A worker does not spawn descendants unless that
assignment was separately approved.

## Profiles and dispatch

Read `~/.claude/claude-forge.json` through `claude-forge-setup` before each new
assignment. That file is ours. Do not rewrite `~/.claude/settings.json`,
`CLAUDE.md`, or Claude's permission rules to store a mode.

Peak, Balanced, Lean, and Sprint are routing preferences. They are not model
names, prices, or proof that a profile is available. Discover the model IDs and
settings the current session's subagent tool actually accepts. An example family
name is not a dispatch ID until that inspection confirms it. Do not send Codex
model IDs, Cursor model slugs, or PStack effort flags.

Record the requested profile, the accepted tool arguments, and the observed
runtime identity separately. A worker's own summary is not runtime identity.
Missing metadata stays Unverified.

A desired parent model is a recommendation until a supported current-session
control applies it and the new identity is observed. Saving this configuration,
spawning a worker, or editing a skill does not switch the parent. If no control
exists, say the parent change is unapplied and continue with the current parent
when that parent is allowed.

After qualification, follow
[sub-agent naming](../../workflow-orchestrator/references/subagent-naming.md).
Use a naming field only when the live tool exposes one. Mode stays out of the name.

## Capability translation

For a selected dynamic workflow, follow [the native workflow binding](dynamic-workflows.md).
It executes the same orchestrator-owned plan with bounded phases and agents.
Do not equate installed instructions or normal Agent-tool access with a working
Workflow runtime; qualify that surface separately.

| Upstream operation | Claude execution |
| --- | --- |
| Task, background delegate, model panel | Bounded request to the orchestrator. It calls the subagent tool this session actually exposes, with arguments from that tool's schema. Follow the tool’s documented completion notifications and resume support; a missing background flag does not establish blocking behavior. |
| poteto-mode, `/setup-pstack`, Cursor `Task` model slugs | Do not call them. They belong to Cursor. Use this package and the live Claude tool schema. |
| `~/.cursor/cursor-forge.json` | `~/.claude/claude-forge.json` for this adapter only. |
| AskQuestion | Use the session's user-input tool only for an unresolved owner decision. Otherwise ask in the reply and continue reversible work. |
| Loop or autonomous goal | Continue the authorized task to its predicate. Create a persisted goal or hook only when the task explicitly asks for one. |
| Cursor transcript path | Use the transcript, checkpoint, or task id the user supplied. Do not scan unrelated Claude or Cursor history. |
| control-ui, control-cli, deslop | Use the browser, terminal, review, or cleanup tool this session actually has. Keep the playbook's evidence bar. |
| Device verification | Use installed device skills only when the target and tools are present. |
| Codex `plan-model-router` | Do not load it. Claude profiles come from `claude-forge-setup`. |

A missing optional tool narrows evidence. A missing required tool blocks that
operation and names the dependency. Do not build a substitute service. After two
failed attempts on the same route, stop retrying and record the blocker.

### Qualify the actual native route

- Read the selected installed instruction file when the native skill invocation
  tool cannot invoke it and the current invocation policy permits that use.
  Do not use reading as a bypass for an explicit-only policy. A matching reviewed
  toolkit adaptation may have its own conditional route. Use the installed skill
  name/namespace exposed by this session rather than inventing slash commands.
- Check tool access inside each worker. A general-purpose worker may receive MCP
  tools while another agent type does not; neither parent access nor a role name
  establishes worker readiness. Missing required access blocks its operation.
- A read-only agent type may still expose shell writes. Supply the read-only
  contract and inspect the post-review diff against the actual initial dirty and
  untracked state. Report unexpected mutations; preserve them for reconciliation
  instead of blindly resetting the workspace. Instructions are not sandboxing.
- Use completion notifications or status tools actually exposed. Absence of a
  background flag does not imply that the host blocks. If no resume capability
  exists, provide a new worker the durable task record, prior result and current
  candidate, then verify that it can access them. A new worker is not the old
  process resumed, and old capability observations require rechecking.
- Validate adapter/resource links in each selected package, skill names against
  discovery metadata, and source/generated-manifest agreement. Then run a native
  discovery and bounded execution trial. Package tests alone are not host proof.

These bindings adapt PStack's Claude guide at
`9580c23696ac8d7abed0c166f2f9918800afb819`. Retain exact task identity for history
recovery and required-evidence blocking when unsupported operations are needed.

## Authority and state

Commit, push, pull request creation, merge, deploy, messages, tracker edits,
installation, deletion, and paid calls are separate permissions. A playbook name
does not grant them. This task's existing authority still applies.

`integrated-workflow` keeps approved programme and publication gates. Prepare
the local change when publication is outside the request.

Do not install hooks, plugins, or MCP servers because a playbook mentions them.
Shared `forge-*` skills install with this harness. `codex-forge` and
`forge-setup` do not. Read the shared Forge runtime before those skills
dispatch a worker.

## Planning and evidence

Planning stays read-only when the assignment says so. Prototype writes need
execution authority. Choose checks that can falsify the real behavior. A green
typecheck does not prove a UI, device, or performance claim.

Recall reads only the authorized task. Redact secrets before they enter a
receipt or pull request. Do not write global memory, `CLAUDE.md`, or another
project's files unless the task asks for that file.

## Sources

The methods come from the shared engineering playbooks, which adapt Lauren Tan's
PStack and poteto-mode. Upstream MIT notice:
`../../engineering-playbooks/LICENSE.txt`. This adapter is an independent Claude
binding. It does not change the Cursor plugin or claim that every Claude product
surface was executed.
