---
name: research-synthesizer
description: Use when the user asks for deep research, competitive analysis, current facts, cited summaries, decision memos, source extraction, or a multi-source answer that should separate evidence from inference and recommendations.
---

# Research Synthesizer

## Workflow

1. Define the question, decision, audience, and time sensitivity.
2. Search current sources when facts may have changed. Prefer primary sources, official docs, papers, filings, or vendor docs over commentary.
3. Collect source URLs and note what each source actually proves.
4. Synthesize into the requested shape: brief, memo, table, recommendation, or Markdown notes.
5. Separate confirmed facts, reasoned inferences, and open questions.
6. Include citations and dates for time-sensitive claims.

## Standards

- Do not hide uncertainty. Say what is unknown or conflicting.
- Avoid over-weighting one source when multiple independent sources are needed.
- For technical answers, rely on official docs, source code, standards, or primary research.
- For EVERSO, connect research back to product value, cost, privacy, and implementation risk.

## Helpful MCPs

- `perplexity` for broad live research with citations.
- `firecrawl` or browser tooling for crawling source pages.
- `openaiDeveloperDocs` for OpenAI product/API facts.
- GitHub, Notion, Drive, Slack, or filesystem connectors for private/internal sources.

## Optional collaboration guidance

The orchestrator may assign independent read-only researchers for clearly
separable source sets, source verification, or evidence extraction. A
collaborator must receive the question, audience, time boundary, source
criteria, owned source set, non-goals, parent model and reasoning ceilings, and
required citation format. Return sources with what each proves, uncertainty,
and conflicts; do not make the final recommendation or claim overall research
completion. The orchestrator decides whether to use the hint and the main
agent reconciles the synthesis.
