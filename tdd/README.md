# TDD Plugin

Structured test-driven development workflow for Claude Code. Provides a hypothesis-driven red/green/refactor cycle with todo tracking.

## Skills

### `tdd`

Guides implementation using TDD: form a hypothesis, write a failing test, make it pass, refactor. Works with pytest (Python) and dbt test.

## Installation

### Step 1: Add the marketplace (first time only)

```bash
claude plugin marketplace add /path/to/claude-plugins/.claude-plugin/marketplace.json
```

### Step 2: Install the plugin

```bash
claude plugin install tdd
```

### Step 3: Verify installation

```bash
claude plugin list
```

## Prerequisites

- Python 3.x + [pytest](https://pytest.org) for Python projects
- `dwh-cli` + dbt for data warehouse projects

## Usage

Invoke via the skill system:

```
Use TDD to fix the bug in...
Implement this feature test-first...
Debug this using red/green/refactor...
```

Or reference it explicitly: `use the tdd skill to implement X`.
