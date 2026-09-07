# OpenDesign application workflows

The seven lanes are OpenDesign's taxonomy, not a claim that every named service
or target has a native integration. CLI spellings below were checked at the
pin in [provenance.md](provenance.md); use the installed CLI's help when versions
differ. Each command goes through the real configured native runtime.

| Lane | Native route | Dependencies, verification and limits |
|---|---|---|
| Import | `project import <baseDir>`, `import-folder <path>`, `figma import`, `design-systems import-local/import-github/import-shadcn`, `library import` | Confirm selected project/files. Local `.fig` decoding is offline; Figma URLs need the configured connector. Remote imports need network. Inspect imported artifact and relative resource closure. Library imports accept selected design formats, not arbitrary audio/video binaries |
| Create | `project create --name ... --skill ... --design-system ...`; `run start --project <id> --prompt-file <path> --agent <available-agent> --follow`; `plugin run <id> --project <id> --agent <available-agent> --follow`; `media scaffold/generate/wait` | Select an installed template/skill and complete resources. Confirm agent/provider/model and spend scope. `plugin run` applies a plugin and starts a run on an existing project. Inspect actual artifacts, run status and host questions; never fabricate a completed stage |
| Export | `export <file> --project <id> --format html\|pdf\|image\|pptx --out <path>`; framework export scenarios; HyperFrames media rendering | HTML is headless; PDF/image/PPTX requires Electron renderer. React/Vue/Next.js handoff is agent adaptation into a real receiving codebase with its checks. MP4 needs browser/native media dependencies. Open the produced format and check referenced assets |
| Share | `share url --url ...`; `collab share/publish`, `share-resource`; connector or plugin publication flows | URL sharing prepares share targets and does not itself post or host the artifact. Team sharing needs workspace/member/service scope. Publication and external messages require their own authorization. Verify the actual destination only when posting/sharing was requested |
| Deploy | `deploy <projectId> --file <fileName> --provider vercel-self\|cloudflare-pages [--target preview\|production]` | Requires accepted artifact, network and provider account/configuration. Vercel's explicit production target is rejected at this pin; its current route behaves as preview. Other taxonomy targets need a real plugin/connector/CLI. Verify returned deployment and public route within authority |
| Refine | `od-design-refine`, critique/patch atoms, `run redesign --path ...`, follow-up `run start`, `files diff`, saved versions, `lint <file>` | Inspect current artifact and design contract, apply bounded changes, and use real host critique/run state. Lint does not establish visual quality. Use the selected host's approved rendering/inspection tools and report any missing evidence |
| Extend | `plugin scaffold/validate/pack/install/doctor/simulate/verify/publish-repo`; `skill install` | Author portable `SKILL.md` with an OD sidecar for native plugin behavior. Preserve assets, references, licenses and relative paths. Registry-bound validation may warn offline; packing success is partial evidence. Installation and publication remain separate actions |

## Host mechanisms that remain native

OD Next is bundled strategy content and needs validated host binding; merely
copying it does not activate it. The host owns eligible agent/task selection,
content/behavior enablement, bundled identity, assignments, runtime capability
verification, production-active approval and stop-latch state.

Scenario binding persists provenance, plugin ID and snapshot identity. The
host checks snapshot consistency, strategy provenance and task profile,
validates the prompt recipe and stage atoms, hashes a resource roster, and
stages non-prompt resources separately. Legacy and OD Next prompt composition
are distinct paths. Preserve deck navigation/message contracts, continuation
and actual critique events in that host.

Required connectors can be connected, pending or unavailable; token issuance
and execution recheck grants. Headless `ui list/show/respond` exposes host
forms but does not let an agent invent the user's answer. A missing binding,
renderer, connector or admission is a blocked native route, not permission to
emulate a successful runtime from copied prompts.
