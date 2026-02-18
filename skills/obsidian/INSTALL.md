# Obsidian Skill Installation Guide

## Prerequisites

1. **Obsidian** installed
2. **Claude Code** installed

## Step 1: Install obsidian-cli

### macOS (Homebrew)

```bash
brew install obsidian-cli
```

### Other platforms

Download from [GitHub releases](https://github.com/Yakitrak/obsidian-cli/releases) or build from source.

## Step 2: Set Default Vault

```bash
# List available vaults (Obsidian must have been opened at least once)
obsidian-cli print-default

# Set your default vault
obsidian-cli set-default "Your Vault Name"
```

## Step 3: Verify Installation

```bash
# Check default vault
obsidian-cli print-default

# List files in vault
obsidian-cli list

# Read a note
obsidian-cli print "Some Note"
```

## Step 4: Use with Claude Code

Simply ask Claude to help with your Obsidian notes:

- "Read my daily note for today"
- "Create a meeting note for the Q1 planning session"
- "Search for notes containing 'project-alpha'"
- "Add a task to my Meeting Notes"

## Troubleshooting

### Command not found

**Problem:** `obsidian-cli: command not found`
**Solution:** Install via brew or download from GitHub releases

### No vault found

**Problem:** "No default vault set"
**Solution:** Run `obsidian-cli set-default "Vault Name"`

### Note not found

**Problem:** Cannot find a specific note
**Solution:**
- Use `obsidian-cli list` to see available files
- Check the note path is correct (e.g., `folder/Note Name`)

## Uninstalling

```bash
# Remove via brew
brew uninstall obsidian-cli

# Or manually delete the skill
rm -rf claude-plugins/skills/obsidian
```

## Support

For issues with:
- **obsidian-cli**: https://github.com/Yakitrak/obsidian-cli/issues
- **Claude Code**: https://github.com/anthropics/claude-code/issues
