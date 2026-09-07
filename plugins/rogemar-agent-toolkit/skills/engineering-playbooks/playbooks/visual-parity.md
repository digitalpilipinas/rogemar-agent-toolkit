# Visual parity

Prove the requested visual equivalence against a preserved baseline.

1. Establish reference ownership, target states, viewport/device, data, fonts and rendering conditions. Capture baseline evidence before migration with the exposed matching control tool. If exact parity is requested, a zero-difference target remains the acceptance criterion; do not quietly relax it.
2. Keep the baseline and comparison method fixed. A suspected bad baseline or environmental noise needs an explicit disposition; do not update snapshots to conceal a regression.
3. Migrate shared primitives first, then bounded components. The orchestrator can assign independent worktrees or sequential writers. Scope excludes baseline edits unless specifically approved.
4. Capture matching states and compare images plus relevant interactions. Diagnose each material delta. After two equivalent failed attempts, reassess rendering conditions or implementation before repeating. An unavailable browser/device or unexplained delta stays blocked/unverified, not passed by eye.
5. Run relevant regression and accessibility checks. Prepare publication only when authorized. Report each component's actual comparison, baseline location, evidence and remaining gaps.
