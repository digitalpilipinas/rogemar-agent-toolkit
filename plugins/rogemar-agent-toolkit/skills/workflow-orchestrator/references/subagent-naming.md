# Sub-agent task names across harnesses

Apply to new sub-agent assignments in default operation and every Forge mode.
The orchestrator owns one provider-neutral label convention; native adapters
supply the supported naming controls and qualified profiles. Decide whether to
delegate and qualify the profile before naming; a label cannot select a model,
change a role contract, authorize a spawn or satisfy an evidence gate.

## Construct the label

Use `Role — Task · Model / Reasoning` for readable handoffs and native display
names that support free text and these separators. Use the native field's allowed
encoding otherwise; do not send special characters to Codex `task_name`.

- Prefer short labels such as `Review`, `Explore` and `Build` when they accurately
  describe the assignment. These are display labels, not replacements for native
  role IDs or permission contracts. Keep the task to two to four meaningful words,
  such as `Naming rules` or `Navigation fix`, with role and task first.
  Retain reasoning values such as `medium` and `xhigh` without custom abbreviations.
- Use an unambiguous compact alias for the qualified native model. Retain
  version/family information when needed to distinguish models; use the full
  native model ID when no unambiguous alias exists. Preserve exact IDs in the
  existing receipt and tool arguments; aliases never replace dispatch IDs.
- Use the actual assigned native reasoning/thinking setting. If the control is
  a budget, retain its value and units; if several settings matter, keep enough
  to distinguish the assignment and retain full settings in the receipt. Never
  translate provider settings into assumed Codex effort levels or infer settings
  from a model's marketing name. Equal labels do not imply equivalent reasoning
  across providers.
- For confirmed inheritance, use the known inherited profile. If inheritance is
  selected but a value is unavailable, use `inherited` for that field; use
  `unknown` when its assignment is not established. Use `not_exposed` for
  reasoning only when the backend exposes no reasoning control. Preserve known
  fields when only one is unavailable. These labels do not relax routing checks;
  the native router decides whether inheritance or partial metadata is sufficient.
- Omit mode, execution status and verification badges. Keep mode in existing
  dispatch status and receipts, including a no-mode route when relevant.
- Check sibling names, including completed siblings when exposed. Add the first
  free numeric suffix starting at 2 only for collisions, using the native field's
  permitted encoding. Keep returned canonical paths or IDs for subsequent tool
  calls; do not reconstruct them from a displayed title.

## Bind to native controls

- **Codex:** when surfaced, encode `task_name` by joining the four fields with
  underscores, lowercasing the result, and replacing non-ASCII characters,
  spaces and punctuation with underscores. Collapse repeated underscores and
  trim leading/trailing underscores so the result uses only lowercase ASCII
  letters, digits and underscores. Normalize before checking collisions and
  applying suffixes `_2`, `_3`, and so on.
- **Cursor:** after the active authorized Cursor route qualifies the profile,
  inspect the live worker tool for a caller-controlled naming field. Cursor Forge
  keeps Setup as its primary route and retains the existing universal fallback;
  default operation follows its native qualification policy. Use the field's documented
  format and limits. Do not send Codex's `task_name` or reasoning arguments by
  analogy, rewrite a native role definition, or change PStack settings to add a
  label. The primary Cursor route remains the profile authority.
- **Universal/other harnesses:** after native qualification, use only the surfaced
  caller-controlled naming field and its constraints. Unknown host identity is
  not permission to assume Codex or Cursor syntax. Keep native model/setting
  arguments unchanged.
- **No naming control:** put the readable label in the ordinary task handoff and
  report that native naming is unavailable. Do not assume a prompt or description
  field renames the sidebar, or edit runtime state to simulate a rename. Naming
  unavailability alone does not block otherwise authorized, qualified work.
- **No sub-agent capability:** keep the work with the main agent under the
  existing workflow; do not invent a worker or claim independent execution.

Examples illustrate labels, not profile recommendations or runtime observations:

| Readable assignment | Codex encoding, when supported |
| --- | --- |
| Review — Design routing · GPT-5.6 Sol / medium | `review_design_routing_gpt56_sol_medium` |
| Build — Navigation fix · GPT-6 Sol / high | `build_navigation_fix_gpt6_sol_high` |
| Explore — Helper paths · inherited / inherited | `explore_helper_paths_inherited_inherited` |
| Review — Naming rules · GPT-6 Astra / xhigh | `review_naming_rules_gpt6_astra_xhigh` |

For other providers, substitute the qualified native model and actual native
setting in the readable form; the Codex examples do not establish availability
or supported controls in another harness.

## Identity and reuse

The name records the assignment at creation, not a verified effective profile.
Preserve requested, applied and observed model/settings separately in the existing
receipt. Report runtime mismatches through the routing contract; a matching label
or worker self-introduction cannot prove identity.

Keep existing agents, native agent-type IDs, role pins and generated nicknames
unchanged. Reused agents retain their original names; describe later assignments
in the handoff. A changed mode must not relabel an existing agent or imply its
model changed. Create a fresh worker only when the existing dispatch policy
independently requires it, never merely to refresh a label.

Each harness owns sidebar formatting, punctuation, capitalization and truncation.
Successful native name acceptance does not prove exact visual presentation.
Task-label changes do not change sub-agent images or avatars; those require a
separate exposed native customization control.
