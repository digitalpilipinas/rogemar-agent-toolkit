---
name: meeting-notes-task-extractor
description: Use when summarizing meeting transcripts, call notes, voice transcriptions, calendar notes, or raw discussion logs into decisions, action items, owners, due dates, risks, and follow-up messages.
---

# Meeting Notes Task Extractor

## Workflow

1. Load the transcript, notes, or source document. Use Drive, Notion, Slack, calendar, or filesystem connectors when available.
2. Identify participants, date, meeting purpose, decisions, unresolved questions, and commitments.
3. Extract tasks with owner, due date, confidence, and source evidence. Use `Unassigned` or `No due date` instead of guessing.
4. Produce a concise summary plus a task table.
5. If asked, draft follow-up email/message or create tasks in the connected system.

## Guardrails

- Do not invent attendance, owners, dates, or commitments.
- Mark ambiguous or implied tasks as low confidence.
- Keep sensitive internal context out of public-ready summaries unless requested.
