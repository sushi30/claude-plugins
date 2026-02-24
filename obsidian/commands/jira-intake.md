---
description: Create structured JIRA ticket draft from source material with automated research
allowed-tools:
  - Bash(obsidian-cli create:*)
  - Bash(obsidian-cli c:*)
  - Bash(obsidian-cli append:*)
  - Bash(obsidian-cli a:*)
  - Bash(obsidian-cli open:*)
  - Bash(obsidian-cli o:*)
  - Bash(obsidian-cli list:*)
  - Bash(obsidian-cli ls:*)
  - Bash(date *)
  - AskUserQuestion
  - mcp__Glean__search
  - mcp__Glean__read_document
  - mcp__sourcegraph__search_code
  - mcp__sourcegraph__get_file_content
  - Read
  - Glob
  - Grep
---

Create a comprehensive JIRA ticket draft in Obsidian from source material with automated repository discovery and implementation research.

**Step 1** — Gather information using AskUserQuestion:

Ask these questions sequentially:

1. **Source Material**: "Where is this coming from?"
   - Options: Let them provide URL (Slack, Google Doc, Confluence) or select "Verbal description"

2. **Project Key**: "Which JIRA project is this for?"
   - Options: INTERCOM, GRAPHAI, DWH, TRAVINTEL, or let them type custom

3. **Summary**: "Provide a brief ticket title (under 100 characters)"
   - Options: Let them type it

4. **Ticket Type**: "What type of ticket is this?"
   - Options: Task, Bug, Story, Epic
   - Default: Task

5. **Priority**: "What's the priority level?"
   - Options: High, Medium, Low
   - Default: Medium

6. **Labels**: "Any labels to add? (comma-separated)"
   - Options: Let them type (e.g., ci, de, data-engineering, workflow)
   - Note: Will auto-suggest after reading source material

7. **Repositories**: "Which GitLab repositories are involved?"
   - Options: Let them type repo names/URLs or select "Auto-detect"
   - Note: Will use Glean to discover if auto-detect selected

8. **Split Strategy**: "How should multiple repositories be handled?"
   - Options: Single ticket (all repos in one), Per-repo tickets (separate for each), Manual (ask me later)
   - Default: Single ticket
   - Note: Only ask if multiple repos detected

**Step 2** — Read and analyze source material:

If source material is a URL:
- Use `mcp__Glean__read_document` for Google Docs or Slack links
- Use `Read` tool for local files
- Extract key information:
  - Problem description
  - Impact/urgency statements
  - Repository mentions (gitlab.com URLs or repo names)
  - Suggested labels from keywords (ci, deployment, testing, etc.)
  - Team/person mentions

If source is verbal:
- Use user's summary as the problem description
- Prompt for impact and acceptance criteria separately

**Step 3** — Repository discovery (if auto-detect selected):

```bash
# Use Glean to find repository URLs
mcp__Glean__search
query: "${project_key} repository GitLab ${extracted_keywords}"
# Parse gitlab.com/booking-com/* URLs from results
# Present list to user for confirmation
```

**Step 4** — Research implementation approaches (for each repository):

Run these searches in parallel using Sourcegraph:

```bash
# CODEOWNERS pattern research
mcp__sourcegraph__search_code
query: "CODEOWNERS OR .gitlab/CODEOWNERS"
repo: "${repo_url}"

# CI/CD configuration research
mcp__sourcegraph__search_code
query: ".gitlab-ci.yml OR .github/workflows"
repo: "${repo_url}"

# Test structure research
mcp__sourcegraph__search_code
query: "test/ OR tests/ OR __tests__"
repo: "${repo_url}"
```

Use Glean to fetch README or documentation:
```bash
mcp__Glean__search
query: "${repo_name} README documentation setup"
```

Synthesize findings into implementation approach for each repo.

**Step 5** — Generate ticket(s):

### File Naming Convention
`JIRA Drafts/${YYYY-MM-DD}-${PROJECT}-${sanitized-title}.md`

Example: `JIRA Drafts/2026-02-24-INTERCOM-update-codeowners-validation.md`

For per-repo split: `JIRA Drafts/${YYYY-MM-DD}-${PROJECT}-${sanitized-title}-${repo-name}.md`

### Single Ticket Template

```bash
TICKET_DATE=$(date +%Y-%m-%d)
TICKET_TIME=$(date +%H:%M)
TICKET_FILENAME="JIRA Drafts/${TICKET_DATE}-${PROJECT_KEY}-${SANITIZED_TITLE}.md"

cat <<'EOF' | obsidian-cli c "${TICKET_FILENAME}"
---
type: jira-draft
status: draft
project: ${PROJECT_KEY}
ticket_type: ${TICKET_TYPE}
priority: ${PRIORITY}
labels: [${LABELS}]
repos:
  - name: ${REPO1_NAME}
    url: ${REPO1_URL}
  - name: ${REPO2_NAME}
    url: ${REPO2_URL}
created: ${TICKET_DATE}
source_material: ${SOURCE_URL_OR_VERBAL}
split_strategy: single
related_tickets: []
---

# ${TICKET_SUMMARY}

## The What

${PROBLEM_DESCRIPTION}

## The Impact & Urgency

**Cost of Not Fixing:**
${IMPACT_POINTS}

**Business Value:**
${BUSINESS_JUSTIFICATION}

## Acceptance Criteria

${ACCEPTANCE_CRITERIA_CHECKLIST}

## Implementation Approach

### Repository: ${REPO1_NAME}

**CODEOWNERS Pattern:**
${CODEOWNERS_FINDINGS}

**CI/CD Approach:**
${CI_CD_FINDINGS}

**Testing Strategy:**
${TEST_FINDINGS}

**Implementation Steps:**
1. ${STEP_1}
2. ${STEP_2}
3. ${STEP_3}

### Repository: ${REPO2_NAME}

[Repeat structure for each repository]

## Source Material

${SOURCE_LINK_OR_DESCRIPTION}

## Related Tickets

None

## Notes

Created via /jira-intake on ${TICKET_DATE} at ${TICKET_TIME}
EOF
```

### Per-Repo Split Template

For each repository, create a separate ticket with:
- Same frontmatter structure but `split_strategy: per-repo`
- `related_tickets` array listing other ticket names
- Focus "Implementation Approach" section on single repo
- Add cross-reference in body: "This ticket is part of a multi-repository effort. Related tickets: [[ticket1]], [[ticket2]]"

**Step 6** — Review and finalize:

1. Display summary:
```
Created ${TICKET_COUNT} JIRA draft ticket(s) for project ${PROJECT_KEY}:
- Ticket 1: ${FILENAME1}
- Ticket 2: ${FILENAME2}

Repositories researched:
- ${REPO1_NAME}: ${REPO1_URL}
- ${REPO2_NAME}: ${REPO2_URL}
```

2. Open first ticket in Obsidian:
```bash
obsidian-cli o "${FIRST_TICKET_PATH}"
```

3. Log to daily note:
```bash
obsidian-cli a @daily "\n- $(date +%H:%M) Created ${TICKET_COUNT} JIRA draft(s) for ${PROJECT_KEY}: [[${FIRST_TICKET_NAME}]]"
```

4. Print confirmation:
```
JIRA draft(s) created successfully. The first ticket is now open in Obsidian for review.
```

## Guidelines

1. **Sequential questions, not batch**: Ask one question at a time - easier for users to think through
2. **Auto-suggest intelligently**: After reading source material, suggest labels and repos based on content analysis
3. **Research thoroughly**: Don't skip Sourcegraph/Glean searches - they provide critical implementation context
4. **Handle missing data gracefully**: If research fails, add "TODO: Research implementation approach" placeholders
5. **Cross-link aggressively**: For per-repo split, ensure all related tickets reference each other in frontmatter and body
6. **Follow repo conventions**: Use research findings to suggest implementation approaches that match existing patterns
7. **Default to single ticket**: Unless user explicitly wants per-repo split, create one comprehensive ticket
8. **Preserve source context**: Always link back to original source material (Slack, Doc, etc.)

## Edge Case Handling

### Source Material Unreachable
- If Glean/WebFetch fails: "I couldn't access that URL. Would you like to provide a verbal description instead?"
- Fall back to asking for problem/impact/criteria separately

### No Repositories Found
- If Glean search returns empty: "I couldn't find any repositories. Please provide them manually."
- Allow user to type repo names or URLs directly

### Research Timeout/Failure
- If Sourcegraph fails: Generate ticket with skeleton implementation section
- Add note: "TODO: Research CODEOWNERS/CI/CD patterns for ${REPO_NAME}"
- Don't block ticket creation on research failures

### Unclear Split Strategy
- If user unsure: Default to single ticket
- Explain: "Single ticket covers all repos in one place. You can split later if needed."

### Multiple Repos, Different Implementation Approaches
- If repos have very different patterns (e.g., Bazel vs direct edit):
- Suggest per-repo split: "These repos have different approaches. Recommend separate tickets?"

## Template Variations by Ticket Type

### Task (Default)
Focus: What's being built, how, and why

### Bug
Emphasize:
- "The What" → Current broken behavior and expected behavior
- "The Impact & Urgency" → User impact, data quality issues, blocker status
- Add "Root Cause" subsection if known

### Story
Emphasize:
- "The What" → User story format ("As a [user], I want [goal], so that [benefit]")
- "Acceptance Criteria" → User-facing outcomes

### Epic
Emphasize:
- "The What" → High-level initiative and strategic goals
- Add "Scope" section with in-scope/out-of-scope boundaries
- Add "Success Metrics" section

## Examples

### Example 1: Single Repo Task

**Input:**
- Source: Slack thread about CODEOWNERS update
- Project: INTERCOM
- Repos: data-warehouse
- Type: Task

**Output:** One ticket with CODEOWNERS research, CI/CD validation approach, testing strategy

### Example 2: Multi-Repo Per-Repo Split

**Input:**
- Source: Google Doc describing workflow migration
- Project: DWH
- Repos: bkng-data, data-warehouse
- Type: Task
- Split: per-repo

**Output:** Two tickets, each focused on one repo, cross-linked via frontmatter and body

### Example 3: Bug Ticket

**Input:**
- Source: Verbal description of Airflow DAG failure
- Project: GRAPHAI
- Repos: ml-pipelines
- Type: Bug

**Output:** One ticket emphasizing root cause, impact on pipelines, and verification steps

## JIRA Template Reference

This command implements the team's standard JIRA ticket template:

**The What**: Current unsolved problem
- What is the issue?
- What problem are we solving?
- What are we being asked to do?

**The Impact & Urgency**: Cost of not fixing it
- What doesn't work as it should?
- What does it mean for the business?
- How does it link to strategic objectives?

**Acceptance Criteria**: Conditions for completion
- Specific, testable conditions
- When is the work "done"?
- What needs to be validated?

This structure ensures tickets are ready to implement with clear problem statements, business justification, and success criteria.
