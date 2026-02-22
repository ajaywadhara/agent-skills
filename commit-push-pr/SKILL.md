---
name: commit-push-pr
description: "Commit, push, and optionally create a PR for changes. Use when user says: commit my changes, commit and push, push my code, create a PR, commit push pr, or any variation requesting to commit/push changes to git."
---

# Commit Push PR

## Workflow

### Step 1: Check Current Branch

Run: `git branch --show-current`

If branch is `main`, `master`, `develop`, or any protected branch:
1. Run `git branch -a` to list all branches
2. If a feature branch exists (typically named like `feature/*`, `feat/*`, `bugfix/*`, `fix/*`, or Jira ticket like `PROJ-123-description`):
   - Ask user: "I see you're on a protected branch. Switch to existing feature branch [branch-name]?"
   - If yes, run `git checkout <branch-name>`
3. If no feature branch exists:
   - Use question tool to ask user: "I see you're on a protected branch ([branch-name]). No feature branch detected. Do you want me to create a feature branch? If yes, what should I name it?"
   - Wait for user response
   - If user wants to create a branch:
     - Run `git checkout -b <branch-name>`
     - Continue to Step 2

### Step 2: Check for Changes

Run: `git status --porcelain`

If no changes (empty output):
- Inform user: "No changes to commit."
- Stop here.

### Step 3: Pre-commit Checks

Before staging, check for potential issues:
1. Run `git status` to see changed files
2. If any file matches `.env`, `credentials.json`, `secrets.json`, `*.pem`, `*.key`, or similar secret patterns:
   - Warn user: "I notice files that may contain secrets: [list them]. Should I exclude them from the commit?"
   - If user says yes, exclude them: `git add <files> --exclude=<secret-files>`
3. If project has lint/typecheck scripts (check package.json, Makefile, or similar):
   - Ask user: "I found lint/typecheck scripts. Run them before committing?"
   - If yes, run them and report results
   - If failures, ask user if they want to proceed anyway

### Step 4: Stage Changes

Run: `git add -A`

### Step 5: Generate Commit Message

Run: `git diff --staged --stat` to see what changed

Analyze changes and generate a good commit message following conventional commits:
- Format: `type(scope): description`
- Types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, `build`, `ci`
- Description should be concise (under 72 chars)
- If multiple file types changed, use `chore` or `feat` with scope

Examples based on file analysis:
- Only docs files → `docs: update README`
- Only code files → `feat: add new endpoint` or `fix: resolve null pointer`
- Mixed → `feat: implement user authentication`

### Step 6: Commit

Run: `git commit -m "<message>"`

### Step 7: Pull with Rebase

Run: `git pull --rebase origin <branch-name>`

If there are conflicts:
1. Inform user: "There are merge conflicts after pulling. Please resolve them."
2. After user resolves, run: `git add -A && git rebase --continue`
3. If rebase is complex, ask user for help

### Step 7: Push

Run: `git push -u origin <branch-name>`

### Step 8: Offer PR Creation (Optional)

After successful push, ask user: "Changes pushed to `<branch-name>`. Would you like me to create a pull request? If so, which base branch should I target?"
