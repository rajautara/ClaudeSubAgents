---
description: Run the full test suite and triage failures
argument-hint: [unit|integration|all]
---

Run the .NET test suite (`$ARGUMENTS`, default all) and report results honestly.

1. Run `dotnet test` (filter to unit vs integration via traits/categories if a
   scope was given; integration tests may require Docker for Testcontainers).
2. Summarize pass/fail counts and list each failure with its assertion message.
3. For genuine product bugs, hand the fix to the relevant engineer
   (`backend-engineer`/`data-engineer`/etc.); for missing coverage, hand to
   `test-engineer` or `integration-test-engineer`.
4. Do NOT weaken or delete a test to make it pass — a failing test that reflects
   a real defect is the point.
