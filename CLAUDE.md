# Agent Skills Repository

This repository contains custom Claude Code skills (agent-skills) that extend Claude's capabilities for specific workflows and tasks.

## Project Structure

```
agent-skills/
├── <skill-name>/              # Skill directories at root level
│   ├── SKILL.md              # Skill definition file (required)
│   ├── references/           # Supporting reference documents (optional)
│   └── scripts/              # Executable scripts (optional)
├── .output/                   # Generated reports (gitignored)
└── CLAUDE.md                 # This file
```

## Skills Overview

| Skill | Version | Description | Triggers |
|-------|---------|-------------|----------|
| [pr-guardian](#pr-guardian) | 1.1 | Pre-PR code review and bug detection for Java/Spring Boot (interactive) | "review code", "review my branch", "compare against develop", "find bugs", "check security" |
| [openapi-architect](#openapi-architect) | 1.0 | Design and generate OpenAPI 3.1 specifications | "design an API", "create OpenAPI spec", "review API design", "architect REST endpoints" |
| [spring-boot-4-migration](#spring-boot-4-migration) | 1.0 | Comprehensive migration guide for Spring Boot 3.x to 4.x | "migrate to Spring Boot 4", "upgrade Spring Boot", "Spring Boot 4 migration", "modernize Spring Boot" |

**Author:** Ajay Wadhara
**License:** MIT
**Specification:** [agentskills.io](https://agentskills.io/specification)

---

## Skill Details

### pr-guardian

**Location:** `pr-guardian-skill/`

**Purpose:** Pre-PR defense system that analyzes Java/Spring Boot code for bugs, security vulnerabilities, and quality issues before raising a pull request. Supports both local changes and full branch comparison with **interactive fix workflows**.

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
- **Interactive fix application** - Offers to fix issues after review
- **Selective fixing** - Fix all, BLOCKERs only, or choose individually
- **Commit integration** - Optionally commit fixes with proper messages

**Interactive Workflows:**
1. **Clarify scope** - Asks what to review if unclear (local/branch/commits)
2. **After analysis** - Offers to fix BLOCKERs, all issues, or let user choose
3. **After fixes** - Offers to review changes, re-run analysis, or commit
4. **Commit options** - Single commit, separate by category, or manual

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

**Location:** `openapi-architect-skill/`

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

### spring-boot-4-migration

**Location:** `spring-boot-4-migration-skill/`

**Purpose:** Comprehensive, modular skill for migrating Spring Boot applications from 3.x to 4.x. Provides step-by-step guidance through all migration phases with detailed reference documentation.

**Migration Strategies:**
- **Gradual Migration** - Uses compatibility bridges for incremental adoption across 6 independent tracks
- **All-at-Once Migration** - Execute all 10 phases sequentially for smaller codebases

**Migration Phases:**
1. Pre-Migration Preparation - Version checks, deprecation fixes, test baseline
2. Build File Migration - Parent version, comprehensive starter changes by category
3. Property Migration - Renamed properties, Jackson property restructuring
4. Jackson 3 Migration - Package changes, class renames, default behavior changes
5. Package and API Relocations - Key package moves, removed APIs
6. Spring Security 7 Migration - DSL changes, authorization updates, request matchers
7. Testing Infrastructure Migration - MockBean replacement, @SpringBootTest changes
8. Observability Migration - OpenTelemetry starter, configuration updates
9. Spring Framework 7 Changes - JSpecify null safety, resilience, Hibernate 7.1
10. Verification and Cleanup - Run verification script, remove compatibility bridges

**Starter Changes by Category:**
- **Web & API** - `starter-web` → `starter-webmvc`, `starter-web-services` → `starter-webservices`
- **Security** - OAuth2/SAML starters renamed with `-security-` prefix, new `starter-security-test`
- **Database** - New `starter-flyway`, `starter-liquibase` (now required)
- **Batch** - New `starter-batch-jdbc`, `starter-batch-mongodb` for metadata persistence
- **Observability** - New unified `starter-opentelemetry`
- **AOP** - `starter-aop` → `starter-aspectj`
- **Serialization** - New `starter-kotlin-serialization`
- **Containers** - `starter-undertow` removed (use Jetty)
- **Testing** - New slice test starters (`starter-webmvc-test`, `starter-data-jpa-test`, etc.)
- **Session** - Hazelcast/MongoDB session support moved to external providers
- **Migration Bridges** - `starter-classic`, `starter-test-classic`, `spring-boot-jackson2`

**Minimum Requirements:**
- Java 17+ (21+ recommended)
- Kotlin 2.2+ (if using Kotlin)
- Maven 3.6.3+ or Gradle 8.14+
- GraalVM 25+ (for native images)

**Key Dependencies Updated:**
- Spring Framework 7.0
- Spring Security 7.0
- Spring Data 2025.1
- Hibernate 7.1
- Jackson 3.0
- JUnit 6
- Testcontainers 2.0
- Jakarta EE 11 (Servlet 6.1)

**Reference Documents:**
- `references/pre-migration.md` - Pre-migration assessment and preparation
- `references/build-migration.md` - Build file changes for Maven and Gradle
- `references/property-changes.md` - Configuration property migrations
- `references/jackson3-migration.md` - Jackson 2 to 3 migration details
- `references/api-changes.md` - Package relocations and API changes
- `references/security7-migration.md` - Spring Security 7 migration guide
- `references/testing-migration.md` - Test infrastructure updates
- `references/observability-migration.md` - Observability and metrics migration
- `references/framework7-changes.md` - Spring Framework 7 specific changes
- `references/verification-checklist.md` - Post-migration verification steps

**Scripts:**
- `scripts/verify-migration.sh` - Automated migration verification script

**Example Commands:**
- "Migrate to Spring Boot 4"
- "Upgrade Spring Boot 3 to 4"
- "Spring Boot 4 migration"
- "Update to Boot 4"
- "Spring Boot 4.x upgrade"
- "Modernize Spring Boot application"
- "What's the upgrade path from 3.2?"
- "Help me migrate Jackson to version 3"
- "Update my tests for Spring Boot 4"

---

## Creating New Skills

Following the [Agent Skills Specification](https://agentskills.io/specification).

### Steps

1. Create a new directory at the repository root: `<skill-name>/`
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
