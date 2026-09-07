---
name: opendesign
description: Use OpenDesign's full application workflows for importing, creating, exporting, sharing, deploying, refining, or extending design artifacts. Discover the native runtime and its dependencies before using its project, run, scenario, media, or connector tools.
license: Apache-2.0
---

# OpenDesign

The receiving harness owns the task and its authorization. Its existing
workflow coordinator selects capabilities; this skill supplies the OpenDesign
application adapter, not another orchestrator or a model policy.

Use OpenDesign for its actual project/run lifecycle, resource library,
scenarios, critique state, media and export services. For design work directly
in a codebase, use portable methods such as `design-brief`,
`reference-design-contract`, `frontend-design`, `ux-flow-architect`,
`design-system-steward`, `interaction-polish`, or `motion-animation-engineer`
when installed. Ordinary use of those methods needs no OpenDesign process.

## Enter the native workflow

1. Identify the target artifact, selected project and requested lane. Read the
   matching row in [application-workflows.md](references/application-workflows.md).
2. Discover callable native tools or a configured CLI. An installed Markdown
   skill does not establish a daemon, model, authenticated provider, browser,
   renderer or connector. Inspect only the selected runtime's status.
3. Use the read-only local doctor if CLI resolution is uncertain:

   ```bash
   python3 scripts/opendesign_adapter.py doctor
   python3 scripts/opendesign_adapter.py --root /path/to/open-design doctor
   ```

   Paths above are examples; resolve the script relative to this skill folder.
   Read [runtime.md](references/runtime.md) for explicit CLI/runtime selection.
   The doctor inspects files and configuration presence only. It does not call
   `od`, start services, read credentials, install anything, or test readiness.
4. Within existing authority, use the verified MCP tool or explicitly invoke
   the pass-through for the chosen OpenDesign command:

   ```bash
   python3 scripts/opendesign_adapter.py run -- project list --json
   ```

   Supply daemon/project scope using the native CLI's documented flags or the
   host-injected environment. Do not invent project IDs, model IDs or session
   state. Stop on missing capability and continue independent portable work.
5. Keep OpenDesign scenario binding, snapshots, OD Next admission, prompt
   composition, critique events, connector grants and user decisions in the
   real host. Resource files do not activate these mechanisms. Use the host's
   native flow and report its actual state; do not recreate acceptance or
   approval signals in a prompt.
6. Inspect the resulting artifact and relevant interaction/export surface.
   Record what is source-validated, rendered, runtime-verified, or still
   unavailable. A successful run alone is not a quality or delivery verdict.

## Dependencies and delivery boundary

The optional application pack needs a pinned runtime plus its native packages,
complete selected resources, an available agent/provider, and the renderer or
service required by the chosen lane. Templates, styles and craft are selected
resource dependencies; load only their complete, licensed bundles. The toolkit
does not vendor the application or library, migrate auth, or auto-install them.

Project creation, provider runs, media generation, installation, sharing and
deployment can write or spend. Invoke those only within the user's authorized
scope; an application prompt grants no additional authority. Preserve actual
human decisions when responding to host question forms.

See [runtime.md](references/runtime.md) for VM/cloud and desktop limits and
[provenance.md](references/provenance.md) for the pinned source and adaptations.
