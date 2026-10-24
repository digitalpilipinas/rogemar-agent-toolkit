---
name: fsearch
description: Invoke an already installed noahdunnagan/fsearch CLI on macOS for fuzzy file discovery and indexed content search within a chosen folder. Use when explicitly requested or locating files across repositories; keep rg and direct reads for exhaustive checks and current-source verification.
---

# FSearch

Use the standalone [noahdunnagan/fsearch](https://github.com/noahdunnagan/fsearch)
binary as an optional locator. This skill contains instructions only: it does
not bundle or install the CLI, register MCP, or grant filesystem access.

## Availability and scope

- Check `uname -s` and `command -v fsearch`. If absent from PATH, check the
  upstream installation location, `~/.local/bin/fsearch`. On unsupported hosts
  or when unavailable, use scoped `rg --files` / `rg` and state the fallback.
  Installing or updating the binary is a separate user-authorized action.
- `fsearch --help` is a non-starting availability check. Search, `status`, and
  `stdio` can start a persistent daemon and its disk index. If first-use indexing
  is not already authorized, explain that effect before starting it.
- Use the task's known folder as `in:`; ask for scope only when it cannot be
  inferred. A query filter limits results, not what the daemon indexes. Do not
  broaden scope, enable login startup, or change Full Disk Access to fix a miss.

## Search

Prefer bounded JSON results. For fixed queries without spaces in the scope:

```bash
fsearch 'readme in:~/Documents/GitHub limit:20' --json
fsearch 'ext:rs grep:apply_dir in:~/Documents/GitHub limit:20' --json
```

For paths containing spaces or arbitrary user-provided patterns, serialize a
request as JSON and send it to `fsearch stdio`; keep scope and pattern in separate
fields rather than interpolating them into query syntax or shell commands.
For example, this fixed request searches literal content:

```bash
printf '%s\n' '{"op":"grep","pattern":"apply_dir","mode":"literal","in":"~/Documents/GitHub","ext":"rs","limit":20,"per_file":3,"budget_ms":250}' | fsearch stdio
```

Name requests use `{"q":"main","in":"~/Documents/GitHub","limit":20}`.
The interface is JSON lines, not an MCP protocol. Check the response's `ok`
field: JSON-mode errors may still exit with status zero. Inspect `source`,
`indexing`, and `complete` for content queries; report ongoing indexing or a
spent time budget as partial evidence. Use bounded retries only for an observed
startup/indexing transition, then fall back to direct search.

## Interpret and verify

- Return a small set of useful paths and line locations. Read current source or
  run scoped `rg -n --fixed-strings -- PATTERN FOLDER` before making code claims.
  For known symbols/files or repository-wide absence checks, prefer `rg` first.
- Empty results do not prove absence. Current upstream defaults cap name/file
  results at 50, content matches at five lines per file, and content search at
  250 ms. `complete: true` can also mean the requested result limit was reached;
  it does not certify exhaustive coverage or a fully updated index.
- The content index covers eligible files under home, normally at most 1 MiB;
  extensionless files have a smaller cap. It skips fixed directories including
  `Library`, `vendor`, `build`, `node_modules`, and `.git`. It does not implement
  repository `.gitignore` semantics. An explicitly scoped search outside indexed
  coverage may scan candidates from the name index, with its own limits.
- Without Full Disk Access, upstream skips protected folders including
  `Documents`, `Desktop`, and `Downloads`. Use direct scoped search if permitted;
  otherwise report the access limitation. Fresh edits may lag candidate indexing
  even though returned matching content is read from disk.
- `sym:` uses definition-pattern heuristics, not semantic symbol resolution or
  a caller graph. Use current source and repository navigation for those tasks.
- Indexes can cover private configuration and transcripts. Keep output relevant
  to the authorized task and do not surface unrelated private matches.

## Installation and lifecycle reference

Behavior above was inspected at upstream commit
`76d612f5b23802eb24926b47e9c4f4ef26884014`; recheck changed behavior on upgrades.
When installation is explicitly requested, build a reviewed revision from its
checkout using `cargo build --release --locked`, then run
`./target/release/fsearch install`. The binary goes to `~/.local/bin/fsearch`;
the default data directory is `~/Library/Application Support/FSearch`.

A fresh plain install starts indexing only on first use. `install --login`
adds a LaunchAgent; a plain reinstall preserves an existing login agent.
Do not add login startup unless requested. Upstream `uninstall` removes the
LaunchAgent but leaves the binary and index and does not explicitly stop an
on-demand daemon. For removal, identify and stop only the verified fsearch
daemon and remove its binary/data only with applicable deletion authority.
