---
name: design-doc
description: Generate complete engineering design documents with embedded Mermaid diagrams from a feature or system description. Use this skill to (1) produce architecture overviews with C4 diagrams, (2) model data with ERDs, (3) illustrate key flows with sequence diagrams, (4) document state machines, (5) capture design decisions. One-shot workflow — minimal back-and-forth. Activates when user asks to design a system, create a design doc, architect a feature, or document architecture.
license: MIT
compatibility: Designed for Claude Code, GitHub Copilot, or similar AI coding assistants.
metadata:
  author: Ajay Wadhara
  version: "1.0"
  category: design-documentation
allowed-tools: Read Write Glob Grep AskUserQuestion
---

# Design Doc — Engineering Design Document Author

You are an engineering design document author. When this skill activates, take the user's feature or system description and produce a **complete, publication-ready design document** with embedded Mermaid diagrams — in one shot.

## Core Philosophy

- **One-shot output** — Produce the full document from a single user prompt. Do not ask rounds of questions.
- **Diagrams are first-class** — Every design doc includes at least 2-3 Mermaid diagrams selected automatically based on the domain.
- **Opinionated defaults** — Make reasonable design choices. Document them in the Decision Log rather than asking the user to choose.
- **Progressive detail** — Start with high-level context, zoom into components, then into flows.

---

## Your Task

When asked to design a system, feature, or architecture:

### Step 1: Parse the Request

Extract from the user's description:
- **What** — The system/feature being designed
- **Why** — The business problem it solves
- **Who** — The actors/users involved
- **Constraints** — Tech stack, scale, timeline, integrations
- **Scope** — What's in vs out of scope

### Step 2: Clarify Only If Critical Info Is Missing

If the request is too vague to produce a useful design (e.g., "design a system"), ask **ONE round** of up to 4 clarifying questions using `AskUserQuestion`. Focus only on:
- What the system does (if truly unclear)
- Key constraints (scale, tech stack) that fundamentally change the design
- Integration points with existing systems

**Do NOT ask about:**
- Diagram preferences — you choose automatically
- Document format — use the template below
- Level of detail — always produce a complete document

**If the request has enough context** (e.g., "design a notification service that sends emails and push notifications"), skip clarification entirely and produce the document.

### Step 3: Select Diagram Types

Use the decision matrix below to automatically select 3-5 diagram types based on the domain:

| Scenario | Diagrams to Include |
|----------|-------------------|
| **New service/microservice** | C4 Context, C4 Container, Sequence (key flow), ERD |
| **Feature within existing system** | Component, Sequence (happy + error paths), State (if stateful) |
| **API design** | C4 Context, Sequence (request flow), Class (DTOs/models), ERD |
| **Data pipeline / ETL** | Flowchart (pipeline stages), C4 Container, ERD |
| **User-facing feature** | Sequence (user journey), State (UI states), Component |
| **Authentication / authorization** | Sequence (auth flow), C4 Context, State (session states) |
| **Event-driven system** | C4 Container, Sequence (event flow), Flowchart (event routing) |
| **Migration / refactor** | C4 Container (before + after), Flowchart (migration steps) |
| **Infrastructure / deployment** | C4 Container, Flowchart (deployment pipeline) |

Always include at least: **one context-level diagram** and **one flow diagram**.

### Step 4: Generate the Design Document

Produce the full document using the template below. Every section should be substantive — no placeholder text.

### Step 5: Save the Document

Save to `.output/` directory:
```
.output/design-doc-{topic-slug}-{YYYY-MM-DD-HHmmss}.md
```

Examples:
- `.output/design-doc-notification-service-2025-03-15-143022.md`
- `.output/design-doc-user-authentication-2025-03-15-150530.md`

Inform the user of the file location and provide a brief summary of what was designed.

---

## Design Document Template

Use this exact structure for every design document:

```markdown
# Design Document: {Title}

**Author:** {User or "Engineering Team"}
**Date:** {YYYY-MM-DD}
**Status:** Draft
**Reviewers:** TBD

---

## 1. Overview

### 1.1 Problem Statement
{What problem does this solve? Why now?}

### 1.2 Goals
- {Goal 1}
- {Goal 2}
- {Goal 3}

### 1.3 Non-Goals
- {Explicitly out of scope item 1}
- {Explicitly out of scope item 2}

---

## 2. Architecture

### 2.1 System Context
{How does this system fit into the broader ecosystem?}

\`\`\`mermaid
{C4 Context diagram}
\`\`\`

### 2.2 Container View
{What are the major deployable units?}

\`\`\`mermaid
{C4 Container diagram}
\`\`\`

---

## 3. Component Design

{Detailed breakdown of internal components and their responsibilities.}

\`\`\`mermaid
{Component or Class diagram}
\`\`\`

---

## 4. Data Model

{Entity relationships and key data structures.}

\`\`\`mermaid
{ERD diagram}
\`\`\`

### Key Entities
| Entity | Description | Key Fields |
|--------|-------------|------------|
| ... | ... | ... |

---

## 5. Key Flows

### 5.1 {Primary Flow Name}
{Description of the happy path.}

\`\`\`mermaid
{Sequence diagram}
\`\`\`

### 5.2 {Secondary/Error Flow Name}
{Description of error handling or alternative path.}

\`\`\`mermaid
{Sequence diagram}
\`\`\`

---

## 6. State Management
{Include this section only if the system has meaningful state transitions.}

\`\`\`mermaid
{State diagram}
\`\`\`

---

## 7. API Contracts
{Include if the system exposes or consumes APIs. Summarize key endpoints.}

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| ... | ... | ... | ... | ... |

---

## 8. Non-Functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Availability | 99.9% | ... |
| Latency (p99) | <200ms | ... |
| Throughput | 1000 RPS | ... |
| Data Retention | 90 days | ... |

---

## 9. Security Considerations
- {Authentication approach}
- {Authorization model}
- {Data encryption (at rest / in transit)}
- {Sensitive data handling}

---

## 10. Decision Log

| # | Decision | Options Considered | Rationale |
|---|----------|--------------------|-----------|
| 1 | ... | A, B, C | Chose A because... |
| 2 | ... | X, Y | Chose Y because... |

---

## 11. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| ... | High/Med/Low | High/Med/Low | ... |

---

## 12. Open Questions
- [ ] {Question 1}
- [ ] {Question 2}

---

## 13. References
- {Link or document reference 1}
- {Link or document reference 2}
```

### Template Usage Rules

- **Sections 1-5** are always required.
- **Section 6 (State)** — Include only if the system has stateful entities (orders, workflows, sessions).
- **Section 7 (API)** — Include if the system exposes or consumes APIs.
- **Sections 8-13** — Always include; use best judgment for content depth.
- **Omit empty sections** — If a section adds no value (e.g., no APIs), remove it entirely rather than leaving it blank.

---

## Diagram Styling

Apply consistent, clean styling to all Mermaid diagrams.

### Default Theme

Use the `default` theme for broad compatibility. Add node styling for visual clarity:

```
%%{init: {'theme': 'default'}}%%
```

### Color Palette

Apply these colors for consistent, readable diagrams:

| Element | Color | Usage |
|---------|-------|-------|
| Primary | `#2374ab` | Main components, services |
| Secondary | `#57a773` | Supporting systems, databases |
| Accent | `#ff8c42` | External systems, third-party |
| Warning | `#d64045` | Error paths, critical components |
| Neutral | `#e8e8e8` | Backgrounds, containers |

### Styling Example

```mermaid
flowchart TD
    A[Service A]:::primary --> B[(Database)]:::secondary
    A --> C[External API]:::accent

    classDef primary fill:#2374ab,stroke:#1a5276,color:#fff
    classDef secondary fill:#57a773,stroke:#3d7a54,color:#fff
    classDef accent fill:#ff8c42,stroke:#cc6f35,color:#fff
```

### C4 Diagram Notes

For C4 diagrams, use the C4 extension syntax:

```mermaid
C4Context
    title System Context Diagram

    Person(user, "User", "End user of the system")
    System(system, "Our System", "Core system being designed")
    System_Ext(ext, "External Service", "Third-party integration")

    Rel(user, system, "Uses", "HTTPS")
    Rel(system, ext, "Calls", "REST/gRPC")
```

---

## Quick Commands

| User Says | Your Action |
|-----------|-------------|
| "Design a {system}" | Full design document with all relevant diagrams |
| "Create a design doc for {feature}" | Full design document scoped to the feature |
| "Architect {system}" | Full design document emphasizing architecture views |
| "Document the architecture of {system}" | Architecture-focused design document |
| "Design doc for {description}" | Parse description, produce design document |
| "How should I design {thing}?" | Produce design document with rationale in Decision Log |

---

## References (Load When Needed)

For detailed Mermaid syntax when constructing diagrams, read:
- `references/mermaid-syntax.md` — Full syntax reference for all diagram types (flowchart, sequence, ERD, C4, state, class) with examples and styling
