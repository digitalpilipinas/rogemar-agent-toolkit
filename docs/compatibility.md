# Compatibility and evidence boundary

The installer targets Python 3.9+ on macOS, Linux and WSL. It copies selected complete skill trees and resolves declared hard skill dependencies. File placement is testable separately from whether a running agent discovers or executes a skill.

## Harness adapters

| Harness | Project root | User root | Runtime evidence |
| --- | --- | --- | --- |
| agent-skills | `.agents/skills` | `.agents/skills` | Fresh-session discovery required |
| codex | `.agents/skills` | `.agents/skills` | Fresh-session discovery required |
| cursor | `.cursor/skills` | `.cursor/skills` | Fresh-session discovery required |
| gemini | `.gemini/skills` | `.gemini/skills` | Fresh-session discovery required |
| antigravity | `.agent/skills` | `.gemini/antigravity/skills` | Fresh-session discovery required |
| grok-build | `.grok/skills` | `.grok/skills` | Fresh-session discovery required |
| junie | `.junie/skills` | `.junie/skills` | Fresh-session discovery required |
| command-code | `.commandcode/skills` | `.commandcode/skills` | Fresh-session discovery required |
| z-code | `.zcode/skills` | `.zcode/skills` | Fresh-session discovery required |
| claude | `.claude/skills` | `.claude/skills` | Fresh-session discovery required |

Codex places native-only entries in `.codex/skills`; shared methods live once in
`.agents/skills`. Its full 45-skill Forge family uses `plan-model-router` to qualify
worker assignments. Cursor uses `cursor-forge` and `cursor-forge-setup` for native
role/model mappings; the universal router is a fallback when that route is
unavailable. Upstream PStack/poteto-mode remains a separate, unchanged entry.
Other assistants use `universal-forge` with `universal-plan-model-router` and their
own observed capabilities. Shared engineering methods may run sequentially on the
current model when worker controls are unavailable.

Peak, Balanced, Lean and Sprint share intent across adapters, not identical model
IDs, prices or capabilities. A selected profile and an accepted dispatch are not
proof of the effective model. Record observed runtime identity separately. A saved
mode does not switch the running parent; parent switching needs a supported live
control and verified result. Required independence cannot be supplied by merely
renaming a sequential pass.

See [installation and recovery](installation.md) for matching previews, saved
selections and plugin-archive boundaries. Unknown assistant names should use the
portable route and that assistant's documented import mechanism; do not invent a
new installer `--harness` ID or assume native controls from a product name.

These paths combine official format support and the local inventory's observed user layouts. They are delivery adapters, not certification of every harness version. For a harness whose installed version differs, use its documented skill import path and verify discovery; do not copy into runtime builtin/plugin cache directories. Use only one primary managed installation per shared root. Project overlays are never inferred from global skills.

## Evidence levels

- Local catalogue, content, packaging and installer tests verify static structure and simulated target layouts.
- Independent instruction walkthroughs cover Gemini sequential engineering, Codex native Forge, and Cursor review ownership; they do not execute those runtimes.
- OpenDesign command-adapter tests verify resolution, literal argv, read-only doctor and native exit codes. A pinned resource import verifies complete file delivery separately.
- Fresh Codex/Cursor/Gemini/Grok/Junie/ZCode/Command Code sessions, clean Linux/WSL hosts, authenticated providers and rendered app/device behavior require separate smoke evidence.
- A dependency's presence, CLI success or cached plugin version does not prove it is enabled, callable or authenticated.

## OpenDesign and platform limits

OpenDesign keeps its real project/run, scenario admission, snapshots, critique and connector mechanisms. It needs Node 24.x, the pinned pnpm/build lock, native SQLite/PTY/media packages, and the chosen provider. Headless project/HTML workflows are source-supported. PDF/image/PPTX need the Electron renderer; its absence is an unsupported dependency path. The Docker source omits agent CLIs and template copies; selected resource import does not provision a whole runnable image. See [design integration](design-integration.md).

Argent is a full external 16-skill family. Methods may be read without MCP; device actions require its supported tool server and device runtime. iOS simulators require a Mac/Xcode host. Android requires the matching SDK/JDK and a usable device or emulator; ordinary cloud containers may lack virtualization. Web checks need a supported browser driver. Expo's current upstream entry names differ from the recorded local cache and are updated by its owner. Codex Security remains a separate optional provider.

## Provenance and updates

Runtime-managed system skills, proprietary plugin caches, credentials, histories and project-only overlays are not vendored. The complete canonical inventory includes licensed source snapshots and owner-maintained methods; keep each upstream notice. Changing a pinned source requires review, a new lock and relevant validation. The optional resource importer reads pinned Git objects rather than the source working tree.

## Checked discovery references

- [Cursor skill locations and cloud copying](https://cursor.com/docs/skills): project `.agents/skills` or `.cursor/skills`; personal shared skills are not automatically copied into remote workers. Install project skills or bake them into the worker image.
- [Gemini discovery tiers](https://geminicli.com/docs/cli/skills/): native and `.agents/skills` aliases are supported; the shared alias wins within a tier.
- [Junie skill locations](https://junie.jetbrains.com/docs/agent-skills.html): project and user `.junie/skills`.
- [Command Code skill locations](https://commandcode.ai/docs/skills): native and shared paths are supported, with native precedence.

These documentation checks were made on 2026-09-07. Grok/ZCode user directories are local observations; their fresh remote discovery remains unverified.

## Invocation and provider compatibility

Skill discovery, explicit-only policy, MCP registration and service access are
separate checks. The capability maintainer's trigger reference covers moved
paths, native invocation controls and recoverable duplicate selection. Cursor
`disable-model-invocation` imports need Codex `agents/openai.yaml` policy when
explicit-only behavior is intended; retain their native Cursor metadata.

CodeRabbit remains standalone: use its own installed skill and full review of
the selected candidate. Shared review reconciliation does not replace or shorten
its provider workflow. No new login or installation follows from discovery alone.
