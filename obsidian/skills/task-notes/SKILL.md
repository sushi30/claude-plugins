---
description: Manage tasks using Obsidian CLI with frontmatter-based metadata
allowed-tools:
  - Bash(obsidian-cli create:*)
  - Bash(obsidian-cli c:*)
  - Bash(obsidian-cli list:*)
  - Bash(obsidian-cli ls:*)
  - Bash(obsidian-cli print:*)
  - Bash(obsidian-cli p:*)
  - Bash(obsidian-cli frontmatter:*)
  - Bash(obsidian-cli fm:*)
  - Bash(obsidian-cli search-content:*)
  - Bash(obsidian-cli sc:*)
  - Bash(obsidian-cli delete:*)
  - Bash(obsidian-cli move:*)
  - Bash(date *)
  - Read
  - Grep
  - Glob
---

# Task Management with Obsidian Frontmatter

Manage tasks as Obsidian notes with YAML frontmatter metadata. Tasks are stored in the `Tasks/` directory and organized using frontmatter fields for status, project, tags, priority, and due dates.

## Overview

This skill uses the Obsidian CLI to manage tasks as markdown notes with structured frontmatter. Each task is a note with metadata stored in YAML frontmatter, making them fully compatible with Obsidian plugins and queries.

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

**List All Tasks:**
```bash
obsidian-cli ls "Tasks"
```

**List with Filtering (using grep/pattern matching):**
```bash
# List pending tasks
obsidian-cli ls "Tasks" | while read task; do
  status=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "status:" | cut -d: -f2 | xargs)
  [[ "$status" == "pending" ]] && echo "$task"
done

# List high priority tasks
obsidian-cli ls "Tasks" | while read task; do
  priority=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "priority:" | cut -d: -f2 | xargs)
  [[ "$priority" == "high" ]] && echo "$task"
done
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

**Search Task Content:**
```bash
# Search for tasks mentioning "authentication"
obsidian-cli sc "authentication" | grep "Tasks/"

# Search for JIRA ticket
obsidian-cli sc "JIRA-456" | grep "Tasks/"
```

**Find by Tag or Project:**
```bash
# Find all tasks (using standard task tag)
obsidian-cli ls "Tasks" | while read task; do
  tags=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep -A 10 "tags:")
  [[ "$tags" =~ "task" ]] && echo "$task"
done

# Find tasks with specific tag
obsidian-cli ls "Tasks" | while read task; do
  tags=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep -A 10 "tags:")
  [[ "$tags" =~ "urgent" ]] && echo "$task"
done

# Find tasks by project
obsidian-cli ls "Tasks" | while read task; do
  project=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "project:" | cut -d: -f2 | xargs)
  [[ "$project" == "jira-456" ]] && echo "$task"
done
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

Check tasks for the day:

```bash
# Find tasks due today
today=$(date +%Y-%m-%d)
obsidian-cli ls "Tasks" | while read task; do
  due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "due:" | cut -d: -f2 | xargs)
  [[ "$due" == "$today" ]] && echo "$task"
done

# Log to daily note
obsidian-cli a @daily "\n- $(date +%H:%M) Task review: X tasks pending, Y completed"
```

### Weekly Task Summary

```bash
# Count completed tasks this week
completed_count=0
obsidian-cli ls "Tasks" | while read task; do
  status=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "status:" | cut -d: -f2 | xargs)
  completed=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "completed:" | cut -d: -f2 | xargs)
  # Check if completed this week
  [[ "$status" == "completed" ]] && ((completed_count++))
done
echo "Completed tasks: $completed_count"
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

### List Tasks by Status

```bash
list_tasks_by_status() {
  local filter_status="$1"
  obsidian-cli ls "Tasks" | while read task; do
    status=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "status:" | cut -d: -f2 | xargs)
    if [[ "$status" == "$filter_status" ]]; then
      priority=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "priority:" | cut -d: -f2 | xargs)
      due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "due:" | cut -d: -f2 | xargs)
      echo "[$priority] $task ${due:+(due: $due)}"
    fi
  done
}

# Usage:
# list_tasks_by_status "pending"
# list_tasks_by_status "in-progress"
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

1. **No Complex Filtering**: Unlike TaskNotes CLI, filtering requires shell scripts
2. **Manual Tag Updates**: Updating frontmatter arrays requires careful editing
3. **No Built-in Stats**: Need custom scripts for project statistics
4. **File-based**: Each task is a separate file (can clutter vault)

## Advantages

1. **Native Obsidian**: Works with all Obsidian plugins (Dataview, Tasks, etc.)
2. **No HTTP API**: No dependency on running plugin servers
3. **Plain Markdown**: Tasks are readable, editable markdown files
4. **Version Control**: Easy to track in git with meaningful diffs
5. **Flexible Structure**: Can add custom frontmatter fields as needed
6. **Links Work**: Can use `[[wikilinks]]` to reference other notes
7. **Standard Tag**: All tasks have the `task` tag for easy filtering with Dataview queries (`FROM #task`)

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

# 2. Check pending tasks
list_tasks_by_status "pending"

# 3. Find overdue tasks
today=$(date +%Y-%m-%d)
obsidian-cli ls "Tasks" | while read task; do
  status=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "status:" | cut -d: -f2 | xargs)
  due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "due:" | cut -d: -f2 | xargs)
  if [[ "$status" != "completed" && "$due" < "$today" ]]; then
    echo "OVERDUE: $task (due: $due)"
  fi
done

# 4. Log task plan to daily
obsidian-cli a @daily "\n- $(date +%H:%M) Today's focus: Task A, Task B"
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

# 2. Update in-progress tasks
obsidian-cli fm "Tasks/refactor-database" --edit -k "status" --value "in-progress"

# 3. Log progress to daily
obsidian-cli a @daily "\n- $(date +%H:%M) Session end: Completed API, refactoring in progress"

# 4. Review tomorrow's tasks
tomorrow=$(date -v+1d +%Y-%m-%d)
obsidian-cli ls "Tasks" | while read task; do
  due=$(obsidian-cli fm "Tasks/$task" --print 2>/dev/null | grep "due:" | cut -d: -f2 | xargs)
  [[ "$due" == "$tomorrow" ]] && echo "Tomorrow: $task"
done
```
