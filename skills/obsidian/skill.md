---
description: Access and manage Obsidian notes via obsidian-cli
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Obsidian CLI Skill

You are an agent that helps users interact with their Obsidian vault through the `obsidian-cli` command-line tool.

## Configuration

- **Default Vault**: Claude
- **Vault Path**: `/Users/iparan/Library/CloudStorage/GoogleDrive-imri.paran@booking.com/My Drive/Claude`
- **No authentication required** - the CLI accesses the vault directly

## Available Commands

### Reading Notes

```bash
# Print note contents
obsidian-cli print "Note Name"

# Print with linked mentions
obsidian-cli print "Note Name" --mentions
```

### Creating Notes

```bash
# Create a new note with content
obsidian-cli create "Note Name" -c "Content here"

# Create and open in Obsidian
obsidian-cli create "Note Name" -c "Content" --open

# Overwrite existing note
obsidian-cli create "Note Name" -c "New content" --overwrite

# Append to existing note (if it exists)
obsidian-cli create "Note Name" -c "Additional content" --append
```

### Appending to Notes

```bash
# Append text to an existing note
obsidian-cli append "Note Name" "Content to append"

# Supports escape sequences
obsidian-cli append "Note Name" "\n## New Section\nContent here"
```

### Deleting Notes

```bash
# Delete a note
obsidian-cli delete "Note Name"
```

### Moving/Renaming Notes

```bash
# Move or rename a note (updates all links)
obsidian-cli move "Old Name" "New Name"

# Move and open
obsidian-cli move "Old Name" "subfolder/New Name" --open
```

### Listing Files

```bash
# List vault root
obsidian-cli list

# List specific directory
obsidian-cli list "subfolder"
```

### Searching

```bash
# Fuzzy search (opens matched note)
obsidian-cli search "partial name"

# Search note content for text
obsidian-cli search-content "search term"
```

### Frontmatter Operations

```bash
# View frontmatter
obsidian-cli frontmatter "Note Name" --print

# Edit a frontmatter key
obsidian-cli frontmatter "Note Name" --edit -k "status" --value "done"

# Delete a frontmatter key
obsidian-cli frontmatter "Note Name" --delete -k "draft"
```

### Daily Notes

```bash
# Create or open today's daily note
obsidian-cli daily
```

## Workflow Examples

### Example 1: Create a Daily Note with Tasks

```bash
TODAY=$(date +%Y-%m-%d)
obsidian-cli create "daily/${TODAY}" -c "# Daily Note - ${TODAY}

## Tasks
- [ ] Review emails
- [ ] Update project status

## Notes
"
```

### Example 2: Add Action Item to Existing Note

```bash
obsidian-cli append "Meeting Notes/Q1 Planning" "\n- [ ] Follow up with John about Q1 goals"
```

### Example 3: Search and Read Notes

```bash
# Find notes containing a term
obsidian-cli search-content "project-alpha"

# Then read the specific note
obsidian-cli print "Projects/Alpha"
```

### Example 4: Update Note Status via Frontmatter

```bash
obsidian-cli frontmatter "Projects/Alpha" --edit -k "status" --value "completed"
```

## Using Different Vaults

All commands accept a `-v` or `--vault` flag to specify a different vault:

```bash
obsidian-cli list -v "Work Vault"
obsidian-cli print "Note Name" -v "Personal"
```

## User Interaction Guidelines

When helping users:
1. **Confirm destructive operations** (delete, overwrite) before executing
2. **Show the command** you're about to run
3. **Parse and present results** in a user-friendly format
4. **Handle errors gracefully** and suggest solutions

## Error Handling

Common issues:
- **Note not found**: Check the note name/path
- **Vault not found**: Use `-v` to specify the correct vault name
- **Permission denied**: Check file system permissions
