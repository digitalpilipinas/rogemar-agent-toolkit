# Claude adapter

Use only with the shared working instructions in Claude Code. The user entry is `~/.claude/CLAUDE.md`; use supported `@path` imports for the installed core and this adapter. Preserve repository/nested CLAUDE.md imports of their AGENTS.md; AGENTS.md alone is not assumed to auto-load in Claude. Imported content consumes context and does not extend cache lifetime.

Use supported Claude skills and controls. `workflow-orchestrator` dispatches; `claude-forge` and `claude-forge-setup` own native Forge mapping. Qualify actual worker settings and existing parent/user limits; do not import Codex/Cursor model IDs or claim a parent switch from a saved preference. Portable fallback preserves constraints and required independent evidence.

Keep existing tool, permission and scheduling settings. No hook, paid provider, authentication or new background process follows from installing instruction files. Use loading diagnostics when available; persisted files do not prove an active session reread them.
