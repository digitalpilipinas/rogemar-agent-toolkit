# Lifecycle stage routing

Use this reference when work crosses planning, GoalBuddy preparation,
implementation, review, or delivery. It defines entry packages, not additional
permission. `workflow-orchestrator` remains the only skill that selects
specialists or Workers.

## Entry packages

| Stage | User-facing entry | Default internal contract | Output or handoff |
| --- | --- | --- | --- |
| Read-only planning | `create-plan` | `workflow-orchestrator`; add `plan-model-router` only for multi-PR, sprint, phased, materially mixed-risk, or explicitly routed work | An approved-plan candidate with a capability handoff |
| Goal compilation | `goalbuddy:goal-prep` | Goal Prep only; it records named capabilities without loading or executing them | `goal.md`, `state.yaml`, task scopes, verification, and stop conditions |
| Approved programme execution | `deliver-approved-programme` | `workflow-orchestrator` plus `first-time-right-delivery` | Bounded implementation, evidence, PR handling, and exact-target proof within recorded authority |
| Small direct implementation | `workflow-orchestrator` or the relevant specialist | Add `first-time-right-delivery` only when the change is non-trivial | The smallest coherent verified change |
| Standalone specialist work | The named specialist | That specialist only unless a real cross-surface dependency appears | Its documented focused artifact or evidence |

Goal Prep must preserve an approved plan's capability handoff in task `inputs`
or `constraints`; it does not execute those skills during preparation. During
execution, the active task's scope and current evidence determine which listed
specialists actually activate. A plan hint is not a command to load them all.

## Capability preflight by stage

- **Planning (`create-plan`):** infer required capabilities and use read-only
  discovery across relevant skill families and the separate live-tool registry
  to record the preferred route, observed availability, the smallest fallback,
  and any later authorization need. Inspect only capabilities installed or
  surfaced in Codex; do not search the external marketplace. Do not install,
  authenticate, access private connector data, or perform the planned work.
- **Goal compilation (`goalbuddy:goal-prep`):** copy the approved capability
  handoff into task `inputs` or `constraints`. Goal Prep does not load skills,
  call MCPs or connectors, test authentication, or activate fallbacks; schedule
  those checks for execution.
- **Execution (`deliver-approved-programme`):** revalidate the capabilities the
  active slice actually needs because surfacing and authentication may have
  changed since planning. Use the preferred route when usable and activate its
  recorded fallback only when necessary and authorized.
- **Standalone specialist work:** discover only the live route needed by that
  specialist. Escalate to the orchestrator only when a real cross-surface
  dependency or fallback decision appears.

Capability selection is automatic for ordinary in-scope work, so the user does
not need to remember every useful skill or MCP. A user must still choose or
authorize a specific provider, private data source, paid-credit use,
installation or login, or externally mutating action when that choice changes
scope or authority.

## Conditional specialist packages

Select the smallest applicable subset.

### Product and interface

- `ux-flow-architect`: journeys, navigation, permissions, recovery, or state
  architecture.
- `design-system-steward`: shared tokens, components, themes, or reusable
  interaction states.
- `accessibility-auditor`: semantics, focus, assistive technology, contrast,
  text scaling, or touch behavior.
- `visual-qa`: rendered responsive, theme, safe-area, typography, or export
  evidence after a viewable candidate exists.

These are sequential lenses when needed, not a mandatory four-skill bundle. A
copy-only flow correction may need only UX; a token-only change may need design
system plus focused visual evidence.

### Data, trust, and resilience

- Prefer the namespaced Supabase plugin skill and authenticated tools when they
  are available. Use the global `supabase` skill as the connector-independent
  CLI/documentation fallback or when it is explicitly requested.
- `activity-schema-guardian`: canonical IDs, aliases, flexible payloads,
  migrations, or historical compatibility.
- `offline-sync-auditor`: drafts, outbox, retry, cache isolation, conflict, or
  reconciliation behavior.
- `privacy-safety-review`: personal, social, location, wellness, sharing,
  generated insight, or truthfulness boundaries.
- `test-architecture-engineer`: deciding which evidence layers are sufficient;
  do not invoke it merely to write an obvious existing-pattern unit test.

### Pull requests and CI

- Prefer the authenticated GitHub integration for connected PR context.
- Use `gh-address-comments` or `gh-fix-ci` as CLI fallbacks when the integration
  is unavailable or the owner explicitly selects CLI.
- Existing programme authority carries into bounded comment or CI remediation;
  a fallback must not demand a duplicate plan or approval for already approved
  work.

## Conflict prevention

- Entry skills own lifecycle boundaries; specialists own only their domain.
- A specialist's read-only reviewer hint restricts that reviewer role only. It
  does not prohibit a separate, explicitly scoped implementation Worker.
- Fallback skills do not run alongside a healthy primary integration unless
  independent evidence or an explicit owner request justifies both.
- Do not create a new wrapper skill for every combination. Add a package here
  only when the same lifecycle handoff recurs and materially reduces routing
  mistakes.
