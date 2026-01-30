# Agent Skills Repository

This repository contains custom Claude Code skills (agent-skills) that extend Claude's capabilities for specific workflows and tasks.

## Project Structure

```
agent-skills/
├── skills/                    # All skill definitions
│   └── <skill-name>/
│       ├── SKILL.md          # Skill definition file (required)
│       └── references/       # Supporting reference documents (optional)
└── CLAUDE.md                 # This file
```

## Skills Overview

| Skill | Description | Triggers |
|-------|-------------|----------|
| [pr-guardian](#pr-guardian) | Pre-PR code review and bug detection for Java/Spring Boot | "review code", "find bugs", "check security", "prepare for PR" |

---

## Skill Details

### pr-guardian

**Location:** `skills/pr-guardian-skill/`

**Purpose:** Pre-PR defense system that analyzes Java/Spring Boot code for bugs, security vulnerabilities, and quality issues before raising a pull request.

**Capabilities:**
- Detect bugs, security vulnerabilities, and performance issues
- Review Java files for common problems
- Generate self-review checklists
- Calculate risk scores (1-10)
- Suggest fixes for identified issues

**Issue Severity Levels:**
- `BLOCKER` - Critical bug or security flaw (must fix before PR)
- `WARNING` - Potential problem (should fix)
- `SUGGESTION` - Improvement opportunity (nice to have)

**Key Patterns Checked:**
- Null safety (Optional.get() without check, NPE risks, null returns)
- Security (SQL injection, hardcoded secrets, missing validation, sensitive data in logs)
- Resource leaks (unclosed streams)
- Spring issues (@Transactional problems, entity exposure)
- Performance (N+1 queries, EAGER fetching)
- Code quality (empty catch blocks, System.out usage)

**Reference Documents:**
- `references/bug-patterns.md` - 30+ Java/Spring bug patterns with fixes
- `references/security-checklist.md` - Complete OWASP Top 10 checks
- `references/performance-antipatterns.md` - N+1, memory, CPU issues
- `references/code-smells.md` - Code quality indicators
- `references/review-checklist-templates.md` - Checklist templates by file type

**Example Commands:**
- "Review my code"
- "Check for security issues"
- "Find bugs in X.java"
- "What's my risk score?"
- "Generate PR checklist"
- "Is this code ready for PR?"

---

## Creating New Skills

To add a new skill:

1. Create a new directory under `skills/`: `skills/<skill-name>/`
2. Add a `SKILL.md` file with frontmatter containing:
   - `name`: Skill identifier
   - `description`: What the skill does and when it activates
3. Add any supporting reference files in a `references/` subdirectory
4. Document the skill in this CLAUDE.md file

### SKILL.md Template

```markdown
---
name: skill-name
description: Brief description of what this skill does and when it should activate.
---

# Skill Title

Instructions for Claude when this skill is activated...
```

---

## Usage

These skills are designed to be used with Claude Code. They automatically activate based on trigger phrases in your conversations. You can also explicitly invoke them by referencing the skill's purpose or commands.
