---
description: Create a structured plan in Obsidian from user's ideas
allowed-tools:
  - Bash(obsidian-cli create:*)
  - Bash(obsidian-cli c:*)
  - Bash(obsidian-cli append:*)
  - Bash(obsidian-cli a:*)
  - Bash(obsidian-cli print:*)
  - Bash(obsidian-cli p:*)
  - Bash(obsidian-cli list:*)
  - Bash(obsidian-cli ls:*)
  - Bash(obsidian-cli open:*)
  - Bash(obsidian-cli o:*)
  - Bash(date *)
  - AskUserQuestion
  - Read
  - Glob
  - Grep
---

Create a structured plan note in Obsidian from the user's ideas.

**Step 1** — Gather information from the user using AskUserQuestion:

Ask these questions:
1. **Plan Description (Summary)**: "What is the plan about? Provide a brief description of what is being built/fixed/changed."
   - Options: Let them type it

2. **Plan Objective**: "What is the objective? What needs to be accomplished and why?"
   - Options: Let them type it

3. **Category**: "What category best describes this plan?"
   - Options: Feature, Bug Fix, Refactor, Infrastructure, Documentation, Research, Investigation

4. **Repository**: "Which repository or project is this for?" (optional)
   - Options: data-warehouse, bkng-data, bdx-dwh-utils, claude-plugins, or custom

5. **Tech Stack**: "What languages or technologies are involved?" (multi-select)
   - Options: Python, SQL, dbt, Airflow, Bash, TypeScript, Snowflake

6. **JIRA Ticket**: "Is there a JIRA ticket associated with this plan?" (optional)
   - Options: Yes (they'll provide the key), No

**Step 2** — Generate the plan name:

Create a descriptive plan name based on the description. Format: `{Brief Title} - {Month} {Day}, {Year} {Time}`. For example: "Add User Authentication - Feb 12, 2026 2-30pm"

**Step 3** — Extract additional metadata:

- If JIRA ticket provided, construct URL: `https://booking.atlassian.net/browse/{TICKET_KEY}`
- Generate tags from: category, repository, tech stack (lowercase, hyphenated)
- Get current ISO timestamp for `created` field

**Step 4** — Ask for plan structure:

Ask the user: "What additional sections should the plan include?"
- Note: Summary and Objective are mandatory and will always be the first two sections
- Default options: Context/Background, Implementation Steps, Files to Modify, Technology Stack, Risk, Complexity, Questions, Blockers, Decision Log, Testing Strategy, Root Cause Analysis (for bugs), Migration Strategy (for refactors)
- Let them select multiple or provide custom sections

**Step 5** — Create the plan note:

Use obsidian-cli to create the plan with this structure:

```bash
cat <<'EOF' | obsidian-cli c "Plans/{plan-name}"
---
created: {ISO_TIMESTAMP}
date: {YYYY-MM-DD}
category: {category}
type: plan
repository: {repository}
jira: {JIRA_URL}
languages: [{lang1}, {lang2}, ...]
tags: [{tag1}, {tag2}, ...]
status: draft
---

# Plan: {Title}

## Summary
{Brief description from user - what is being built/fixed/changed}

## Objective
{What needs to be accomplished and why - the goal and desired outcome}

## Context
{Background information, motivation, and relevant history}

## Technology Stack
{Technologies, frameworks, and tools involved}

## Complexity
**Estimated Complexity**: Low/Medium/High
{Factors contributing to complexity}

## Questions
{Open questions that need answers before proceeding}
- Question 1?
- Question 2?

## Implementation Steps

### Step 1: {Phase name}
- [ ] Task 1
- [ ] Task 2

### Step 2: {Phase name}
- [ ] Task 1

## Files to Modify
{If applicable, list files}

## Risk
**Risk Level**: Low/Medium/High
{Potential risks and mitigation strategies}
- Risk 1: {Description} - Mitigation: {Strategy}
- Risk 2: {Description} - Mitigation: {Strategy}

## Blockers
- None currently

## Decision Log
- {YYYY-MM-DD}: Plan created

## Notes
{Any additional notes}
EOF
```

**Step 6** — Open the plan for editing:

```bash
obsidian-cli o "Plans/{plan-name}"
```

**Step 7** — Log to daily note:

```bash
obsidian-cli a @daily "\n- $(date +%H:%M) Created plan: [[Plans/{plan-name}]]"
```

**Step 8** — Print confirmation:

Tell the user: "Plan created at `Plans/{plan-name}`. The note is now open in Obsidian for you to fill in the details."

## Guidelines

1. **Mandatory structure**: EVERY plan MUST start with Summary and Objective as the first two sections
   - **Summary**: Brief description of what is being built/fixed/changed
   - **Objective**: Clear statement of what needs to be accomplished and why
2. **Be conversational**: Ask follow-up questions to understand the user's vision
3. **Keep it flexible**: Not all fields need to be filled initially - the user can elaborate after creation
4. **Suggest structure**: Based on the category, suggest relevant additional sections
   - **Technology Stack**: Always useful for understanding dependencies and tools
   - **Complexity**: Helps set expectations (Low/Medium/High with reasoning)
   - **Questions**: Critical for identifying unknowns before starting
   - **Risk**: Important for features, refactors, and infrastructure changes
   - **Testing Strategy**: Essential for features and bug fixes
   - **Root Cause Analysis**: Key for bug fixes
5. **Link to context**: If JIRA ticket exists, include it in frontmatter and mention in summary
6. **Use checkboxes**: For implementation steps, use `- [ ]` format for tasks
7. **Status progression**: Plans start as `draft`, then move to `active` → `completed`/`blocked`/`abandoned`
8. **Assess complexity**: Consider factors like:
   - Number of files/systems involved
   - External dependencies
   - Data migration requirements
   - Testing complexity
9. **Identify risks early**: Document potential issues and mitigation strategies upfront

## Examples

**Note**: All plans MUST start with Summary and Objective as the first two sections.

### Feature Plan
- Required: Summary, Objective
- Include: Context, Technology Stack, Complexity, Implementation Steps, Files to Modify, Risk, Testing Strategy, Decision Log
- Focus on: What's being built, technology choices, complexity drivers, and rollout risks

### Bug Fix Plan
- Required: Summary, Objective
- Include: Symptoms, Root Cause Analysis, Fix Strategy, Complexity, Files to Modify, Risk, Testing Strategy, Verification Steps
- Focus on: Understanding the bug, complexity of the fix, risk of regression

### Research Plan
- Required: Summary, Objective
- Include: Questions, Approach, Technology Stack, Complexity, Findings, Risk, Next Steps, Resources
- Focus on: Questions to answer, investigation approach, complexity of analysis

### Refactor Plan
- Required: Summary, Objective
- Include: Current State, Target State, Technology Stack, Complexity, Migration Strategy, Risk, Files to Modify, Testing Strategy
- Focus on: What's changing and why, migration complexity, risk mitigation

### Infrastructure Plan
- Required: Summary, Objective
- Include: Context, Technology Stack, Complexity, Implementation Steps, Risk, Rollback Strategy, Monitoring
- Focus on: Infrastructure changes, deployment complexity, operational risks, rollback plans
