# Spring Boot 4.x Migration Skill

A comprehensive, modular skill for migrating Spring Boot applications from 3.x to 4.x.

## Features

- **10 Migration Phases** - Systematic approach covering all aspects
- **Two Strategies** - Gradual (enterprise) or All-at-Once migration
- **Detailed Reference Docs** - In-depth guides for each technical area
- **Verification Script** - Automated migration validation
- **Maven & Gradle Support** - Both build systems covered
- **Rollback Strategy** - Safe migration with fallback options

## Quick Start

### 1. Check Requirements

```bash
java -version   # 17+ required, 21+ recommended
./mvnw -version # 3.6.3+ required (Maven)
./gradlew --version # 8.14+ required (Gradle)
```

### 2. Read the Main Skill

Start with [SKILL.md](SKILL.md) for the complete migration workflow.

### 3. Run Verification

```bash
chmod +x scripts/verify-migration.sh
./scripts/verify-migration.sh
```

## Directory Structure

```
spring-boot-4-migration-skill/
├── SKILL.md                           # Main migration skill/workflow
├── README.md                          # This file
├── references/
│   ├── pre-migration.md               # Pre-migration preparation
│   ├── build-migration.md             # Maven/Gradle changes
│   ├── property-changes.md            # Configuration properties
│   ├── jackson3-migration.md          # Jackson 2 → 3 migration
│   ├── security7-migration.md         # Spring Security 7 changes
│   ├── testing-migration.md           # Test infrastructure
│   ├── observability-migration.md     # Metrics/tracing/logging
│   ├── api-changes.md                 # Package relocations & API changes
│   ├── framework7-changes.md          # Spring Framework 7 features
│   └── verification-checklist.md      # Complete verification checklist
└── scripts/
    └── verify-migration.sh            # Automated verification script
```

## Key Changes Summary

### Minimum Requirements

| Requirement | Version |
|-------------|---------|
| Java | 17+ (21+ recommended) |
| Kotlin | 2.2+ |
| Maven | 3.6.3+ |
| Gradle | 8.14+ |
| GraalVM | 25+ (for native) |

### Major Changes

- **Modular Starters** - 70+ focused modules replace monolithic JARs
- **Jackson 3** - New package structure, immutable JsonMapper
- **Spring Security 7** - Lambda-only DSL, no `.and()` chaining
- **Testing** - `@MockitoBean` replaces `@MockBean`
- **OpenTelemetry** - New unified observability starter
- **JSpecify** - Standardized null safety annotations
- **Jakarta EE 11** - Servlet 6.1, JPA 3.2, Validation 3.1

### Removed Features

- Undertow server support
- JUnit 4 support
- `@MockBean`/`@SpyBean` (use `@MockitoBean`/`@MockitoSpyBean`)
- Executable JAR launch scripts
- Spring Session Hazelcast/MongoDB (now external)
- Reactive Pulsar support

## Migration Strategies

### Strategy A: Gradual (Recommended for Enterprise)

1. Add compatibility bridges
2. Migrate in 6 independent tracks
3. Remove bridges after validation

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-classic</artifactId>
</dependency>
```

### Strategy B: All-at-Once

Execute all 10 phases sequentially. Best for smaller codebases.

## References

### Official Documentation

- [Spring Boot 4.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Spring Boot 4.0 Release Notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Release-Notes)
- [Spring Framework 7 Reference](https://docs.spring.io/spring-framework/reference/)
- [Spring Security 7 Migration](https://docs.spring.io/spring-security/reference/migration/index.html)

### Automation Tools

- [OpenRewrite Spring Boot 4 Recipes](https://docs.openrewrite.org/recipes/java/spring/boot4)
- [Moderne Platform](https://www.moderne.ai/)

## License

Apache 2.0

## Contributing

Contributions welcome! Please submit issues and pull requests.
