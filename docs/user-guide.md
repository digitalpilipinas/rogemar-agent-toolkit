# User guide

A plain-language guide for owners and first-time users. You do not need to be a
developer to follow it. For the short version, read the
[README](../README.md); for exact installer options, see
[installation and recovery](installation.md).

## What the toolkit does

It gives your AI coding assistant a set of written methods, called **skills**, so
it plans before it builds, checks its own work, gets that work reviewed and shows
you what it did. You only need to remember three skills:

| Skill | When you use it |
| --- | --- |
| `create-plan` | You want a substantial change planned before anything is built. |
| Your assistant's Forge entry (`claude-forge`, `codex-forge`, `cursor-forge`, `devin-forge` or `universal-forge`) | You want something built or fixed, with the full coordinated approach. |
| `integrated-workflow` | You have an approved plan and want it carried out, reviewed and delivered. |

A fourth skill, `project-readiness`, runs by itself at the start of every task. You
can also call it directly: `/rogemar-agent-toolkit:project-readiness` in Claude,
or `$project-readiness` in Codex.

## Install or update

Pick **one** route per computer or project. Installing through two routes gives you
duplicate skills.

| Route | Choose it when | How |
| --- | --- | --- |
| Native plugin | Your assistant has a plugin marketplace and you want the quickest start. | Add this repository as a marketplace, then install the plugin. |
| Managed installer | You want to choose packs, get third-party skills in one step and update safely. | Run `scripts/toolkit.py` from a checkout of this repository. |
| `npx skills` | You want every skill copied with no choices. | One command; skill files only. |

**Claude Code, plugin route:**

```text
/plugin marketplace add digitalpilipinas/rogemar-agent-toolkit
/plugin install rogemar-agent-toolkit@rogemar-agent-toolkit
```

**Managed installer** (needs Git and Python 3.9 or later). Replace `codex` with
`claude`, `cursor` or `droid` for those assistants, and `/path/to/project` with your
project folder. Preview first, then install:

```bash
git clone https://github.com/digitalpilipinas/rogemar-agent-toolkit.git
cd rogemar-agent-toolkit
python3 scripts/toolkit.py install --harness codex --profile core --pack engineering --pack design --target project --project-root /path/to/project --dry-run
python3 scripts/toolkit.py install --harness codex --profile core --pack engineering --pack design --target project --project-root /path/to/project
```

Leave out both `--pack` options to install only the seven core skills. The Forge
entries and `integrated-workflow` come with the engineering pack, so a core-only
install has `create-plan` but not the other two entry points.

**Updating.** Fetch and check out the newer revision, then preview and run:

```bash
python3 scripts/toolkit.py upgrade --harness codex --target project --project-root /path/to/project --dry-run
python3 scripts/toolkit.py upgrade --harness codex --target project --project-root /path/to/project
```

Your saved choices are kept. The installer stops if you have edited a skill
locally, rather than overwriting your changes. Plugins update through the
assistant's own plugin screen instead; see [Troubleshooting](#troubleshooting).

After installing or updating, **start a fresh session** in your assistant. Skills
are read when a session starts.

## Your first session in a project

Start by asking for something small, for example: "Run project-readiness and tell
me what you find." In practice you will not need to ask: any entry skill runs it
first.

Readiness is **read-only**. It looks at the project and reports three things:

1. **What it detected**, such as TypeScript or web code.
2. **A setup plan, only if something needs your decision.** For example, a folder
   skills write to may need an ignore rule, and the project's instruction file may
   need one added line telling agents to run readiness. All items arrive together,
   once.
3. **Your review route**, meaning how independent review will happen (see
   [Review without CodeRabbit](#review-without-coderabbit)).

Example of what you might see (wording varies by assistant):

```text
Readiness: needs-owner (plan 8874da1070bb)
Detected: typescript, web
Review route: fresh-context (no CodeRabbit CLI; a separate reviewer runs code-review-and-quality)
- [needs-owner] AGENTS.md: Add this line: At the start or resume of any task in this
  repository, run the `project-readiness` skill before planning or execution.
```

**To approve**, say so in chat ("Approve the setup plan"). The agent applies the
items and records the approval, so it will not ask again until the plan changes.
**To decline**, say "Decline", and it records that too. Declining is safe: nothing is
changed, and skills still work. If readiness is already fine, it says nothing and
moves on.

The plan never grants permission to commit, publish or spend money. Those stay
separate decisions.

## A worked example

You want a "show password" toggle on the sign-in form. These steps use Claude's
notation; Codex uses `$skill-name`.

**1. Plan it.**

```text
/rogemar-agent-toolkit:create-plan Add a show-password toggle to the sign-in form.
It must work with a keyboard and a screen reader. Do not implement yet.
```

The agent reads the code, may ask a few focused questions, and returns one plan with
the outcome and the checks that will prove it. **You approve the plan**, or ask for
changes. This is your main decision point.

**2. Start the work and choose how far it goes.**

```text
/rogemar-agent-toolkit:integrated-workflow Implement the approved plan at
docs/plans/show-password.md.
Harness: Claude
Delivery to main: BRANCH + PR, STOP BEFORE MERGE
```

Invoking `integrated-workflow` to carry out approved work normally lets the agent
open a pull request and merge it once required checks pass. Adding `STOP BEFORE
MERGE` keeps the final merge in your hands. Other options are `LOCAL ONLY` (nothing
leaves your computer) and `BRANCH + PR + MERGE AUTHORIZED`.

**3. Read the announcement.** At the start of the slice the agent says, in one
line, what it will use and what it will not. For example:

```text
Using claude-forge with frontend-design, accessibility-auditor and playwright.
Not applicable: mobile and database skills (no such code in this change).
```

You do not need to act on this. It is there so you can see the plan for methods and
object if something is missing.

**4. The agent builds.** It builds the whole change as one piece, running focused
tests as it goes. Visible changes also get an accessibility and interface check.

**5. The method receipt.** As it finishes, the agent records every method the
changed files called for. The review row is added after step 6, once the review
has run, and the receipt is checked at acceptance. The finished receipt might look
like this:

| Method | State | Reason or evidence |
| --- | --- | --- |
| `frontend-design` | used | Evidence: the changed component and its test |
| `accessibility-auditor` | used | Evidence: keyboard and screen-reader notes in the pull request |
| `code-review-and-quality` | used | Evidence: fresh-context review of the exact final commit |
| `playwright` | unavailable | No browser is installed here; the check is deferred |

**How to read it:**

- **used** means it ran, and the row points at proof.
- **unavailable** means the tool was not there. That is not a pass. It needs a
  reason, and you decide whether to install the tool or accept the gap.
- **blocked** means something stopped it. Acceptance waits until the block is
  resolved or you explicitly waive it. A waiver is recorded as a waiver, never as
  a pass.
- **not applicable** means the change does not touch that area, with a reason.

Rows with no reason, or "used" with no evidence, fail the check. That is the point:
a skipped step cannot hide.

**6. Independent review.** A reviewer that did not build the change reads the whole
final version. The receipt says which reviewer ran, for example
"fresh-context reviewer" or "CodeRabbit". Findings are checked together; real
defects are fixed and the rest are explained or deferred. Only then is the review
recorded as used in the receipt, pointing at the review's own output.

**7. Merge.** Because you said `STOP BEFORE MERGE`, you get a pull request ready to
merge, with the receipt attached. Merging is not the same as deploying; deployment
is a separate decision.

## Review without CodeRabbit

Every substantial change needs **one independent, full review** of the exact final
version. CodeRabbit is the preferred reviewer when it is installed and signed in,
but the toolkit never requires it. The first route that is available applies:

1. **Local CodeRabbit**, when its command-line tool is installed and signed in.
2. **A fresh-context reviewer.** A separate agent or session that did not build the
   change runs `code-review-and-quality` on it. This is the default when CodeRabbit
   is missing.
3. **Another review tool** your project already uses.

Readiness shows which route your project has. To fix it, add it to the readiness
record, `.agents/readiness.json` by default, for example `"review_route":
"fresh-context"`. The receipt always records which reviewer actually ran.

Skipping review entirely still blocks acceptance. Cloud pull-request reviews (GitHub
CodeRabbit and Codex) are optional and set per project; if your repository does
not use them, nothing waits on them.

## Optional hooks

Hooks make routing automatic even when the assistant forgets to open a skill. They
are **opt-in**: nothing installs them without your approval.

- **Session start:** runs readiness and shows the situation map.
- **Each prompt:** adds only the few rows that match your request (600 characters at
  most).
- **Finish:** warns, without blocking, if changed files call for a method the
  receipt has not recorded.

Claude Code is supported first. To enable them, ask: "Set up the readiness hooks."
`claude-forge-setup` prints a settings snippet and where it goes (the project's
`.claude/settings.json`, or your user settings for every project). Read it, and
approve it only if you are comfortable. Start a new session to confirm the
readiness note appears. To remove the hooks, delete the three entries. Other
assistants rely on the entry skills, the announcement and the receipt until their hook
formats are verified.

## Troubleshooting

**I see the same skill twice.** Two routes installed the same toolkit, for example a
plugin plus a managed copy, or `npx skills` plus the installer. Keep one. Check
which folders hold toolkit skills (for Claude, `.claude/skills` in the project and
your home folder, plus installed plugins). Remove the copy you do not want, or use
`toolkit.py upgrade` to preview and `toolkit.py rollback` to undo. The installer
never silently deletes a second copy. See
[recovery and duplicate copies](installation.md#updates-and-recovery).

**My plugin did not update.** Refreshing the marketplace list is not the same as
updating the installed plugin. In Claude Code, open `/plugin`, update the
plugin, then reload or start a new session. Auto-update is off by default for
third-party marketplaces; you can enable it under Marketplaces. Updates are also
tied to the plugin's version number, so a change published under the same version
may not show up as an update until a new version is released. See
[updating an installed toolkit](installation.md#updating-an-installed-toolkit).

**The agent says "unavailable".** A tool or service the method needs is not present
in this environment, such as a browser driver, a signed-in review tool or a device.
Ask the agent what exactly is missing. Then either install it (your decision),
accept the stated fallback, or accept the gap in the receipt. Optional tools do not
block the work; a required one stops only the step that needs it.

**The agent says "blocked".** Something required cannot proceed. Read the reason.
You can fix the cause, or explicitly waive that one gate for this task.

**Readiness keeps asking the same thing.** Approve or decline once. Either choice
is recorded in `.agents/readiness.json`, and it only asks again if the plan changes.

**The assistant does not know the skills.** Start a fresh session. Check that the
files are in the folder your assistant reads, and that you used one install route.
Installed files do not prove the assistant loaded them; ask it to name the
`create-plan` skill as a quick test.

**Factory or Gemini loads far too many skills.** Those two read every skill in a
plugin folder and cannot filter. Use a selected archive or the managed installer.

## Glossary

- **Acceptance record**: the single record of what was done and proved for a task.
- **Candidate**: the exact final version of the change being reviewed or merged.
- **Entry skill**: one of the three skills you invoke yourself.
- **Forge**: your assistant's engineering entry skill (`claude-forge` and so on).
- **Fresh-context reviewer**: a reviewer, such as a separate agent or session, that
  did not build the change.
- **Harness**: the assistant environment, such as Claude Code, Codex or Cursor.
- **Hook**: a small automatic action your assistant runs at fixed moments. Opt-in.
- **Managed installer**: `scripts/toolkit.py`, which installs and upgrades skills
  with backups and rollback.
- **Marketplace**: a catalogue of plugins your assistant can install from.
- **Method receipt**: the list of methods each task used, could not use or did not
  need, with reasons.
- **Orchestrator**: `workflow-orchestrator`, which chooses the methods for a task.
- **Pack**: a group of related skills you can add, such as engineering or design.
- **Plugin**: a bundle of skills installed through a marketplace.
- **Pull request (PR)**: a proposed change waiting for review and merge.
- **Readiness**: the read-only check at the start of a task.
- **Situation map**: the short list of skills that apply to this project.
- **Skill**: a reusable set of written instructions for the assistant.
- **Slice**: one complete piece of user-visible behavior, built and reviewed together.
