> INACTIVE RECIPE. This file is not a registered skill and must not execute by being read. Activation requires explicit current user authority, a verified Codex automation/control adapter, source/repository scope, and separate permission for every external action. `workflow-orchestrator` owns workers and `plan-model-router` applies both parent ceilings. Unsupported Cursor service examples below are reference requirements, not tools to invent. Silence never grants authority. Compensation must be separately authorized, reversible where possible, and must verify the target is unchanged and still owned by this run; never delete another person's work. See FOR_AGENTS.md at the recipe root.

# benny

benny gives you two cursor automations for slack issue reports. one triages each report. the other reproduces confirmed bugs and may prepare a small draft fix.

the files in this directory are dormant setup and automation sources. they do not appear as slash skills.

## set it up

1. point cursor at [`FOR_AGENTS.md`](./FOR_AGENTS.md) and name the target repository.
2. let setup merge this whole directory into the target at `.cursor/automations/benny/`. it must preserve destination-only files and review conflicts instead of overwriting local edits.
3. let setup enable pstack in the target repository's `<upstream Cursor settings example; unsupported in Codex>` for shared dependencies:

```json
{
	"plugins": {
		"pstack": { "enabled": true }
	}
}
```

4. keep user-owned configuration outside the copied pack, for example in `.agents/forge-benny/`. adapt [`configuration.example.yaml`](./templates/configuration.example.yaml) and [`feature-map.example.md`](./skills/reproduce-and-fix-issues/references/feature-map.example.md).
5. commit `<upstream Cursor settings example; unsupported in Codex>`, `.cursor/automations/benny/`, and any secret-free configuration before enabling either automation.
6. review each new automation draft or update existing automations in their editors. then send a harmless test report and verify every source-channel post stays in the original thread.
