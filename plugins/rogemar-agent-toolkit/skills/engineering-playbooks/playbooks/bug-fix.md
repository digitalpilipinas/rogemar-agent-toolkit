# Bug fix

Tie the fix to evidence of the causal mechanism. The main agent owns investigation, implementation and verification and may request bounded independent help through the orchestrator.

1. Reproduce on the matching surface using an exposed control tool or repository-native harness. Synthesize triggers or add bounded instrumentation when needed. If the environment is unavailable, collect the strongest static/repro evidence and label the runtime gap; do not invent a reproduction or weaken the criterion.
2. Trace with `source tracing`, consult `history investigation` for regression history when useful, and form competing hypotheses. Choose experiments that eliminate the most plausible causes. Confirm the mechanism before investing in a redesign. After two equivalent failed attempts, reassess the hypothesis or environment.
3. Plan the smallest justified fix. Use `design exploration` only for a consequential design decision. Request worker role `bug-fix` through the orchestrator when useful; no specialist dispatches directly.
4. Add a failing-before/passing-after regression test when it can meaningfully guard the bug. Use `regression-first verification` for the cheap local path; do not manufacture tests that mirror a trivial implementation.
5. Rerun the original reproduction and applicable regression checks. Wrong-surface, inconclusive and unavailable evidence remain distinct from a pass. Remove only the task's disproven experimental changes and temporary instrumentation, preserving unrelated work.
6. Prepare publication through `opening-a-pr.md` only within explicit authority. Separate test-first history is optional and requires commit authority.

Report broken behavior, causal evidence, fix, before/after checks and any remaining runtime gap.
