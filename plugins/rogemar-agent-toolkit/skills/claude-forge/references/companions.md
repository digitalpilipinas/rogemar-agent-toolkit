# Claude companion index

Portable playbooks name the work. When a playbook uses one of these names, read
the installed skill, then apply
[the Claude runtime contract](claude-runtime.md) before any worker. If that
skill is absent, read the linked section in
[companion-methods.md](../../engineering-playbooks/references/companion-methods.md).

`codex-forge` and `forge-setup` are not installed on Claude. Upstream PStack
skills are not the procedure when the matching `forge-*` skill is installed.

| Playbook name | Installed skill | Fallback section | Claude binding |
| --- | --- | --- | --- |
| source tracing | forge-how | How | The parent reads the current code. Ask the orchestrator for read-only workers only when the question splits into independent slices. |
| history investigation | forge-why | Why | Use git history and the files the task already allows. Do not infer intent from a filename. |
| design exploration | forge-architect | Architect | Sketch the data shape and the caller-facing signatures before editing. Skip this for a settled local change. |
| assumption critique | forge-interrogate | Interrogate | Attack the assumption that would change the plan. Review does not include permission to edit. |
| regression-first verification | forge-tdd | Tdd | Add a failing check only when it can catch the real bug. Then make that check pass. |
| blinded alternatives | forge-arena | Arena | Keep candidates comparable. Say so when one agent produced every alternative. |
| decision logging | forge-show-me-your-work | Show me your work | Record hypothesis, change, evidence, and verdict for a long run. Do not create a second status system. |
| comment review | forge-no-comments | No comments | Remove narration. Keep a comment that states a constraint the code cannot show. |
| technical writing | forge-technical-writing | Technical writing | Lead with the behavior a reader must act on, then the evidence and the limit. |
| plain-language editing | forge-unslop | Unslop | Edit the requested prose. Do not impose a new voice on code or on the user's writing. |
| scoped session recovery | forge-recall | Recall | Read only the supplied checkpoint or transcript. Verify the branch and diff before trusting the summary. |
| coverage partition | forge-swarm | Swarm | Ask the orchestrator for separate slices only when the scopes do not share files. |
| personal mode capture | forge-automate-me | Automate me | Draft a skill only when the user asks to save a working convention. |
| caller and data trace | forge-blast-radius | Blast radius | Trace the changed interface through callers and stored data. Do not audit the whole repository. |
| conversational support | forge-bro | Bro | Stay on the asked question. Conversation is not implementation authority. |
| reusable verification | forge-create-verification-skill | Create verification skill | Add a recipe only for a repeated gap. Keep it draft until an authorized run passes. |
| verification refresh | forge-maintain-verification-skill | Maintain verification skill | Fix the broken check for the behavior that changed. Do not replace the suite. |
| bot interface | forge-make-bot-ui | Make bot ui | Follow the installed UI skill for the actual client. Do not add a new component kit. |
| reflection | forge-reflect | Reflect | Propose a reusable lesson. Write it only inside the authority already granted. |
| teaching | forge-teach | Teach | Explain the requested mechanism from the code that implements it. |
| TypeScript practices | forge-typescript-best-practices | Typescript best practices | Apply them when the change is TypeScript. Do not reformat unrelated files. |
| setup | claude-forge-setup | Setup | Mode and profile setup belong to `claude-forge-setup`, not `forge-setup`. |
| figure it out | forge-figure-it-out | Figure it out | Use it when none of the 23 playbooks match. Keep the same task and evidence. |

Principles install as `forge-principle-*` skills. Read the installed skill when
it is present. Otherwise read
[the shared principle index](../../engineering-playbooks/references/principles.md).
A principle is a decision aid. It does not widen the task.
