---
name: agent-map
description: Use a local, on-demand repository map to reduce exploratory file reads and token use during unfamiliar-code, architecture, multi-file refactor, branch, and commit tasks. Build incremental metadata-only indexes, locate likely files/symbols/callers, check freshness, and fall back to direct search when the map is stale or incomplete. Do not use for known-file edits or simple one-file tasks.
---

# Agent Map

## Purpose

Use a small local index as a navigation aid before reading unfamiliar code. The map is a locator, not source-of-truth: always verify decisions against current source and tests.

The skill is intentionally local-only. It does not install Graft, use an LLM, send source over the network, add hooks, register MCP, edit agent configuration, or modify `.gitignore`.

## When to use

Use this skill when the task involves one or more of:

- an unfamiliar repository or subsystem;
- architecture discovery or “where does this live?” questions;
- a multi-file change, refactor, rename, or dependency-impact review;
- tracing callers, imports, entry points, or related tests;
- repeated work in a repository where broad search/read cycles are expensive.

Skip it when the user names the exact file and symbol, the change is a small one-file edit, or the repository is small enough that indexing would cost more than direct inspection.

## Workflow

Resolve the bundled script path as `<skill-dir>/scripts/agent_map.py` and run it with the repository as `--root` (normally `.`). Keep command output bounded; do not dump the generated index or whole source files into context.

### 1. Check freshness

```bash
python3 <skill-dir>/scripts/agent_map.py status --root .
```

The status check compares the current branch/HEAD, working-tree state, file set, and size/mtime metadata. It is local and cheap; refresh hashes files that changed. Use `status --full-hash` after unusual tooling that may preserve timestamps. If the map is missing or stale, refresh it before querying.

### 2. Refresh incrementally

```bash
python3 <skill-dir>/scripts/agent_map.py refresh --root .
```

Refresh only re-parses changed files when the existing manifest is compatible. Use `--full` after parser/schema changes, large merges, or when the map reports uncertainty.

The default output directory is `.agent-map/`. It contains metadata and line locators only. `INDEX.md` and `RELATIONSHIPS.md` are the human-readable views; the JSON files are machine-readable caches and may be large. Do not commit the directory unless the project explicitly wants generated architecture artifacts; add it to the project’s ignore policy manually if needed. The script never edits ignore files.

### 3. Orient, locate, and trace

```bash
python3 <skill-dir>/scripts/agent_map.py map --root .
python3 <skill-dir>/scripts/agent_map.py find "booking status" --root .
python3 <skill-dir>/scripts/agent_map.py callers "createBooking" --root .
python3 <skill-dir>/scripts/agent_map.py skeleton src/booking/service.ts --root .
```

- `map` shows bounded repository clusters, entry points, hubs, languages, tests, and freshness.
- `find` ranks paths, symbols, and import relationships matching the query.
- `callers` shows inbound references and the defining file for a symbol.
- `skeleton` shows a file’s declarations and line locations without opening its body.

Read the returned files and narrow line spans directly. Run one locator query, then act; do not repeatedly rephrase the same query.

### 4. Verify and fall back

If a result is stale, partial, ambiguous, unsupported, or inconsistent with source, stop relying on it and use `rg`, language-server tooling already present in the repository, or direct reads. Treat missing edges as unknown, never as proof that no caller exists.

Before changing a shared symbol, run `callers` and inspect the relevant tests. For a known file or symbol, go directly to source instead of paying the map-query overhead.

## Refresh policy across edits, commits, and branches

Use frequent freshness checks, not frequent full rebuilds:

1. Build once when first needed.
2. Check the manifest before each map query.
3. Re-index only changed files and rebuild affected import/reference edges.
4. Detect branch/HEAD changes and use a matching cache or incrementally refresh.
5. Run `refresh --full` periodically, after parser changes, or after a difficult merge.

Do not install a global commit or prompt hook. A project may opt into a local post-commit or post-checkout refresh later, but the skill must remain correct without hooks and must never block a coding task on background indexing.

## Safety and privacy

- Keep generated output local and metadata-only; do not store source bodies, secrets, credentials, or LLM summaries.
- Exclude dependency directories, build output, generated files, `.env*`, key/certificate material, and other secret-like paths.
- Never make network calls or install dependencies as part of mapping.
- Do not modify source, agent settings, `.gitignore`, hooks, MCP, or global configuration automatically.
- Show `fresh`, `stale`, `partial`, and `unsupported` states explicitly.

## Token and correctness guardrails

- Keep root orientation output roughly 1,000–2,000 tokens or less.
- Prefer paths, symbols, line numbers, and relationships over source bodies.
- Count map generation, refresh, query, targeted reads, and fallback reads when evaluating savings.
- Do not emit “tokens saved” claims unless actual provider usage is available; `chars / 4` is not billing data.
- A map is successful only when total context/tool cost decreases without a correctness regression.

## Reusable project instruction

When a project wants Codex to use this skill routinely, add only a short rule to its `AGENTS.md` (do not paste the generated map):

```text
For unfamiliar architecture or multi-file changes, use the agent-map skill once to locate files and callers, then read current source directly. Check freshness first, verify all conclusions against source/tests, and fall back to rg when the map is stale or incomplete. Skip the map for known-file or simple edits.
```

## Evaluation

Before adopting the workflow broadly, compare 5–10 representative tasks against a graft-free control. Record available provider input/output tokens, tool calls, elapsed time, correctness, stale/unsupported results, and local refresh overhead. Keep the map only if the complete workflow is measurably cheaper and no less accurate.

## Resource

- `scripts/agent_map.py` — dependency-free local indexer and bounded query CLI.
