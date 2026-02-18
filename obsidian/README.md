# Obsidian Plugin

An Obsidian integration for Claude Code with knowledge management capabilities. Browse, read, search, and maintain persistent notes in your vault.

## Features

- **Read-only MCP Access**: Browse and search via MCP protocol
- **Knowledge Management**: Track complex plans and maintain daily notes
- **Task Management**: Create, organize, and track tasks with TaskNotes CLI
- **Proactive Logging**: Hook prompts agent to log significant decisions

## Installation

### Step 1: Add the marketplace (first time only)

```bash
claude plugin marketplace add /Users/iparan/projects/claude-plugins/.claude-plugin/marketplace.json
```

### Step 2: Install the plugin

```bash
claude plugin install obsidian
```

### Step 3: Verify installation

```bash
claude plugin list
```

### Updating

```bash
claude plugin update obsidian
```

## Prerequisites

1. **Obsidian** with **Local REST API** plugin installed and enabled
2. **obsidian-cli** installed: `brew install obsidian-cli`
3. Default vault configured: `obsidian-cli set-default "Vault Name"`
4. **TaskNotes** plugin installed and running with HTTP API enabled (for task management)
5. **tn CLI** installed: `npm install -g tasknotes-cli` (for task management)

### Environment Setup

```bash
# For MCP access (read-only browsing)
export OBSIDIAN_API_KEY='your-api-key-here'
```

## Skills

### obsidian.md (Read-Only)
Browse, read, and search via MCP tools:
- `list_files_in_vault` - List vault contents
- `list_files_in_dir` - List directory contents
- `get_file_contents` - Read note content
- `search` - Search across vault

### knowledge-management.md (Read-Write)
Persistent memory via obsidian-cli:
- **Daily Notes**: Timestamped logging of decisions, milestones, blockers
- **Plan Notes**: Structured tracking of multi-layer implementations
- **Proactive Logging**: Hook prompts logging after significant work

### task-notes.md (Task Management)
Manage tasks via tn CLI:
- `tn create` - Natural language task creation with NLP parsing
- `tn list` - List and filter tasks with advanced queries
- `tn complete` - Mark tasks complete or toggle status
- `tn search` - Search tasks by content
- `tn projects` - Project management and organization
- `tn update` - Modify task properties
- JSON output support for automation

## Commands

### /daily
Recall session work and log observations to the daily note. Extracts accomplishments, decisions, quirky behaviors, and automation opportunities from the conversation.

### /plan
Create a structured plan note in Obsidian from your ideas. Interactively gathers information about:
- Plan description and goals
- Category (Feature, Bug Fix, Refactor, etc.)
- Repository and tech stack
- JIRA ticket linkage
- Custom sections and structure

Creates a well-formatted plan note in `Plans/` with proper frontmatter (date, category, type, languages, tags, JIRA link) and opens it in Obsidian for editing.

### /tn
Create a task with guided prompts and context awareness. Automatically detects JIRA tickets and plan notes from context for smart tagging and project linking. Features:
- Interactive questionnaire for task details
- Natural language date parsing (tomorrow, friday, next week)
- Smart defaults based on context (JIRA tickets, plan notes, time of day)
- Project organization for complex work
- Optional plan note integration

## Usage Examples

**Browse vault**: "What's in my vault?"

**Read a note**: "Show me my daily note"

**Log a decision**: "Log that we chose JWT over sessions"

**Create a plan**: `/plan` or "Create a plan for adding user authentication"

**Review daily notes**: `/daily` or "Summarize today's work for my daily note"

**Create a task**: `/tn` or "Create a task to review MR with high priority"

**List tasks**: "Show me today's tasks" or "Show overdue tasks"

**Complete task**: "Mark task <id> as complete"

**Filter tasks**: "Show high priority tasks with urgent tag"

**Link to plan**: "Create task project for JIRA-123 plan" or "Link task to current plan"

## Hooks

The plugin includes a `Stop` hook that evaluates whether to prompt for daily note logging:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Evaluate if notes should be logged..."
      }]
    }]
  }
}
```

## Plugin Structure

```
obsidian/
├── .mcp.json                    # MCP server configuration
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── commands/
│   ├── daily.md                 # Daily note reflection command
│   ├── plan.md                  # Structured plan creation command
│   └── tn.md                    # Interactive task creation command
├── skills/
│   ├── obsidian/                # Read-only MCP skill
│   ├── knowledge-management/    # Read-write CLI skill
│   └── task-notes/              # Task management skill
├── hooks/
│   └── hooks.json               # Stop hook for note prompting
└── README.md
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MCP tools not showing | Check `OBSIDIAN_API_KEY`, restart Claude Code |
| obsidian-cli not found | `brew install obsidian-cli` |
| No default vault | `obsidian-cli set-default "Vault Name"` |
| Connection refused | Ensure Obsidian running with Local REST API |
| tn commands not working | Install: `npm install -g tasknotes-cli` |
| TaskNotes not responding | Enable HTTP API in TaskNotes plugin settings (localhost:8080) |
| tn config errors | Run: `tn config` to set up connection |

## Related

- [obsidian-cli](https://github.com/Yakitrak/obsidian-cli)
- [mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)
- [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)
