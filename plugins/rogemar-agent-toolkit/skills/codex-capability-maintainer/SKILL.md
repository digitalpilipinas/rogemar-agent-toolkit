---
name: codex-capability-maintainer
description: Use when auditing, adding, updating, or troubleshooting Codex skills, MCP servers, plugins, connectors, automations, hooks, AGENTS.md, global config, or secret-safe local agent capabilities.
---

# Codex Capability Maintainer

## Workflow

1. Inspect the capabilities relevant to the request: installed skill instructions,
   surfaced live tools, applicable guidance and configuration. Static methods need
   readable instructions/resources; live services need authentication only when
   that service requires it. Discovery does not authorize installation or login.
2. Separate durable surfaces:
   - Skills for reusable workflows.
   - MCP servers/connectors for live data and actions.
   - Plugins for bundled skills/tools/connectors.
   - Custom agents for reusable role, permission, and sandbox contracts.
   - `AGENTS.md` for repo conventions.
   - Config/hooks for mechanical enforcement.
3. Maintain one canonical source for reusable methods. Identify consumers and
   resolve symlinks before updating installed copies. True mirrors of the same
   implementation should match byte-for-byte; intentional harness adapters may
   differ. Preserve native controls, licenses and approved differences, and
   validate shared behavior against the canonical contract. Back up changed
   files; do not overwrite unrelated local work or runtime-managed caches.
4. Before retiring a skill, inspect its callers and resources. Move reusable
   behavior to the canonical global skill and project-only contracts to the
   repository's `AGENTS.md` or maintained product documentation.
5. Prefer official or widely maintained MCP servers over obscure packages.
6. Keep API keys and secrets local, ignored, and out of committed files.
7. After skill changes, run the applicable validator, inspect referenced
   resources and compare true mirrors byte-for-byte. Review harness adaptations
   for shared-contract consistency and preservation of intentional differences.
   For global guidance, check instruction consumers, links, scope/authorization
   boundaries and conflicting clauses. After custom-agent or config changes,
   verify the relevant runtime controls when available; file edits alone do not
   prove that a running session reloaded guidance or applied a profile.
8. Treat a custom-agent role as behavior and permission policy. Use the active
   harness's qualified routing contract: native Codex workers retain parent
   ceilings without a named Forge mode; an explicitly selected Codex Forge mode
   uses its permitted profiles. Explicit user limits and runtime availability
   still apply. Keep resolution with the model router and dispatch with
   workflow-orchestrator; never bypass the governing policy with a fixed role
   setting or claim a parent-model switch from a preference edit.
9. For a materially changed orchestration workflow, perform focused smoke
   exercises for one exploration handoff, one authorized implementation-routing
   example, and one independent-review handoff. Report them as separate
   evidence from structural validation.
10. Verify registrations with `codex mcp list` or `codex mcp get <name>` after
    MCP changes. Tell the user when a restart or login is required before new
    tools appear in future turns.

For discovery drift, explicit-only imports, or service/skill overlap, read
[trigger maintenance](references/trigger-maintenance.md). Preserve working
entrypoints and provider workflows; repair concrete paths and controls.

## Conditional integrations

These are examples to consider only when the task needs them and a suitable
route is available. They are not a required installation set or authority to
install, authenticate or spend. Select the smallest sufficient route.

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
- Verify a live tool is surfaced/enabled and, when required, authenticated before
  relying on it. Do not require a service login for static skill instructions.
- Avoid adding too many overlapping tools to a single active context.
- Retire duplicate skills recoverably until replacement discovery and caller
  checks pass.
