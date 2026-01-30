# Agent Skills Repository

This repository contains custom Claude Code skills (agent-skills) that extend Claude's capabilities for specific workflows and tasks.

## Project Structure

```
agent-skills/
├── skills/                    # All skill definitions
│   └── <skill-name>/
│       ├── SKILL.md          # Skill definition file (required)
│       └── references/       # Supporting reference documents (optional)
├── .output/                   # Generated reports (gitignored)
└── CLAUDE.md                 # This file
```

## Skills Overview

| Skill | Version | Description | Triggers |
|-------|---------|-------------|----------|
| [pr-guardian](#pr-guardian) | 1.0 | Pre-PR code review and bug detection for Java/Spring Boot | "review code", "review my branch", "compare against develop", "find bugs", "check security" |
| [openapi-architect](#openapi-architect) | 1.0 | Design and generate OpenAPI 3.1 specifications | "design an API", "create OpenAPI spec", "review API design", "architect REST endpoints" |

**Author:** Ajay Wadhara
**License:** MIT
**Specification:** [agentskills.io](https://agentskills.io/specification)

---

## Skill Details

### pr-guardian

**Location:** `skills/pr-guardian-skill/`

**Purpose:** Pre-PR defense system that analyzes Java/Spring Boot code for bugs, security vulnerabilities, and quality issues before raising a pull request. Supports both local changes and full branch comparison.

**Review Modes:**
- **Local Changes** - Review uncommitted/staged changes in working directory
- **Branch Comparison** - Compare entire feature branch against base branch (develop/main/master)
- **Commit Range** - Review changes from specific commits

**Capabilities:**
- Detect bugs, security vulnerabilities, and performance issues
- Review Java files for common problems
- Compare feature branches against develop/main/master
- Handle partially committed changes
- Generate self-review checklists
- Calculate risk scores (1-10)
- Suggest fixes for identified issues
- Save detailed reports to `.output/` directory

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
- "Review my code" - Review local uncommitted changes
- "Review my branch" - Compare feature branch against base
- "Compare against develop" - Explicit base branch comparison
- "Compare against main" - Compare with main branch
- "Review last 3 commits" - Review recent commit changes
- "What changed since develop?" - List all branch changes
- "Check for security issues" - Security-focused review
- "Find bugs in X.java" - Single file analysis
- "What's my risk score?" - Risk assessment
- "Is this code ready for PR?" - Quick pass/fail check

**Report Output:**
Reports are saved to `.output/` directory:
- `.output/pr-report-{context}-{timestamp}.md` for local changes
- `.output/pr-report-{feature}-vs-{base}-{timestamp}.md` for branch comparison

---

### openapi-architect

**Location:** `skills/openapi-architect-skill/`

**Purpose:** Design and generate OpenAPI 3.1 specifications following industry best practices, RFCs, and recommendations from API design experts (Fielding, Massé, Higginbotham).

**Capabilities:**
- Create complete OpenAPI 3.1 specs from requirements
- Review existing specs for compliance and best practices
- Apply RESTful design principles
- Implement proper error handling per RFC 7807 (Problem Details)
- Design authentication/authorization schemes
- Structure pagination, filtering, and sorting
- Guide versioning strategy decisions

**Core Principles Applied:**
- Resource-oriented design (nouns, not verbs)
- Consistent patterns across all endpoints
- Predictable URL structures
- Evolvable APIs without breaking changes
- Self-documenting with clear naming

**Standards & RFCs Followed:**
- OpenAPI 3.1 Specification
- RFC 9110 - HTTP Semantics
- RFC 7807 - Problem Details for HTTP APIs
- RFC 8288 - Web Linking (pagination)
- RFC 7396 - JSON Merge Patch
- RFC 3986 - URI Standard

**Reference Documents:**
- `references/http-standards.md` - RFC 9110, 7807, 8288 details
- `references/security-patterns.md` - OAuth flows, API key best practices, OWASP Top 10
- `references/pagination-patterns.md` - Cursor vs offset, filtering, sorting
- `references/naming-conventions.md` - URLs, fields, schemas, operations
- `references/versioning-strategies.md` - URL, header, content-type versioning

**Example Commands:**
- "Design an API for X"
- "Create an OpenAPI spec for a user management system"
- "Review my API spec"
- "Add pagination to this endpoint"
- "How should I handle errors?"
- "What status code should I use for X?"
- "Help me design authentication for my API"

---

## Creating New Skills

Following the [Agent Skills Specification](https://agentskills.io/specification).

### Steps

1. Create a new directory under `skills/`: `skills/<skill-name>/`
2. Add a `SKILL.md` file with proper frontmatter (see template below)
3. Add supporting reference files in a `references/` subdirectory (optional)
4. Add scripts in a `scripts/` subdirectory (optional)
5. Document the skill in this CLAUDE.md file

### Directory Structure

```
skill-name/
├── SKILL.md              # Required - Main skill definition
├── references/           # Optional - Additional documentation
│   ├── patterns.md
│   └── checklist.md
├── scripts/              # Optional - Executable scripts
│   └── analyze.py
└── assets/               # Optional - Static resources
    └── templates/
```

### SKILL.md Template

```markdown
---
name: skill-name
description: A detailed description of what this skill does and when to use it. Include specific keywords that help agents identify relevant tasks. Max 1024 characters.
license: MIT
compatibility: Environment requirements (e.g., requires git, docker, specific tools).
metadata:
  author: Ajay Wadhara
  version: "1.0"
  category: category-name
  custom-field: custom-value
allowed-tools: Bash(git:*) Read Write Glob Grep
---

# Skill Title

Instructions for the agent when this skill is activated...

## Your Task

Step-by-step instructions...

## Examples

Input/output examples...

## References

Links to reference files for detailed information...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric and hyphens only |
| `description` | Yes | 1-1024 chars, describes what skill does and when to use it |
| `license` | No | License name (e.g., MIT, Apache-2.0) |
| `compatibility` | No | Environment requirements (max 500 chars) |
| `metadata` | No | Key-value pairs for additional info (author, version, etc.) |
| `allowed-tools` | No | Space-delimited list of pre-approved tools |

### Naming Rules

- Lowercase letters, numbers, and hyphens only
- Must not start or end with hyphen
- No consecutive hyphens (`--`)
- Directory name must match `name` field

### Progressive Disclosure

Structure skills for efficient context usage:

1. **Metadata** (~100 tokens) - `name` and `description` loaded at startup
2. **Instructions** (<5000 tokens) - Full SKILL.md loaded when activated
3. **Resources** (as needed) - Reference files loaded only when required

Keep main SKILL.md under 500 lines. Move detailed content to reference files.

---

## Usage

These skills are designed to be used with Claude Code, GitHub Copilot, or similar AI coding assistants. They automatically activate based on trigger phrases in your conversations. You can also explicitly invoke them by referencing the skill's purpose or commands.
