---
name: codex-capability-maintainer
description: Use when auditing, adding, updating, or troubleshooting Codex skills, MCP servers, plugins, connectors, automations, hooks, AGENTS.md, global config, or secret-safe local agent capabilities.
---

# Codex Capability Maintainer

## Workflow

1. Inventory current capabilities first: installed skills, MCP servers, plugins/connectors, repo guidance, and config.
2. Separate durable surfaces:
   - Skills for reusable workflows.
   - MCP servers/connectors for live data and actions.
   - Plugins for bundled skills/tools/connectors.
   - Custom agents for reusable role, permission, and sandbox contracts.
   - `AGENTS.md` for repo conventions.
   - Config/hooks for mechanical enforcement.
3. Prefer one canonical global source for reusable skills. When multiple
   runtimes require installed mirrors, keep them byte-identical and validate
   every surfaced copy; do not maintain independent repository forks of a
   global workflow.
4. Before retiring a skill, inspect its callers and resources. Move reusable
   behavior to the canonical global skill and project-only contracts to the
   repository's `AGENTS.md` or maintained product documentation.
5. Prefer official or widely maintained MCP servers over obscure packages.
6. Keep API keys and secrets local, ignored, and out of committed files.
7. After skill changes, run the skill validator, inspect referenced resources,
   and compare every required installed mirror byte-for-byte. After custom-agent
   or config changes, confirm the config loads, the expected agent types surface,
   and any configured model/effort is accepted by the active runtime.
8. Treat a custom-agent role as behavior and permission policy. Route its model
   and reasoning through the active parent ceiling; a fixed role setting must
   not silently override that ceiling.
9. For a materially changed orchestration workflow, perform focused smoke
   exercises for one exploration handoff, one authorized implementation-routing
   example, and one independent-review handoff. Report them as separate
   evidence from structural validation.
10. Verify registrations with `codex mcp list` or `codex mcp get <name>` after
    MCP changes. Tell the user when a restart or login is required before new
    tools appear in future turns.

## Recommended Core Stack

- Official OpenAI docs MCP for current OpenAI/Codex docs.
- GitHub MCP for PRs, issues, checks, and repo workflows.
- Supabase MCP for projects using Supabase database, auth, storage, functions,
  and logs.
- Perplexity for live research.
- Firecrawl for crawling and structured web extraction.
- Replicate or image generation tools for asset creation.
- Private workspace plugins such as Notion, Drive, Gmail, Calendar, Slack, or Teams when the user wants private data access.

## Guardrails

- Do not install API-backed MCPs with real keys in public repo files.
- Do not promise a tool is usable until it is registered and authenticated.
- Avoid adding too many overlapping tools to a single active context.
- Retire duplicate skills recoverably until replacement discovery and caller
  checks pass.
