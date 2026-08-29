---
name: knowledge-base-answering
description: Use when answering questions from a scoped document set, repository docs, Notion/Drive/Slack content, internal notes, product specs, manuals, or local files where citations and source boundaries matter.
---

# Knowledge Base Answering

## Workflow

1. Define the source boundary first: which folder, docs, repo, workspace, or connector should be trusted.
2. Search within that boundary before using public web sources.
3. Answer only from retrieved evidence unless the user explicitly asks for outside knowledge.
4. Cite files, page titles, URLs, or message/document identifiers.
5. If the KB lacks the answer, say so and suggest the nearest source or update needed.

## Guardrails

- Do not blend private KB facts with public assumptions without labeling them.
- Do not present stale memory or old notes as current unless verified.
- Respect access controls and avoid copying large copyrighted/private passages.

## Helpful MCPs

- Filesystem for local repositories and docs.
- Notion or Drive connectors for workspace docs.
- Slack/Teams connectors for discussions.
- GitHub for issues, PRs, and repository knowledge.

Use a connector only when its tools are surfaced and authenticated in the current environment. If it is unavailable, use scoped local or user-provided sources only when they can answer the question; otherwise state the access limitation and request the smallest useful export, path, or authorization. Never imply that an inaccessible private source was checked.
