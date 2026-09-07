> INACTIVE RECIPE. This file is not a registered skill and must not execute by being read. Activation requires explicit current user authority, a verified Codex automation/control adapter, source/repository scope, and separate permission for every external action. `workflow-orchestrator` owns workers and `plan-model-router` applies both parent ceilings. Unsupported Cursor service examples below are reference requirements, not tools to invent. Silence never grants authority. Compensation must be separately authorized, reversible where possible, and must verify the target is unchanged and still owned by this run; never delete another person's work. See FOR_AGENTS.md at the recipe root.

# Reproduce automation prompt

> Source material for the copied setup workflow. Paraphrase this intent into a built-in `automate` draft after `automate` confirms that the copied pack is committed in the repository where the automation will run.

Read and follow `.cursor/automations/benny/skills/reproduce-and-fix-issues/RECIPE.md` for this run.

Configuration source. Include this repository-relative path only when it is committed in the same target repository. Otherwise paraphrase the configured values. Never use a plugin source or cache path:

```text
{{BENNY_CONFIG_PATH}}
```

Trigger:

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"message_ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

The creation intent should describe this as a new top-level report in the configured source Slack channel. It should include the configured repository, default branch, issue tracker, control adapter, feature map, and draft pull request capability.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting.

Wait for a configured triage marker from the configured triage identity in this exact thread. Proceed only for `[benny:bug]` or `[benny:performance]`.

Require the configured control-adapter skill before attempting a repro. Reproduce the exact discriminating symptom twice through the real UI. Verify existing pull requests or commits without authoring over them. Attempt a bounded fix only after a confirmed repro and the operational file's fix gate.

The coordinator is the only Slack poster. Every child prompt must forbid `SendSlackMessage`, `PostToSlack`, `chat.postMessage`, and all other Slack writes. Children return findings only.

Never post a root message in the source channel.
