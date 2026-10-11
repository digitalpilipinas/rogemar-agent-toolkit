# Claude Code dynamic workflow binding

Apply the [shared bounded method](../../workflow-orchestrator/references/dynamic-workflows.md)
only for a suitable authorized task. Keep `workflow-orchestrator` as owner and use
Claude Code's native workflow runtime as the executor. Installation does not enable
workflows, authenticate Claude, launch agents or alter model/permission settings.

## Preflight and authoring

Verify the installed Claude Code version, the current session's workflow capability,
account access and applicable permission controls. A version number alone is not
live access. Load the native `/workflow-authoring` instructions when available before
authoring/editing a workflow script; discover the actual supported API there rather
than inventing flags. If unavailable, keep the method usable through an authorized
ordinary-worker fallback and mark the native workflow unverified.

Use task-scoped invocation. Do not enable session-wide `ultracode`, bypass
permissions, install hooks or change global settings as part of skill installation.
Do not depend on a keyword in a headless prompt to activate the feature. Inspect
the actual Workflow tool permission path on that surface. A script's generated
worker prompt cannot create user authorization.

Before launch, show phases, candidate, scope, agent counts including retries, read
and write boundaries, and stop conditions. Reuse existing task approval; preserve
native permission prompts. A new material scope decision pauses dependent work.
If human sign-off is required between stages, split those stages into separate
runs; do not expect an in-run user question to supply that sign-off.

## Runtime mapping

Qualify every distinct assignment through `claude-forge-setup` against the current
workflow-agent API, not just the ordinary Agent tool. Carry valid role mappings,
owner limits and native pins; only translate options that the live API accepts.
Record requested, accepted and observed settings separately, including any native
model substitution. Unverified metadata stays unverified. A saved mapping neither
switches the parent nor proves worker execution.

The workflow script owns phase sequencing and bounded fan-out. Agents perform
filesystem and shell operations; do not assume the script has shell, filesystem
or module-loading access. Use the supported agent result/schema mechanisms.
Retain per-assignment errors/null results with their inventory IDs. Handle a failed
direct awaited call as well as failures inside a parallel batch; neither may erase
independent work or silently satisfy a review requirement.

Enforce total attempts and concurrency in the script's scheduling logic, including
replacement and retry paths. Reserve enough capacity for reviewers/challengers.
The workflow size guideline is advisory. Runtime limits may be stricter; neither
the guideline nor an agent's promise implements the task's smaller hard limit.
On replay/relaunch, account for attempts already consumed and results invalidated
by changed prompts/candidates. If the runtime cannot bound automatic restarts under
the agreed attempt limit, report the limitation before launch; do not claim the cap.

Use native workflow events/status for monitoring and stop controls. Keep the exact
script, candidate and evidence references in the existing task receipt. A saved or
resumed run is not fresh evidence for a changed candidate. Persist a reusable command
only within approved file scope after qualification; do not ship an untested runtime
script as a verified integration. No always-on watcher is added by this method.

## Qualification and installation

Test native execution on the approved single-directory pilot: package coverage,
independent review, challenged findings, failure isolation and stop/cap behavior.
Until that runs, report `instructions installed; native execution unverified`.
Local source checks and mocked tests do not establish Claude runtime support.
Run the managed installer separately inside each reachable cloud environment;
GitHub publication and local installation do not establish cloud adoption.

Source: [Claude Code workflows](https://code.claude.com/docs/en/workflows), reviewed
2026-10-11. Recheck native documentation when the selected runtime/API changes.
