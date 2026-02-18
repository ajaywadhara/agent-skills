---
name: spring-boot-4-migration
description: Migrate Spring Boot applications from 3.x to 4.x with step-by-step guidance. Covers all 10 migration phases including build files, Jackson 3, Security 7, testing, and observability. Use when upgrading Spring Boot, migrating to Boot 4, or modernizing Spring applications. Supports gradual (6 tracks) or all-at-once migration strategies.
license: MIT
metadata:
  author: Ajay Wadhara
  version: "2.0"
  category: migration
---

# Spring Boot 4 Migration Guide

You are a Spring Boot migration expert. Guide users through upgrading from Spring Boot 3.x to 4.x with clear, actionable steps.

## Minimum Requirements

| Requirement | Version |
|-------------|---------|
| Java | 17+ (21+ recommended) |
| Kotlin | 2.2+ |
| Maven | 3.6.3+ |
| Gradle | 8.14+ |

## Key Dependencies Updated

Spring Framework 7.0, Spring Security 7.0, Jackson 3.0, Hibernate 7.1, JUnit 6, Jakarta EE 11

---

## Migration Strategies

### Strategy A: Gradual (6 Independent Tracks)

Use compatibility bridges for incremental adoption:
1. **Starters** → Modular starters
2. **Jackson** → Jackson 2 to 3
3. **Properties** → Config updates
4. **Security** → Spring Security 7
5. **Testing** → Test infrastructure
6. **Framework** → Spring Framework 7

**Enable bridges:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-classic</artifactId>
</dependency>
```

### Strategy B: All-at-Once (10 Phases)

Execute sequentially for smaller codebases or dedicated sprints.

---

## Migration Phases

### Phase 1: Pre-Migration
1. Ensure on Spring Boot 3.5.x
2. Fix all deprecation warnings
3. Run full test suite (must pass)
4. Create migration branch

**Reference:** `references/pre-migration.md`

### Phase 2: Build Files

**Update parent/plugin version to 4.0.0 and Java to 21.**

Key starter changes:
| Category | Change |
|----------|--------|
| Web | `starter-web` → `starter-webmvc` |
| Security | Add `-security-` prefix (e.g., `starter-security-oauth2-client`) |
| Database | NEW `starter-flyway`, `starter-liquibase` (now required) |
| Batch | NEW `starter-batch-jdbc` (required for DB metadata) |
| Observability | NEW unified `starter-opentelemetry` |
| AOP | `starter-aop` → `starter-aspectj` |
| Undertow | REMOVED → use Jetty |

**Reference:** `references/build-migration.md`

### Phase 3: Properties

Key renames:
| Old | New |
|-----|-----|
| `spring.dao.*` | `spring.persistence.*` |
| `management.tracing.enabled` | `management.tracing.export.enabled` |

Jackson restructuring: `spring.jackson.*` → `spring.jackson.json.*`

**Reference:** `references/property-changes.md`

### Phase 4: Jackson 3

Package change: `com.fasterxml.jackson.databind` → `tools.jackson.databind`

Class renames: `@JsonComponent` → `@JacksonComponent`, `JsonObjectSerializer` → `ObjectValueSerializer`

**Reference:** `references/jackson3-migration.md`

### Phase 5: API Changes

Package relocations (see `references/api-changes.md`)

### Phase 6: Security 7

DSL changes: Remove `.and()` chaining, use lambdas
Matchers: `antMatchers` → `requestMatchers`

**Reference:** `references/security7-migration.md`

### Phase 7: Testing

`@MockBean` → `@MockitoBean`
`@SpyBean` → `@MockitoSpyBean`
MockMvc requires `@AutoConfigureMockMvc`

**Reference:** `references/testing-migration.md`

### Phase 8: Observability

NEW unified `starter-opentelemetry`

**Reference:** `references/observability-migration.md`

### Phase 9: Framework 7

JSpecify annotations: `org.springframework.lang.Nullable` → `org.jspecify.annotations.Nullable`

**Reference:** `references/framework7-changes.md`

### Phase 10: Verification

1. Run tests
2. Verify actuator endpoints
3. Remove compatibility bridges
4. Run `scripts/verify-migration.sh`

**Reference:** `references/verification-checklist.md`

---

## OpenRewrite Automation

```xml
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0</recipe>
        </activeRecipes>
    </configuration>
</plugin>
```

Run: `mvn rewrite:run` or `./gradlew rewriteRun`

---

## Quick Commands

| User Says | Action |
|-----------|--------|
| "Migrate to Spring Boot 4" | Run pre-migration checks, guide through phases |
| "Upgrade from Boot 3.x" | Assess current version, recommend upgrade path |
| "Help with Jackson 3" | Load jackson3-migration.md, apply changes |
| "Migrate Security to 7" | Load security7-migration.md, apply changes |
| "Fix my tests" | Load testing-migration.md, fix MockBean issues |
