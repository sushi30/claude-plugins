# Python Plugin

Python development workflows for code refinement and test optimization.

## Skills

### `/refine`

Refine AI-generated Python code by removing over-engineering, redundant comments, and applying style guidelines. Works on files changed in the current branch.

### `/compact-pytest [filepath]`

Compact repetitive test patterns using pytest parametrization. Optionally specify a filepath to target a specific test file.

## Prerequisites

- Python 3.x
- [ruff](https://docs.astral.sh/ruff/) - `pip install ruff` or `uv pip install ruff`
- pytest - `pip install pytest`

## Installation

```bash
claude plugin install python --source /path/to/claude-plugins
```

## Usage

```bash
# Refine code in current branch
/refine

# Compact tests in a specific file
/compact-pytest tests/test_module.py

# Compact all test files in current branch
/compact-pytest
```
