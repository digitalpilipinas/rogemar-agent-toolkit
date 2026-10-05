# Shared Forge runtime

Use this contract from every shared `forge-*` method. `codex-forge` and
`forge-setup` stay Codex-only and keep their own contracts.

`workflow-orchestrator` owns specialist selection and worker dispatch. The
skill that sent you here supplies the method and bounded hints. A role hint is
not a model ID and not a reason to spawn a worker. Do the work in the parent
when a worker would not add independent evidence.

Read the runtime for the active entry. Do not load a second router.

| Active entry | What to read and use |
| --- | --- |
| `codex-forge`, or a Codex session whose entry is Codex Forge | The installed `codex-forge` runtime contract and `plan-model-router` |
| `cursor-forge`, or a Cursor session whose entry is Cursor Forge | `cursor-forge-setup`. Do not send PStack or poteto-mode model slugs |
| `claude-forge`, or a Claude session whose entry is Claude Forge | The installed `claude-forge` runtime contract and `claude-forge-setup` |
| `universal-forge`, or any other harness | `universal-plan-model-router` |

If that router or setup skill is not installed, keep the work in the parent and
say which control was missing. Do not borrow another harness's model IDs.

These methods are the maintained adaptations of the pinned PStack skills at
`e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`. Upstream PStack skills keep Cursor
Task defaults. When both an upstream skill and its `forge-*` skill are
installed, follow `forge-*` and do not also run the upstream model list.
Do not edit upstream PStack files, `/poteto-mode`, or plugin caches.
