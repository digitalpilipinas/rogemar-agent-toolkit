# Source and adaptation notice

Copyright and license: OpenDesign contributors, Apache-2.0; full terms in
[LICENSE.txt](../LICENSE.txt). This toolkit adapter and its references are
modified/new integration material, prepared 2026-09-07. The OpenDesign app,
private state, plugin cache and resource catalogue are not copied here.

Source snapshot: `digitalpilipinas/open-design`, version `0.21.1`, commit
`ff2cc80f336f94786128113eddbbb9e3719fecc8`; upstream `nexu-io/open-design`.

- [Portable skill protocol](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/docs/skills-protocol.md)
- [Seven lanes and plugin contract](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/plugins/spec/README.md)
- [Native CLI](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/apps/daemon/src/cli.ts)
- [Generated runtime/MCP configuration](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/apps/daemon/src/mcp-install-info.ts)
- [Export and renderer boundary](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/apps/daemon/src/import-export-routes.ts)
- [Runtime quickstart](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/QUICKSTART.md)
- [Container recipe](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/deploy/Dockerfile)
- [Deployment contract](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/apps/daemon/src/routes/deploy.ts)
- [OD Next admission](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/apps/daemon/src/strategies/od-next/rollout.ts)
- [Prompt composition](https://github.com/digitalpilipinas/open-design/blob/ff2cc80f336f94786128113eddbbb9e3719fecc8/docs/prompt-composition.md)

Adaptation: retain the complete application route through the native CLI/MCP;
make local preflight read-only; avoid ambiguous POSIX `od`; keep the receiving
harness's tools/model/authorization policy; distinguish external dependencies
and live proof. Optional templates/style/craft remain selected, licensed
resource bundles with their own provenance and asset constraints.
