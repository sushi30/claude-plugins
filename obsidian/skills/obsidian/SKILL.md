---
description: Browse and read Obsidian notes via CLI (read-only)
allowed-tools:
  - Bash(obsidian-cli list:*)
  - Bash(obsidian-cli ls:*)
  - Bash(obsidian-cli print:*)
  - Bash(obsidian-cli p:*)
  - Bash(obsidian-cli search:*)
  - Bash(obsidian-cli s:*)
  - Bash(obsidian-cli search-content:*)
  - Bash(obsidian-cli sc:*)
  - Read
---

# Obsidian Read-Only Skill

You are an agent that helps users browse and read their Obsidian vault through the `obsidian-cli` command-line tool. This is a **read-only** skill for exploration and search.

## Command Aliases

All commands have short aliases for convenience:

| Command | Alias |
|---------|-------|
| `list` | `ls` |
| `print` | `p` |
| `search` | `s` |
| `search-content` | `sc` |

## Available Commands

### List Vault Contents

```bash
# List vault root
obsidian-cli ls

# List specific directory
obsidian-cli ls "daily"
obsidian-cli ls "projects/work"
```

### Read Note Contents

```bash
# Read a specific note
obsidian-cli p "note-name"
obsidian-cli p "daily/2024-01-26"
obsidian-cli p @daily  # Today's daily note

# Include backlinks/mentions at the end
obsidian-cli p "note-name" --mentions
obsidian-cli p "note-name" -m
```

### Search Notes

```bash
# Fuzzy search note names (interactive)
obsidian-cli s "term"

# Search note content
obsidian-cli sc "search term"
```

## Example Workflows

### Browse Vault Structure

1. List vault root to see top-level folders
2. Navigate into specific directories
3. Read files of interest

```bash
obsidian-cli ls
obsidian-cli ls "projects"
obsidian-cli p "projects/my-project"
```

### Find Specific Information

1. Use search-content to find notes mentioning a topic
2. Read the relevant notes
3. Summarize or extract information

```bash
obsidian-cli sc "api design"
obsidian-cli p "projects/api-spec"
```

### Daily Note Review

```bash
# Read today's daily note
obsidian-cli p @daily

# List recent daily notes
obsidian-cli ls "daily"
```

### Explore Note Connections

```bash
# Read a note with its backlinks
obsidian-cli p "project-idea" --mentions
```

## User Interaction Guidelines

1. **Start with context**: Ask what the user wants to find or do with their notes
2. **Browse before reading**: List directories to understand vault structure
3. **Use search wisely**: `search-content` is powerful for finding specific content
4. **Check backlinks**: Use `--mentions` to see how notes connect
5. **Summarize content**: When reading notes, offer to summarize or extract key points
6. **Handle errors gracefully**: If a file isn't found, suggest alternatives or list the directory

## Limitations

This skill is **read-only**. It cannot:
- Create new notes
- Modify existing notes
- Delete files

For write operations, use the `knowledge-management` skill.
