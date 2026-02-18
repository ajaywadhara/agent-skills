# Review Workflow - Git Operations

This reference provides guidance for gathering code changes across different review modes.

## Branch Detection Logic

```
1. Get current branch name
2. If on develop/main/master:
   → Ask user which feature branch to review
3. Else (on feature branch):
   → Auto-detect base branch in order:
      a. develop → GitFlow
      b. main → GitHub Flow  
      c. master → Legacy
   → If none found, ask user
4. Confirm: "Comparing {feature} against {base}"
```

## Commands by Agent

Different coding agents have different tools. Use the appropriate commands:

### Claude Code / Kilo
```bash
# Current state
git status --porcelain
git branch --show-current

# Branch comparison
git diff --name-only <base>..HEAD
git diff <base>..HEAD
git diff --stat <base>..HEAD

# Commit history
git log --oneline <base>..HEAD

# Specific commits
git diff HEAD~N..HEAD
git show <commit-hash>
```

### GitHub Copilot
Use built-in VS Code Git integration or terminal commands above.

### Other Agents
Adapt using available git/file tools.

## Common Branch Patterns

| Repository Type | Base Branch | Feature Pattern |
|-----------------|-------------|-----------------|
| GitFlow | `develop` | `feature/*`, `bugfix/*` |
| GitHub Flow | `main` | `feature/*`, `fix/*` |
| Legacy | `master` | Any |
| Trunk-based | `main`/`trunk` | Short-lived |

## Handling Mixed Changes

When user has both committed and uncommitted changes:

1. **Committed changes** (feature vs base): `git diff <base>..HEAD`
2. **Uncommitted changes**: `git diff`
3. **Staged only**: `git diff --cached`
4. **Combined view**: `git diff <base>`

## Report Naming Convention

| Mode | Filename Pattern |
|------|------------------|
| Local changes | `pr-report-local-{timestamp}.md` |
| Branch comparison | `pr-report-{feature}-vs-{base}-{timestamp}.md` |
| Specific commits | `pr-report-commits-{timestamp}.md` |

## Merge Base Detection

For accurate diff of diverged branches:

```bash
git merge-base <base> HEAD
git diff $(git merge-base <base> HEAD)..HEAD
```

This shows only changes since branches diverged, not all of base branch.