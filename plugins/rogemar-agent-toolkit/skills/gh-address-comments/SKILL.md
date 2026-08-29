---
name: gh-address-comments
description: CLI fallback for addressing open GitHub PR comments when the GitHub plugin is unavailable, unauthenticated, or the user explicitly requests gh CLI. Prefer the GitHub-plugin gh-address-comments skill for connected review-thread context.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Prefer the GitHub-plugin `gh-address-comments` skill for connected review-thread context; this is the connector-independent fallback. Start GitHub CLI calls normally; retry only the exact command with narrowly scoped elevation if a network or sandbox denial blocks it.

Prereq: run `gh auth status` normally. If a network or sandbox denial blocks it, retry with narrowly scoped elevation. If authentication is absent, ask the user to authorize or complete `gh auth login`; do not initiate login automatically.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Resolve remediation authority
- Number all review threads and comments, deduplicate them by semantic root
  cause, and summarize what each genuinely new actionable item requires.
- If an approved plan, active programme, or explicit owner instruction already
  authorizes remediation of all current actionable PR feedback, do not ask for
  the same approval again. Proceed inside that recorded scope.
- Otherwise ask which numbered comments should be addressed.

## 3) Address authorized comments
- Apply fixes only for selected or already-authorized comments. Reply with
  evidence before resolving a thread, and preserve rejected or deferred
  dispositions so duplicates do not create another work loop.

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
