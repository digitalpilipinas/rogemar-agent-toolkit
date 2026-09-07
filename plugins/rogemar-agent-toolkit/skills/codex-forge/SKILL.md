---
name: codex-forge
description: Execute rigorous coding tasks with the full Forge engineering skill and playbook family. Use for Codex Forge, substantive implementation, diagnosis, refactoring, review, verification, or approved programme execution. Integrates with workflow-orchestrator and task-based Codex model routing.
license: MIT
---
# Codex Forge

Read [the runtime contract](references/codex-runtime.md) before runtime work.
`workflow-orchestrator` owns capability selection and every subagent dispatch.
`plan-model-router` owns model policy. `integrated-workflow` retains
approved programme and publication authority. The manually selected main model
and reasoning effort remain the defaults and ceilings, including Astra.

## Choose the work

Select the playbook below that matches the requested result. Carry its meaningful
steps and evidence into the existing task plan; mark inapplicable steps briefly.
Load only applicable principle and companion skills. An engineering principle
is a decision aid, not permission to widen scope or impose unrelated work.

- Understand a subsystem with `forge-how`; reconstruct design history with
  `forge-why`. Use `forge-recall` for an explicitly requested context recovery.
- Model the data and affected boundaries before logic. Request `forge-architect`
  when a real architectural fork warrants it, and `forge-interrogate` when an
  independent adversarial review can resolve a consequential uncertainty.
- Request `forge-swarm` for justified coverage partitions and `forge-arena` for
  competing designs. The orchestrator decides whether fresh contexts earn their
  cost; the main agent remains an active writer and integrator.
- Use `forge-figure-it-out` when no bundled playbook fits. A standing approved
  programme uses the Orchestrate playbook inside `integrated-workflow`.
- Use `forge-unslop`, `forge-technical-writing`, and `forge-no-comments` for
  their applicable prose and code-review surfaces. Preserve safety/compatibility
  constraints and the user's writing style. For skill authoring, use the
  installed Codex `skill-creator`, not a Cursor-format helper.
- Verify on the surface affected by the change using discovered native tools.
  Browser, terminal, and Argent device evidence are separate from source tests.
  Use `forge-create-verification-skill` when reusable verification is needed.
- Use Babysit for an explicit PR-status or remediation request. Shipping and
  Opening a PR apply only within the approved delivery route. Existing review
  gates and canonical finding dispositions remain authoritative.
- Use `forge-show-me-your-work` for useful decision evidence in long runs.
  Reflection and automation requests have their own skills; do not silently
  save memories, install tools, create jobs, or open side PRs.

## Execution discipline

Proceed through authorized reversible work. Investigate discoverable facts;
ask only for material unresolved owner decisions. A playbook invocation grants
no new external-action authority. Keep an unavailable service or required
runtime check visibly blocked and continue independent authorized work.

For each materially different package, the orchestrator requests a fresh model
fit assessment. Workers inherit the selected parent unless a justified lower
profile passes availability, effort, and ceiling checks. Setup is optional;
`forge-setup` stores preferences without changing the parent or Codex settings.
Reconcile the actual diff, executable evidence, and independently useful review
before acceptance. Never infer delivery from a worker summary or a green badge.

## Principles

Read the leaf skill in full for any principle you apply. Each entry names when it applies.

**Core**

- **Laziness Protocol** (**forge-principle-laziness-protocol**). Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem.
- **Foundational Thinking** (**forge-principle-foundational-thinking**). Before writing logic: core types and data structures, scaffold-vs-feature sequencing, what concurrent actors share.
- **Redesign from First Principles** (**forge-principle-redesign-from-first-principles**). Integrating a new requirement into an existing design. Redesign as if it had been foundational from day one.
- **Subtract Before You Add** (**forge-principle-subtract-before-you-add**). Sequencing an addition, refactor, or rewrite. Remove dead weight first, then build on the simpler base.
- **Minimize Reader Load** (**forge-principle-minimize-reader-load**). Reviewing or shaping code that's hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope.
- **Outcome-Oriented Execution** (**forge-principle-outcome-oriented-execution**). Planned rewrites and migrations with explicit phase boundaries. Converge on the approved target while preserving required client and data compatibility.
- **Experience First** (**forge-principle-experience-first**). Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience.
- **Exhaust the Design Space** (**forge-principle-exhaust-the-design-space**). A novel interaction or architectural decision with no precedent. Build 2-3 competing prototypes and compare before committing.
- **Build the Lever** (**forge-principle-build-the-lever**). Any non-trivial work. Use a reusable tool when it materially improves correctness or repeated work.

**Architecture**

- **Model the Domain** (**forge-principle-model-the-domain**). Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection) instead of scattered conditionals.
- **Boundary Discipline** (**forge-principle-boundary-discipline**). Wiring validation, error handling, or framework adapters. Guards at system boundaries, trust internal types, keep business logic pure.
- **Type System Discipline** (**forge-principle-type-system-discipline**). Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries.
- **Make Operations Idempotent** (**forge-principle-make-operations-idempotent**). Designing commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- **Migrate Callers Then Delete Legacy APIs** (**forge-principle-migrate-callers-then-delete-legacy-apis**). Introducing a new internal API while old callers exist. Migrate controlled callers together; remove legacy APIs only when compatibility permits.
- **Separate Before Serializing Shared State** (**forge-principle-separate-before-serializing-shared-state**). Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first.

**Verification**

- **Prove It Works** (**forge-principle-prove-it-works**). After a task, before declaring done. Verify against the real artifact, not a proxy or "it compiles".
- **Fix Root Causes** (**forge-principle-fix-root-causes**). Debugging. Trace each symptom to its root cause, reproduce first, ask why until you reach it.
- **Sequence Work into Verifiable Units** (**forge-principle-sequence-verifiable-units**). Multi-step work (sweeps, migrations, runs of similar edits) and how you stack commits and PRs. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself.

**Delegation**

- **Guard the Context Window** (**forge-principle-guard-the-context-window**). Context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread.
- **Never Block on the Human** (**forge-principle-never-block-on-the-human**). Tempted to ask "should I do X?" on reversible work. Proceed, present the result, let the human course-correct.

**Meta**

- **Encode Lessons in Structure** (**forge-principle-encode-lessons-in-structure**). You catch yourself writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script instead of more text.

## Playbooks

Each playbook preserves a PStack task method with Codex runtime and authority
adaptations. Read the selected file in full. The Opening a PR helper is included
in addition to the 22 task playbooks.

- **Investigation.** Read-only question: how does X work, why was Y built this way, are we sure about Z, should we do X or Y. `playbooks/investigation.md`.
- **Bug fix.** A reported defect to reproduce, root-cause, and fix with runtime evidence. `playbooks/bug-fix.md`.
- **Perf issue.** A measured slowness to trace and improve against a baseline. `playbooks/perf-issue.md`.
- **Hillclimb.** Sustained, scientific improvement of one metric against a target: loop hypotheses with before/after measurement, a decision log, and one verified record per accepted win; commit only within authority. Distinct from Perf issue, which is a one-off fix. `playbooks/hillclimb.md`.
- **Runtime forensics.** Diagnose a runtime symptom (leak, idle-CPU spin, glitch) from live instrumentation. The deliverable is a diagnosis, not a fix. `playbooks/runtime-forensics.md`.
- **Trace forensics.** Diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot) handed to you after the fact. The deliverable is a diagnosis, not a fix. `playbooks/trace-forensics.md`.
- **Feature.** New or changed behavior, built from a named data shape. `playbooks/feature.md`.
- **Refactoring.** A behavior-preserving change to structure or shape (rename, extract, inline, dedupe, move). `playbooks/refactoring.md`.
- **Prototype.** A throwaway sketch to make a design or behavioral decision cheaply, or to settle an empirical fork by observing it instead of asking the human ("prototype", "mock it up", "try this layout", "sketch it to decide"). `playbooks/prototype.md`.
- **Visual parity.** Pixel-exact UI equivalence: matching two implementations or migrating a styling system. `playbooks/visual-parity.md`.
- **Authoring or modifying a skill.** Writing or editing a SKILL.md. `playbooks/authoring-a-skill.md`.
- **Eval.** Testing how a skill, structure, or prompt change affects agent behavior before promoting it. `playbooks/eval.md`.
- **Babysit.** Driving a PR or a stack to merge-ready: conflicts, review threads, CI. `playbooks/babysit.md`.
- **Shipping.** The half after Babysit. Independently verifying a green stack, then landing the contiguous verified run bottom-up through `gh` by default or Origin when its CLI is available. `playbooks/shipping.md`.
- **Autonomous run.** A long task to drive to completion without stopping ("run until done", "/loop until X"). `playbooks/autonomous-run.md`.
- **Orchestrate.** A standing project handed to one coordinator chat: multi-day, many stacked PRs, bounded batches of subagents, minimal human turns ("run this whole project", "own this migration until it lands"). Distinct from Autonomous run, which drives one task to a predicate; work one agent could finish inside the session's budget routes there, not here, however program-shaped the phrasing sounds. `playbooks/orchestrate.md`.
- **Autopilot-full.** A queue of independent PRs run through the authorized delivery boundary: one owner per PR carries build through its authorized boundary, and the root swarm-verifies each merge-ready head before its owner merges ("autopilot this queue", "full autopilot", one-owner-per-PR programs). `playbooks/autopilot-full.md`.
- **Autopilot-stack.** A queue of changes built and verified with full autonomy, delivered as one linear reviewed base-branch stack the operator lands herself ("autopilot-stack", "stack them, don't ship", "build the stack, I'll land it"). `playbooks/autopilot-stack.md`.
- **Session pickup.** Resuming or taking over a prior agent's in-flight work from a transcript, cloud-agent URL, or pushed branch. `playbooks/session-pickup.md`.
- **Pause safely.** Suspending in-flight work cleanly so it can be resumed, on an explicit pause, going offline, a Codex restart, or imminent context compaction. The complement to Session pickup. Full steps: `playbooks/pause-safely.md`.
- **Multi-phase or multi-PR plan.** Work that spans phases or stacked PRs. `playbooks/multi-phase-plan.md`.
- **Worktree and simulator cleanup.** Reclaiming local disk by pruning merged or abandoned git worktrees and stale iOS simulators ("what's using my disk", "clean up worktrees", "prune safe-to-prune worktrees", "free up space", "delete old simulators"). `playbooks/worktree-cleanup.md`.
- **Opening a PR.** Use when PR creation is in the approved delivery route. `playbooks/opening-a-pr.md`.
