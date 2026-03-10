---
name: tdd
description: This skill should be used when the user asks to "fix a bug using TDD", "implement using test-driven development", "write a failing test first", "add a feature test-first", "use red/green/refactor", "debug this systematically", or when working on a git repository and needing to implement or debug code incrementally. Provides a structured TDD red/green/refactor workflow with hypothesis-driven debugging.
---

# TDD Development Workflow

Structured test-driven development using a red/green/refactor cycle. Start with a hypothesis, write a failing test, make it pass, then clean up.

## Workflow

### 1. Plan with Todos

Before writing any code, create a todo list to reflect the implementation plan. This makes the intent explicit and tracks progress.

Use `TaskCreate` to define:
- The hypothesis or expected behaviour change
- The test(s) to write
- The implementation steps
- Any refactoring tasks

### 2. Establish a Hypothesis

Before writing any code or test, form a hypothesis:

- **For bugs:** State why the system is failing — which component, which condition, what incorrect behaviour. If a hypothesis cannot be formed, state why and identify what information is missing.
- **For features:** State the expected behaviour that does not yet exist.

A good hypothesis is falsifiable: it predicts what a test will reveal.

### 3. Red — Write a Failing Test

Write the minimal test that validates the hypothesis:

- **Re-use an existing test** if one already covers the failing behaviour — just run it.
- **Write a new test** only when no existing test covers the case.

The test must fail for the *right reason* — not due to a syntax error or missing import, but because the behaviour under test is incorrect or absent.

Run the test. Confirm it fails.

```bash
# Python / pytest — run a single test
pytest path/to/test_file.py::TestClass::test_method -v

# Run a module
pytest path/to/test_file.py -v

# Run with output (useful for hypothesis validation)
pytest path/to/test_file.py -v -s
```

### 4. Green — Write the Minimal Code

Write only the code needed to make the failing test pass. Do not over-implement.

Run the test. Confirm it passes.

If it does not pass:
- Re-read the error — is the hypothesis still valid?
- Update the hypothesis if the error reveals something unexpected.
- Adjust the code and run again.

### 5. Refactor

With tests green, clean up without changing behaviour:

- Remove duplication
- Improve naming
- Simplify logic
- Extract functions or classes if complexity warrants it

Run the full affected test suite after each refactor step to confirm nothing regressed.

```bash
# Run all tests in a module or package
pytest path/to/tests/ -v

# Run with coverage to spot untested paths
pytest path/to/tests/ --cov=src/module --cov-report=term-missing
```

Repeat the refactor/run loop until the code is in a satisfying state.

## Iteration

If after making a test pass a new edge case becomes apparent, return to step 2:

1. Form a new hypothesis for the next case
2. Write a failing test
3. Make it pass
4. Refactor

Each cycle should be small and focused. Avoid implementing more than one behaviour change per cycle.

## Stopping Criteria

A cycle is complete when:
- All tests pass (including pre-existing ones)
- The code expresses intent clearly
- No obvious duplication or complexity remains

Mark todos as complete as each step finishes.

## Notes for Python / pytest

- Prefer `pytest` over `unittest` runner
- Use `pytest -x` to stop on first failure during red/green cycles
- Use `pytest -k "test_name"` to filter by test name pattern
- Fixtures go in `conftest.py`; keep test files close to the code they test
- For dbt models, use `dbt test` or `dwh-cli dbt test` instead of pytest
