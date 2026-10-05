# Claude companion index

Portable playbooks name the work, not a Codex slash command. When a playbook
uses one of these names, read the linked section in
[companion-methods.md](../../engineering-playbooks/references/companion-methods.md),
then apply [the Claude runtime contract](claude-runtime.md).

Codex `forge-*` skills are not installed on Claude. Cursor PStack skills are not
installed on Claude. Do not invent those slash commands here.

| Playbook name | Companion section | Claude binding |
| --- | --- | --- |
| source tracing | How | The parent reads the current code. Ask the orchestrator for read-only workers only when the question splits into independent slices. |
| history investigation | Why | Use git history and the files the task already allows. Do not infer intent from a filename. |
| design exploration | Architect | Sketch the data shape and the caller-facing signatures before editing. Skip this for a settled local change. |
| assumption critique | Interrogate | Attack the assumption that would change the plan. Review does not include permission to edit. |
| regression-first verification | Tdd | Add a failing check only when it can catch the real bug. Then make that check pass. |
| blinded alternatives | Arena | Keep candidates comparable. Say so when one agent produced every alternative. |
| decision logging | Show me your work | Record hypothesis, change, evidence, and verdict for a long run. Do not create a second status system. |
| comment review | No comments | Remove narration. Keep a comment that states a constraint the code cannot show. |
| technical writing | Technical writing | Lead with the behavior a reader must act on, then the evidence and the limit. |
| plain-language editing | Unslop | Edit the requested prose. Do not impose a new voice on code or on the user's writing. |
| scoped session recovery | Recall | Read only the supplied checkpoint or transcript. Verify the branch and diff before trusting the summary. |
| coverage partition | Swarm | Ask the orchestrator for separate slices only when the scopes do not share files. |
| personal mode capture | Automate me | Draft a skill only when the user asks to save a working convention. |
| caller and data trace | Blast radius | Trace the changed interface through callers and stored data. Do not audit the whole repository. |
| conversational support | Bro | Stay on the asked question. Conversation is not implementation authority. |
| reusable verification | Create verification skill | Add a recipe only for a repeated gap. Keep it draft until an authorized run passes. |
| verification refresh | Maintain verification skill | Fix the broken check for the behavior that changed. Do not replace the suite. |
| bot interface | Make bot ui | Follow the installed UI skill for the actual client. Do not add a new component kit. |
| reflection | Reflect | Propose a reusable lesson. Write it only inside the authority already granted. |
| teaching | Teach | Explain the requested mechanism from the code that implements it. |
| TypeScript practices | Typescript best practices | Apply them when the change is TypeScript. Do not reformat unrelated files. |
| setup | Setup | Mode and profile setup belong to `claude-forge-setup`. |
| figure it out | Figure it out | Use it when none of the 23 playbooks match. Keep the same task and evidence. |

Principles live in
[the shared principle index](../../engineering-playbooks/references/principles.md).
Read the leaf file before applying it. A principle is a decision aid. It does
not widen the task.
