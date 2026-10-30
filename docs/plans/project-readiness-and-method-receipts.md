# Plan: portable project readiness and method receipts (1.3.0)

Status: approved 2026-10-30 by the owner ("Approve, plan it") after a Forge
arena comparison; amended the same day to the hybrid readiness entry ("Yes, use
the hybrid") and to an enforced-by-default method receipt ("Yes, enforce by
default"). The owner invokes only `create-plan`, the harness Forge entry and
`integrated-workflow`, and expects agents to follow every routed method. Delivery: Integrated Workflow, branch + PR + safe merge, one
PR per slice, on `claude/toolkit-1-3-0-readiness`. The branch starts stacked on
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
the methods that the changed paths call for are recorded as used or not
applicable with a reason, so a skipped review is visible rather than silent.
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
| L2 | Project setup needs surfaced mid-sprint, three consents | 3 |
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
  code exists → formal-verification-maintain after merges touching covered code.
- `e2e` only where the project already pins it or the owner authorizes the
  dependency; otherwise extend the existing journey framework.
- Completion checklist in the final acceptance record: findings, learning
  checkpoint, continuity record, selected methods (used / not applicable with a
  reason), role/model/mode report, skipped steps with reasons.
- Reviewer-unavailable substitute: with an explicit owner exception, a full
  local review of the exact head is recorded as `deferred` substitute evidence,
  never as a pass for the missing provider.
- How to provision trusted-policy pins outside the candidate checkout.
- Project learning: batch accepted lessons per milestone; standing grant
  limited to the ledger file in guarded repositories.
- Entry obligation: read entry skills fully and follow every link the active
  situation routes to; the owner names entries, not specialists.
- Slice-start announcement: one short line naming the playbook, the selected
  skills, and those judged not applicable with a reason.
- Each independent ticket or package gets a fresh worker (from
  mattpocock/skills #1341/#1342).
- Opt-in design count against the project's stated tokens (adapted from
  Appllama), with no universal ban.

Acceptance: `toolkit.py lock` and `verify`, full unit suite, both package
builds, local CodeRabbit on the frozen candidate, PR reviews per Integrated
Workflow.

### 2. Footprint metadata, lint and tags

- `catalog/skills.yaml`: optional per-skill `footprint` entries
  (`path`, `access`, `tracking`, `class`, `gitignore` hint) and expanded
  `task_tags_any` with a pinned tag vocabulary (today 11 tags, mostly Swift and
  formal verification).
- `scripts/routing_catalog.py`: copy footprints into `skill-routing.json`.
- Test: fail when a SKILL.md or reference names a repository path prefix that
  no skill declares.

Acceptance: generator check, lint test with a seeded undeclared path, routing
regression tests for `select_methods.py`.

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
- Docs: the README's "six core skills" (two places), its everyday-use and
  delivery sections (readiness runs automatically), `docs/everyday-workflow.md`
  and the generated inventory.

Acceptance: fixture repositories for ready, missing, ignored, and guarded
cases; a test proving no file is written; Python 3.9 and 3.11; the new skill
resolves in every harness package and the core profile includes it.

### 4. Method receipt

- Receipt block `methods: [{id, state: used|not-applicable, reason}]`.
  `start` prints the methods the changed paths and tags call for, expanding
  sequences such as the slice-1 state-heavy chain; one record per alternative
  group.
- Enforced by default at Integrated Workflow acceptance: `accept` fails on a
  missing record or a not-applicable without a reason. Small bounded
  corrections are exempt; a trusted-policy `methods: report-only` opts a
  project out. Outside Integrated Workflow the check reports only.

Acceptance: checkpoint tests for missing records, empty reasons, a sequence
chain, alternative groups, the small-correction exemption, and the policy
opt-out.

## Risks

- Rubber-stamped "not applicable" answers. Keep the receipt-required set small
  and require reasons; the receipt proves a method was considered, not used.
- Tag growth changes `select_methods.py` context checks. Pin the vocabulary in
  tests.
- Pin churn: every policy change needs its own review; refresh pins only then.

## Next action

Slice 1 on `claude/toolkit-1-3-0-readiness`.
