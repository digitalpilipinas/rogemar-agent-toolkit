# Plan: portable project readiness, method receipts and packaging (1.3.0)

Status: approved 2026-10-30 by the owner ("Approve, plan it") after a Forge
arena comparison; amended the same day to the hybrid readiness entry ("Yes, use
the hybrid") and to an enforced-by-default method receipt ("Yes, enforce by
default"). The owner invokes only `create-plan`, the harness Forge entry and
`integrated-workflow`, and expects agents to follow every routed method.
Extended later that day with a situation map, CI-enforced evidence-linked
receipts, opt-in harness hooks and compliance measurement, on the owner's
condition that each addition be optimized, value-adding and not redundant;
the prompt hook was then approved explicitly.

Delivery: Integrated Workflow, branch + PR + safe merge. Slices 1 and 2 shipped as
PRs #35 and #36; slices 3–9 ship as one PR, with focused tests and a local
CodeRabbit review per slice and one full CI run plus one cloud review wave at the
end (owner, 2026-10-30). All nine slices form one 1.3.0 release tagged
once at the end (owner, 2026-10-30), starting on `claude/toolkit-1-3-0-readiness`. The branch starts stacked on
PR #34 (`ee30ab4`) and is rebased onto `main` once #34 merges. No new provider,
deployment or installation authority. Release tagging stays a separate owner
decision.

Source: the EVERSO proposal (2026-10-30, toolkit 1.2.2) and its three audits,
held outside this repository. Its lessons L1–L11 are summarized below; the
EVERSO-specific capability map and audits stay in that project.

## Outcome

In any supported harness and any project, an agent starting work can see,
before the first task, which repository paths the toolkit's skills will need
and one consolidated setup plan for the owner to approve once. At acceptance,
the methods that the changed paths call for are recorded as used, unavailable,
blocked or not applicable, with a reason for every state but used, so a skipped
review is visible rather than silent.
Nothing in the core names a harness-specific tool, parses a project's own
policy format, or writes policy, pins or ignore rules without owner authority.

## Decisions (from the arena)

- Hybrid readiness entry. The readiness logic lives once, in a script inside a
  thin `project-readiness` method skill in the core pack, so core-only installs
  have it; `integrated-workflow`'s `checkpoint.py` (engineering pack) calls that
  script when both are installed. Its description triggers on
  starting or resuming work in a repository, which every harness surfaces to
  the model; a paragraph inside another skill is only read if an agent follows
  the link, which is how EVERSO's reviews were skipped. The skill is not a
  dispatcher: `workflow-orchestrator` still selects and dispatches.
  `scripts/toolkit.py doctor` is not shipped to installed skills, so it cannot
  host the probe (verified 2026-10-30 against `~/.claude/skills` and the
  `all` agent-plugin package).
- Three layers, because none alone guarantees use: the description-triggered
  skill; a one-line readiness instruction the setup plan proposes for the
  project's own instruction file (`AGENTS.md`, `CLAUDE.md` or equivalent, with
  owner consent); and the method receipt at acceptance.
- Skill footprints are declared in `catalog/skills.yaml` and generated into the
  routing index; a lint fails on undeclared repository paths in skill text.
- The method receipt is enforced by default at Integrated Workflow acceptance.
  Small bounded corrections are exempt; a project can opt out in its trusted
  policy. Elsewhere it reports only.
- Connection state for MCP servers and plugins is observed by the agent at
  runtime and kept in a session file, never generated or committed.
- Declined: parsing a project's ownership policy file; changing agent-map's
  default output (a location declared through readiness wins instead).

## Lessons and where each lands

| Lesson | Summary | Slice |
| --- | --- | --- |
| L1 | Specialist reviews were skipped because routing ran from memory | 1 (record), 4 (check) |
| L2 | Project setup requirements surfaced mid-sprint and needed three consents | 3 |
| L3 | Skill paths collide with guarded repositories | 2, 3 |
| L4 | Trusted-policy pins have no setup path | 1 (how-to), 3 (printer) |
| L5 | Findings lived only in PR merge records | 1 |
| L6 | Role/model plan not shown at slice start | 1 |
| L7 | Statechart → code-level formal check sequence implicit | 1 |
| L8 | Cloud reviewers unavailable; local substitute undocumented | 1 |
| L9 | One PR per lesson is noise; standing single-file grant works | 1 |
| L10 | The full routing index is too broad to scan per slice | 2, 3 |
| L11 | Owner names entry skills only and expects links to be followed | 1 |

## Slices

### 1. Portable docs-only fixes

Files: `workflow-orchestrator/references/route-readiness.md`,
`workflow-orchestrator/references/method-contract.md`,
`workflow-orchestrator/references/context-efficiency.md`, `README.md`,
`interaction-polish/SKILL.md`,
`integrated-workflow/references/execution-loop.md`,
`integrated-workflow/references/coderabbit-review.md`,
`engineering-playbooks/references/agent-friendly-workflow.md`,
`project-learning/SKILL.md`, `CHANGELOG.md`.

- State-heavy sequence: statechart design → formal-verification-create once
  code exists → formal-verification-maintain on any candidate touching covered
  code, before merge.
- `e2e` only where the project already pins it or the owner authorizes the
  dependency; otherwise extend the existing journey framework.
- Completion checklist in the final acceptance record: findings, learning
  checkpoint, continuity record, selected methods (used, unavailable, blocked or
  not applicable, with a reason for each non-used state), role/model/mode report,
  skipped steps with reasons.
- Reviewer-unavailable substitute: with an explicit owner exception, a full
  local review of the exact head is recorded as `deferred` substitute evidence,
  never as a pass for the missing provider.
- How to provision trusted-policy pins outside the candidate checkout.
- Project learning: batch accepted lessons per milestone; standing grant
  limited to the ledger file in guarded repositories.
- Entry obligation: read entry skills fully and follow every link the active
  situation routes to; the owner names entries, not specialists.
- Slice-start announcement: one short line naming the playbook, the selected
  skills, and any that are unavailable, blocked or not applicable, with reasons.
- Each independent ticket or package gets a fresh worker (from
  mattpocock/skills #1341/#1342).
- Opt-in design count against the project's stated tokens (adapted from
  Appllama), with no universal ban.

Acceptance: `toolkit.py lock` and `verify`, full unit suite, both package
builds, local CodeRabbit on the frozen candidate, PR reviews per Integrated
Workflow.

### 2. Footprint metadata, lint, tags and catalog fixes

- `catalog/skills.yaml`: optional per-skill `footprint` entries
  (`path`, `access`, `tracking`, `class`, `gitignore` hint) and expanded
  `task_tags_any` with a pinned tag vocabulary (today 11 tags, mostly Swift and
  formal verification).
- `scripts/routing_catalog.py`: copy footprints into `skill-routing.json`.
- Test: fail when a SKILL.md or reference names a repository path prefix that
  no skill declares.

- Catalog fixes found by the EVERSO audit: reconcile the argent saved-path
  skill names (`argent-create-e2e` / `argent-qa-e2e` in argent's own rule
  versus `argent-create-flow` / `argent-qa-flows` in routing) against the
  pinned upstream; route the installed folders that have no routing entry, or
  record why they stay unrouted (resolved: the remaining folders are installed
  outside the toolkit, such as GoalBuddy's `goal-prep` and the `instabox`
  skills, so readiness lists them as unmanaged rather than routing them); add `Appllama/appllama-skills` at `dd5caae`
  to `catalog/imported-sources.json` so drift tracking covers it.

Acceptance: generator check, lint test with a seeded undeclared path, routing
regression tests for `select_methods.py`, and an `upstream_compare.py` run that
includes Appllama.

### 3. Readiness plan, `project-readiness` skill, entry wiring and pin printer

- `project-readiness/scripts/readiness.py` (stdlib): detect technology tags from path markers, check
  each routed footprint path with git (exists, tracked, ignored), and print one
  setup plan with a stable `plan_id` (sha256 of the canonical items) and
  `grants_authority: false`. Writes nothing.
- An optional project-declared readiness record with locations (agent-map,
  findings, learning, handoffs) and the approved `plan_id`; declared locations
  win over defaults.
- `--print-pins POLICY`: print the policy and validator sha256 values and the
  exact acceptance command. Writes nothing.
- `skills/project-readiness/SKILL.md`: a thin, portable method skill in the
  core pack that runs the readiness check, presents the one plan for consent,
  and proposes the one-line project instruction. `checkpoint.py --phase start`
  calls the same script when Integrated Workflow is installed.
- Entry wiring: one line in the body of `create-plan`, each Forge entry
  (`claude-forge`, `codex-forge`, `cursor-forge`, `devin-forge`,
  `universal-forge`) and `integrated-workflow`, plus the same step in
  `workflow-orchestrator/references/task-handoff-discovery.md`, which every
  entry reaches. Second-hop links alone are what EVERSO skipped.
- Situation map: readiness generates a one-page "situation → skills" view from
  the routing index and the project's detected tags, refreshed when installed
  skills change, with no live connection state. The slice-start announcement
  cites its matching row. It is a filtered view, not a second routing source.
- Entry wording for skimming models: obligations in the first lines of each
  entry skill body, and descriptions written as triggers ("Use at the start of
  every task in a repository") rather than summaries.
- Docs: the README's "six core skills" (two places), its everyday-use and
  delivery sections (readiness runs automatically), `docs/everyday-workflow.md`
  and the generated inventory.

Acceptance: fixture repositories for ready, missing, ignored, and guarded
cases; a test proving no file is written; Python 3.9 and 3.11; the new skill
resolves in every harness package and the core profile includes it.

### 4. Method receipt

- Receipt block `methods: [{id, state: used|unavailable|blocked|not-applicable,
  reason}]`. An applicable method that cannot run is `unavailable` or `blocked`,
  never `not-applicable`.
  `start` prints the methods the changed paths and tags call for, expanding
  sequences such as the slice-1 state-heavy chain; one record per alternative
  group.
- Enforced by default at Integrated Workflow acceptance: `accept` fails on a
  missing record or an unavailable, blocked or not-applicable record without a
  reason. Small bounded corrections are exempt; a trusted-policy
  `methods: report-only` opts a project out. Outside Integrated Workflow the
  check reports only.
- Evidence-linked `used`: each `used` record cites an artifact (review output,
  test file or commit) that the check confirms exists in the candidate.
- CI enforcement: readiness proposes, for the owner's consent, a CI job that
  runs the same checkpoint from trusted configuration on every PR, so a
  required check fails when the receipt is incomplete. It reuses the existing
  trusted-CI pin route; no new mechanism.
- Workers: every worker brief carries the exact paths of its assigned skills,
  so a worker can read them in any harness without inheriting the parent's
  loaded skills; each worker returns its own method records, which the parent
  merges into the receipt.
- Align `method-contract.md`'s pre-existing progress list (selected, read,
  applied, verified, blocked, not applicable) with the four receipt states.

Acceptance: checkpoint tests for missing records, empty reasons, a sequence
chain, alternative groups, the small-correction exemption, the policy
opt-out, a `used` record whose artifact is missing, and a CI fixture that fails
on an incomplete receipt.

### 5. Per-harness packaging and lighter skills

- Each harness's plugin route exposes only skills that target it plus
  universal ones. Cursor's manifest already lists its 124; Claude adds manifest
  paths to its default `skills/` scan, and Factory and `npx skills` read the
  folder directly. Verify each harness's actual plugin rules first, then build
  the structure that works for all of them; record any harness that cannot
  filter.
- Check cross-skill links into skills a harness does not receive (for example
  `workflow-orchestrator` linking `plan-model-router` docs) and reword or
  repoint them.
- Retire the 23 `forge-principle-*` wrappers: their text duplicates the 24
  files in `engineering-playbooks/references/principles/`. Migrate every caller
  first (Forge mappings, routing index, tests), linking prove-it-works and
  encode-lessons-in-structure by path.
- Move `plan-model-router`'s validation and role evidence JSON (about 7 MB,
  read only by one repo test and the docs) to `docs/`; keep
  `scripts/routing_catalog.json`, which the router reads at runtime.
- Installer: a supported, backed-up command to convert a full managed install
  to external-only, for the plugin-plus-extras route.

Acceptance: per-harness package and plugin listings show only compatible
skills; link check passes; principle callers resolve; package size drops;
conversion tested on a fixture with backup and rollback.

### 6. tla-ts as an optional statechart engine

- Optional TLA+ engine for the statechart-verification fork that needs no
  Java, pinned at an exact version and fetched only under the existing
  install-authority gate. TLC stays the default until a trial on the local
  statechart corpus matches TLC's results.

Acceptance: corpus comparison recorded; both engines selectable; missing
engine reported, never passed.

### 7. `programmatic-video` method skill

- Our own content-pack method: brief, storyboard, a deterministic `render(t)`
  timeline, headless-browser frames, ffmpeg mux, contact-sheet QA and a
  licensing check. Credits JohnHeibel/ClaudeAnimationBase and
  lemomo-ai/lemo-opuscar (both MIT); routes to Remotion or other installed
  video plugins when present; no paid API by default.

Acceptance: verify, lock and package checks; one rendered sample journey
recorded as evidence where the tools exist.

### 8. Opt-in harness hooks, Claude first

- Through each harness's existing Forge setup (`claude-forge-setup` first,
  then others whose hooks support it), offer three hooks with owner consent: a
  session-start hook that runs readiness and injects the situation map; a
  prompt hook that puts the matching situation row in front of each request;
  and a finish hook that warns when the method receipt is incomplete. No new skill;
  harnesses without hooks rely on the other layers.
- Claude first because the owner observes Claude skipping skills most often,
  and Claude Code has the strongest hook support.
- Verify whether Claude sub-agent definitions can preload named skills; where
  they can, the setup offers it, and worker briefs still carry skill paths.

Acceptance: hooks install only after consent, back up existing settings, are
removable, and are exercised in a real Claude session; other harnesses record
supported or unsupported.

### 9. Compliance measurement (release acceptance)

- Replay one EVERSO-like task per harness (Claude, Codex, Cursor) with the
  existing Eval playbook, before and after slices 3, 4 and 8, and count routed
  methods recorded as used versus silently skipped. Receipts then give an
  ongoing record. No new tooling.
- Pilot one real EVERSO slice before tagging 1.3.0.

Acceptance: a recorded before/after comparison per harness; release notes
state measured results, not assumed ones.

### Not added (already covered)

- Separate per-situation skill packs: the situation map serves that need;
  packs stay install bundles.
- A separate local-review rule: Integrated Workflow already requires local
  CodeRabbit at slice acceptance and limits cloud reviews per PR.

## Release

One 1.3.0 tag after slice 9. 1.2.2 was merged but never tagged; it is not
tagged separately.

## Separate tasks

- Installed-plugin overlap audit (read-only): classify each installed plugin
  as adapt-a-method, reference-only or skip, reusing the EVERSO first pass.
- Local Claude install reconciliation, after slice 5's conversion command:
  back up `~/.claude/skills` toolkit copies, convert to external-only, keep
  third-party skills and every other harness untouched. Needs the owner's
  go-ahead.

## Risks

- Rubber-stamped "not applicable" answers. Keep the receipt-required set small
  and require reasons; the receipt proves a method was considered, not used.
- Tag growth changes `select_methods.py` context checks. Pin the vocabulary in
  tests.
- Pin churn: every policy change needs its own review; refresh pins only then.

## Next action

Slice 1 merged (PR #35). Slice 2 on `claude/toolkit-1-3-0-slice-2`.
