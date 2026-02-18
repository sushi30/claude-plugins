---
description: Persistent memory using Obsidian for tracking plans and daily notes
allowed-tools:
  - Bash(obsidian-cli append:*)
  - Bash(obsidian-cli a:*)
  - Bash(obsidian-cli create:*)
  - Bash(obsidian-cli c:*)
  - Bash(obsidian-cli print:*)
  - Bash(obsidian-cli p:*)
  - Bash(obsidian-cli frontmatter:*)
  - Bash(obsidian-cli fm:*)
  - Bash(obsidian-cli list:*)
  - Bash(obsidian-cli ls:*)
  - Bash(obsidian-cli open:*)
  - Bash(obsidian-cli o:*)
  - Bash(obsidian-cli move:*)
  - Bash(obsidian-cli m:*)
  - Bash(obsidian-cli delete:*)
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Knowledge Management Skill

You are an agent with persistent memory through Obsidian. Use this skill to track complex plans, log decisions, and maintain running notes.

## Command Aliases

All commands have short aliases for convenience:

| Command | Alias |
|---------|-------|
| `append` | `a` |
| `create` | `c` |
| `print` | `p` |
| `frontmatter` | `fm` |
| `list` | `ls` |
| `open` | `o` |
| `move` | `m` |
| `delete` | `d` |

## Core Behaviors

### 1. Proactive Logging
Log to the daily note when you:
- Start work on a new Jira ticket
- Make significant architectural decisions
- Complete implementation milestones
- Encounter blockers or change approach
- Finish a task or session

### 2. Plan Tracking
For complex multi-layer implementations, create and maintain plan notes.

## Commands

### Append (Simplified Syntax)

The `append` command now supports escape sequences directly:

```bash
# Basic append with newline
obsidian-cli a @daily "\n- $(date +%H:%M) Your note here"

# Multi-line content
obsidian-cli a "Plans/my-plan" "\n\n## New Section\nContent here"

# Tabs work too
obsidian-cli a "note" "\n- Item\n\t- Sub-item"
```

### Daily Note Operations

```bash
# Ensure today's daily note exists and open it
obsidian-cli daily

# Append a timestamped bullet to daily note
obsidian-cli a @daily "\n- $(date +%H:%M) Your note here"

# Print today's daily note
obsidian-cli p @daily

# Print with backlinks
obsidian-cli p @daily --mentions
```

### Open Notes

```bash
# Open a note
obsidian-cli o "note-name"

# Open at a specific section/heading
obsidian-cli o "Plans/my-plan" --section "Decision Log"
obsidian-cli o "Plans/my-plan" -s "Blockers"

# Create note if it doesn't exist
obsidian-cli o "new-note" --create-if-not-exist
```

### Plan Operations

```bash
# Create a new plan
obsidian-cli c "Plans/plan-name" -c "---
status: active
ticket: https://booking.atlassian.net/browse/JIRA-123
created: $(date +%Y-%m-%d)
updated: $(date +%Y-%m-%d)
---

# Plan: Title

## Overview
Description here

## Implementation Layers

### Layer 1: Name
- [ ] Task 1
- [ ] Task 2

## Blockers
- None

## Decision Log
- $(date +%Y-%m-%d): Initial plan created
"

# Update plan status via frontmatter
obsidian-cli fm "Plans/plan-name" --edit -k "status" --value "completed"
obsidian-cli fm "Plans/plan-name" --edit -k "updated" --value "$(date +%Y-%m-%d)"

# View frontmatter
obsidian-cli fm "Plans/plan-name" --print

# Delete a frontmatter key
obsidian-cli fm "Plans/plan-name" --delete -k "draft"

# Append to decision log
obsidian-cli a "Plans/plan-name" "\n- $(date +%Y-%m-%d): Decision made"

# List all plans
obsidian-cli ls "Plans"

# Read a plan
obsidian-cli p "Plans/plan-name"
```

### Move and Rename Notes

```bash
# Move a note (updates all links automatically)
obsidian-cli m "old-path/note" "new-path/note"

# Open the note after moving
obsidian-cli m "old-name" "new-name" --open
```

### Stdin/Piped Content

Create or update notes using piped content instead of the `-c` flag:

```bash
# Pipe string content
echo "Hello World" | obsidian-cli c "note"

# Pipe file contents
cat document.txt | obsidian-cli c "imported-doc"

# Pipe command output
git log --oneline -10 | obsidian-cli c "git-log"

# Combine with other tools
curl -s https://api.example.com/data | jq '.results' | obsidian-cli c "api-response"

# Useful for multi-line content without escape sequences
cat <<'EOF' | obsidian-cli c "Plans/new-plan"
---
status: active
---

# Plan Title

## Overview
Content here
EOF
```

### In-place Text Replacement

Use sed with print/create --overwrite for text replacement:

```bash
# Replace first occurrence of "old" with "new"
obsidian-cli c "note" --overwrite -c "$(obsidian-cli p "note" | sed 's/old/new/')"

# Replace all occurrences (global)
obsidian-cli c "note" --overwrite -c "$(obsidian-cli p "note" | sed 's/old/new/g')"
```

## Templates

### Daily Note Entry Types

```bash
# Starting work
obsidian-cli a @daily "\n- $(date +%H:%M) Started work on JIRA-123: Brief description"

# Decision made
obsidian-cli a @daily "\n- $(date +%H:%M) Decision: Chose X over Y because Z"

# Milestone completed
obsidian-cli a @daily "\n- $(date +%H:%M) Completed: Layer 1 of plan-name"

# Blocker encountered
obsidian-cli a @daily "\n- $(date +%H:%M) Blocker: Waiting on X, switching to Y"

# Session end
obsidian-cli a @daily "\n- $(date +%H:%M) Session end: Summary of progress"
```

### Plan Note Structure

Plans should have:
- **Frontmatter**: status, ticket link, dates
- **Overview**: Brief description of what's being built
- **Implementation Layers**: Ordered phases with checkboxes
- **Blockers**: Current impediments
- **Decision Log**: Chronological record of key decisions

Plan statuses:
- `active` - Currently being worked on
- `completed` - All layers done
- `blocked` - Waiting on external dependency
- `abandoned` - No longer pursuing

## Workflow Example

**Starting a new ticket:**
```bash
# Log to daily note
obsidian-cli a @daily "\n- $(date +%H:%M) Started JIRA-123: Add user authentication"

# Create plan if complex
obsidian-cli c "Plans/jira-123-auth" -c "..."
```

**During work:**
```bash
# Log significant decisions
obsidian-cli a @daily "\n- $(date +%H:%M) Decision: Using JWT over sessions for stateless auth"

# Update plan progress
obsidian-cli a "Plans/jira-123-auth" "\n- $(date +%Y-%m-%d): Completed Layer 1 (database schema)"

# Jump to specific section for reference
obsidian-cli o "Plans/jira-123-auth" -s "Decision Log"
```

**Finishing work:**
```bash
# Mark plan complete
obsidian-cli fm "Plans/jira-123-auth" --edit -k "status" --value "completed"

# Log session end
obsidian-cli a @daily "\n- $(date +%H:%M) Completed JIRA-123, MR !456 ready for review"
```

## Guidelines

1. **Be concise**: Daily bullets should be scannable
2. **Include context**: Reference ticket IDs and plan names
3. **Log decisions**: Capture the "why" not just the "what"
4. **Update plans**: Keep status and decision log current
5. **Link notes**: Use `[[Plan Name]]` to link between notes
6. **Use sections**: Jump to specific headings with `--section` for quick navigation
