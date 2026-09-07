# Opening a PR

Prepare a reviewable change; publish only with commit, push and PR authority appropriate to the current request. Routine local implementation does not imply publication.

1. Inspect repository instructions, branch, remotes, status, diff and existing PR. Preserve unrelated work. Use a separate worktree when isolation is needed; do not reset a dirty checkout or move other work without authority.
2. Review the actual diff and run relevant checks. Apply `forge-no-comments` only where comment cleanup helps and preserve necessary comments and suppressions. Use `forge-technical-writing` and `forge-unslop` for the description without imposing prose rules over the repository template.
3. Prepare narrowly scoped staging paths and a concrete title/body. Prefer the repository's convention; otherwise use a concise imperative title naming the problem or resulting behavior. Explain why, scope, material tradeoffs, blast radius and actual verification in the space the change warrants.
4. With explicit authority, commit the reviewed paths and push the intended branch. Confirm remote identity and inspect the result. No catch-all staging, force push or history rewrite by default. Reuse an existing PR where appropriate; a draft is valid for work awaiting evidence or review.
5. Choose a verified authorized forge tool. GitHub CLI is a fallback when available/authenticated. Optional services require explicit availability; do not silently switch destinations or require Graphite. Read multiline bodies from a file or structured argument.
6. For a stack, record branch/base/head relationships. The root targets verified trunk; each child targets its intended parent. Topology has one writer. Changes to base or head require fresh integration evidence even when the patch appears equivalent.
7. Verify the published PR URL, state, head and base before reporting. A PR does not imply a merge, monitor, notification or deployment. Start babysitting only when that scope is authorized. Workers return artifacts or authorized PR receipts to the parent and do not acquire publication authority from this playbook.
