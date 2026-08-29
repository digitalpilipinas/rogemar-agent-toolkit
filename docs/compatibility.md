# Compatibility and evidence boundary

## Verified targets for version 0.1

- Static package validation on macOS.
- Project and user installation logic on macOS and Linux/WSL-compatible Python.
- Codex plugin structure through `.codex-plugin/plugin.json`.
- Cursor/Agent Skills structure through `.agents/skills` and the portable
  Agent Plugins manifest.

Runtime discovery in a fresh Codex task, Cursor UI discovery, Codex workspace
GitHub import, and a Linux/WSL host remain separate smoke-test evidence. Do not
claim them passed until they are actually performed in those environments.

## Functional parity

Vendored skills are installed from this repository. System skills, third-party
skills, marketplace plugins, MCP servers, apps, and credentials remain owned by
their source runtime. `doctor` reports their observed availability but does not
install, enable, authenticate, or copy them.

A skill that references a tool can be discovered even when the tool is absent.
That state is degraded, not functionally ready. Provider permissions and
workspace policies remain authoritative.

The root README links each currently represented public upstream and gives its
author-supported latest-install command. Those mutable latest installs are an
operator choice; they do not replace the toolkit's pinned lockfile. Refreshing
a vendored upstream requires a license/diff review followed by lock regeneration
and validation.

## Cursor pstack and GoalBuddy

GoalBuddy is represented as an external, runtime-managed dependency from
[tolibear/goalbuddy](https://github.com/tolibear/goalbuddy). It is recorded in
the catalog and detected by `doctor` when the local Codex plugin is available;
the toolkit does not vendor or authenticate it.

Cursor's `pstack` is represented as a separate external Cursor plugin from
[cursor/plugins/tree/main/pstack](https://github.com/cursor/plugins/tree/main/pstack).
Install it in Cursor with `/add-plugin pstack`. It is not installed in the
current Codex environment and is intentionally not copied into `.agents/skills`:
its playbooks, principles, and Cursor-specific runtime behavior do not provide
portable cross-harness parity by themselves. The pstack upstream also points
to `cursor-team-kit` for additional `deslop`, `control-cli`, and `control-ui`
capabilities; those are separate dependencies and are not silently included.

## Project overlays

Repository-specific `AGENTS.md`, hooks, credentials, database policy, release
rules, and project learning stay in their project repositories. They are not
silently injected by this toolkit.
