# Capability Fallbacks

Use a fallback only after checking that the preferred capability is genuinely unavailable, unauthenticated, quota-limited, timed out, or unsuitable. Preserve the exact evidence boundary.

## Discovery before fallback

1. Derive the actual capability need from the active slice, repository, risk,
   and required evidence rather than waiting for the owner to name a tool.
2. Inspect skill names and descriptions, relevant members of namespaced or
   specialist families, and the separate live-tool/MCP/app/connector registry.
   A live tool may have no matching skill, and an installed plugin may have no
   callable tool. Keep the search targeted and do not load every skill.
3. Verify the chosen live route is surfaced and, when material, enabled,
   authenticated, and suitable for the approved data and action boundary.
   Installed or advertised is not the same as callable.
4. Select one primary route. Activate only the smallest safe fallback if the
   primary cannot satisfy the need; do not run both by default.
5. Limit discovery to capabilities installed or surfaced in Codex, including
   installed marketplace plugins. Do not search the external marketplace or
   suggest new installation unless the owner separately requests it.
6. If an installed capability layer cannot be inspected, record that layer as
   `unverified` and use the
   smallest repository-local fallback whose evidence boundary is honest.

Capability discovery does not authorize installation, enablement, login,
private connector access, paid-credit use, exposure of additional files, or an
external mutation. Obtain or rely on existing explicit authority for those
actions before proceeding.

| Need | Preferred capability | Fallback |
| --- | --- | --- |
| Long-running control | GoalBuddy `state.yaml` and execution contract | Existing board plus manual checker/PM handling, or an approved plan with native plan tracking; do not claim GoalBuddy automation passed |
| Local code review | CodeRabbit CLI | A separately labeled native review plus repository tests |
| Independent review | Authorized external provider or read-only sub-agent | Native verification reviewer or main-agent review; never invent independence |
| Security/privacy | Relevant Codex Security and domain skills | Repository security checks, secret scan, server-authority, privacy, RLS/migration, and domain counterexamples |
| React Native QA | Expo and Argent | Repository build/tests; mark simulator QA blocked or deferred if exact runtime provenance cannot be established |
| Web/native platform QA | Matching web, iOS, macOS, Android, browser, or visual skill | Repository-native build/test evidence; do not claim visual/device acceptance |
| GitHub operations | Authenticated GitHub connector or CLI | Use the other authenticated surface; if neither works, stop at the last verified local or remote state |
| CI unavailable by quota | Required CI provider | Record `blocked` or `unavailable_by_quota`; rely on named local checks only and never convert CI to passed |
| External provider | Named provider/model through an authorized `agent-collaboration-terminal` run | For `OPTIONAL`, use a separately labeled native read-only review; for `REQUIRED`, block the named review boundary if no listed provider succeeds |

## Fallback rules

- Optional capability failure does not block safe in-scope work. Required acceptance evidence without an equivalent fallback does block the gate.
- A fallback is a new evidence source, not a relabeling of the failed provider.
- Do not silently install or authenticate integrations, expose additional files, spend credits, weaken a gate, or change scope to make a capability appear available.
- Use the smallest relevant capability set. Do not invoke every installed reviewer, security scanner, platform plugin, or external model for routine changes.
- Keep one writer per worktree. Parallelize only independent read-only review, research, or validation unless separate write worktrees and reconciliation are explicitly approved.
- The manually selected main-agent model and reasoning effort are ceilings for native sub-agents. Route to the lowest sufficient available profile and use tests and review as the quality gate. External provider model availability remains provider-owned.
- For external review, freeze the exact workspace and allowed/excluded paths, keep artifacts outside the repository, monitor changed-only receipts, and validate the actual code rather than the provider summary.
- Do not replace a named Grok, Antigravity/Gemini, Cursor, or Junie provider/model silently. Verify its executable, authentication, credits, and model availability. Optional failure may use the recorded fallback; required failure blocks only the named risk boundary while other safe work may continue.
- Simulator or physical-device unavailability follows the selected gate: `REQUIRED` blocks the applicable delivery boundary, `CONDITIONAL` applies only to relevant supported changes, `DEFERRED` remains deferred, and `NOT APPLICABLE` requires a truthful scope reason. An explicit owner invocation makes simulator evidence required for the named scope; repository tests or screenshots do not replace it.

## Default exclusions

Unless the approved scope says otherwise, exclude secrets, credentials, environment files, ignored files, private test-user data, research material, generated diagnostics, temporary files, GoalBuddy control files, and unrelated user work from commits and external reviews. Untracked files require an explicit scope decision before external review.

## Evidence vocabulary

- `passed`: executed and successful;
- `failed`: executed and unsuccessful;
- `blocked`: required evidence could not be obtained;
- `unavailable`: optional capability could not be used;
- `skipped`: intentionally not applicable;
- `deferred`: intentionally postponed under the approved plan;
- `partial`: some but not all required evidence exists.

Report the observable state and reason. Do not infer quality from provider availability, credit balance, terminal exit, or a green-looking UI.
