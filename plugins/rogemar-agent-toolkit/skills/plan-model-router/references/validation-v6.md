# GPT-6 Sol and Luna: Forge routing comparison

This update changes the existing five policies, using 714 new native worker assignments across 17 model/reasoning profiles and 42 locked Harbor Notes cases. All requested profiles were checked against native metadata. The three main-owned roles received 51 proposal checks, not parent-coordination trials.

The historical 28-run dataset remains unchanged. The new work includes 112 representative qualification assignments plus 7 exact existing pairs reused with their failures. Two independent assessors graded anonymous answers without profile/usage labels. Main reconciliation inspected source and executable counterexamples and had access to the full experiment; it was not independently blinded. Grading, coordination, diagnostics and retries are separate overhead.

## What the initial benchmark supports

These are narrow focus results, not universal intelligence scores. Every profile had the same 42 supplied cases; a pass on a short readiness answer does not demonstrate operating a device or implementing a product.

| Profile | Meets focus / 42 | Needs revision | Critical | Standard credit proxy | Median worker seconds | Raw tokens | Response rounds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-sol/high | 39 | 3 | 0 | 62.850 | 28.0 | 1,060,390 | 45 |
| gpt-5.6-sol/low | 31 | 10 | 1 | 62.736 | 25.3 | 1,081,864 | 46 |
| gpt-5.6-sol/max | 41 | 1 | 0 | 58.624 | 32.9 | 1,069,774 | 45 |
| gpt-5.6-sol/medium | 36 | 5 | 1 | 61.972 | 27.0 | 1,106,723 | 47 |
| gpt-5.6-sol/ultra | 40 | 2 | 0 | 64.420 | 33.1 | 1,046,191 | 44 |
| gpt-5.6-sol/xhigh | 38 | 4 | 0 | 67.065 | 27.7 | 1,087,796 | 46 |
| gpt-6-luna/high | 36 | 6 | 0 | 1.597 | 24.9 | 1,046,489 | 44 |
| gpt-6-luna/low | 34 | 7 | 1 | 1.352 | 19.8 | 990,740 | 42 |
| gpt-6-luna/max | 39 | 3 | 0 | 1.625 | 29.6 | 1,086,468 | 45 |
| gpt-6-luna/medium | 29 | 13 | 0 | 1.494 | 20.0 | 1,087,917 | 46 |
| gpt-6-luna/xhigh | 39 | 3 | 0 | 1.707 | 27.8 | 1,029,710 | 43 |
| gpt-6-sol/high | 42 | 0 | 0 | 31.541 | 25.3 | 1,028,889 | 43 |
| gpt-6-sol/low | 38 | 4 | 0 | 30.534 | 20.6 | 1,023,218 | 43 |
| gpt-6-sol/max | 41 | 1 | 0 | 25.434 | 30.0 | 1,040,790 | 43 |
| gpt-6-sol/medium | 40 | 2 | 0 | 31.142 | 23.8 | 1,027,244 | 43 |
| gpt-6-sol/ultra | 41 | 1 | 0 | 29.571 | 29.6 | 1,065,119 | 44 |
| gpt-6-sol/xhigh | 39 | 3 | 0 | 30.520 | 27.8 | 1,033,174 | 43 |

GPT-6 Sol/High met all 42 initial focuses in this sample. That does not make it the best profile for every actual playbook: representative implementation checks, relevant failures and task boundaries still decide promotion. Luna's low token rates make it useful for suitable bounded support, but Economy retains required acceptance checks and disclosed failures.

Max is not categorically worse or more expensive. GPT-6 Sol/Max had a lower observed credit estimate than some lower-effort runs because more input was cached. It generated more output/reasoning and had a longer median duration. Cache variation prevents attributing that credit difference to reasoning alone. Ultra and Max were both included where supported; Luna/Ultra was not supported or tested.

The published Standard token rates currently make GPT-6 Sol cheaper than GPT-5.6 Sol. Lean nevertheless retains the user-approved GPT-5.6 Sol parent/pool boundary; this update does not silently redesign the agreed modes. Account credits are estimates, API-equivalent dollars are a separate scenario, and neither is an observed Pro-account deduction.

## Qualification and installed decisions

Decision statuses: historically-verified: 29, newly-verified: 97, provisional: 34, task-dependent: 10, unavailable: 12, user-selected-profile: 43.

| Proposed consultant | Mode | Profile | Outcome |
| --- | --- | --- | --- |
| hillclimb | peak | gpt-6-luna/max | Qualified read-only-consultation; practical need still required |
| hardest-tasks | peak | gpt-6-sol/max | Qualified bounded-implementation-or-consultation; practical need still required |
| hillclimb | balanced | gpt-6-luna/max | Qualified read-only-consultation; practical need still required |
| hardest-tasks | balanced | gpt-6-sol/max | Qualified bounded-implementation-or-consultation; practical need still required |
| hillclimb | lean | gpt-6-luna/max | Qualified read-only-consultation; practical need still required |
| hardest-tasks | lean | gpt-6-sol/max | Qualified bounded-implementation-or-consultation; practical need still required |
| hillclimb | economy | gpt-6-luna/max | Qualified bounded-implementation-or-consultation; practical need still required |
| hardest-tasks | economy | gpt-6-luna/xhigh | Not promoted; failed or incomplete pair, parent fallback remains disclosed |

Exact historical consultant records remain separately identified in the ledger; records contradicted by relevant new defects are retired from active dispatch. No old Terra or GPT-5.6 Luna record was renamed into a new-model exception.

The initial candidate ranking used observed worker credit proxies after quality/policy filtering. Already-planned passing representative pairs were then compared within the same packet. A failed candidate pair retains a disclosed parent fallback; it does not trigger repeated attempts until an answer passes. Every selected profile, alternative, rationale and source assignment is in [the decision ledger](role-evidence.json).

SQLite implementation checks cover authorization, whitespace rejection, owner-scoped concurrent retries, persistence/reopening and stable IDs. Working UI checks cover a single form at 320px and 1280px, keyboard, accessible state semantics and save/recovery. Source tracing checks entry points, helper lines, facts and unknowns. Monitoring/consolidation uses a frozen completed-review snapshot and does not gain validation or publication authority. These contracts remain separate.

Two routine workers issued `pwd` despite their packet prohibiting execution; their tool usage and protocol failures are retained. This is one event per affected batch, not a new tool invocation for every focus. Grader identifier/coverage collection errors are retained separately; no candidate answer is repaired to make it pass. Packet-specific word limits and checker assumptions are explicitly adjudicated.

Parent fallback is a routing decision, not resolution of a demonstrated quality defect. Required independent reviews and native GoalBuddy receipts cannot be replaced by a parent fallback or an ordinary Forge reviewer.

## Comparative limitations and provenance

The new CLI wrappers contained roughly 23–24k input context; older desktop runs commonly contained 80–100k. Native recommended-plugin lists and the local date changed during the cohort; audit-only normalization confirmed the remaining wrapper was stable. Actual prompts were not rewritten. Cache and context differ, so dated comparisons are observational. Forty common ordinary cases exclude historical Scout/Judge native-pin mismatches; the full original 42-case totals are retained separately.

Cached input is already included in input totals. Response rounds, assignment turns, tool calls and agent counts remain different measures. Whole representative-batch costs are never divided into fictional per-role costs. The three main roles do not add fictitious workers. Tests verify policy and scoped outcomes, not parent coordination or actual parent switching. The updated role mixtures are routing decisions, not newly measured end-to-end mode totals; do not sum overlapping qualification-batch costs into a fictional mode cost.

Original packets, output answers, native records, two assessments, adjudications, executable artifacts and current pricing are retained with hashes. Vendored summaries omit runtime session identifiers and session hashes; original private audit artifacts remain unchanged. Ambiguous blank-text-versus-replay ordering is excluded consistently in the original prose benchmark; the SQLite qualification explicitly specifies replay precedence and tests it. Candidate answers are not repaired before assessment. Missing prices stay unknown.

Pricing sources retrieved for this cohort: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing), [Codex pricing and usage](https://help.openai.com/en/articles/11481834), and [ChatGPT credit usage](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-freegopluspro-sora). Published Standard equivalents are estimates; account and service-tier effects are disclosed separately.

[Role mapping](role-mapping.md) · [225-decision ledger](role-evidence.json) · [Paired evidence and benchmark summary](validation-v6.json)

## Observed usage and overhead

Capture cutoff: 2026-09-23T18:59:13.150249+00:00. Coordinator usage stops at the recorded cutoff and excludes later work/final response. Unknown usage is not zero.

| Category | New worker sessions | Response rounds | Known token subtotal | Estimated Standard credit subtotal | Complete estimate? |
| --- | ---: | ---: | ---: | ---: | --- |
| candidate | 714 | 752 | 17,912,496 | 564.185 | Yes, to cutoff |
| benchmark-grading | 12 | 12 | 727,424 | 166.898 | Yes, to cutoff |
| qualification | 112 | 143 | 3,678,087 | 220.672 | Yes, to cutoff |
| qualification-grading | 44 | 44 | 1,739,955 | 315.263 | Yes, to cutoff |
| grading-completion-overhead | 1 | 1 | 27,701 | 1.268 | Yes, to cutoff |
| diagnostic | 2 | 2 | 87,320 | 0.127 | No: missing records/rates |
| routing-review-and-probes | 8 | 31 | 2,183,203 | 100.152 | Yes, to cutoff |
| coordination-to-cutoff | 0 | 509 | 83,718,047 | 3016.469 | Yes, to cutoff |

Grading-completion overhead contains only omitted assessments, not new candidate attempts. Tool retry rounds are an overlapping subset already counted above; their incremental causal cost cannot be isolated. Reused historical pairs incur no new candidate cost in this run. Native probe sessions validate dispatch and receipts, not a live parent switch or completed project gate.
