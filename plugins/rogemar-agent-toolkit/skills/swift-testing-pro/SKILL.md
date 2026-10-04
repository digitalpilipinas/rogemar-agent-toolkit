---
name: swift-testing-pro
description: Writes, reviews, and improves Swift Testing code using modern APIs and best practices. Use when reading, writing, or reviewing projects that use Swift Testing.
license: MIT
metadata:
  author: Paul Hudson
  version: "1.0"
---

## Toolkit integration

Read the actual project deployment targets, compiler/concurrency settings, persistence
architecture and test conventions before applying these references. Examples using
new SDKs are conditional on availability; this skill does not authorize a platform,
framework or data migration. Preserve compatible existing UIKit, XCTest and storage.
Reuse approved task authority. Load only references needed for the affected behavior.
Static review needs no login or Xcode; build, simulator, UI, accessibility and device
claims each require their own observed evidence. Missing prerequisites remain blocked.
`workflow-orchestrator` remains the sole dispatcher; this method does not own delivery.

Write and review Swift Testing code for correctness, modern API usage, and adherence to project conventions. Report only genuine problems - do not nitpick or invent issues.

Review process:

1. Ensure tests follow core Swift Testing conventions using `references/core-rules.md`.
1. Validate test structure, assertions, dependency injection, and other best practices using `references/writing-better-tests.md`.
1. Check async tests, confirmations, time limits, actor isolation, and networking mocks using `references/async-tests.md`.
1. Ensure new features like raw identifiers, test scopes, exit tests, and attachments are used correctly using `references/new-features.md`.
1. If migrating from XCTest, follow the conversion guidance in `references/migrating-from-xctest.md`.

If doing partial work, load only the relevant reference files.


## Core Instructions

- Follow the installed compiler and the project’s Swift language/concurrency settings.
- Use Swift Testing where the project uses it or an approved migration selects it. Existing XCTest tests are not defects merely because they use XCTest.
- Swift Testing does *not* support UI tests – XCTest must be used there.
- Use a consistent project structure, with folder layout determined by app features.

Swift Testing evolves with each Swift release, so expect three to four releases each year, each introducing new features. This means existing training data you have will naturally be outdated or missing key features.

Check API availability against the installed toolchain and current primary documentation; resolve discrepancies with a compiling reproducer.


## Output Format

If the user asks for a review, organize findings by file. For each issue:

1. State the file and relevant line(s).
2. Name the rule being violated.
3. Show a brief before/after code fix.

Skip files with no issues. End with a prioritized summary of the most impactful changes to make first.

If the user asks you to write or improve tests, follow the same rules above but make the changes directly instead of returning a findings report.

Example output for an explicitly approved XCTest-to-Swift Testing migration:

### UserTests.swift

**Line 5: Use struct, not class, for test suites.**

```swift
// Before
class UserTests: XCTestCase {

// After
struct UserTests {
```

**Line 12: Use `#expect` instead of `XCTAssertEqual`.**

```swift
// Before
XCTAssertEqual(user.name, "Taylor")

// After
#expect(user.name == "Taylor")
```

**Line 30: Use `#require` for preconditions, not `#expect`.**

```swift
// Before
#expect(users.isEmpty == false)
let first = users.first!

// After
let first = try #require(users.first)
```

### Summary

1. **Fundamentals (high):** Test suite on line 5 should be a struct, not a class inheriting from `XCTestCase`.
2. **Migration (medium):** `XCTAssertEqual` on line 12 should be migrated to `#expect`.
3. **Assertions (medium):** Force-unwrap on line 30 should use `#require` to unwrap safely and stop the test early on failure.

End of example.


## References

- `references/core-rules.md` - core Swift Testing rules: structs over classes, `init`/`deinit` over setUp/tearDown, parallel execution, parameterized tests, `withKnownIssue`, and tags.
- `references/writing-better-tests.md` - test hygiene, structuring tests, hidden dependencies, `#expect` vs `#require`, `Issue.record()`, `#expect(throws:)`, and verification methods.
- `references/async-tests.md` - serialized tests, `confirmation()`, time limits, actor isolation, testing pre-concurrency code, and mocking networking.
- `references/new-features.md` - raw identifiers, range-based confirmations, test scoping traits, exit tests, attachments, `ConditionTrait.evaluate()`, and the updated `#expect(throws:)` return value.
- `references/migrating-from-xctest.md` - XCTest-to-Swift Testing conversion steps, assertion mappings, and floating-point tolerance via Swift Numerics.
