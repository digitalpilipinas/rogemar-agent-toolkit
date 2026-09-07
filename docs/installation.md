# Installation and recovery

Start with the [README quick start](../README.md#get-started). This guide covers
selection, alternative installation routes and recovery. Run commands from a
reviewed toolkit checkout using Git and Python 3.9 or later.

## Choose packs

A fresh install starts with six core skills: `workflow-orchestrator`, `create-plan`,
`first-time-right-delivery`, `bug-triage`, `code-review-and-quality` and
`code-review-tests`. Add only the packs useful for the project.

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
Use `--profile all` for every compatible pack. It does not install every external
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
