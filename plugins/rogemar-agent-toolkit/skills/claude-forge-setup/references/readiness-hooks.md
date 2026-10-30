# Readiness hooks for Claude Code (opt-in)

Hooks run whether or not the model chooses to open a skill. They are the strongest
layer for keeping routing in front of Claude, and they are never installed without
the owner's explicit consent.

| Event | Command | Effect |
| --- | --- | --- |
| SessionStart (`startup`, `resume`, `compact`) | `hooks.py session-start` | Runs readiness and adds its status and the situation map to the session |
| UserPromptSubmit | `hooks.py prompt` | Adds only the situation rows the request mentions, at most 600 characters |
| Stop | `hooks.py stop` | Warns, without blocking, when changed files call for methods the receipt has not recorded |

`hooks.py` lives in `project-readiness/scripts/`. It reads nothing but the project
and its Git state, writes only a situation-map cache in the system temp folder, and
never fails the session: an error becomes a short note. The Stop hook does nothing
when Claude is already continuing because of a stop hook, so it cannot loop.

## Install with consent

1. Print the snippet: `python3 -B <project-readiness folder>/scripts/hooks.py claude-settings`
   (add `--receipt <path>` when the project keeps its task receipt at a fixed path).
2. Show it to the owner and say where it goes: the project's `.claude/settings.json`,
   or the user's settings for every project. Apply it only after approval, merging
   with existing `hooks` entries, with a backup, a validated temporary file, atomic
   replacement and a readback.
3. Start a new session and confirm the readiness note appears. Report it as
   observed, or as unverified when it does not.

Removing the three entries removes the hooks.

## Sub-agents

Worker briefs carry the exact paths of their assigned skills, which works in every
harness. Claude sub-agent definitions can also preload skills with a `skills`
frontmatter list; skills marked `disable-model-invocation: true`, such as the
`forge-principle-*` skills, cannot be preloaded, so name their principle files in
the brief. Preloading in plugin-provided agents is undocumented; verify it before
relying on it.

## Other harnesses

The same `hooks.py` commands are harness-neutral. Codex, Cursor and others are
recorded as not yet qualified until their hook formats are verified against a real
session; they rely on the entry wiring, the slice-start announcement and the method
receipt.
