# description: Generate Advanced Slides presentation from a GitLab MR

You are tasked with creating a presentation slide deck using the Obsidian Advanced Slides format from a GitLab merge request (MR).

## Instructions

1. **Fetch the MR details**: Use the GitLab MCP tools to retrieve information about the merge request, including:
   - MR title and description
   - Code changes (diffs)
   - Discussion threads and comments
   - Any related design decisions or technical context

2. **Analyze the MR**: Identify:
   - **Problem**: What issue or requirement does this MR address?
   - **Solution**: What approach was taken to solve it?
   - **Implementation**: Key code changes, architecture, and technical details
   - **Design Choices**: Important decisions made and trade-offs considered

3. **Generate the slide deck** following this structure:

```markdown
# [MR Title]

MR: [Link to MR]

note: Press 'S' to open speaker view during presentation

---

## Problem

- [Describe the problem or requirement]
- [Context and background]
- [Why this needed to be addressed]

note:
- Provide background on why this problem was important
- Share any metrics or user feedback that motivated this change
- Mention any related tickets or previous attempts

---

## Solution

- [High-level approach taken]
- [Key components or modules affected]
- [Overall strategy]

note:
- Explain why this solution was chosen over alternatives
- Mention any prototypes or spikes done
- Reference any architecture discussions

---

## Implementation

<!-- slide split -->

### Changes Overview

- [Summary of main changes]
- [Files modified/added]
- [Technical approach]

note:
- Walk through the main files changed
- Explain the scope of changes
- Highlight any migration steps needed

---

### Code Highlights

```[language]
[Key code snippet 1]
```

<!-- element class="code-highlight" -->

note:
- Explain what this code does line by line if needed
- Point out any clever solutions or patterns
- Mention performance implications

---

### Code Highlights (cont.)

```[language]
[Key code snippet 2]
```

<!-- element class="code-highlight" -->

note:
- Continue explaining key implementation details
- Highlight edge cases handled
- Discuss error handling approach

---

## Design Choices

- [Decision 1 and rationale]
- [Decision 2 and rationale]
- [Trade-offs considered]

note:
- Dive deeper into the reasoning behind choices
- Discuss what was considered but rejected
- Mention future considerations or tech debt

---

## Discussion Highlights

- [Key points from code review]
- [Important questions or concerns raised]
- [Resolutions or agreements]

note:
- Expand on interesting discussion threads
- Share learnings from code review
- Mention any follow-up items

---

## Summary

- [Brief recap of the changes]
- [Impact and benefits]
- [Next steps if applicable]

note:
- Recap key takeaways
- Mention rollout plan or monitoring approach
- Share links to related documentation
```

4. **Formatting guidelines**:
   - Use `---` to separate slides
   - Use appropriate heading levels (# for titles, ## for main sections)
   - Include code snippets with proper syntax highlighting
   - Use `<!-- slide split -->` for side-by-side content when appropriate
   - Keep bullet points concise and focused

5. **Speaker Notes**:
   - Add speaker notes using `note:` followed by the content
   - Speaker notes are visible in speaker view (press 'S' during presentation)
   - Use notes for additional context, talking points, or detailed explanations
   - Notes can be single line: `note: Brief reminder`
   - Or multi-line for detailed points:
     ```
     note:
     - Point 1
     - Point 2
     - Point 3
     ```
   - Include a reminder on the first slide that pressing 'S' opens speaker view

6. **Output**: Generate a complete markdown file ready to be used with Obsidian Advanced Slides.

## User Input Required

Please provide the GitLab MR URL or MR number (and project path if needed).
