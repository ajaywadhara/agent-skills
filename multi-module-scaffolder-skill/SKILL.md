---
name: multi-module-scaffolder
description: Scaffold complete multi-module Gradle projects with Spring Boot 4, Java 21, and a production-grade exception handling architecture. Generates server, api-gateway, and common:exception modules with version catalog, GlobalExceptionHandler, ErrorCode enum, ErrorResponse record, and per-module exception hierarchy. Use when asked to scaffold a project, create a multi-module Gradle project, generate a new Spring Boot project, or set up a microservice skeleton.
license: MIT
compatibility: Requires Python 3.8+. Generated projects require Java 21+, Gradle 8.14+, and Spring Boot 4.0.0.
metadata:
  author: Ajay Wadhara
  version: "1.0"
  category: project-scaffolding
allowed-tools: Bash Read Write Glob Grep AskUserQuestion
---

# Multi-Module Scaffolder — Spring Boot 4 Project Generator

You are a project scaffolding assistant. When this skill activates, generate a complete multi-module Gradle project with Spring Boot 4, Java 21, and a production-grade exception handling architecture — with minimal user interaction.

## Core Philosophy

- **Single-shot output** — Ask only for project name, base package, and target directory, then generate everything.
- **Production-grade defaults** — Every generated project includes a fully-wired exception handling system with GlobalExceptionHandler, ErrorCode enum, ErrorResponse record, and per-module exception classes.
- **Proven patterns** — Follows multi-module Gradle patterns used in production Spring Boot 4 applications.
- **Ready to run** — Generated project compiles and passes context load tests after adding Gradle wrapper.

---

## Your Task

When asked to scaffold a project, create a multi-module project, or generate a new Spring Boot project:

### Step 1: Gather Inputs

Ask the user for **3 inputs** using `AskUserQuestion`:

1. **Project name** (kebab-case, e.g., `my-app`, `order-service`)
2. **Base package** (e.g., `com.example.myapp`, `com.company.orders`)
3. **Target directory** (where to create the project — defaults to current working directory)

If the user provides these in their initial message, skip asking.

### Step 2: Validate Inputs

Before running the script:
- Project name must be kebab-case (lowercase letters, numbers, hyphens; no leading/trailing hyphens)
- Base package must be valid Java package (lowercase, dots as separators, no hyphens)
- Target directory must exist

### Step 3: Run the Scaffold Script

Execute the Python scaffold script:

```bash
python3 "<skill-directory>/scripts/scaffold.py" --name <project-name> --package <base-package> --output-dir <target-directory>
```

The script generates the full project structure including:
- Root Gradle build files with version catalog (`libs.versions.toml`)
- `server` module — Spring Boot application with `@SpringBootApplication`
- `api-gateway` module — library module for API layer
- `common:exception` module — complete exception handling framework
- `.gitignore` for Java/Gradle/IDE files

### Step 4: Display Summary

After successful generation, show the user:

1. **Project summary** — name, package, modules created
2. **File tree** — all generated directories and files
3. **Exception hierarchy** — visual tree of the exception classes
4. **Next steps** — instructions to initialize git, add Gradle wrapper, import in IDE, and run

Use the output template at `scripts/output-template.md` for formatting.

### Step 5: Offer Follow-up

After showing the summary, offer:
- "Want me to initialize a git repository?"
- "Want me to add the Gradle wrapper?" (requires Gradle installed)
- "Want me to open any of the generated files?"

---

## Generated Project Structure

```
{project-name}/
├── build.gradle.kts                          # Root: java toolchain, checkstyle
├── settings.gradle.kts                       # Module includes with findProject renames
├── gradle.properties                         # Gradle JVM args
├── gradle/libs.versions.toml                 # Version catalog (Boot 4.0.0, Java 21)
├── .gitignore                                # Java/Gradle/IDE gitignore
│
├── server/
│   ├── build.gradle.kts                      # Boot app, depends on api-gateway + common:exception
│   └── src/
│       ├── main/java/{pkg}/server/
│       │   ├── {Name}Application.java        # @SpringBootApplication + @ComponentScan
│       │   └── exception/
│       │       └── ServerException.java      # Module exception
│       ├── main/resources/
│       │   └── application.yml               # Server config with profiles
│       └── test/java/{pkg}/server/
│           └── {Name}ApplicationTests.java   # Context load test
│
├── api-gateway/
│   ├── build.gradle.kts                      # Library module
│   └── src/
│       ├── main/java/{pkg}/gateway/
│       │   └── exception/
│       │       └── ApiGatewayException.java  # Module exception
│       └── test/java/{pkg}/gateway/
│
├── common/
│   ├── build.gradle.kts                      # Parent common module
│   └── exception/
│       ├── build.gradle.kts                  # Exception library module
│       └── src/
│           ├── main/java/{pkg}/common/exception/
│           │   ├── {Name}Exception.java              # Base: extends RuntimeException
│           │   ├── ResourceNotFoundException.java
│           │   ├── ValidationException.java          # With inner ValidationError
│           │   ├── BadRequestException.java
│           │   ├── ServiceException.java             # Static factory methods
│           │   ├── config/
│           │   │   └── ExceptionHandlingConfig.java  # @Configuration @Import
│           │   ├── handler/
│           │   │   └── GlobalExceptionHandler.java   # @RestControllerAdvice (15+ handlers)
│           │   └── model/
│           │       ├── ErrorCode.java                # Enum with code, message, category
│           │       ├── ErrorCategory.java            # Enum: GENERAL, VALIDATION, AUTH, etc.
│           │       └── ErrorResponse.java            # Record with Builder pattern
│           └── test/java/{pkg}/common/exception/
```

## Exception Hierarchy

```
RuntimeException
└── {Name}Exception (common:exception) — ErrorCode field + details map + fluent addDetail()
    ├── ResourceNotFoundException     — resource type + identifier constructors
    ├── ValidationException           — field-level errors with inner ValidationError
    ├── BadRequestException           — field + reason constructors
    ├── ServiceException              — static factories: externalServiceError(), databaseError()
    ├── ServerException (server)      — module-level exception
    └── ApiGatewayException (gateway) — module-level exception
```

## ErrorCode Categories (Generic)

| Category | Codes | Range |
|----------|-------|-------|
| GENERAL | INTERNAL_SERVER_ERROR, SERVICE_UNAVAILABLE | ERR-001 to ERR-002 |
| VALIDATION | VALIDATION_ERROR, INVALID_REQUEST, MISSING_REQUIRED_FIELD, INVALID_FORMAT | ERR-100 to ERR-103 |
| AUTHENTICATION | UNAUTHORIZED, INVALID_CREDENTIALS, TOKEN_EXPIRED | ERR-200, ERR-202, ERR-203 |
| AUTHORIZATION | FORBIDDEN | ERR-201 |
| RESOURCE | RESOURCE_NOT_FOUND, RESOURCE_ALREADY_EXISTS, RESOURCE_CONFLICT | ERR-300 to ERR-302 |
| EXTERNAL_SERVICE | EXTERNAL_SERVICE_ERROR, DATABASE_ERROR | ERR-500, ERR-502 |

---

## Quick Commands

| User Says | Your Action |
|-----------|-------------|
| "Scaffold a project" | Ask for name + package, generate project |
| "Create a multi-module Gradle project" | Ask for name + package, generate project |
| "New Spring Boot project called X" | Parse name from request, ask for package, generate |
| "Generate a project skeleton" | Ask for name + package, generate project |
| "Set up a microservice skeleton" | Ask for name + package, generate project |

---

## References (Load When Needed)

For detailed information about generated content, read:
- `references/spring-boot-4-dependencies.md` — Version catalog and dependency details
- `references/project-structure.md` — Module layout, dependency graph, and Gradle patterns
