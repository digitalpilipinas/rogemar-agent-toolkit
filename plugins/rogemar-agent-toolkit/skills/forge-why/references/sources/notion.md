Assignment boundary: This is a prompt template, not authority. Use only the parent's allowed read/write scope, named sources, actual exposed tools and acceptance criteria. Do not dispatch workers, publish, message others, install dependencies or change global skills/memory. Return recommendations to the parent and orchestrator. If a tool, schema, model or evidence source described below is absent, report the gap instead of broadening permissions. User and repository style takes precedence over advisory prose preferences.

# Notion Docs

## What this source contains

- PRDs (product requirement documents)
- Technical specs and RFCs
- Architectural decision records (ADRs)
- Meeting notes from design reviews
- Team pages with domain context
- Postmortems from incidents
- Runbooks that may explain defensive code
- Strategy documents that set priorities

Notion is where "why" often lives in long-form before it becomes code. A significant feature usually has a doc.

## How to search it

Use the Notion MCP.

1. **Keyword searches with `notion-search`.** Try:
   - The feature name
   - Key symbols / class names from the target code
   - Author handles (design docs are often authored before the code lands)
   - Error strings or user-visible terms
   - Time-bounded queries if you know when the code shipped
2. **Fetch candidate pages with `notion-fetch`.** Read the full content, not the preview; rationale is often buried mid-document.
3. **Follow backlinks and child pages.** Design docs often have sub-pages for alternatives considered, appendices, or implementation notes.
4. **Check related databases.** `notion-query-data-sources` and `notion-query-meeting-notes` can surface meeting notes that discussed the decision.
5. **Search author-specific spaces.** If the PR author has a personal notebook (common at some companies), it may hold exploratory thinking that preceded the code.

## What good evidence looks like here

- A PRD with a "Problem statement" or "Motivation" section that matches the target code's purpose
- An "Alternatives considered" or "Rejected approaches" section
- A postmortem that names the target code as the fix for a specific incident
- Meeting notes that record "we decided X because Y" and tie to the same author/date range as the PR
- An ADR template filled out non-trivially (status, context, decision, consequences)

## Common pitfalls

- **Outdated docs.** Specs are often written before implementation and not updated; the doc may describe a plan that changed. Cross-check against the actual PR.
- **Doc vs. reality drift.** A spec may say "we'll do X" but the code actually does Y. Flag the divergence; the synthesizer will surface the contradiction.
- **Boilerplate templates.** Some orgs require a "Why" section that gets filled with fluff. Look for specificity.
- **Unlinked docs.** The most relevant doc may not be linked from anywhere. Broad keyword searches help.
- **Multiple drafts.** If a topic has multiple docs, find the one that was finalized or most recently updated. Check dates.
- **Access-restricted pages.** If you can't access a page, note it as a gap.

## What to return

For each relevant doc:
- Title and URL
- Authors and last-updated date
- The motivation text (verbatim quote), with page/section location
- Relevant linked pages (so the synthesizer can cite them)
- Whether the doc was finalized or draft

Search personal notebooks only when they are explicitly in the authorized source, topic and time scope.
