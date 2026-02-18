---
description: Refine python code after its written by AI
allowed-tools:
  - Bash(git diff*)
  - Bash(git status*)
  - Bash(ruff*)
  - Read
  - Edit
  - Grep
  - Glob
---

# Python Code Refinement

Refine AI-generated Python code by removing over-engineering, redundant comments, and applying style guidelines.

**IMPORTANT**: Only modify files within the scope of the current branch/ticket. Do not refactor or touch unrelated files. Git status should be clean with no untracked files or changes. If git workspace is dirty prompt the user to run the /hand-off command to clean the workspace.

## Step 1: Identify Files in Scope

```bash
# Get changed files in this branch vs target
git diff --name-only origin/main..HEAD | grep '\.py$'

# For uncommitted changes
git status --short | grep '\.py$'

# Full diff of MR changes
git diff origin/main..HEAD -- '*.py'
```

## Step 2: Refinement Checklist

1. **Remove redundant comments**: Delete any line comments that explain obvious behavior. Only keep comments for non-trivial operations like external constraints, hacky work-arounds, or complex algorithms. Leave docstrings in place.

2. **Organize imports**: Move all imports to the top level, grouped by: standard library, third-party, local imports.

3. **Simplify over-engineering**: Remove unnecessary abstractions, helper functions used once, or defensive code for scenarios that can't happen.

4. **Clean up type annotations**: Remove obvious type hints that don't add value (e.g., `x: int = 5`). Keep them for function signatures and non-obvious cases.

5. **Remove placeholder patterns**: Delete generic error messages like "TODO", "FIXME", or boilerplate exception handling that just re-raises.

6. **Run ruff for styling**: Don't manually fix style issues - use ruff:
   ```bash
   ruff check --fix path/to/file.py
   ruff format path/to/file.py
   ```

7. **Validate patterns**: Ensure pydantic models are used (not dataclasses), prefer CTEs in SQL queries, use appropriate data engineering patterns for Airflow/Snowflake/PySpark code.

8. **Simplify variable names**: Replace overly verbose names with concise, clear alternatives while maintaining readability.

9. **Remove unused arguments**: Identify and remove dangling function arguments. Note that some might be used by children implementations so testing is crucial.

## Example Workflow

```bash
# 1. Find changed Python files
git diff --name-only origin/main..HEAD | grep '\.py$'

# 2. Review each file
# Read and apply refinements

# 3. Run ruff
ruff check --fix .
ruff format .

# 4. Verify changes
git diff
```
