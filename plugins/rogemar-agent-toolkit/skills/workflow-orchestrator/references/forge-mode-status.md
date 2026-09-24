# Forge mode selection and status

Apply this contract at Codex, Cursor and Universal Forge entry, resume and new
worker dispatch. The existing orchestrator owns it; do not create a new agent,
configuration service or background process. Native routers retain their model
catalogues, limits and tool controls.

## Resolve the mode once

Use this precedence: explicit current request → established task/handoff mode →
valid saved preference for this harness. Normalize supported legacy aliases.
An explicitly requested no-mode/inheritance route remains an owner choice; do
not replace it with a saved mode or repeatedly ask. Never infer a mode from the
parent model. Its capability may inform a recommendation, not choose a budget.

If no choice exists, ask once using the active harness’s supported modes. Codex
offers Default, Peak, Balanced, Lean and Economy; other harnesses retain their
native catalogues and labels. Use the host’s supported question channel.
Continue safe inspection and useful direct work while awaiting the answer; keep
mode-dependent worker dispatch pending. Elapsed time or silence is not a choice.
Record `mode: pending` and whether the question was already asked. On resume,
restore that state rather than asking again. If the host cannot ask, disclose
that limitation and use native defaults for permitted direct work; do not claim
a named mode or its restrictions were applied.

Read only this harness's saved configuration. A malformed preference is an
explicit configuration problem, not absence: preserve it and report the issue.
Missing model selection controls do not invalidate an established mode's intent,
but may leave its requested profiles unapplied. Never silently inherit an
excluded profile or bypass required independence and explicit limits.

Retain the selected mode and source in existing task context. A task-only choice
never writes settings. Persist only an explicit save/setup request through the
native setup validation and backup procedure. A new explicit task choice wins;
a changed saved preference does not silently replace an established task mode.
Requalify new workers after mode changes. Existing workers keep their original
assignment mode/profile unless a supported change is applied and verified.
There is no automatic parent-derived mode and no new Auto mode.

## Inspect profile evidence before reporting status

Before reporting a parent profile as unavailable or unverified, make one bounded
inspection of the current harness's exposed metadata and controls. Prefer
current-task runtime metadata; if using a local session record, first match its
task identity and latest applicable turn, and report it as recorded evidence.
Read only the model and reasoning fields needed, not unrelated session content.
Global defaults, saved preferences and the available model catalogue do not prove
which profile is executing this turn. Reuse fresh evidence while the task and
profile remain unchanged; do not repeatedly scan sessions.

Resolve the desired profile through the existing harness router. Distinguish
requested settings, an accepted control action, and verified runtime settings.
Inventory supported current-task controls before declaring switching unavailable.
A follow-up message, new task, worker spawn or global configuration edit is not
a substitute for switching the active parent. Do not claim full mode application
when the desired parent remains unapplied.

If evidence or a supported control is absent, name what was inspected, the
specific limitation, the desired profile if resolved, and the manual selection
needed in the current task. Do not invent a UI path or model identity. Apply the
parent clarification below; diagnostics and skill maintenance remain exempt.

## Clarify a different parent before execution

At execution entry or a mode change, resolve the mode's desired parent through
its harness router and compare both model and reasoning effort with authoritative
current-parent metadata. In Codex, use `parent-coordinator`, `target: parent`.
A desired profile is a recommendation, not an observed switch.

If either setting differs, show the mode, desired profile, and actual profile,
then ask once: “This mode recommends <desired model / effort>; your current
parent is <actual model / effort>. Keep the current parent for this task, or
switch it manually before proceeding?” Recommend keeping the current parent
when it is sufficient and no explicit user limit prohibits it. An explicit
prior instruction to keep that parent already answers the question.

Keep implementation and mode-dependent worker dispatch pending until the user
chooses. Safe read-only inspection may continue. Silence is not acceptance.
If the user keeps the parent, record an accepted fallback for this task; requalify
workers under the selected harness policy. Codex normal workers obey both the
mode and accepted parent's model and reasoning ceilings; a higher fallback
parent does not expand the mode. If the
user chooses a manual switch, wait and verify fresh runtime metadata before
proceeding; a claim of switching or a settings update alone is not verification.
Never apply a parent change silently.

Carry the decision and compared mode/desired/actual profiles through handoffs.
Do not ask again for the same accepted combination on follow-ups or resume.
Recheck when the mode, desired profile, or observed parent changes. Matching
profiles need no clarification. If identity or the desired profile is unavailable,
state that it is unverified rather than inventing a mismatch; ask whether to
continue with the unverified current parent before mode-dependent execution.
Inspection-only setup, routing diagnostics, and skill maintenance do not require
this execution question. Do not persist a fallback preference unless requested.

## Show role, model, effort and mode

At initial entry and resume, show one compact coordinator label, for example:

`Coordinator · GPT-6 Sol / xhigh · Balanced · model verified · source: saved preference`

Use the actual available model identifier or an unambiguous friendly name,
including its generation when multiple generations share a family name.
Do not infer active parent identity or effort from a configuration default.
If metadata is unavailable, show `model unverified` and/or `effort unverified`;
if the backend has no reasoning selector, use `effort not exposed`. Never present
an inferred effort as observed. Show `mode pending` or `no named mode` when apt.
Examples are formats, not actual runtime observations.

At useful worker dispatch, show role, requested model/effort and assignment mode:

`Explorer · GPT-6 Luna / low requested · Balanced`

After dispatch, distinguish requested settings, tool acceptance and authoritative
runtime observation. Only runtime metadata can justify `model verified`; a worker
self-introduction, role name or successful spawn cannot. When observation is
unavailable, retain the requested profile with `effective model unverified`.
Report mismatches promptly and requalify or stop affected work as appropriate.
Workers return their role, assignment mode and evidence status in their ordinary
receipt; they must not claim identity based on the assignment prompt.

Repeat status labels only at entry/resume, relevant dispatch, a mode/profile/constraint
change, or on request. New sub-agent labels follow
[sub-agent naming](subagent-naming.md): role, task, assigned native model and
reasoning, with mode retained only in status and receipts. Use the active harness's
naming controls or handoff fallback; native role IDs and existing agents remain unchanged.
When multiple models were used, include a compact final routing receipt covering
roles, assignment modes, requested profiles, observed profiles and unresolved
mismatches. Use the existing receipt rather than a second ledger.

Carry selected mode, source, pending-question state, explicit limits and worker
assignment profiles in the existing handoff. Parent proposals remain separate
from observed identity. A mode change, saved preference or worker launch is not
proof of a parent switch; report a desired parent change as unapplied unless a
supported current-task control and runtime evidence establish it.

## Codex five-mode policy

The Codex router is authoritative for targets, Default profiles, normal ceilings
and verified exceptions. Shared labels do not rewrite Cursor or Universal pools.
For an accepted parent fallback, carry the exact mode, desired and actual profiles
plus the affirmative choice; refresh the choice if any changes. Pass them as
`parent_fallback: {mode, desired, actual, accepted: true}`. Normal worker limits
are the stricter mode target and actual-parent limits. A higher actual parent
cannot expand a preset. Default remains exact and needs an explicitly matching
task `default_profile` if the owner chooses a different parent.

Carry `goalbuddy_required`, explicit limits, and any qualified exception evidence
in the existing handoff. Do not treat a mode label as proof of native contracts,
a parent switch, tested coordination quality or an increase in available quota.

Codex handoffs also preserve `consequential`, `implementation`, the exact
qualification ID, limitations and any justified exception need. An accepted
higher fallback parent does not expand the mode worker pool. Default is exact;
main-owned integration and final acceptance remain with the main agent.

Carry `known_quality_failures` into current acceptance checks; a provisional parent
fallback does not clear those findings. Record resolution only after verification.
