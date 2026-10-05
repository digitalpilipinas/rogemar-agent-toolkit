# Authoring or modifying a skill

Read [the Claude runtime contract](../references/claude-runtime.md) before any worker, model, tool, or publication action. Resolve companion names through [the companion index](../references/companions.md). The method below is the shared engineering playbook, with links adjusted so they resolve from this package.

Apply the [task-handoff method contract](../../workflow-orchestrator/references/method-contract.md).
Check that descriptions, body instructions, invocation policy, routing and portable fallbacks agree; verify referenced resources.

**You own the skill's voice.** Agent-facing prose has a higher bar than human prose; unhelpful sentences become instructions.

1. Use an installed skill-authoring validator when available for authoring and validating SKILL.md files.
2. Validate the skill: frontmatter has `name` and `description`, referenced files exist, cross-skill links resolve.
3. Test cases if structural; skip if subjective.
4. Prepare **Opening a PR** only within explicit publication authority.

When in doubt, delete; prose earns its keep by changing a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config); hardcoded details go stale (the **encode-lessons-in-structure** principle skill). Delegate to other skills by path; don't restate. A workflow you keep hitting but isn't captured → propose a new skill.

For agent-facing instructions, make each step end in an observable completion
condition. Keep one authoritative definition and conditional links that name the
cases needing them. Remove duplicate guidance and cheap environment lookups that
can go stale. Adapted from Matt Pocock's `writing-for-agents` at
`24fe0ef7737efae15c87225755e9f6f5965e4888`
([MIT notice](../../engineering-playbooks/upstream-notices/mattpocock-LICENSE)).

**Reply:** summary of the skill, key design decisions, validation notes.
