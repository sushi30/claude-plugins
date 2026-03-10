# claude-plugins

Personal plugin collection for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [OpenCode](https://opencode.ai). Skills, commands, and hooks for knowledge management, Python development, TDD, and GitLab workflows.

## Plugins

| Plugin | Description |
|---|---|
| **obsidian** | Obsidian integration — browse, search, daily notes, plan tracking, task management |
| **python** | Python dev workflows — code refinement and pytest compaction |
| **tdd** | Test-driven development — red/green/refactor with hypothesis-driven debugging |
| **gitlab-workflow** | Commit, push, and create GitLab merge requests in one step |

## Installation

```bash
git clone https://github.com/sushi30/claude-plugins.git
cd claude-plugins
```

### Claude Code

```bash
claude plugin marketplace add "$(pwd)/.claude-plugin/marketplace.json"
claude plugin install obsidian
claude plugin install python
claude plugin install tdd
claude plugin install gitlab-workflow
```

### OpenCode

#### Per-project install

Symlink (or copy) `.opencode/` into your target project:

```bash
ln -s "$(pwd)/.opencode" /path/to/your-project/.opencode
```

#### Global install

Make skills, commands, and plugins available across all projects:

```bash
mkdir -p ~/.config/opencode/skills ~/.config/opencode/commands ~/.config/opencode/plugins
ln -s "$(pwd)"/.opencode/skills/* ~/.config/opencode/skills/
ln -s "$(pwd)"/.opencode/commands/* ~/.config/opencode/commands/
ln -s "$(pwd)"/.opencode/plugins/* ~/.config/opencode/plugins/
```

OpenCode discovers them automatically on startup.

## Regenerating OpenCode artifacts

Claude Code is the source of truth. The `.opencode/` directory is generated from the Claude Code plugin structure using a Python converter:

```bash
cd deploy
uv sync
uv run deploy-opencode --source .. --output ../.opencode --clean
```

Options:

| Flag | Description |
|---|---|
| `--source PATH` | Repo root (default: `.`) |
| `--output PATH` | Output directory (default: `.opencode`) |
| `--dry-run` | Preview without writing |
| `--clean` | Remove output directory before generating |

### What gets converted

| Claude Code | OpenCode | Notes |
|---|---|---|
| `skills/*/SKILL.md` | `.opencode/skills/<name>/SKILL.md` | Frontmatter rewritten (`name` + `description`), `allowed-tools` dropped, body preserved |
| `commands/*.md` | `.opencode/commands/*.md` | Frontmatter rewritten (`description` only), `allowed-tools` dropped, body preserved |
| `hooks/hooks.json` | `.opencode/plugins/hooks.ts` | `Stop` → `session.idle`, `PreToolUse` → `tool.execute.before`, etc. |

## Prerequisites

- **obsidian-cli**: `brew install obsidian-cli` (for obsidian plugin)
- **glab**: GitLab CLI (for gitlab-workflow plugin)
- **ruff**: Python linter/formatter (for python plugin)
- **pytest**: Python test runner (for python and tdd plugins)

## Structure

```
claude-plugins/
├── .claude-plugin/marketplace.json   # Claude Code plugin registry
├── .opencode/                        # Generated OpenCode artifacts
│   ├── skills/                       #   6 skills
│   ├── commands/                     #   4 commands
│   └── plugins/hooks.ts             #   Event hooks
├── obsidian/                         # Obsidian plugin (Claude Code format)
├── python/                           # Python plugin (Claude Code format)
├── tdd/                              # TDD plugin (Claude Code format)
├── gitlab-workflow/                  # GitLab plugin (Claude Code format)
└── deploy/                           # Python converter tool
    ├── pyproject.toml
    ├── src/deploy_opencode/
    └── tests/
```
