# Portable planning and review methods

Reviewed on 2026-09-07. The portable core keeps four existing entry names:
`create-plan`, `first-time-right-delivery`, `code-review-and-quality`, and
`code-review-tests`. Planning produces one plan; quality review owns one finding
record and verdict; the other two contribute evidence to that work. Runtime
adapters retain model selection, native agent/tool APIs, and provider setup.

## Planning coverage

The local inventory was grouped by `(name, skill_sha256)`, so identical copies
and symlinks were not treated as separate methods. The case-insensitive name
filter `plan|brainstorm|goal|orchestrat` found **17 distinct descriptors**. All are
accounted for below. Hashes identify the reviewed pre-integration source, not the
new portable revision. Source labels are inventory categories, not install paths.

| Source and entry | Descriptor hash prefix | Decision |
| --- | --- | --- |
| Canonical/Codex/shared and Junie `create-plan` | `f4239ff9fa`, `accc91eab2` | Retain repository grounding, scope, useful steps, and acceptance. Remove the older mandatory per-plan model routing and mandatory large template. |
| Superpowers `brainstorming` | `4a54a4858b` | Retain context first, meaningful alternatives, scope control, and checking ambiguity. Do not require repeated design approvals or a committed spec for an obvious edit. |
| Superpowers `writing-plans` | `72190c88b2` | Retain concrete paths, interfaces, dependency order, and coverage self-review. Do not require complete implementation code, minute-sized tasks, or a commit per step. |
| Superpowers `executing-plans` | `c4c3d8b628` | Retain revalidation of an existing plan and evidence before completion. Execution remains a separate selected workflow, not a planning prerequisite. |
| Grok bundled `execute-plan` | `d864306344` | Retain dependency validation and recovery from recorded evidence. Keep its PR DAG runner, worktree protocol, state schema, and stack tools native. |
| Cursor native/shared `goal` | `95d2b1b1fb`, `e3a2388ae1` | Native goal controls. A renamed description does not translate the runtime mechanism. No automatic goal creation in the core. |
| GoalBuddy Codex and Claude `goal-prep` | `ceef8e95a9`, `39ca616027` | Retain observable completion, preserving an existing plan, bounded useful slices, and final evidence audit. Its board compiler, visual hub, roles, and prep/execution boundary remain optional GoalBuddy behavior. |
| Canonical/Codex/shared and Junie `plan-model-router` | `6044e2252f`, `0c9daaa632` | Runtime policy rather than a universal planner. Preserve task-fit and validation principles; fixed families and callable model choices belong to the selected adapter. |
| Canonical/Codex/shared and Junie `workflow-orchestrator` | `05774fc6d0`, `75083d2fcc` | Keep one coordination owner, scoped capability selection, ownership, and evidence. Planning hands back once rather than starting a second coordinator. |
| Cursor Figma `generate-project-plan` | `0cc7b78009` | FigJam board production with native foundation skills and rendering tools. Optional artifact workflow, not required for a text plan. |
| Antigravity IDE extension `gcp-pipeline-orchestration` | `197afdeb6d` | Cloud Composer deployment/configuration method. Domain pack; “orchestration” here is application behavior. |
| Cursor RevenueCat `rc-plan-changes` | `b61b3fe23f` | Android subscription replacement method. Domain pack; “plan” here is a billing product. |

The source review also followed method-bearing entries outside that name filter:

- **PStack and Codex Forge:** both local Poteto Mode versions, PStack's
  investigation, feature, and multi-phase-plan playbooks, and the Forge
  multi-phase-plan/runtime contract. Retain investigation before decisions,
  explicit data/contracts, useful increments, and evidence on the affected
  surface. PStack's Cursor bindings and Forge's Codex bindings stay separate.
  Fixed reviewer counts, mandatory live/performance checks for every edit, and
  automatic publication or scheduling do not enter the portable planning core.
- **Grok `design`:** inspected its document writer/reviewer methods and execution
  boundary. Retain concrete decisions, feasibility checks, and evidence-backed
  disagreement. Do not import a mandatory two-agent loop or “zero nits” exit rule.
- **Existing delivery family:** compared both `first-time-right-delivery` and
  `dream-team` revisions, plus `integrated-workflow` and its
  `deliver-approved-programme` alias. Preserve acceptance, compatibility,
  authority, and evidence. Personas remain presentation choices; programme
  execution remains optional. The evidence skill no longer creates its own
  mandatory matrix or model-routing step.

A broader metadata filter, `\bplan(?:ning|s)?\b|brainstorm|goal|orchestrat` over
name and description, produced **77 distinct descriptors**. The additional
matches were classified from their stated purpose. They include domain plans
(hackathon `build-spec`, React Doctor `improve-react`, migration, release,
security-hardening, Webflow and data workflows), artifact templates and charts,
provider/connection controls, workflow runtimes, and incidental uses such as
subscription pricing plans. They are not 77 competing general planners.
Domain planning entrypoints were checked where needed to establish that boundary;
their full operational workflows were not executed or folded into the core.

## Independent review consolidation

| Source method | Retained | Kept separate or removed from the default |
| --- | --- | --- |
| Existing `code-review-and-quality` (`8f3cabca58`), identified by the owner as the Antigravity-style method | Correctness, readability, architecture, security, performance; concrete remedies and fair review judgment. | This is the toolkit's approved local source. The inventory does not establish that it is an official Antigravity runtime skill. Remove blanket file/diff-size blockers, duplicated checklists, and mandatory model diversity. |
| Existing `code-review-tests` (`1131d5d1a2`) | Requirements coverage, regression checks, relevant counterexamples, and evidence at the reviewed candidate. | It contributes to the same review; a missing test is not itself proof of a bug. |
| Codex runtime `review-agent` (`07079efd0d`) | Defect-first, complete in-scope diff, affected callers, reproducible impact, no invented findings. | Native invocation and priority/output contract remain runtime-owned. No runtime file is vendored. |
| Cursor `review`, `review-bugbot`, `review-security`; Grok `review` (`656c5e50f5`) | Exact review target, read-only findings, truthful empty/unavailable states, scoped evidence. | Native subagent APIs, scratch helpers, UI choice, and GitHub review posting stay in their adapters. A review request does not silently publish comments. |
| Cursor `thermo-nuclear-code-quality-review` and Grok `code-review` (`df6f708a52`) | Find specific structural burdens and propose a simpler model or ownership boundary. Their reviewed bodies differ only in naming/frontmatter. | Strict maintainability mode remains opt-in. A plausible rewrite, a line threshold, or taste alone is not a default blocker. |
| Superpowers requesting/receiving review; Ponytail review | Review a named candidate against requirements, independently verify feedback, preserve valid compatibility, and identify concrete unnecessary complexity. | No mandatory external reviewer, automatic fix loop, “net lines” score, or complexity-only shipping verdict. |
| CodeRabbit personal snapshot (`6be93f37ed`), Codex plugin 1.1.4 (`515ef4f096`), Cursor plugin snapshot (`5cd8d760a2`) | Preserve distinct provider identity, scope, authentication, and its reported results. | These same-named `code-review` entries invoke CodeRabbit; they are not aliases for the general five-axis owner. No provider execution, installation, authentication, or transmission is implied by loading the portable method. |

Use one current finding ledger, including external IDs when several reviewers
report the same cause. Validate disagreements against source and checks before
fixing. Keep optional suggestions distinct from required defects. Focused
rereview follows changed behavior or a required gate; repeated full passes do
not run merely because another skill contributed a lens. Required independent
review stays unmet when the selected capability is unavailable.

## Provenance and packaging

- The maintained source is
  [the toolkit skill tree](../plugins/rogemar-agent-toolkit/skills/), with source
  declarations in [the catalogue](../catalog/skills.yaml). Existing license files
  remain intact; the modified Apache-licensed planning files carry change notices.
- Superpowers source was inspected from the local plugin declaring version 6.2.0,
  with its [upstream repository](https://github.com/obra/superpowers) and MIT license.
  The core synthesizes task methods rather than vendoring that plugin.
- PStack provenance and the existing adapted playbook coverage remain in
  [the Forge manifest](../catalog/codex-forge-upstream.json) and
  [its runtime contract](../plugins/rogemar-agent-toolkit/skills/codex-forge/references/codex-runtime.md).
  This change does not replace either engineering family.
- Grok, Codex system, Cursor-native, GoalBuddy, CodeRabbit, and application/plugin
  sources were read as local evidence. Their proprietary or runtime-managed
  contents were not copied. Their availability remains an adapter/dependency
  concern. Existing unverified upstream attribution is not upgraded to a license
  claim by this review.
- Install the four portable entries together in the core. They have no required
  MCP, model family, external provider, board, or GUI dependency. Both planning
  templates must accompany `create-plan`. Keep `code-review-tests` discoverable
  for compatibility; route general reviews to `code-review-and-quality`.

## Validation and limits

The installed skill-creator `scripts/quick_validate.py` passed for all four
modified skill directories. Local reference checks and `git diff --check` cover
the edited files. These checks establish structure and resource presence, not
behavioral certification across harnesses. Repository lock, installer, package,
and integration checks belong to the final integrated candidate.

No provider CLI, planning workflow, goal board, app runtime, or external review
was executed during this source review. Fresh Codex, Cursor, Grok, VM, and cloud
behavior still requires the corresponding installation and runtime evidence.
