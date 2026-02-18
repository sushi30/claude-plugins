# Obsidian CLI Skill

A Claude Code skill for interacting with Obsidian notes via the `obsidian-cli` command-line tool.

## Prerequisites

1. **Obsidian** installed
2. **obsidian-cli** installed (via `brew install obsidian-cli` or from [releases](https://github.com/Yakitrak/obsidian-cli))
3. A default vault configured (`obsidian-cli set-default <vault-name>`)

## Installation

The skill is located in `claude-plugins/skills/obsidian/` and includes:
- `skill.md` - Skill definition and instructions for Claude
- `README.md` - This file
- `INSTALL.md` - Installation guide

## Usage with Claude Code

The skill can be invoked when working with Obsidian notes. Claude will:
- Help you read and write notes
- Search your vault
- Manage daily notes
- Manage frontmatter metadata
- Move and rename notes (with link updates)

### Example Interactions

**Reading a note:**
```
User: Read my daily note for today
Claude: [Runs obsidian-cli print and displays the note]
```

**Searching notes:**
```
User: Find notes containing "project-alpha"
Claude: [Runs obsidian-cli search-content and lists results]
```

**Creating a note:**
```
User: Create a new meeting note for the Q1 planning meeting
Claude: [Runs obsidian-cli create with appropriate content]
```

**Appending to a note:**
```
User: Add a task "Review PR #123" to my Meeting Notes
Claude: [Runs obsidian-cli append to add the task]
```

## Command Reference

| Command | Description |
|---------|-------------|
| `print <note>` | Display note contents |
| `create <note> -c "content"` | Create a new note |
| `append <note> "content"` | Append to existing note |
| `delete <note>` | Delete a note |
| `move <old> <new>` | Move/rename note (updates links) |
| `list [path]` | List files in vault/directory |
| `search <term>` | Fuzzy search note names |
| `search-content <term>` | Search note contents |
| `frontmatter <note>` | View/edit frontmatter |
| `daily` | Open/create daily note |

## Troubleshooting

**Note not found:**
- Check the note name/path is correct
- Use `obsidian-cli list` to see available notes

**Vault not found:**
- Set a default vault: `obsidian-cli set-default <vault-name>`
- Or specify vault with `-v` flag: `obsidian-cli print "Note" -v "Vault Name"`

**Command not found:**
- Ensure obsidian-cli is installed and in your PATH
- Try: `brew install obsidian-cli`

## Links

- [obsidian-cli GitHub](https://github.com/Yakitrak/obsidian-cli)
- [Obsidian](https://obsidian.md/)
