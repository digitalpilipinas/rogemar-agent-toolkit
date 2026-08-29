# Compatibility and evidence boundary

## Verified targets for version 0.2

- Static package validation on macOS.
- Project and user installation logic on macOS and Linux/WSL-compatible Python.
- Codex plugin structure through `.codex-plugin/plugin.json`.
- Cursor/Agent Skills structure through `.agents/skills` and the portable
  Agent Plugins manifest.

Runtime discovery in a fresh Codex task, Cursor UI discovery, Codex workspace
GitHub import, and a Linux/WSL host remain separate smoke-test evidence. Do not
claim them passed until they are actually performed in those environments.

The catalog also records audit-observed Antigravity/Gemini, Grok Build, Junie,
Command Code, and codex-router runtime surfaces. “Audit-observed” describes
catalog evidence captured during a bounded local audit; it is not a live probe
and does not prove that a fresh VM, cloud worker, or newly authenticated account
has the same capabilities.

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

## Cursor, pstack, Team Kit, and GoalBuddy

GoalBuddy is represented as an external, runtime-managed dependency from
[tolibear/goalbuddy](https://github.com/tolibear/goalbuddy). It is recorded in
the catalog and reported by `doctor` as an external dependency when the local
Codex plugin catalog is available;
the toolkit does not vendor or authenticate it.

Cursor's `pstack` is represented as a separate external Cursor plugin from
[cursor/plugins/tree/main/pstack](https://github.com/cursor/plugins/tree/main/pstack).
Install it in Cursor with `/add-plugin pstack`. It is not installed in the
current Codex environment and is intentionally not copied into `.agents/skills`:
its playbooks, principles, and Cursor-specific runtime behavior do not provide
portable cross-harness parity by themselves. The pstack upstream also points
to `cursor-team-kit` for additional `deslop`, `control-cli`, and `control-ui`
capabilities; those are separate dependencies and are not silently included.

The bounded audit recorded a local pstack package labeled `0.14.2` and a cache
label `0.14.5`; the catalog records both without treating either label as
proof of Cursor activation. Cursor's first-party `skills-cursor` directory,
Cursor Team Kit, and other marketplace cache entries are runtime-managed.
Cache presence is not proof of enablement or authentication.

## External runtimes and provider integrations

Antigravity/Gemini, Grok Build, Junie, Command Code, and codex-router are
documented as runtime integrations or external skill groups. The toolkit does
not copy their binaries, provider homes, credentials, sessions, histories,
chat databases, or proprietary/unlicensed payloads. The
`agent-collaboration-terminal` skill can coordinate compatible providers, but
it does not make a missing provider runtime or credential available.

Junie remains an IDE/CLI runtime with a separate Codex supervisor package. Do
not treat an IntelliJ plugin archive or Junie CLI ACP documentation as proof of
a direct Codex ACP bridge; verify the target protocol and package format first.

## Project overlays

Repository-specific `AGENTS.md`, hooks, credentials, database policy, release
rules, and project learning stay in their project repositories. They are not
silently injected by this toolkit.
