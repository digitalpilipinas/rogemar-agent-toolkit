# Test Behavior, Not Implementation

A useful test detects a meaningful defect in the behavior or contract it protects. Start with the caller, concrete input, expected observable result and a plausible broken implementation that must fail the test.

- Exercise the real subject and compare with an independently chosen expectation. Do not derive the expected answer by calling the same implementation twice.
- When practical, temporarily introduce the plausible defect or run the test against the pre-fix version and verify that it fails for the intended reason. Restore the mutation before completing work.
- Prefer observable outputs, persisted state or external effects over incidental helper calls. If the interaction itself is the contract, check the meaningful payload, ordering or denied side effect.
- Preserve legitimate negative, security, schema and static-contract tests. Absence can be the required behavior, and a compile-time or configuration invariant can prevent a real defect. An assertion name cannot tell you whether the test is valuable.
- Rewrite or remove a test only after identifying its contract, callers and replacement coverage. A test that still passes when a function returns nothing may be a valid denial-path test; use a relevant mutation rather than a universal undefined-return rule.

Examples: unauthorized writes must produce no database call; test an allowed caller too when useful, and confirm removing authorization makes the denial test fail. An empty search result is valid behavior if a matching query returns the expected record. A schema check that rejects an unknown property and accepts the valid request protects a boundary. A static check preventing a secret from entering a client bundle is valuable even without a UI action.
