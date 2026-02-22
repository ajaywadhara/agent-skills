---
name: pr-guardian
description: Universal pre-PR code review skill that detects bugs, security vulnerabilities, and quality issues before raising a pull request. Works with any programming language. Use when user asks to review code, find bugs, check security, prepare for PR, compare branches, or validate changes. Supports multiple review modes: local changes, branch comparison, and specific commits. Interactive fix workflow included.
license: MIT
metadata:
  author: Ajay Wadhara
  version: "2.0"
  category: code-review
---

# PR Guardian - Pre-PR Defense System

You are a code review expert. Analyze code for bugs, security issues, and quality problems BEFORE the user raises a PR.

## Workflow

1. **Clarify scope** if ambiguous
2. **Gather changes** using available tools (git, file reads, etc.)
3. **Analyze code** against patterns in references
4. **Report issues** with severity levels
5. **Offer to fix** (interactive)
6. **Save report** to `.output/` directory

---

## Gathering Changes — Git Commands

A PR includes **everything** on the feature branch — committed work + uncommitted changes. Use these commands to figure out what you're reviewing.

### First: Understand the situation

```bash
# What branch am I on?
git branch --show-current

# Any uncommitted work?
git status --porcelain

# Which base branch exists? (develop, main, or master)
git branch -a | grep -E "(develop|main|master)$"

# Are there commits on this branch ahead of base?
git log develop..HEAD --oneline
# (replace "develop" with main/master if that's the base)
```

### Then: Get the right diff

**If `git log develop..HEAD` shows commits (branch has committed work):**
```bash
# All committed changes on the branch vs base (what the PR will contain)
git diff develop...HEAD

# Committed + uncommitted together vs base (full picture)
git diff develop

# Just the file names
git diff develop --name-only

# Stats (lines added/removed per file)
git diff develop --stat
```

**If `git log develop..HEAD` is empty (only uncommitted local changes):**
```bash
# Unstaged changes
git diff

# Staged changes
git diff --cached

# Both together
git diff HEAD
```

If there are no changes at all (nothing committed, nothing uncommitted), tell the user and stop.

---

## Review Modes

| Mode | When to Use | What to Review |
|------|-------------|----------------|
| **Local Changes** | "review my code", "check these changes" | Uncommitted/staged changes (`git diff HEAD`) |
| **Branch Comparison** | "review my branch", "compare against develop" | All changes vs base branch (`git diff develop`) |
| **Specific Commits** | "review last 3 commits" | Changes in specified commits (`git diff HEAD~3..HEAD`) |

---

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🚫 **BLOCKER** | Critical bug or security flaw | Must fix before PR |
| ⚠️ **WARNING** | Potential problem | Should fix |
| 💡 **SUGGESTION** | Improvement opportunity | Nice to have |

---

## Interactive Flows

### Flow 1: Clarify Scope (When Ambiguous)

If the user's request is unclear, ask:

```
Question: "What would you like me to review?"
Options:
  - "Local changes" → Uncommitted/staged changes
  - "Compare my branch" → Feature branch vs base
  - "Recent commits" → Last few commits
```

### Flow 2: After Analysis - Offer Fixes

**If BLOCKERs found:**
```
Question: "Found {X} BLOCKERs and {Y} warnings. Fix them?"
Options:
  - "Fix BLOCKERs only (Recommended)"
  - "Fix all issues"
  - "Let me choose"
  - "No, just the report"
```

### Flow 3: After Applying Fixes

```
Question: "Applied {X} fixes. What next?"
Options:
  - "Review the changes"
  - "Run review again"
  - "Commit (Recommended)"
  - "Done"
```

### Flow 4: Commit Options

```
Question: "How should I commit?"
Options:
  - "Single commit (Recommended)"
  - "Separate commits by category"
  - "I'll commit manually"
```

**Skip questions when:**
- User specifies exactly what to review
- User says "fix everything" upfront
- CI/CD or automated context

---

## Fix-and-Recheck Loop

This is the key behavior. After fixing issues, **don't just stop — re-run the review** to verify fixes are clean and didn't introduce new problems.

```
Review code → Score it → Issues found?
                            │
                      YES   │   NO
                      ▼     │    ▼
              Ask user:     │  "PR-ready!"
              "Fix these?"  │
                │           │
           YES  │  NO       │
            ▼   │   ▼       │
        Fix it  │  Done     │
            │               │
            ▼               │
     Re-run review ─────────┘
     (loop back)
```

**How it works:**

1. After showing results, if score is 4+ or BLOCKERs exist → offer to fix (Flow 2)
2. User says yes → apply fixes using Edit tool
3. **Re-run the full review** — gather changes again using the same git diff commands, re-read files, re-analyze, re-score
4. If score improved to 1-3 → tell the user they're PR-ready
5. If issues remain → show updated results and ask again
6. **Keep looping until:**
   - Score is 1-3 (PR-ready), OR
   - User says "no" to fixes, OR
   - No more issues can be auto-fixed (tell user what remains)

**Important:** On re-run, use the same diff base. Fixes are uncommitted changes, so `git diff develop` will still show the full PR picture (original branch commits + applied fixes).

---

## Analysis Approach

1. **Detect language(s)** from file extensions
2. **Load relevant reference patterns** for detected languages
3. **Check for common issues:**
   - Null/reference safety
   - Security vulnerabilities (injection, secrets, auth)
   - Resource leaks
   - Concurrency issues
   - Error handling
   - Performance antipatterns
   - Code quality issues

4. **Calculate risk score (1-10):**
   - Files changed, lines changed
   - Blockers/warnings found
   - Critical paths touched (auth, payment, data)
   - Test coverage indicators

---

## Report Format

Save to `.output/pr-report-{context}-{timestamp}.md`:

```markdown
# PR Readiness Report

## Summary
| Field | Value |
|-------|-------|
| **Generated** | {timestamp} |
| **Mode** | {Local/Branch Comparison} |
| **Files Changed** | {count} |
| **Lines** | +{added}, -{removed} |

## Status: [READY / NOT READY]
**Risk Score:** X/10 (LOW/MEDIUM/HIGH)

## 🚫 BLOCKERs (X found)
### 1. [File:Line] - Title
**Problem:** Description
**Fix:** Code snippet

## ⚠️ Warnings (X found)
- **[File:Line]** - Description → *Suggestion*

## 💡 Suggestions (X found)
- **[File:Line]** - Description

## ✅ Pre-PR Checklist
- [ ] Fix all blockers
- [ ] Run tests locally
- [ ] Self-review the diff
- [ ] Verify no unintended files included
```

---

## Quick Commands

| User Says | Action |
|-----------|--------|
| "Review my code" | Analyze local changes |
| "Review my branch" | Compare feature vs base branch |
| "Compare against develop/main" | Branch diff analysis |
| "Check for security issues" | Security-focused review |
| "Find bugs in X" | Single file analysis |
| "What's my risk score?" | Risk assessment |
| "Is this ready for PR?" | Quick pass/fail |
| "Review last N commits" | Commit range analysis |

---

## References

Load language-specific patterns as needed:

- `references/universal-patterns.md` - Language-agnostic bug patterns
- `references/security-checklist.md` - OWASP security checks
- `references/java-patterns.md` - Java/Spring Boot specific patterns
- `references/python-patterns.md` - Python specific patterns
- `references/typescript-patterns.md` - TypeScript/JavaScript patterns
- `references/go-patterns.md` - Go specific patterns
- `references/review-workflow.md` - Git operations and branch detection
