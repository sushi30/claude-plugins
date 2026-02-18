---
description: Recall session work and log observations to the daily note
allowed-tools:
  - Bash(obsidian-cli print:*)
  - Bash(obsidian-cli p:*)
  - Bash(obsidian-cli append:*)
  - Bash(obsidian-cli a:*)
---

Recall the work done in this conversation and distill it into a daily note entry.

**Step 1** — Read the daily note to see what has already been logged today:

```bash
obsidian-cli p @daily
```

**Step 2** — Review the conversation history and extract observations in these categories:

**Automation & Efficiency** — Opportunities spotted where a manual, repetitive, or error-prone process could be automated or streamlined. Examples: a deployment step that could be a CI job, a repeated SQL pattern that should be a macro, a manual data check that could be a test.

**Quirky Behaviors** — Surprising, undocumented, or counterintuitive behaviors encountered in existing processes, tools, or systems. Examples: a dbt model that silently drops nulls, an Airflow task that retries on a non-retryable error, a Snowflake function that behaves differently than expected.

**Accomplishments** — Meaningful completions: merged MRs, resolved blockers, shipped features, or significant progress on a plan. Not routine steps, only milestones worth remembering.

**Step 3** — Skip empty categories. Only include a category if there is something genuine to note. Do not fabricate entries. If the session was purely exploratory with nothing notable, append a single summary line instead.

**Step 4** — Append to the daily note:

```bash
obsidian-cli a @daily "\n\n## Session Reflection ($(date +%H:%M))\n\n### Automation & Efficiency\n- ...\n\n### Quirky Behaviors\n- ...\n\n### Accomplishments\n- ..."
```

Omit empty sections. Keep bullets concise (one or two sentences). Reference ticket IDs, file paths, and plan names using `[[links]]` where relevant. Prefer specifics over generalities — "`dbt run` silently succeeds when the profile is missing" beats "found some issues with dbt".

**Step 5** — Print the updated daily note so the user can review:

```bash
obsidian-cli p @daily
```
