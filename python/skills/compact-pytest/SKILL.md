---
description: Compact repetitive tests using pytest parametrization
argument-hint: [filepath]
allowed-tools:
  - Bash(git diff*)
  - Bash(git status*)
  - Bash(pytest*)
  - Read
  - Edit
  - Grep
  - Glob
---

# Compact Pytest Tests

Identify and compact repetitive test patterns using pytest parametrization.

If a filepath is provided, compact only that specific test file. Otherwise, identify and compact all test files in the current branch scope.

**IMPORTANT**: Only modify test files within the scope of the current branch/ticket. Do not refactor unrelated tests.

## Step 1: Identify Test Files in Scope

```bash
# If filepath provided: use that file directly
# Otherwise get changed test files in this branch vs target
git diff --name-only origin/main..HEAD | grep test_

# For uncommitted changes
git status --short | grep test_
```

## Parametrization Guidelines

### When to Parametrize

- Simple input -> output transformations
- Input -> specific exception raised
- Multiple similar assertions with different data values

### Basic Pattern

```python
@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (5, 10),
    (-1, 0),
])
def test_function(input_val, expected):
    assert transform(input_val) == expected
```

### Exception Testing

```python
@pytest.mark.parametrize("input_val,exception", [
    (None, ValueError),
    ("", TypeError),
    (-999, InvalidRangeError),
])
def test_function_raises(input_val, exception):
    with pytest.raises(exception):
        transform(input_val)
```

### Use Descriptive IDs

```python
@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (5, 10),
], ids=["single_digit", "larger_value"])
def test_function(input_val, expected):
    assert transform(input_val) == expected
```

## When NOT to Parametrize

- Tests with complex setup/teardown that differs between cases
- Tests with multiple unrelated assertions
- Tests where the logic (not just data) varies
- Tests with extensive mocking that differs per case
- Integration tests with different workflow paths

## Step 3: Verify Changes

```bash
# Run the compacted tests
pytest path/to/test_file.py -v
```
