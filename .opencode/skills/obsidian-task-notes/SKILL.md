---
name: obsidian-task-notes
description: Manage tasks using Obsidian CLI with frontmatter-based metadata
---

# Task Management with Obsidian Frontmatter

Manage tasks as Obsidian notes with YAML frontmatter metadata. Tasks are stored in the `Tasks/` directory and organized using frontmatter fields for status, project, tags, priority, and due dates.

## Overview

This skill uses the Obsidian CLI to manage tasks as markdown notes with structured frontmatter. Each task is a note with metadata stored in YAML frontmatter, making them fully compatible with Obsidian plugins and queries.

**Key Features:**
- **Frontmatter Filtering**: Native `--meta` support for efficient task queries
- **Progress Tracking**: Track tasks by status (pending, in-progress, completed)
- **Project Organization**: Filter and group tasks by project
- **Priority Management**: Filter by priority (low, medium, high, urgent)
- **Context Tagging**: Organize by context (work, home, backend, frontend)
- **Due Date Tracking**: Monitor deadlines and overdue tasks

## Quick Reference

**Common Commands:**

```bash
# List todos (pending tasks)
obsidian-cli ls "Tasks" --meta status=pending

# Track progress (in-progress tasks)
obsidian-cli ls "Tasks" --meta status=in-progress

# List by project
obsidian-cli ls "Tasks" --meta project=jira-456

# High priority todos
obsidian-cli ls "Tasks" --meta status=pending --meta priority=high

# Project progress
obsidian-cli ls "Tasks" --meta project=jira-456 --meta status=pending
obsidian-cli ls "Tasks" --meta project=jira-456 --meta status=in-progress

# Interactive search
obsidian-cli search --meta status=pending
obsidian-cli search --meta project=jira-456
```

**Task Format:**
```markdown
---
status: pending
priority: high
tags:
  - task
  - urgent
  - backend
project: jira-123
due: 2026-02-25
created: 2026-02-18
estimate: 120
context: work
---

# Fix authentication bug

## Description
Details about the task...
```

## Task Metadata Fields

### Frontmatter Fields

- **status** (required): `pending`, `in-progress`, `completed`
- **created** (auto): ISO date when task was created
- **tags** (required): Array of strings for categorization, always includes `task` as first tag
- **priority**: `low`, `medium`, `high`, `urgent`
- **project**: Project or plan name (links to `Plans/` notes)
- **context**: Context label (e.g., `work`, `home`, `backend`, `frontend`)
- **due**: ISO date when task is due
- **estimate**: Time estimate in minutes
- **completed**: ISO date when marked complete (auto-added)

## Core Commands

### Create Tasks

Create tasks using the obsidian CLI with piped content for clean multi-line formatting:

**Basic Task:**
```bash
cat <<EOF | obsidian-cli c "Tasks/fix-auth-bug"
---
status: pending
created: $(date +%Y-%m-%d)
tags:
  - task
  - bug
---

# Fix authentication bug

Need to resolve token validation issue.
EOF
```

**With Full Metadata:**
```bash
cat <<EOF | obsidian-cli c "Tasks/implement-feature-jira-456"
---
status: pending
priority: high
created: $(date +%Y-%m-%d)
due: 2026-02-25
project: jira-456
tags:
  - task
  - feature
  - jira-456
  - urgent
context: backend
estimate: 120
---

# Implement user authentication

## Description
Add JWT-based authentication to the API.

## Requirements
- JWT token generation
- Token validation middleware
- Refresh token flow
EOF
```

### List Tasks

The Obsidian CLI supports frontmatter filtering with `--meta` flags, making task queries simple and efficient.

**List All Tasks:**
```bash
obsidian-cli ls "Tasks"
```

**List by Status:**
```bash
# List pending tasks (todos)
obsidian-cli ls "Tasks" --meta status=pending

# List in-progress tasks
obsidian-cli ls "Tasks" --meta status=in-progress

# List completed tasks
obsidian-cli ls "Tasks" --meta status=completed
```

**List by Priority:**
```bash
# High priority tasks
obsidian-cli ls "Tasks" --meta priority=high

# Urgent tasks
obsidian-cli ls "Tasks" --meta priority=urgent
```

**List by Project:**
```bash
# All tasks for a specific project
obsidian-cli ls "Tasks" --meta project=jira-456

# All tasks for a project (alternative naming)
obsidian-cli ls "Tasks" --meta project=feature-auth
```

**Combined Filters:**
```bash
# Pending high-priority tasks
obsidian-cli ls "Tasks" --meta status=pending --meta priority=high

# In-progress tasks for specific project
obsidian-cli ls "Tasks" --meta status=in-progress --meta project=jira-456

# Urgent pending tasks
obsidian-cli ls "Tasks" --meta status=pending --meta priority=urgent
```

**View Task Details:**
```bash
# Read full task
obsidian-cli p "Tasks/task-name"

# View just frontmatter
obsidian-cli fm "Tasks/task-name" --print
```

### Update Tasks

**Update Status:**
```bash
# Start working on task
obsidian-cli fm "Tasks/task-name" --edit -k "status" --value "in-progress"

# Mark complete
obsidian-cli fm "Tasks/task-name" --edit -k "status" --value "completed"
obsidian-cli fm "Tasks/task-name" --edit -k "completed" --value "$(date +%Y-%m-%d)"
```

**Update Priority:**
```bash
obsidian-cli fm "Tasks/task-name" --edit -k "priority" --value "high"
```

**Update Due Date:**
```bash
obsidian-cli fm "Tasks/task-name" --edit -k "due" --value "2026-02-25"
```

**Add/Update Project:**
```bash
obsidian-cli fm "Tasks/task-name" --edit -k "project" --value "jira-123"
```

**Update Tags (requires reading and recreating):**
```bash
# Read current frontmatter, modify tags, recreate
# Note: This is more complex and should be done carefully
# Prefer to set tags during creation
```

### Search Tasks

The Obsidian CLI `search` command supports frontmatter filtering for interactive fuzzy search.

**Search with Status Filter:**
```bash
# Search pending tasks interactively
obsidian-cli search --meta status=pending

# Search in-progress tasks
obsidian-cli search --meta status=in-progress
```

**Search by Project:**
```bash
# Find tasks in specific project
obsidian-cli search --meta project=jira-456
```

**Search Task Content:**
```bash
# Search for tasks mentioning "authentication"
obsidian-cli sc "authentication" | grep "Tasks/"

# Search for JIRA ticket
obsidian-cli sc "JIRA-456" | grep "Tasks/"
```

**Combined Filters:**
```bash
# Search urgent pending tasks
obsidian-cli search --meta status=pending --meta priority=urgent

# Search tasks for project with specific context
obsidian-cli search --meta project=jira-456 --meta context=backend
```

## Progress Tracking & Todo Lists

### View Current Work (In Progress)

Track what you're actively working on:

```bash
# Show all in-progress tasks
obsidian-cli ls "Tasks" --meta status=in-progress

# In-progress tasks for specific project
obsidian-cli ls "Tasks" --meta status=in-progress --meta project=jira-456

# View details of in-progress tasks
obsidian-cli ls "Tasks" --meta status=in-progress | while read task; do
  echo "=== $task ==="
  obsidian-cli p "Tasks/$task"
  echo
done
```

### View Todos (Pending Tasks)

List all pending work that needs attention:

```bash
# All pending tasks
obsidian-cli ls "Tasks" --meta status=pending

# Pending tasks by priority
obsidian-cli ls "Tasks" --meta status=pending --meta priority=high
obsidian-cli ls "Tasks" --meta status=pending --meta priority=urgent

# Pending tasks for specific project
obsidian-cli ls "Tasks" --meta status=pending --meta project=jira-456

# Pending backend tasks
obsidian-cli ls "Tasks" --meta status=pending --meta context=backend
```

### Project Progress Overview

Track progress across a project:

```bash
# Function to show project progress
show_project_progress() {
  local project="$1"
  echo "=== Project: $project ==="
  echo
  echo "Pending:"
  obsidian-cli ls "Tasks" --meta project="$project" --meta status=pending | sed 's/^/  - /'
  echo
  echo "In Progress:"
  obsidian-cli ls "Tasks" --meta project="$project" --meta status=in-progress | sed 's/^/  - /'
  echo
  echo "Completed:"
  obsidian-cli ls "Tasks" --meta project="$project" --meta status=completed | sed 's/^/  - /'
}

# Usage:
# show_project_progress "jira-456"
```

### Count Tasks by Status

Quick statistics:

```bash
# Function to count tasks
count_tasks() {
  local project="${1:-}"

  if [[ -n "$project" ]]; then
    pending=$(obsidian-cli ls "Tasks" --meta project="$project" --meta status=pending 2>/dev/null | wc -l)
    in_progress=$(obsidian-cli ls "Tasks" --meta project="$project" --meta status=in-progress 2>/dev/null | wc -l)
    completed=$(obsidian-cli ls "Tasks" --meta project="$project" --meta status=completed 2>/dev/null | wc -l)
    echo "Project $project: $pending pending, $in_progress in progress, $completed completed"
  else
    pending=$(obsidian-cli ls "Tasks" --meta status=pending 2>/dev/null | wc -l)
    in_progress=$(obsidian-cli ls "Tasks" --meta status=in-progress 2>/dev/null | wc -l)
    completed=$(obsidian-cli ls "Tasks" --meta status=completed 2>/dev/null | wc -l)
    echo "All tasks: $pending pending, $in_progress in progress, $completed completed"
  fi
}

# Usage:
# count_tasks              # All tasks
# count_tasks "jira-456"   # Specific project
```

### List All Projects

Find all unique projects:

```bash
# Extract unique project values
obsidian-cli ls "Tasks" | while read task; do
  obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^project:" | cut -d: -f2 | xargs
done | sort -u | grep -v "^$"
```

### Delete Tasks

**Delete Completed Tasks:**
```bash
# Archive by moving to archive folder
obsidian-cli m "Tasks/task-name" "Archive/Tasks/task-name"

# Or permanently delete
obsidian-cli delete "Tasks/task-name"
```

## Task Naming Convention

**Recommended Pattern:**
- Use kebab-case for task file names
- Include ticket ID for traceability: `task-jira-456-implement-auth`
- Keep names concise but descriptive
- Examples:
  - `fix-auth-bug`
  - `implement-jira-456-user-auth`
  - `refactor-database-schema`
  - `write-api-docs`

## Integration Workflows

### Link to Plan Notes

Tasks should reference plan notes via the `project` field:

```bash
# Create task linked to plan
cat <<EOF | obsidian-cli c "Tasks/setup-database-jira-123"
---
status: pending
project: jira-123-feature
tags:
  - task
  - jira-123
  - database
context: backend
---

# Set up database schema

Part of [[Plans/jira-123-feature]] implementation.
EOF

# Reference in plan note
obsidian-cli a "Plans/jira-123-feature" "\n- [ ] [[Tasks/setup-database-jira-123]]"
```

### JIRA Ticket Tracking

Include JIRA ticket IDs in both filename and frontmatter tags:

```bash
cat <<EOF | obsidian-cli c "Tasks/implement-jira-456"
---
status: pending
tags:
  - task
  - jira-456
  - feature
project: jira-456
---

# Implement feature from JIRA-456

See: https://booking.atlassian.net/browse/JIRA-456
EOF
```

### Daily Task Review

Check tasks for the day using frontmatter filters:

```bash
# Find pending tasks (your current todos)
obsidian-cli ls "Tasks" --meta status=pending

# Find high-priority pending tasks
obsidian-cli ls "Tasks" --meta status=pending --meta priority=high

# Find tasks currently in progress
obsidian-cli ls "Tasks" --meta status=in-progress

# Log to daily note
obsidian-cli a @daily "\n- $(date +%H:%M) Task review: X tasks pending, Y in progress"
```

### Due Date Management

Track tasks with due dates (requires shell scripting since due date filtering isn't built-in):

```bash
# Find tasks due today
today=$(date +%Y-%m-%d)
obsidian-cli ls "Tasks" | while read task; do
  due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^due:" | cut -d: -f2 | xargs)
  status=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^status:" | cut -d: -f2 | xargs)
  if [[ "$due" == "$today" && "$status" != "completed" ]]; then
    priority=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^priority:" | cut -d: -f2 | xargs)
    echo "[$priority] $task"
  fi
done

# Find overdue tasks
today=$(date +%Y-%m-%d)
obsidian-cli ls "Tasks" | while read task; do
  due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^due:" | cut -d: -f2 | xargs)
  status=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^status:" | cut -d: -f2 | xargs)
  if [[ "$status" != "completed" && -n "$due" && "$due" < "$today" ]]; then
    echo "OVERDUE: $task (due: $due)"
  fi
done
```

### Weekly Task Summary

```bash
# Count completed tasks (simple)
obsidian-cli ls "Tasks" --meta status=completed | wc -l

# Show completed tasks
echo "Completed tasks:"
obsidian-cli ls "Tasks" --meta status=completed

# Show pending work
echo "Pending tasks:"
obsidian-cli ls "Tasks" --meta status=pending

# Show in-progress work
echo "In progress:"
obsidian-cli ls "Tasks" --meta status=in-progress

# Full summary
echo "=== Weekly Task Summary ==="
echo "Completed: $(obsidian-cli ls "Tasks" --meta status=completed 2>/dev/null | wc -l)"
echo "In Progress: $(obsidian-cli ls "Tasks" --meta status=in-progress 2>/dev/null | wc -l)"
echo "Pending: $(obsidian-cli ls "Tasks" --meta status=pending 2>/dev/null | wc -l)"
```

## Helper Scripts

### Quick Task Creation Function

For convenience, you can create wrapper functions:

```bash
create_task() {
  local name="$1"
  local description="$2"
  local priority="${3:-medium}"
  local project="${4:-}"

  cat <<EOF | obsidian-cli c "Tasks/$name"
---
status: pending
priority: $priority
created: $(date +%Y-%m-%d)
tags:
  - task
${project:+project: $project}
---

# $description
EOF
  echo "Created task: Tasks/$name"
}

# Usage:
# create_task "fix-bug" "Fix authentication bug" "high" "jira-123"
```

### List Tasks by Status (Simplified)

```bash
list_tasks_by_status() {
  local filter_status="$1"
  obsidian-cli ls "Tasks" --meta status="$filter_status"
}

# Usage:
# list_tasks_by_status "pending"
# list_tasks_by_status "in-progress"
# list_tasks_by_status "completed"
```

### List Tasks by Project

```bash
list_tasks_by_project() {
  local project="$1"
  echo "=== Tasks for project: $project ==="
  echo
  echo "Pending:"
  obsidian-cli ls "Tasks" --meta project="$project" --meta status=pending | sed 's/^/  /'
  echo
  echo "In Progress:"
  obsidian-cli ls "Tasks" --meta project="$project" --meta status=in-progress | sed 's/^/  /'
  echo
  echo "Completed:"
  obsidian-cli ls "Tasks" --meta project="$project" --meta status=completed | sed 's/^/  /'
}

# Usage:
# list_tasks_by_project "jira-456"
```

### Show Task Details with Metadata

```bash
show_task() {
  local task="$1"
  echo "=== $task ==="
  obsidian-cli fm "Tasks/$task" --print
  echo
  obsidian-cli p "Tasks/$task"
}

# Usage:
# show_task "implement-api"
```

### Complete Task with Timestamp

```bash
complete_task() {
  local task="$1"
  obsidian-cli fm "Tasks/$task" --edit -k "status" --value "completed"
  obsidian-cli fm "Tasks/$task" --edit -k "completed" --value "$(date +%Y-%m-%d)"
  echo "Completed: $task"
}

# Usage:
# complete_task "fix-auth-bug"
```

### Daily Dashboard

Show all relevant tasks for today:

```bash
daily_dashboard() {
  echo "=== Daily Task Dashboard ==="
  echo
  echo "In Progress ($(obsidian-cli ls "Tasks" --meta status=in-progress 2>/dev/null | wc -l)):"
  obsidian-cli ls "Tasks" --meta status=in-progress | sed 's/^/  /'
  echo
  echo "High Priority Pending ($(obsidian-cli ls "Tasks" --meta status=pending --meta priority=high 2>/dev/null | wc -l)):"
  obsidian-cli ls "Tasks" --meta status=pending --meta priority=high | sed 's/^/  /'
  echo
  echo "Urgent Pending ($(obsidian-cli ls "Tasks" --meta status=pending --meta priority=urgent 2>/dev/null | wc -l)):"
  obsidian-cli ls "Tasks" --meta status=pending --meta priority=urgent | sed 's/^/  /'
  echo
  echo "All Pending ($(obsidian-cli ls "Tasks" --meta status=pending 2>/dev/null | wc -l)):"
  obsidian-cli ls "Tasks" --meta status=pending | sed 's/^/  /'
}

# Usage:
# daily_dashboard
```

## Best Practices

1. **Consistent Naming**: Use kebab-case and include ticket IDs in filenames
2. **Set Metadata on Creation**: Add all relevant frontmatter when creating tasks
3. **Link to Plans**: Always set `project` field to link tasks to implementation plans
4. **Use Tags Wisely**: All tasks automatically include `task` tag; add ticket IDs, feature labels, and categorization
5. **Update Status**: Keep task status current (pending → in-progress → completed)
6. **Archive Completed**: Move finished tasks to `Archive/Tasks/` to keep workspace clean
7. **Review Daily**: Check `@daily` note and update task statuses
8. **Log to Daily**: Reference tasks in daily notes for context

## Task Queries with Dataview

If you have the Dataview plugin installed in Obsidian, you can query tasks:

```dataview
TABLE priority, status, due, project
FROM "Tasks"
WHERE contains(tags, "task") AND status = "pending"
SORT priority DESC, due ASC
```

```dataview
TABLE priority, status, due
FROM #task
WHERE status = "pending" AND due <= date(today) + dur(7 days)
SORT due ASC
```

```dataview
TASK
FROM "Tasks"
WHERE contains(tags, "jira-456")
```

## Limitations

1. **Manual Tag Updates**: Updating frontmatter arrays requires careful editing
2. **No Date Filtering**: Due date filtering requires shell scripts (not built into `--meta`)
3. **No Built-in Stats**: Need custom scripts for detailed project statistics
4. **File-based**: Each task is a separate file (can clutter vault)

## Advantages

1. **Native Obsidian**: Works with all Obsidian plugins (Dataview, Tasks, etc.)
2. **No HTTP API**: No dependency on running plugin servers
3. **Native Frontmatter Filtering**: Built-in `--meta` support for efficient queries
4. **Plain Markdown**: Tasks are readable, editable markdown files
5. **Version Control**: Easy to track in git with meaningful diffs
6. **Flexible Structure**: Can add custom frontmatter fields as needed
7. **Links Work**: Can use `[[wikilinks]]` to reference other notes
8. **Standard Tag**: All tasks have the `task` tag for easy filtering with Dataview queries (`FROM #task`)
9. **Fast Queries**: Filter by status, priority, project without complex scripting

## Migration from TaskNotes

If migrating from TaskNotes:

1. Export tasks to see current structure
2. Create script to convert to Obsidian format
3. Use frontmatter fields to match TaskNotes metadata
4. Update plan notes to link to new task locations

## Example Workflows

### Morning Routine

```bash
# 1. Create daily note
obsidian-cli daily

# 2. Show daily dashboard
echo "=== Today's Tasks ==="
echo
echo "In Progress:"
obsidian-cli ls "Tasks" --meta status=in-progress | sed 's/^/  - /'
echo
echo "High Priority:"
obsidian-cli ls "Tasks" --meta status=pending --meta priority=high | sed 's/^/  - /'
echo
echo "Urgent:"
obsidian-cli ls "Tasks" --meta status=pending --meta priority=urgent | sed 's/^/  - /'

# 3. Check for overdue tasks
echo
echo "Overdue Tasks:"
today=$(date +%Y-%m-%d)
obsidian-cli ls "Tasks" --meta status=pending | while read task; do
  due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "^due:" | cut -d: -f2 | xargs)
  if [[ -n "$due" && "$due" < "$today" ]]; then
    echo "  - $task (due: $due)"
  fi
done

# 4. Log task plan to daily
obsidian-cli a @daily "\n- $(date +%H:%M) Today's focus: [list key tasks]"
```

### Starting New Work

```bash
# 1. Create task for JIRA ticket
cat <<EOF | obsidian-cli c "Tasks/implement-jira-789-api"
---
status: pending
priority: high
created: $(date +%Y-%m-%d)
project: jira-789
tags:
  - task
  - jira-789
  - api
  - backend
context: backend
estimate: 180
---

# Implement API endpoints for JIRA-789

## Requirements
- POST /api/auth/login
- POST /api/auth/refresh
- GET /api/auth/me
EOF

# 2. Create plan if needed
obsidian-cli c "Plans/jira-789" -c "..."

# 3. Link task to plan
obsidian-cli a "Plans/jira-789" "\n- [ ] [[Tasks/implement-jira-789-api]]"

# 4. Start working
obsidian-cli fm "Tasks/implement-jira-789-api" --edit -k "status" --value "in-progress"

# 5. Log to daily
obsidian-cli a @daily "\n- $(date +%H:%M) Started JIRA-789: API implementation"
```

### End of Day Review

```bash
# 1. Complete finished tasks
complete_task "implement-jira-789-api"

# 2. Review what's still in progress
echo "Still in progress:"
obsidian-cli ls "Tasks" --meta status=in-progress

# 3. Log progress to daily
obsidian-cli a @daily "\n- $(date +%H:%M) Session end: Completed X tasks, Y in progress"

# 4. Check tomorrow's priorities
echo "High priority for tomorrow:"
obsidian-cli ls "Tasks" --meta status=pending --meta priority=high
obsidian-cli ls "Tasks" --meta status=pending --meta priority=urgent
```

### Project-Based Workflow

Working on a specific project:

```bash
# 1. View all project tasks
PROJECT="jira-456"

echo "=== Project $PROJECT Tasks ==="
echo
echo "Pending:"
obsidian-cli ls "Tasks" --meta project="$PROJECT" --meta status=pending
echo
echo "In Progress:"
obsidian-cli ls "Tasks" --meta project="$PROJECT" --meta status=in-progress
echo
echo "Completed:"
obsidian-cli ls "Tasks" --meta project="$PROJECT" --meta status=completed

# 2. Start working on a task
obsidian-cli fm "Tasks/implement-jira-456-api" --edit -k "status" --value "in-progress"

# 3. Track progress in daily note
obsidian-cli a @daily "\n- $(date +%H:%M) Working on $PROJECT"
```
