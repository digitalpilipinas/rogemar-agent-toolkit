# Judgment lens

Read [the reflection review contract](review-contract.md), then inspect the
supplied task, authorized transcript or digest. Apply the judgment lens to:

- Repeated corrections and consequential decisions.
- Assumptions that changed the outcome.
- Durable working conventions demonstrated by the task.
- Execution friction that an existing skill should address.

Name the durable principle behind the incident and the future decision it would
change. Preserve the rationale when it explains a non-obvious tradeoff. A user's
working preference can matter even when it is not a software defect; keep its
scope explicit rather than generalizing it to every project.

## Inspection prompts

Use these prompts where the supplied evidence supports them:

- Mistakes made and corrections received
- User preferences and workflow patterns
- Codebase knowledge gained (architecture, gotchas, patterns)
- Tool/library quirks discovered
- Decisions and their rationale
- Friction in skill execution, orchestration, or delegation
- Repeated manual steps that could be automated or encoded


For each supported finding, return:

- Principle: the reusable decision rule in one sentence.
- Evidence: the source turn or artifact and what it establishes.
- Routing: the current owning skill and section, a missed-trigger correction,
  or a justified new recurring need.
- Proposal: the smallest change that would alter the future decision.

Return no findings when the evidence is one-off, already covered or insufficient.

<AUTHORIZED TRANSCRIPT PATH OR TASK DIGEST>
