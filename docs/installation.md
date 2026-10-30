# Installation and recovery

Start with the [README quick start](../README.md#get-started). This guide covers
selection, alternative installation routes and recovery. Run commands from a
reviewed toolkit checkout using Git and Python 3.9 or later.

## Choose packs

A fresh install starts with seven core skills: `workflow-orchestrator`, `create-plan`,
`first-time-right-delivery`, `bug-triage`, `code-review-and-quality`,
`code-review-tests` and `project-readiness`. Add only the packs useful for the project.

| Pack | What it adds |
| --- | --- |
| `engineering` | Forge adapters, engineering playbooks, Integrated Workflow, testing and performance methods. |
| `design` | Briefs, reference fidelity, UX, frontend implementation, accessibility-related methods, polish and visual checks. |
| `web` | Browser verification and web implementation helpers. |
| `mobile` | Shared mobile lifecycle and compatibility methods. |
| `argent`, `expo`, `ios`, `android` | Platform methods and declarations of the tools needed for their runtime checks. |
| `security`, `data` | Relevant security, privacy, database and data-contract methods. |
| `opendesign` | The OpenDesign application adapter and its native workflow guidance. |
| `opendesign-library` | An optional separately imported resource library. |

The [generated inventory](../README.md#complete-skill-inventory) retains the full
membership and external dependency lists. Packs may share skills; the installer
resolves required skill dependencies and filters incompatible native entries.

`select` previews a selection without reading an existing installation's saved
profile. Supply explicit matching profile/pack options to compare it with an
installation. An install/upgrade `--dry-run` also checks the actual destination,
existing ownership, saved state and conflicts without changing files.

```bash
python3 scripts/toolkit.py select --harness cursor --profile core --pack engineering --pack design
python3 scripts/toolkit.py install --harness cursor --profile core --pack engineering --pack design --target project --project-root /path/to/project --dry-run
```

Remove `--dry-run` only when that proposed installation is the one you want.
Use `--profile all` for every compatible pack. It does not activate every external
application, model, SDK or service. A listed dependency may have its own account,
license, installation and authentication requirements.

## Project, personal or plugin installation

Use `--target project --project-root /path/to/project` to keep skills with one
project. Use `--target user` for a personal installation. Paths depend on the
selected harness; see the [path matrix](compatibility.md#harness-adapters).

Codex shares portable skills through `.agents/skills` and places its native-only
skills in `.codex/skills`. Cursor uses the catalog's `.cursor/skills` layout.
Other targets have their own mappings. These paths specify file delivery, not
proof that a particular assistant version discovers them. Start a fresh task
and verify discovery after installation. Remote workers need their own project
skills or an appropriately prepared environment; personal files do not imply
remote availability.

Choose one primary managed installation per shared project/home root. Avoid
loading the same skill through both an installed plugin and personal copies.
Development-only `--link` creates links back to the checkout; use copied skills
for portable environments.

For a Codex marketplace route, build a selected archive:

```bash
python3 scripts/toolkit.py package --harness codex --profile core --pack engineering --pack design --output /path/to/archives
```

Extract the **Codex marketplace archive**, then register that extracted directory
using the plugin controls supported by your Codex version. The archive contains
only its selected skills and compatible packs. Registering the entire source
repository exposes the full canonical tree and is appropriate only when you
intentionally want that scope. Use the full source checkout to add a pack omitted
from a smaller archive. Do not also install the same selection through personal
skill directories.

The portable agent-plugin archive is the other output. It contains selected
portable skills and a content receipt; it is not a complete machine image with
browsers, device runtimes or authenticated providers.

## Cursor native plugin and managed extras

For native plugin discovery, add this **repository URL** as a marketplace in
Cursor's Customize controls:

```text
https://github.com/digitalpilipinas/rogemar-agent-toolkit
```

The repository's `.cursor-plugin/marketplace.json` points to
`plugins/rogemar-agent-toolkit`, whose generated `.cursor-plugin/plugin.json`
selects the full Cursor-compatible toolkit, including `cursor-forge` and
`cursor-forge-setup`. Codex-only and Claude-only entries are excluded. Keep this
folder name: `main` in GitHub's `/tree/main/...` browsing URL is a branch, not a
directory to create or rename.

The Cursor Agent CLI can register or refresh the marketplace:

```bash
agent plugin marketplace list --format json
# Only if this repository is not already registered:
agent plugin marketplace add https://github.com/digitalpilipinas/rogemar-agent-toolkit
# For an existing registration, use its name from the listing:
agent plugin marketplace update <existing-marketplace-name>
```

Then select and install the toolkit in Cursor's plugin controls. Marketplace
registration alone does not prove plugin installation or skill discovery. Check
the installed plugin's skills for `cursor-forge` and `integrated-workflow`, and
verify their source is this plugin. Use the skill picker for the invocation
name exposed by your Cursor version.

The native plugin does not run our installer or provision external skill files.
From a reviewed toolkit checkout, preview its managed extras in each receiving
environment:

```bash
python3 scripts/toolkit.py install --harness cursor --profile all --external-only --target project --project-root /path/to/project --dry-run
```

Remove `--dry-run` to apply the reviewed selection. Existing separately managed
or runtime-owned copies must be reconciled, not overwritten silently. Upgrade
these extras using the same target with `toolkit.py upgrade --harness cursor`;
the saved external-only mode and selection are retained. Verify managed extras
with scoped `doctor` checks and actual Cursor discovery, separately from the
native plugin. Installation does not authenticate tools or install device runtimes.

Alternatively, omit the native plugin and use the complete managed `--harness
cursor` installation. Do not install the same toolkit selection through both
routes. For an archive, `package --harness cursor --profile all` includes the
Cursor selection; other archive selections may omit Cursor-native methods.
The generated manifest always references only compatible skills in that archive.
See [Cursor's plugin format](https://cursor.com/docs/reference/plugins).

## Native manifests for other harnesses

The repository also contains native Claude and Factory marketplace catalogs,
Gemini extension metadata, and Antigravity-compatible metadata in matching
selected archives. All refer to the same skill source. Keep one toolkit owner in
each environment; a new manifest does not require replacing an existing managed
installation.

For a selected native bundle, run the existing packager with the receiving
harness. Core remains the seven-skill default. For example:

```sh
python3 scripts/toolkit.py package --harness claude --pack engineering --output dist/claude
python3 scripts/toolkit.py package --harness droid --profile all --output dist/droid
python3 scripts/toolkit.py package --harness gemini --pack engineering --output dist/gemini
python3 scripts/toolkit.py package --harness antigravity --pack engineering --output dist/antigravity
```

Extract the **agent-plugin ZIP** from the matching output directory. Its
`rogemar-agent-toolkit/` directory is the plugin/extension root, and its actual
`skills/` directory contains only that catalog selection. The separate
Codex-marketplace ZIP retains its Codex-specific route. Review the
`release-selection.json` receipt before importing a bundle.

For Claude, the extracted directory supports `claude --plugin-dir <directory>`.
For Gemini CLI, its native local route is `gemini extensions install <directory>`.
For Antigravity CLI, use an authorized `agy plugin install <directory>` with the
extracted Antigravity archive. Its root `plugin.json` matches the native schema;
the raw source tree's portable manifest does not. Factory uses a marketplace
entry; its source can point to the extracted directory in an operator-maintained
local marketplace.
These are optional operator actions, not steps performed by `package`.

The repository-root Claude/Factory marketplaces point at the full source plugin.
Claude adds manifest `skills` paths to its default `skills/` scan; Factory loads
skills from that directory. Native metadata alone does not exclude other harness
adapters from the raw source tree. Prefer selected archives or managed
`install --harness claude|droid|gemini|antigravity` for a compatible set.
The native plugin does not provision pinned external packs; those retain the
existing managed `--external-only` route. Installation, discovery, authentication
and workflow execution remain separate evidence.

See the [native compatibility table and official format references](compatibility.md#native-metadata-across-harnesses).

## Devin: choose one toolkit owner

Devin supports both native Git plugins and `.agents/skills`. Use one of these
routes in each receiving environment; installing the same toolkit through both
creates duplicate discovery. Both routes use Universal Forge and the existing
portable model router. There is no separate `devin` installer harness.

| Route | Toolkit skills | Third-party skill files |
| --- | --- | --- |
| Native Git plugin + managed extras | Generated Devin manifest exposes the full compatible portable selection. | Managed `--external-only` installation using selected catalog pins. |
| Complete managed installation | Managed `agent-skills` selection; core by default, `--profile all` for the full setup. | Provisioned by that same installer. |

### Native Git plugin + managed extras

Install the plugin from its **subdirectory**, not the repository root:

```bash
devin plugins install "digitalpilipinas/rogemar-agent-toolkit#plugins/rogemar-agent-toolkit"
devin plugins info rogemar-agent-toolkit
```

In Customize → Plugins → Add plugin → From repository, use repository
`digitalpilipinas/rogemar-agent-toolkit` and subdirectory
`plugins/rogemar-agent-toolkit`. A GitHub `/tree/main/...` browsing URL is not
a substitute for the repository/subdirectory fields. The Cursor marketplace
at the repository root does not make that root a Devin plugin. The generated `.devin-plugin/plugin.json` takes
precedence over the portable manifest and selects compatible skills explicitly.
It excludes native Codex, Cursor and Claude entries. No repository maintenance
`AGENTS.md`, hooks, MCP servers or upstream plugin dependencies are registered.
The existing portable and Codex manifests retain their own behavior.

Invoke toolkit skills with their plugin namespace, for example
`/rogemar-agent-toolkit:create-plan`, `/rogemar-agent-toolkit:universal-forge`,
and `/rogemar-agent-toolkit:integrated-workflow`.

The Git plugin does **not** run the Python installer. From a reviewed toolkit
checkout, provision its compatible third-party skill files separately, inside
**each** receiving project or cloud environment:

```bash
python3 scripts/toolkit.py install --harness agent-skills --profile all --external-only --target project --project-root /path/to/project --dry-run
python3 scripts/toolkit.py install --harness agent-skills --profile all --external-only --target project --project-root /path/to/project
```

Use `--target user` instead of the project options for a personal installation
on that machine. External-only mode copies no canonical toolkit skills; it uses
the existing pinned recipes, resources, notices, conflict checks and backups.
It does not execute upstream installers or register upstream rules and hooks.
It does not install or authenticate provider applications, devices or services.
The native Git plugin always exposes the full compatible toolkit selection;
external pack choices control only the separately managed extras.

### Complete managed installation

If you prefer one managed installer for the toolkit and extras, omit the native
plugin installation and `--external-only`:

```bash
python3 scripts/toolkit.py install --harness agent-skills --profile all --target project --project-root /path/to/project --dry-run
python3 scripts/toolkit.py install --harness agent-skills --profile all --target project --project-root /path/to/project
```

Skills live in the receiving project's `.agents/skills`, without the native
plugin namespace. Omitting `--profile all` retains the normal core default.

### Updating and checking each route

For the native route, update the plugin with
`devin plugins update rogemar-agent-toolkit`. Check out the newly reviewed toolkit
revision separately before upgrading managed extras. For either managed route:

```bash
python3 scripts/toolkit.py upgrade --harness agent-skills --target project --project-root /path/to/project --dry-run
python3 scripts/toolkit.py upgrade --harness agent-skills --target project --project-root /path/to/project
```

Upgrades retain the saved external-only/full mode and pack selection. Existing
installation states remain full installations. A full managed installation cannot
be converted with `--external-only`; reconcile its ownership before switching
routes. Omitting the flag on an external-only installation **does not** convert
it to full mode. `--skip-external` and `--link` conflict with external-only mode,
including when that mode comes from saved state. Dry runs do not fetch or write.
Rollback uses the existing command and restores the preceding transaction; each
external family has its own transaction, so a failed fetch preserves successful
families and can be retried. Removed external pack selections do not delete
previously installed external copies; inspect ownership before removing them.

Verify the native and managed layers separately, from the receiving project:

```bash
devin plugins info rogemar-agent-toolkit  # Native route only
devin skills list
devin skills show rogemar-agent-toolkit:integrated-workflow  # Native route only
devin skills show unlazy  # Both full examples above include this managed extra
```

Confirm the reported source paths, not just names that might come from another
installation. From the toolkit checkout, check managed hashes and resources:

```bash
python3 scripts/toolkit.py doctor --harness agent-skills --target project --project-root /path/to/project --method unlazy --json
```

For a complete managed installation, also check `--method integrated-workflow`.
For the native route, that method is owned by the plugin, not the managed state;
use Devin's plugin/skill commands for it. Discovery is not workflow execution or
authentication evidence. No engineering task is needed for these checks.

Keep existing cloud projects and environments. Run managed install/upgrade there;
a native plugin update cannot update managed extras, and a successful Mac check
does not prove cloud adoption. Missing cloud access remains unverified. Reindex
in Customize if its listing is stale; CLI content update and web indexing are
separate operations. See the official [Devin plugin guide](https://docs.devin.ai/cli/extensibility/plugins/overview)
and [skill locations](https://docs.devin.ai/cli/extensibility/skills/overview).

## Updates and recovery

Check out the reviewed revision you intend to install. Preview before updating:

```bash
python3 scripts/toolkit.py upgrade --harness codex --target user --dry-run
python3 scripts/toolkit.py upgrade --harness codex --target user
```

With neither profile nor pack options, an upgrade preserves the saved selection.
An explicit `--profile core` clears saved optional packs. Add `--pack` options for
the extras you want to keep. Supplying a new pack list replaces the old optional
pack list; it is not an implicit append. Preview removal as well as additions.

The installer refuses to overwrite unmanaged files or locally modified managed
skills silently. A conflict means inspect those copies before proceeding:

- `--adopt-identical` adopts an unmanaged skill only when its complete contents
  match the source.
- `--backup-conflicts` explicitly permits replacement after you review the
  differences, retaining the displaced contents in a backup.
- Skills removed from a managed selection remain recoverable through rollback.
- Legacy installation state requires an explicit harness choice before migration.

To restore the previous managed installation:

```bash
python3 scripts/toolkit.py rollback --harness codex --target user
```

Rollback restores the recorded files and managed state while retaining displaced
newer contents. It is not a way to replace unrelated files. If another copy exists
in a second discovery directory, compare its complete contents, source and owner
before deciding which should remain. The installer does not silently delete it.
Runtime-owned plugin caches and project-specific overlays remain outside this
reconciliation.

## OpenDesign

Choose `design` for portable design methods, `opendesign` for native application
workflows, and `opendesign-library` for optional resources. They can be combined.
The adapter preserves Import, Create, Export, Share, Deploy, Refine and Extend,
including the application's scenario and review state.

The catalog pins OpenDesign 0.21.1. Build/install the app using that revision's
instructions. Its Node/pnpm requirements, native SQLite/PTY/media components,
providers, renderers and connectors remain separate dependencies. Check a built
installation without starting a workflow:

```bash
python3 plugins/rogemar-agent-toolkit/skills/opendesign/scripts/opendesign_adapter.py --root /path/to/built-open-design doctor
```

Import the pinned revision's complete resources from an existing local source:

```bash
python3 scripts/toolkit.py resources --source /path/to/open-design --destination /path/to/design-library --dry-run
python3 scripts/toolkit.py resources --source /path/to/open-design --destination /path/to/design-library
```

This reads pinned Git objects for `design-templates/`, `design-systems/`, `craft/`
and license files. It does not fetch source, copy a user database or credentials,
or install the app. Resources stay outside skill discovery. Configure the native
app to use them through its supported controls, or load a relevant template/style
for portable work.

Headless project/HTML workflows are source-supported. PDF, image and PPTX exports
need the Electron renderer; a bare daemon cannot provide them. Docker still needs
its own provider CLIs and template resources. See the
[application workflow matrix](../plugins/rogemar-agent-toolkit/skills/opendesign/references/application-workflows.md)
for detailed runtime boundaries.

## Verify what is actually ready

`toolkit.py verify` checks the repository and content lock. Installer tests check
selection, placement and recovery. Neither proves that an assistant loaded a
skill, a provider is authenticated or a device flow works.

After installation, check discovery in a fresh task and exercise only the tools
needed for the intended work. Keep installed, discovered and successfully executed
states separate. Required unavailable capabilities remain blocked; optional ones
can use a disclosed in-scope fallback. See [compatibility](compatibility.md) for
current evidence limits and [releasing](releasing.md) for maintainer checks.

## shadcn

Select the optional adapter with `--pack shadcn`, or as part of `--profile all`.
Core and the general design pack do not include it. For example:

```sh
python3 scripts/toolkit.py select --harness codex --profile core --pack design --pack shadcn
python3 scripts/toolkit.py install --harness codex --profile core --pack design --pack shadcn --target project --project-root /path/to/project --dry-run
```

Use the intended harness and complete desired pack selection when installing or
updating. The adapter is portable across supported harnesses; installing it does
not install shadcn packages, fetch registries or start services. Native mobile UI
continues through its existing methods. Runtime invocation must be verified in
the chosen harness independently of package installation.

## Automatic external skill provisioning

`install` and `upgrade` now install and update compatible external skill files for the
selected packs, by default. Use `--profile all` for all compatible packs. The core
profile still installs only core skills. This works in local, CI and Cloud
filesystems, using Git and Python; it does not depend on Mac paths or personal sync.
`--dry-run` lists missing, upgradable, legacy and conflicting names and pinned revisions without network access.
`--skip-external` explicitly requests a vendor-only/offline installation.

The engineering pack selects Unlazy and Ponytail on every harness, and PStack
on Cursor. The compatibility pack selects CodeRabbit. Other packs select their
own pinned repositories, including Expo, Argent, Supabase and Convex. The catalog pins those commits. Skill resources and license
notices are copied directly from upstream Git objects; no upstream installer is
executed. Unchanged toolkit-installed copies are upgraded when their pin changes.
Provenance and executable/content hashes are checked before replacement. Independent,
symlinked or locally edited copies are reported as conflicts and preserved, even
with `--backup-conflicts`. Legacy markers without hashes are compared to their
recorded upstream source before adoption; unavailable evidence cannot authorize replacement.

External updates use the same staged transaction, operation lock, backups and
`rollback` command as vendored updates. Each successful dependency is a recoverable
operation: rollback reverses the latest operation, and can be repeated to reach its
predecessor. A failed dependency does not discard successfully installed dependencies;
installation exits nonzero and lists unresolved conflicts/failures. Retry only after
reviewing the reported cause. Dry-run does not fetch legacy evidence and reports it
as unverified. `--skip-external` preserves installed external copies unchanged.


Native plugins, MCPs, CLIs, platform toolchains, authentication and paid-provider
runs are separate. For example, installing PStack skill files is not installing
its Cursor native workers; Universal Forge supplies portable methods elsewhere.
Factory/Droid uses `--harness droid` and `.factory/skills`; invoking Droid still
requires explicit provider selection and available credentials/models.
Installing this repository does not activate paid services or approve hooks.

In an existing Cloud environment, run the same install command there (or append it
to its existing setup script), then inspect actual skill files and resources in that
runtime. Do not claim all Cloud agents updated from a local directory count.

## Scoped readiness after installation

Use `python3 scripts/toolkit.py doctor --harness cursor --target user --method e2e
--capability node --exercise --json` (on one line) for selected files and tools.
Add `--auth-check` only for a selected live service that needs it. Probes never
log in, expose auth output or prove a completed feature. Installed skills, host
discovery, authenticated services and exercised journeys are separate evidence.
See the orchestrator’s `references/route-readiness.md` for context and worker briefs.
Run the same install/upgrade inside each reachable cloud environment; matching
repository revisions or local sync indicators do not prove VM installation.


### Maintaining routing source metadata

External installation recipes carry per-skill descriptions, invocation policy,
instruction hashes and required files from the exact pinned source. During an
approved source update, fetch the reviewed revision into an inspection checkout,
then inspect `python3 scripts/external_metadata.py --dependency NAME --checkout PATH`.
After reviewing the result, repeat with `--write` and regenerate
`python3 scripts/routing_catalog.py --write`. Run the normal lock/verify and package
checks. Neither helper fetches or executes upstream code; ordinary verification
is offline. Reviewed `routing_overrides` record stricter toolkit boundaries
separately and cannot relax an upstream explicit-only flag.

### Project footprints and task tags

A skill that reads or writes paths inside a project declares them as `footprint`
entries in `catalog/skills.yaml`, on its vendored entry or on its dependency for
pinned third-party packs: `path`, `access` (read or write), `tracking` (tracked,
ignored or either), `class` and an optional `gitignore` hint (ignore or unignore).
`routing_catalog.py` collects them into the routing index's `footprints` list.
Project readiness turns that list into one setup plan for the owner; nothing
writes a project path or ignore rule from this metadata alone.

`task_tags` is the pinned tag vocabulary. Each tag may carry detection `markers`
(a glob, optionally with a `contains` string) that readiness uses to recognize a
project's technologies; tags without markers come from the task itself. A skill's
`task_tags_any` may use only declared tags. `tests/test_footprints.py` fails when
skill text names a project path that no footprint declares, apart from harness
or tool configuration that projects own (`.cursor/`, `.claude/`, `.github/` and
similar).

The routing resolver flags installed instructions that differ from their reviewed
external hash. Preserve local copies and investigate ownership through the managed
installer; do not overwrite them to make a readiness check pass. A matched hash
establishes instruction identity; required-file checks establish resource presence.
Neither proves host discovery, unchanged resource content or authentication.

### Comparing selected upstreams

During approved toolkit maintenance, run `python3 scripts/upstream_compare.py
--source coderabbit --source mattpocock/skills` on one line, or `--all`. Select
dependency IDs or imported repository names from the existing catalogs. The helper
performs read-only requests to public GitHub, authenticated only when `GITHUB_TOKEN`
is set; it never installs, repins, logs in or executes downloaded code. It reports
observed commits, changed paths, selected-content relevance, release-metadata-only
changes and unavailable or incomplete comparisons. Rate limits remain unavailable
evidence, not “current.”

Each adapted path is compared from its own adaptation pin. When an adaptation's
paths have different pins, or GitHub's 300-file compare cap hides them in a large
repository, the helper diffs those paths' Git trees directly (`method: tree`). An
adaptation's optional `reviewed` commit records upstream changes inspected and
deliberately not adopted, with the reason in `divergence`; it does not change
which upstream files were adapted. The weekly `Upstream drift` workflow runs
`--all` and opens or updates one issue when adapted paths change.

Review instruction/resource/license changes before updating a recipe and metadata.
A pinned recipe provisions selected compatible skill files. Native plugins, tools,
accounts and paid services remain conditional runtime integrations. Entries with
only a repository link or runtime-managed provenance remain references, not a
promise of copied skill files. Run comparisons for affected sources at maintenance
time; ordinary tasks reuse installed, qualified methods.

## Diagram Design

Diagram Design is an optional, separately installed upstream plugin/skill. The
`design` pack includes a small integration guide through `vector-asset-pipeline`;
it does not vendor the upstream example library or register its native plugin.
Use one upstream installation per receiving harness, separate from the toolkit.

For Codex, use the upstream marketplace (leave sparse paths empty):

```sh
codex plugin marketplace add cathrynlavery/diagram-design
codex plugin add diagram-design@diagram-design
```

Check existing marketplaces/plugins first to avoid duplicates. For native Claude
or Droid installation, follow the [upstream instructions](https://github.com/cathrynlavery/diagram-design).
Where no supported native route is available, including the documented Cursor
standalone route, install the unmodified upstream Agent Skill with `npx skills add
cathrynlavery/diagram-design`, selecting only the intended harness and copy layout.
Native command wrappers are not included in a standalone skill installation.

Native plugin and standalone skill updates are separate from toolkit updates.
Use the installed upstream version's update command, inspect its actual source,
and test required operations. The integration was reviewed against revision
`7a2e22170ee838e859d8142ba825d83f8b6375e6` (2.6.74); that observation does not pin
an independently updated plugin forever. Do not install another copy when the
same capability is already supplied by a working plugin.

Reuse project tokens and upstream-supported separate profiles; do not edit an
installed skill or plugin cache. Prefer system fonts and no external requests.
Static guidance needs no login. Reviewed Python helpers need Python 3.10+; PNG
needs Python Playwright/Chromium or a separately verified browser capture route.
Resource presence, native discovery and actual execution are separate checks.
Repeat setup and verification inside each receiving cloud environment; no local
plugin update establishes cloud adoption.

## Updating an installed toolkit

A GitHub push updates the source repository. It does not establish that an installed
plugin, a copied skill directory, or a running agent has loaded that revision.
Record the source, tracked ref, installed version and a successful fresh-session
discovery check for each receiving harness. A version recorded in a manifest is
not proof that it was published, installed or loaded by a running session.

| Installation route | Update behavior and verification |
| --- | --- |
| ChatGPT/Codex workspace marketplace imported from GitHub | New workspace imports have daily sync enabled. An admin can use **Sync now**. A tracked branch receives newer commits; a fixed commit remains pinned. Verify the import result and start a fresh session before checking discovery. |
| Personal/local Codex marketplace or plugin | Use the installed Codex version's supported marketplace/plugin refresh controls. Do not infer workspace daily sync applies to this route. Confirm the installed version and resource contents in a new session. |
| Claude Code marketplace | Auto-update is a per-marketplace setting, off by default for third-party and local marketplaces. Enable it in `/plugin` → Marketplaces, or update the installed plugin explicitly. Reload plugins or start a new session to load an update. Refreshing a marketplace list alone is not an installed-plugin update. |
| Cursor team marketplace imported from GitHub | With the GitHub App configured, **Enable Auto Refresh** reindexes pushes on the tracked branch, at most once every ten minutes. Otherwise use **Refresh**. Running Cloud Agents keep their starting version; start a new agent. Other Cursor installation routes need their own observed update behavior. |
| Toolkit installer, archives, copied Agent Skills, other harnesses | These files have no update daemon. Refresh the authorized source, review the change and rerun the existing supported installation/update route for the same selection. Preserve local modifications; never overwrite an unmanaged copy blindly. |

An update receipt should distinguish source publication, marketplace sync, installed
files and runtime loading. Verify representative required resources and one safe
invocation; discovery alone does not qualify the workflow. Toolkit updates do not
update independently installed dependencies, credentials, MCP services or models.
No installation or auto-update setting is changed merely by maintaining this repo.

Sources reviewed on 2026-10-24: [OpenAI workspace marketplace sync](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github),
[Claude plugin updates](https://code.claude.com/docs/en/discover-plugins), and
[Cursor plugins](https://prod.cursor.com/docs/plugins). Recheck native behavior
when the receiving harness or installation route changes.

The local Codex CLI observed during this update is `0.161.0`. Its help exposes
`codex plugin marketplace upgrade <marketplace-name>` to refresh a configured Git
marketplace snapshot. Discover the actual configured name with the supported list
command; do not assume the marketplace name equals the repository name. This
command was inspected, not executed. A refreshed snapshot still needs installed
content and fresh-session verification; the help output does not establish
automatic updates or hot reload of the running session.
