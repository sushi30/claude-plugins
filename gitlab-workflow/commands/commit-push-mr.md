---
description: Commit, push, and open a GitLab merge request
allowed-tools:
  - Bash(git checkout:*)
  - Bash(git add:*)
  - Bash(git status:*)
  - Bash(git push:*)
  - Bash(git commit:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(glab mr create:*)
  - Bash(glab mr view:*)
  - Bash(open:*)
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Your task

Based on the above changes:

1. If on `main` or `master`, create a new descriptive branch and switch to it
2. Stage relevant files and create a single commit with a clear message following the style of recent commits
3. Push the branch to origin with upstream tracking (`-u`)
4. Create a merge request using `glab mr create` with a descriptive title and body
5. Open the MR URL in the browser with `open <url>`

Use a HEREDOC for the commit message and MR body to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
commit message here
EOF
)"
```

```bash
glab mr create --fill --title "title" --description "$(cat <<'EOF'
## Summary
- change 1
- change 2
EOF
)"
```

You MUST do all of the above in a single message. Do not use any other tools or do anything else.
