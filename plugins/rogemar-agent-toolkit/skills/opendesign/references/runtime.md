# Runtime selection and evidence

This adapter targets OpenDesign `0.21.1`, source revision
`ff2cc80f336f94786128113eddbbb9e3719fecc8`. See
[provenance.md](provenance.md) for exact source links. A later distribution
must be rechecked against its own CLI and packaging contracts.

## CLI selection

`scripts/opendesign_adapter.py` uses Python 3.10+ and the standard library.
Run it from any directory using its actual installed path.

Selection precedence is `--bin`, `OD_BIN`, `OPEN_DESIGN_BIN`, then
`--root`/`OPEN_DESIGN_ROOT`. A selected but invalid path fails without falling
back to a different runtime. Bare `od` on PATH is deliberately not selected:
on macOS and many Unix systems it is the octal-dump utility. `/usr/bin/od`,
`/bin/od` and aliases resolving to them are rejected even when explicit.

- **Generated executable launcher:** set `OPEN_DESIGN_BIN` or `--bin` to its
  path. It must be executable. The adapter invokes it directly with an argv
  list, without a shell or argument rewriting.
- **Host-injected JavaScript CLI:** `OD_BIN` commonly names `dist/cli.js` or
  packaged `daemon-cli.mjs`. Runtime precedence is `--node`, `OD_NODE_BIN`,
  `OPEN_DESIGN_NODE_BIN`, then Node on PATH. Preserve the host-generated
  environment, including sidecar context; do not reconstruct opaque values.
- **Packaged Electron runtime:** use the app-generated launcher/configuration,
  including its matching runtime, `ELECTRON_RUN_AS_NODE=1` where needed, and
  explicit `OD_DATA_DIR`. A discovered app bundle alone is not a configured
  CLI. The adapter does not guess an executable inside an app or bootstrap it.
  For an explicit packaged JavaScript entry it requires an absolute
  `OD_DATA_DIR`, avoiding an accidental data root inside an app bundle.
- **Source checkout:** `--root` selects `apps/daemon/bin/od.mjs` in a package
  named `open-design`. The wrapper requires `apps/daemon/dist/cli.js`; an
  unbuilt source tree is reported unavailable. Build/install commands are
  separate, explicitly authorized work.

`doctor` never executes the selected command, Node, git or a network probe.
Its `configured` result means the required launcher files resolve, not that
Node's version, native modules, daemon health, agent auth, resources or exports
work. It reports environment-variable presence without printing values. It
does not open the OpenDesign data root, preferences, projects or credentials.
`run -- <argv...>` is an explicit native invocation and may mutate or bootstrap
according to those arguments. It preserves the child's exit code and streams
its output. Review the exact command against current authority before calling.

## Environment matrix

| Route | Required dependencies | Evidence boundary |
|---|---|---|
| Portable methods | Skill reader, file tools and the receiving project's tools | No app required; verify output on its actual surface |
| Source/web runtime | Node 24.x; pnpm 10.33.2; built daemon/web; native SQLite/PTY packages; persistent data directory | Documented development entry is `pnpm tools-dev run web`; no build/start occurs during skill install |
| Built headless daemon | Built CLI, resource roots, persistent SQLite/files; selected model/provider | `daemon start --headless` suppresses browser opening; `--serve-web` does not build a web bundle or supply a renderer |
| Docker/Linux VM | Pinned image version or digest, native runtime compatibility, data volume and configured remote-access policy | Source Docker recipe omits agent CLIs and `design-templates/`; verify selected resources in the actual image. Do not claim complete library parity |
| Packaged desktop | Matching platform package, generated CLI/runtime environment, native renderer | App presence is separate from active daemon, provider auth and renderer registration |

Native daemon dependencies include `better-sqlite3@12.10.0`, `node-pty@1.1.0`,
FFmpeg installer `1.1.0`, and `hyperframes@0.8.1`. Use the pinned application
lockfile for the complete dependency graph. Agent CLIs are separate runtime
dependencies with their own model availability, auth and cost boundaries.
BYOK uses a separate text-artifact transport; it is not automatically equivalent
to a filesystem-capable agent. Media generation additionally needs its selected
service/model and host-injected project context. HyperFrames rendering needs
the pinned browser/runtime and native dependencies, not just HTML authoring.

Headless standalone HTML export is supported. PDF/image/PPTX export needs the
registered Electron desktop renderer; the bare-daemon endpoint returns 501.
External HTTP dependencies may remain in exported HTML. Test the actual target
format. The newer `shells/terminal` package still has a fixture lifecycle seam
at this pin; it is not the established full-app Linux installer.

## Native bridges and acceptance

The project/artifact `od mcp` bridge documents eight tools: `list_projects`,
`get_active_context`, `get_artifact`, `get_project`, `get_file`, `search_files`,
`list_files`, `create_artifact`. It does not expose every CLI workflow.
`od mcp live-artifacts` is a separate bridge. Confirm the actual tool surface
and auth before relying on either. Use package-generated MCP configuration;
an explicit remote daemon URL disables automatic packaged bootstrap.

For a fresh environment, completion evidence is a successful pinned build or
selected distribution; resource presence; one authorized project/run/artifact
flow using the real provider; the intended rendered/exported artifact; and
the chosen connector/publication path when requested. Keep each evidence state
separate. Offline doctor/tests establish none of the live states.
