# Rogemar Agent Toolkit

Private, versioned Agent Skills for Codex, Cursor, macOS, and Linux/WSL.

Source repository: [digitalpilipinas/rogemar-agent-toolkit](https://github.com/digitalpilipinas/rogemar-agent-toolkit) (private; GitHub access is required).

To use the latest tagged toolkit checkout:

```bash
git clone https://github.com/digitalpilipinas/rogemar-agent-toolkit.git
cd rogemar-agent-toolkit
python3 scripts/toolkit.py verify
python3 scripts/toolkit.py install --target project --project-root /path/to/project
```

The repository has one canonical skill tree under
`plugins/rogemar-agent-toolkit/skills/`. The same tree is exposed through:

- the portable Agent Plugins `plugin.json` manifest;
- the Codex `.codex-plugin/plugin.json` manifest and local marketplace; and
- a project-first installer that writes to `.agents/skills/`.

## Requirements

- Python 3.9 or newer
- macOS, Linux, or Windows Subsystem for Linux
- Git for pinned repository checkout and updates
- Codex or Cursor only when using that harness-specific integration

The installer never copies secrets, authenticates connectors, installs external
plugins, or overwrites an unmanaged skill directory.

## Upstream and third-party skills

This toolkit includes Rogemar-maintained skills and selected redistributable
snapshots from other authors. Third-party work remains owned and licensed by
its original author; inclusion here does not rebrand it as Rogemar-authored.

The toolkit install stays pinned for reproducibility. Use the commands below
only when you intentionally want the latest upstream version. Review upstream
changes before committing them to a shared project or cloud worker image.

| Author | Skills represented here | Canonical repository | Install or update latest upstream |
| --- | --- | --- | --- |
| OpenAI | Codex system skills, licensed standard skills, and `openai-*` plugin dependencies | [openai/plugins](https://github.com/openai/plugins) | Use the current Codex built-in marketplace. The older [openai/skills](https://github.com/openai/skills) catalog is deprecated in favor of `openai/plugins`. |
| Supabase | `supabase` and the runtime Supabase skill/plugin family | [supabase/agent-skills](https://github.com/supabase/agent-skills) | `npx skills add supabase/agent-skills` |
| CodeRabbit | `code-review` and `autofix` | [coderabbitai/skills](https://github.com/coderabbitai/skills) | `npx skills add coderabbitai/skills` — the CodeRabbit CLI and authentication are separate prerequisites. |
| Software Mansion | The `argent-*` mobile, TV, browser, QA, debugging, and profiling skills | [software-mansion/argent](https://github.com/software-mansion/argent) | `npx @swmansion/argent@latest init --local` for a committable project install, or omit `--local` for the interactive global flow. |
| Leonxlnx | `unlazy` | [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy) | `npx skills add Leonxlnx/unlazy` |
| poteto / Cursor | Cursor `pstack` plugin (`/poteto-mode`, `/setup-pstack`, playbooks, and principles) | [cursor/plugins/tree/main/pstack](https://github.com/cursor/plugins/tree/main/pstack) | In Cursor run `/add-plugin pstack`. It is Cursor-specific, is not installed in the current Codex bundle, and is not copied into the portable skill tree. |
| tolibear | GoalBuddy and `goal-prep` | [tolibear/goalbuddy](https://github.com/tolibear/goalbuddy) | `npx goalbuddy@latest`, then restart the harness; later updates can use `npx goalbuddy update`. |
| Remotion | Remotion plugin dependency and the upstream Remotion skill family | [remotion-dev/skills](https://github.com/remotion-dev/skills) | `npx skills add remotion-dev/skills` |
| Vercel | `vercel-deploy` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `npx skills add vercel-labs/agent-skills --skill vercel-deploy` |

The cross-harness `npx skills add ...` commands use the open-source
[Vercel Skills CLI](https://github.com/vercel-labs/skills). They install into
harness-specific skill directories; they do not automatically update this
toolkit's pinned `catalog/skills.lock.json`. After intentionally refreshing a
vendored upstream, review its license and diff, then run:

```bash
python3 scripts/toolkit.py lock
python3 scripts/toolkit.py verify
python3 -m unittest discover -s tests -v
```

Repositories without a public, author-supported installation path remain
listed as runtime-managed dependencies in `catalog/skills.yaml`; this README
does not invent clone commands for them.

## Complete skill inventory

The generated inventory below is the source-of-truth index for what this
release contains and what it only resolves from an external runtime. Every
portable skill links to its checked-in `SKILL.md`; every outsourced or
runtime-managed group lists its declared author, purpose, canonical source,
and latest installation path. “Not declared in snapshot” means the source
skill did not carry an author field; it is not a claim that the work has no
author.

<!-- BEGIN GENERATED SKILL INVENTORY -->
<!-- This section is generated by scripts/inventory_readme.py; edit the catalog or SKILL.md instead. -->
### Vendored portable skills (52)

| Skill | Purpose | Declared author / provenance | Source and upstream |
| --- | --- | --- | --- |
| [`accessibility-auditor`](plugins/rogemar-agent-toolkit/skills/accessibility-auditor/SKILL.md) | Use for accessibility reviews or implementation involving semantic structure, keyboard and focus behavior, screen readers, ARIA, live announcements, contrast, touch targets, Dynamic Type, reduced motion, forms, errors, and automated plus manual a11y evidence. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/accessibility-auditor/SKILL.md) |
| [`activity-schema-guardian`](plugins/rogemar-agent-toolkit/skills/activity-schema-guardian/SKILL.md) | Use for activity, event, telemetry, logging, or domain schema work involving canonical IDs, category discriminators, sport/activity-specific fields, fixtures, aliases, backward compatibility, JSONB or flexible payload validation, database migrations, and derived insight metrics. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/activity-schema-guardian/SKILL.md) |
| [`agent-collaboration-terminal`](plugins/rogemar-agent-toolkit/skills/agent-collaboration-terminal/SKILL.md) | Coordinate native Grok, Antigravity/Gemini, Cursor Agent, Junie, and Codex CLI sessions from Codex for research, planning, implementation, review, validation, or other bounded external-agent work. Prepare exact worktree prompts, Codex-managed PTY or background execution with physical fallback, frozen repository fingerprints, Markdown artifacts, monitoring, handoffs, and Codex synthesis without routing through the Agent Collaboration MCP broker. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/agent-collaboration-terminal/SKILL.md) |
| [`agent-map`](plugins/rogemar-agent-toolkit/skills/agent-map/SKILL.md) | Use a local, on-demand repository map to reduce exploratory file reads and token use during unfamiliar-code, architecture, multi-file refactor, branch, and commit tasks. Build incremental metadata-only indexes, locate likely files/symbols/callers, check freshness, and fall back to direct search when the map is stale or incomplete. Do not use for known-file edits or simple one-file tasks. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/agent-map/SKILL.md) |
| [`article-creator-2`](plugins/rogemar-agent-toolkit/skills/article-creator-2/SKILL.md) | Use when creating researched long-form content, blog posts, documentation pages, product landing pages, or article packages that need source-backed research, an outline, polished HTML/Markdown, visual direction or generated images, and optional PDF/export preparation. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/article-creator-2/SKILL.md) |
| [`bug-triage`](plugins/rogemar-agent-toolkit/skills/bug-triage/SKILL.md) | Use when investigating errors, logs, failed tests, crashes, CI failures, production incidents, bug reports, or confusing runtime behavior that needs hypotheses, reproduction steps, and prioritized fixes. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/bug-triage/SKILL.md) |
| [`cloudflare-deploy`](plugins/rogemar-agent-toolkit/skills/cloudflare-deploy/SKILL.md) | Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. Use when the user asks to deploy, host, publish, or set up a project on Cloudflare. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/cloudflare-deploy/SKILL.md) |
| [`code-review-and-quality`](plugins/rogemar-agent-toolkit/skills/code-review-and-quality/SKILL.md) | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/code-review-and-quality/SKILL.md) |
| [`code-review-tests`](plugins/rogemar-agent-toolkit/skills/code-review-tests/SKILL.md) | Use when reviewing code diffs, pull requests, bug fixes, migrations, or feature branches for correctness, regressions, security-sensitive behavior, missing tests, and focused verification steps. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/code-review-tests/SKILL.md) |
| [`codex-capability-maintainer`](plugins/rogemar-agent-toolkit/skills/codex-capability-maintainer/SKILL.md) | Use when auditing, adding, updating, or troubleshooting Codex skills, MCP servers, plugins, connectors, automations, hooks, AGENTS.md, global config, or secret-safe local agent capabilities. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/codex-capability-maintainer/SKILL.md) |
| [`create-plan`](plugins/rogemar-agent-toolkit/skills/create-plan/SKILL.md) | Create an actionable coding plan. Use when a user explicitly asks for a plan related to a coding task; include a minimal capability handoff and invoke plan-model-router only for multi-PR, sprint, phased, materially different-risk, or explicitly routed plans. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/create-plan/SKILL.md) |
| [`csv-analytics-reporter`](plugins/rogemar-agent-toolkit/skills/csv-analytics-reporter/SKILL.md) | Use when analyzing CSV, TSV, spreadsheet exports, product analytics, finance tables, survey responses, event logs, or tabular data that needs cleaning, aggregation, charts, anomaly checks, or plain-language findings. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/csv-analytics-reporter/SKILL.md) |
| [`deliver-approved-programme`](plugins/rogemar-agent-toolkit/skills/deliver-approved-programme/SKILL.md) | Execute an already approved multi-sprint, multi-PR, or GoalBuddy coding programme through bounded implementation, verification, review, pull-request remediation, merge, and exact-target proof. Use after planning and approval; do not use for creating the plan, simple one-change tasks, or unapproved deployment. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/deliver-approved-programme/SKILL.md) |
| [`deploy-checklist`](plugins/rogemar-agent-toolkit/skills/deploy-checklist/SKILL.md) | Use when preparing releases, deploys, preview builds, production pushes, branch summaries, release notes, rollback plans, QA checklists, or risk reviews before shipping a web, mobile, backend, or Supabase change. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/deploy-checklist/SKILL.md) |
| [`design-system-steward`](plugins/rogemar-agent-toolkit/skills/design-system-steward/SKILL.md) | Use for design-system work involving themes, tokens, components, typography, spacing, icons, dark and light modes, accessibility, reusable UI primitives, visual consistency, and aligning new screens with an existing product language across web or mobile apps. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/design-system-steward/SKILL.md) |
| [`develop-web-game`](plugins/rogemar-agent-toolkit/skills/develop-web-game/SKILL.md) | Use when Codex is building or iterating on a web game (HTML/JS) and needs a reliable development + testing loop: implement small changes, run a Playwright-based test script with short input bursts and intentional pauses, inspect screenshots/text, and review console errors with render_game_to_text. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/develop-web-game/SKILL.md) |
| [`dream-team`](plugins/rogemar-agent-toolkit/skills/dream-team/SKILL.md) | Use for Rogemar's optional persona-based routing and explanation layer across coding projects. Trigger when the user asks for Dream Team help, names a Dream Team persona or squad, requests plain-language translation, or wants coordinated planning, design, implementation, review, or release guidance. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/dream-team/SKILL.md) |
| [`figma`](plugins/rogemar-agent-toolkit/skills/figma/SKILL.md) | Use the Figma MCP server to fetch design context, screenshots, variables, and assets from Figma, and to translate Figma nodes into production code. Trigger when a task involves Figma URLs, node IDs, design-to-code implementation, or Figma MCP setup and troubleshooting. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/figma/SKILL.md) |
| [`first-time-right-delivery`](plugins/rogemar-agent-toolkit/skills/first-time-right-delivery/SKILL.md) | Use for planning, building, reviewing, testing, or shipping any non-trivial coding change when the goal is to avoid missed requirements and rework. Applies project-agnostic evidence gates, cross-functional review lenses, negative testing, staged delivery checks, and honest readiness reporting. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/first-time-right-delivery/SKILL.md) |
| [`gh-address-comments`](plugins/rogemar-agent-toolkit/skills/gh-address-comments/SKILL.md) | CLI fallback for addressing open GitHub PR comments when the GitHub plugin is unavailable, unauthenticated, or the user explicitly requests gh CLI. Prefer the GitHub-plugin gh-address-comments skill for connected review-thread context. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/gh-address-comments/SKILL.md) |
| [`gh-fix-ci`](plugins/rogemar-agent-toolkit/skills/gh-fix-ci/SKILL.md) | CLI fallback for debugging GitHub Actions PR checks when the GitHub plugin is unavailable, unauthenticated, or the user explicitly requests gh CLI. Prefer the GitHub-plugin gh-fix-ci skill when its connected PR context is available. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/gh-fix-ci/SKILL.md) |
| [`hatch-pet`](plugins/rogemar-agent-toolkit/skills/hatch-pet/SKILL.md) | Create, repair, validate, visually QA, and package Codex-compatible v2 animated pets from character art, generated images, company or prospect brand cues, or visual references. Use for any new Codex pet, custom mascot, non-pixel pet style, brand-inspired pet, existing-pet repair, or 8x11 spritesheet workflow requiring all 9 standard animation rows, 16 look directions, deterministic assembly, QA artifacts, and spriteVersionNumber 2 packaging. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/hatch-pet/SKILL.md) |
| [`interaction-polish`](plugins/rogemar-agent-toolkit/skills/interaction-polish/SKILL.md) | Use for interaction polish across apps and websites involving gestures, transitions, haptics, loading states, empty states, error recovery, microcopy, confirmation flows, touch ergonomics, keyboard behavior, perceived performance, and premium product feel. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/interaction-polish/SKILL.md) |
| [`knowledge-base-answering`](plugins/rogemar-agent-toolkit/skills/knowledge-base-answering/SKILL.md) | Use when answering questions from a scoped document set, repository docs, Notion/Drive/Slack content, internal notes, product specs, manuals, or local files where citations and source boundaries matter. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/knowledge-base-answering/SKILL.md) |
| [`linear`](plugins/rogemar-agent-toolkit/skills/linear/SKILL.md) | Manage issues, projects & team workflows in Linear. Use when the user wants to read, create or updates tickets in Linear. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/linear/SKILL.md) |
| [`meeting-notes-task-extractor`](plugins/rogemar-agent-toolkit/skills/meeting-notes-task-extractor/SKILL.md) | Use when summarizing meeting transcripts, call notes, voice transcriptions, calendar notes, or raw discussion logs into decisions, action items, owners, due dates, risks, and follow-up messages. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/meeting-notes-task-extractor/SKILL.md) |
| [`mobile-release-manager`](plugins/rogemar-agent-toolkit/skills/mobile-release-manager/SKILL.md) | Use for Expo, React Native, iOS, Android, or other mobile release readiness work involving build profiles, app config, env checks, icons, splash screens, permissions, App Store and Play Store checklists, QA plans, release notes, rollback notes, and production deployment preparation. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/mobile-release-manager/SKILL.md) |
| [`motion-animation-engineer`](plugins/rogemar-agent-toolkit/skills/motion-animation-engineer/SKILL.md) | Use for app or web motion work involving transitions, animations, gestures, haptics, shared-element movement, React Native Reanimated, Framer Motion, CSS/Web Animations, reduced motion, animation performance, and motion QA. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/motion-animation-engineer/SKILL.md) |
| [`netlify-deploy`](plugins/rogemar-agent-toolkit/skills/netlify-deploy/SKILL.md) | Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/netlify-deploy/SKILL.md) |
| [`offline-sync-auditor`](plugins/rogemar-agent-toolkit/skills/offline-sync-auditor/SKILL.md) | Use for any app with offline or poor-network behavior involving local drafts, outbox queues, sync retry logic, conflict handling, user-scoped cache keys, network transitions, foreground/app-start sync, queued UI states, and data integrity across unreliable connectivity. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/offline-sync-auditor/SKILL.md) |
| [`pdf`](plugins/rogemar-agent-toolkit/skills/pdf/SKILL.md) | Use for lightweight local PDF reading, extraction, or programmatic generation. Prefer the bundled pdf skill when its managed runtime or stricter render-and-verify workflow is available. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/pdf/SKILL.md) |
| [`performance-profiler`](plugins/rogemar-agent-toolkit/skills/performance-profiler/SKILL.md) | Use for performance investigations, profiling, or optimization involving React renders, Core Web Vitals, interaction latency, bundle size, images, virtualization, memory leaks, React Native frame drops, startup time, database/API latency, and measured evidence. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/performance-profiler/SKILL.md) |
| [`plan-model-router`](plugins/rogemar-agent-toolkit/skills/plan-model-router/SKILL.md) | Use when a coding plan contains PRs, sprints, or implementation increments and the user wants an advisory recommendation of the lowest completed-task-cost GPT-5.6 model and reasoning level that preserves the required quality. Produces per-increment execution profiles with evidence, validation, and escalation triggers; it does not replace planning, review, or testing. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/plan-model-router/SKILL.md) |
| [`playwright`](plugins/rogemar-agent-toolkit/skills/playwright/SKILL.md) | Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/playwright/SKILL.md) |
| [`privacy-safety-review`](plugins/rogemar-agent-toolkit/skills/privacy-safety-review/SKILL.md) | Use for product privacy, safety, and honesty reviews involving profiles, location, health or wellness signals, social features, leaderboards, badges, community data, media sharing, permissions, sensitive storage, generated insights, and surfaces where missing backend data must not be fabricated. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/privacy-safety-review/SKILL.md) |
| [`project-learning`](plugins/rogemar-agent-toolkit/skills/project-learning/SKILL.md) | Initialize and maintain project-local continuous learning, review captured lesson candidates, or adapt accepted lessons between repositories. Use for project learning setup and curation, not ordinary coding work. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/project-learning/SKILL.md) |
| [`research-synthesizer`](plugins/rogemar-agent-toolkit/skills/research-synthesizer/SKILL.md) | Use when the user asks for deep research, competitive analysis, current facts, cited summaries, decision memos, source extraction, or a multi-source answer that should separate evidence from inference and recommendations. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/research-synthesizer/SKILL.md) |
| [`screenshot`](plugins/rogemar-agent-toolkit/skills/screenshot/SKILL.md) | Use when the user explicitly asks for a desktop or system screenshot (full screen, specific app or window, or a pixel region), or when tool-specific capture capabilities are unavailable and an OS-level capture is needed. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/screenshot/SKILL.md) |
| [`security-best-practices`](plugins/rogemar-agent-toolkit/skills/security-best-practices/SKILL.md) | Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests security best practices guidance, a security review/report, or secure-by-default coding help. Trigger only for supported languages (python, javascript/typescript, go). Do not trigger for general code review, debugging, or non-security tasks. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/security-best-practices/SKILL.md) |
| [`seo-content-strategy`](plugins/rogemar-agent-toolkit/skills/seo-content-strategy/SKILL.md) | Use when creating SEO briefs, keyword/theme research, competitor heading analysis, content outlines, search-intent mapping, internal-link suggestions, or article strategy for blogs, docs, and landing pages. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/seo-content-strategy/SKILL.md) |
| [`social-content-factory`](plugins/rogemar-agent-toolkit/skills/social-content-factory/SKILL.md) | Use when repurposing long-form content, launch notes, articles, docs, transcripts, or product updates into social posts, LinkedIn copy, tweets, Instagram captions, carousel scripts, or short campaign calendars. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/social-content-factory/SKILL.md) |
| [`sora`](plugins/rogemar-agent-toolkit/skills/sora/SKILL.md) | Use when the user asks to generate, remix, poll, list, download, or delete Sora videos via OpenAI’s video API using the bundled CLI (`scripts/sora.py`), including requests like “generate AI video,” “Sora,” “video remix,” “download video/thumbnail/spritesheet,” and batch video generation; requires `OPENAI_API_KEY` and Sora API access. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/sora/SKILL.md) |
| [`speech`](plugins/rogemar-agent-toolkit/skills/speech/SKILL.md) | Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Audio API; run the bundled CLI (`scripts/text_to_speech.py`) with built-in voices and require `OPENAI_API_KEY` for live calls. Custom voice creation is out of scope. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/speech/SKILL.md) |
| [`supabase`](plugins/rogemar-agent-toolkit/skills/supabase/SKILL.md) | Connector-independent Supabase skill and CLI/documentation fallback. Use when the namespaced Supabase plugin or its live tools are unavailable or unauthenticated, when the user explicitly requests the local skill/CLI route, or when declarative-schema guidance is required. Prefer the installed Supabase plugin when it is healthy. | supabase | [SKILL.md](plugins/rogemar-agent-toolkit/skills/supabase/SKILL.md); [upstream](https://github.com/supabase/agent-skills) |
| [`supabase-guardian`](plugins/rogemar-agent-toolkit/skills/supabase-guardian/SKILL.md) | Use for any project with Supabase work involving RLS audits, migrations, SECURITY DEFINER RPCs, storage policies, auth/session handling, database functions, logs, or sensitive state where client-supplied identity, permissions, counters, rewards, tiers, credits, or ownership must not be trusted. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/supabase-guardian/SKILL.md) |
| [`test-architecture-engineer`](plugins/rogemar-agent-toolkit/skills/test-architecture-engineer/SKILL.md) | Use when designing or reviewing a test strategy for a feature, PR, sprint, bug fix, migration, or release. Routes work between unit, integration, contract, E2E, visual regression, accessibility, native emulator/device, smoke, and flaky-test diagnosis based on risk. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/test-architecture-engineer/SKILL.md) |
| [`transcribe`](plugins/rogemar-agent-toolkit/skills/transcribe/SKILL.md) | Transcribe audio files to text with optional diarization and known-speaker hints. Use when a user asks to transcribe speech from audio/video, extract text from recordings, or label speakers in interviews or meetings. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/transcribe/SKILL.md) |
| [`ux-flow-architect`](plugins/rogemar-agent-toolkit/skills/ux-flow-architect/SKILL.md) | Use for UX architecture across apps and websites involving user journeys, onboarding, navigation, information architecture, core task flows, permission flows, subscription gates, empty states, recovery paths, and reducing friction across desktop and mobile workflows. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/ux-flow-architect/SKILL.md) |
| [`vector-asset-pipeline`](plugins/rogemar-agent-toolkit/skills/vector-asset-pipeline/SKILL.md) | Use for SVG, icon, logo, vector illustration, symbol, map marker, app icon source, themable vector asset, density variant, export pipeline, optimization, accessibility, provenance, and render verification work. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/vector-asset-pipeline/SKILL.md) |
| [`vercel-deploy`](plugins/rogemar-agent-toolkit/skills/vercel-deploy/SKILL.md) | Deploy applications and websites to Vercel using the bundled `scripts/deploy.sh` claimable-preview flow. Use when the user asks to deploy to Vercel, wants a preview URL, or says to push a project live on Vercel. | Vercel | [SKILL.md](plugins/rogemar-agent-toolkit/skills/vercel-deploy/SKILL.md); [upstream](https://github.com/vercel-labs/agent-skills) |
| [`visual-qa`](plugins/rogemar-agent-toolkit/skills/visual-qa/SKILL.md) | Use for visual QA of web or mobile interfaces, screenshot review, small-screen checks, safe areas, responsive layouts, dark and light theme validation, export/share-card framing, typography readability, spacing, touch targets, visual hierarchy, and product-specific polish. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/visual-qa/SKILL.md) |
| [`workflow-orchestrator`](plugins/rogemar-agent-toolkit/skills/workflow-orchestrator/SKILL.md) | Use for non-trivial coding work that spans brainstorming, research, planning, UX or system design, implementation, debugging, review, testing, release, or monitoring and needs the smallest effective capability set, explicit handoffs, risk-based validation, and honest evidence reporting. | Source author not declared; snapshot maintained by Rogemar | [SKILL.md](plugins/rogemar-agent-toolkit/skills/workflow-orchestrator/SKILL.md) |

### External and runtime-managed skill groups

These names are part of the supported capability inventory but are not copied by the portable installer.

| Skill group and members | Purpose | Author / status | Canonical source and latest install |
| --- | --- | --- | --- |
| **`argent-skills`**<br>`argent-android-emulator-setup`<br>`argent-create-flow`<br>`argent-device-interact`<br>`argent-ios-simulator-setup`<br>`argent-lens`<br>`argent-metro-debugger`<br>`argent-native-profiler`<br>`argent-qa-flows`<br>`argent-react-native-app-workflow`<br>`argent-react-native-optimization`<br>`argent-react-native-profiler`<br>`argent-screen-recording`<br>`argent-screenshot-diff`<br>`argent-settings-permissions`<br>`argent-test-ui-flow`<br>`argent-tv-interact` | Mobile, TV, browser, flow, profiling, screenshot, and debugging workflows from Argent. | Argent installation<br>external-plugin | [repository](https://github.com/software-mansion/argent); `npx @swmansion/argent@latest init --local` |
| **`coderabbit-skills`**<br>`autofix`<br>`code-review` | CodeRabbit code review and guarded pull-request autofix workflows. | CodeRabbit<br>external-plugin | [repository](https://github.com/coderabbitai/skills); `npx skills add coderabbitai/skills` |
| **`codex-system-skills`**<br>`imagegen`<br>`openai-docs`<br>`plugin-creator`<br>`review-agent`<br>`skill-creator`<br>`skill-installer` | Codex-provided system skills and capability-maintenance helpers; availability is controlled by the Codex runtime. | OpenAI<br>runtime-system | [repository](https://github.com/openai/plugins); `Use the current Codex built-in marketplace` |
| **`pstack`**<br>`poteto-mode`<br>`how`<br>`why`<br>`recall`<br>`blast-radius`<br>`architect`<br>`arena`<br>`swarm`<br>`interrogate`<br>`automate-me`<br>`make-bot-ui`<br>`setup-pstack`<br>`reflect`<br>`teach`<br>`tdd`<br>`no-comments`<br>`typescript-best-practices`<br>`figure-it-out`<br>`show-me-your-work`<br>`create-verification-skill`<br>`maintain-verification-skill`<br>`unslop`<br>`bro`<br>`technical-writing` | Cursor-native `/poteto-mode` and `/setup-pstack` playbooks, principles, and companion skills. | poteto / Cursor<br>not-installed-locally | [repository](https://github.com/cursor/plugins/tree/main/pstack); `/add-plugin pstack` |
| **`unlazy`**<br>`unlazy` | Depth-tree execution discipline and gate-based completion checks. | Leonxlnx<br>external-git-skill | [repository](https://github.com/Leonxlnx/unlazy); `npx skills add Leonxlnx/unlazy` |

### Runtime plugin packages

These pinned package references preserve the active local capability set. The toolkit records them for diagnosis and provenance; it does not install, authenticate, or copy them.

| Package (pinned version) | Purpose | Author / source | Latest path |
| --- | --- | --- | --- |
| `agent-collaboration-for-codex@agent-collaboration-local` (0.5.3+codex.20260816000000) | Provides the `agent-collaboration-for-codex` runtime skill/tool family. | Rogemar / local runtime<br>Private/local dependency; no public repository declared | `Use the approved local plugin installation` |
| `browser@openai-bundled` (26.825.32147) | Provides the `browser` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `build-web-apps@openai-curated` (11c74d6b) | Provides the `build-web-apps` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `build-web-data-visualization@openai-curated` (11c74d6b) | Provides the `build-web-data-visualization` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `chrome@openai-bundled` (26.825.32147) | Provides the `chrome` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `codex-app-tools@openai-bundled` (0.1.3) | Provides the `codex-app-tools` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `codex-security@openai-curated` (11c74d6b) | Provides the `codex-security` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `computer-use@openai-bundled` (1.0.1000901) | Provides the `computer-use` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `documents@openai-primary-runtime` (26.826.12353) | Provides the `documents` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `expo@openai-curated` (11c74d6b) | Provides the `expo` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `figma@openai-curated` (11c74d6b) | Provides the `figma` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `game-studio@openai-curated` (11c74d6b) | Provides the `game-studio` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `github@openai-curated` (11c74d6b) | Provides the `github` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `goalbuddy@goalbuddy` (0.4.3) | Provides the `goalbuddy` runtime skill/tool family. | tolibear<br>[GoalBuddy repository](https://github.com/tolibear/goalbuddy) | `npx goalbuddy@latest` |
| `junie-supervisor-for-codex@rg-codex-local` (0.1.2) | Provides the `junie-supervisor-for-codex` runtime skill/tool family. | Rogemar / local runtime<br>Private/local dependency; no public repository declared | `Use the approved local plugin installation` |
| `pdf@openai-primary-runtime` (26.826.12353) | Provides the `pdf` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `presentations@openai-primary-runtime` (26.826.12353) | Provides the `presentations` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `remotion@openai-curated` (11c74d6b) | Provides the `remotion` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `sentry@openai-curated` (11c74d6b) | Provides the `sentry` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `sites@openai-bundled` (0.1.46) | Provides the `sites` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `spreadsheets@openai-primary-runtime` (26.826.12353) | Provides the `spreadsheets` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `template-creator@openai-primary-runtime` (26.826.12353) | Provides the `template-creator` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `test-android-apps@openai-curated` (11c74d6b) | Provides the `test-android-apps` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
| `visualize@openai-bundled` (1.0.23) | Provides the `visualize` runtime skill/tool family. | OpenAI runtime<br>[OpenAI Plugins](https://github.com/openai/plugins) | `Enable through the target harness marketplace` |
<!-- END GENERATED SKILL INVENTORY -->

## Verify the checkout

```bash
python3 scripts/toolkit.py verify
python3 scripts/toolkit.py doctor
```

## Install into a project

Run from the toolkit checkout and provide the target project explicitly:

```bash
python3 scripts/toolkit.py install \
  --target project \
  --project-root /path/to/project
```

The default project destination is `<project>/.agents/skills`. Cursor Cloud and
remote workers must receive the project-level skills before the agent starts.

For a user-level installation shared by compatible local harnesses:

```bash
python3 scripts/toolkit.py install --target user
```

Use `--link` only while developing this toolkit locally. Copied installs are the
supported default for cloud and VM use.

## Codex marketplace

The repository contains `.agents/plugins/marketplace.json`. Initial local
registration is an explicit operator action:

```bash
codex plugin marketplace add /absolute/path/to/rogemar-agent-toolkit
codex plugin add rogemar-agent-toolkit@personal
```

Start a new Codex task after installation so the new skills are discovered.
Private workspace import from GitHub requires an authorized workspace admin.

## Releases and rollback

Install from a pinned semantic-version tag. `install` records a managed state
file and `upgrade` creates a recoverable backup before replacing changed skills:

```bash
git switch --detach v0.2.0
python3 scripts/toolkit.py upgrade \
  --target project \
  --project-root /path/to/project
```

`upgrade` requires an existing managed installation and never follows `main`
on your behalf. To restore the immediately preceding managed state:

```bash
python3 scripts/toolkit.py rollback \
  --target project \
  --project-root /path/to/project
```

Build release archives with:

```bash
python3 scripts/toolkit.py package
```

See `catalog/skills.yaml` for the bundle/dependency boundary and
`docs/compatibility.md` for evidence limits.
