---
name: csv-analytics-reporter
description: Use when analyzing CSV, TSV, spreadsheet exports, product analytics, finance tables, survey responses, event logs, or tabular data that needs cleaning, aggregation, charts, anomaly checks, or plain-language findings.
---

# CSV Analytics Reporter

## Workflow

1. Inspect schema, row count, column types, missing values, and obvious data quality issues.
2. Use structured parsers or spreadsheet libraries rather than ad hoc string splitting.
3. Compute requested metrics and sanity-check totals against row counts or known constraints.
4. Report key findings, caveats, and recommended next cuts.
5. Create charts or workbooks only when they help the decision.

## Output Defaults

- Data summary.
- Top findings.
- Metric table.
- Caveats and next questions.

## Guardrails

- Do not silently drop rows or coerce ambiguous values.
- For financial, legal, or medical data, state uncertainty and avoid advice beyond analysis.
