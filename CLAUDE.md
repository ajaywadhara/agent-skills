# Agent Skills

Production-ready AI coding skills that work with Claude Code, GitHub Copilot, Cursor, and other AI assistants.

**Author:** Ajay Wadhara | **License:** MIT | **Spec:** [agentskills.io](https://agentskills.io)

---

## Skills

| Skill | Description |
|-------|-------------|
| [pr-guardian](#pr-guardian) | Universal pre-PR code review — bugs, security, quality issues |
| [commit-push-pr](#commit-push-pr) | Commit, push, and create PRs with branch protection checks |
| [openapi-architect](#openapi-architect) | Design OpenAPI 3.1 specs with REST best practices |
| [spring-boot-4-migration](#spring-boot-4-migration) | Migrate Spring Boot 3.x → 4.x step-by-step |
| [design-doc](#design-doc) | Generate design documents with Mermaid diagrams |
| [multi-module-scaffolder](#multi-module-scaffolder) | Scaffold Spring Boot 4 multi-module Gradle projects |

---

## pr-guardian

**Universal pre-PR code review** — Detect bugs, security vulnerabilities, and quality issues before raising a PR. Works with any programming language.

**Triggers:** "review my code", "find bugs", "check security", "compare branches", "is this ready for PR"

---

## commit-push-pr

**Commit, push, and create PRs** — Safely commit changes with branch protection checks.

**Triggers:** "commit my changes", "commit and push", "push my code", "create a PR"

### Workflow
1. Check current branch - warns if on protected branch (main/master/develop)
2. Offer to create feature branch if needed
3. Pre-commit checks (secrets detection, lint/typecheck)
4. Stage → Commit (conventional commits) → Pull/rebase → Push → PR

---

## openapi-architect

**Design REST APIs with OpenAPI 3.1** — Generate specs from requirements with RFC compliance built-in.

**Triggers:** "design an API", "create OpenAPI spec", "review my API", "add pagination"

### Features
- RESTful URL design (resource-oriented)
- RFC 7807 error handling (Problem Details)
- Cursor-based pagination
- OAuth 2.0 / Bearer token security
- Filtering, sorting, sparse fieldsets

### Standards
OpenAPI 3.1 | RFC 9110 | RFC 7807 | RFC 8288

### Quick Start
```
"Design an API for user management"
"Add pagination to /orders endpoint"
"Review my OpenAPI spec for best practices"
```

---

## spring-boot-4-migration

**Migrate Spring Boot 3.x → 4.x** — Step-by-step guidance through all 10 migration phases.

**Triggers:** "migrate to Spring Boot 4", "upgrade Spring Boot", "help with Jackson 3"

### Migration Strategies
- **Gradual (6 tracks)** — Starters, Jackson, Properties, Security, Testing, Framework
- **All-at-once (10 phases)** — For smaller codebases

### Key Changes
| Area | Change |
|------|--------|
| Starters | `starter-web` → `starter-webmvc` |
| Jackson | `com.fasterxml.jackson` → `tools.jackson` |
| Security | `.and()` removed, lambdas only |
| Testing | `@MockBean` → `@MockitoBean` |
| Undertow | REMOVED → use Jetty |

### Requirements
Java 17+ (21+ recommended) | Gradle 8.14+ | Maven 3.6.3+

### References
`build-migration.md` | `jackson3-migration.md` | `security7-migration.md` | `testing-migration.md`

---

## design-doc

**Generate design documents** — Complete architecture docs with Mermaid diagrams from a single prompt.

**Triggers:** "design a system", "create a design doc", "architect a feature"

### Features
- One-shot output (minimal back-and-forth)
- Auto-selected diagrams based on domain
- Opinionated defaults with Decision Log

### Diagram Types
C4 Context/Container/Component | Sequence | ERD | State | Class | Flowchart

### Document Structure
1. Overview (problem, goals, non-goals)
2. Architecture (C4 diagrams)
3. Component Design
4. Data Model (ERD)
5. Key Flows (sequences)
6. NFRs, Security, Decision Log, Risks

### Output
`.output/design-doc-{topic}-{timestamp}.md`

---

## multi-module-scaffolder

**Scaffold Spring Boot 4 projects** — Multi-module Gradle with production-grade exception handling.

**Triggers:** "scaffold a project", "create multi-module", "new Spring Boot project"

### Generated Modules
```
project/
├── server/           # @SpringBootApplication
├── api-gateway/      # Controllers, DTOs
└── common/exception/ # GlobalExceptionHandler
```

### Exception Hierarchy
```
{Name}Exception
├── ResourceNotFoundException
├── ValidationException
├── BadRequestException
├── ServiceException
├── ServerException
└── ApiGatewayException
```

### Inputs
1. Project name (kebab-case)
2. Base package (e.g., `com.example.app`)
3. Target directory

### Requirements
Python 3.8+ | Java 21+ | Gradle 8.14+

---

## Creating Skills

### Structure
```
skill-name/
├── SKILL.md          # Required (keep <200 lines)
└── references/       # Optional (loaded as needed)
```

### SKILL.md Template
```yaml
---
name: skill-name
description: What it does and when to use. Include triggers.
license: MIT
metadata:
  author: Your Name
  version: "1.0"
---

# Skill Title

Brief instructions...

## Workflow
1. Step one
2. Step two

## References
- `references/detailed-info.md`
```

### Key Principles
1. **Concise SKILL.md** — Essential workflow only
2. **References for details** — Load as needed
3. **Progressive disclosure** — Metadata → Instructions → References
