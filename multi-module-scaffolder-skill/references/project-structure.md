# Project Structure Reference

## Directory Tree

```
{project-name}/
├── build.gradle.kts                    # Root build: java toolchain, checkstyle, no tests
├── settings.gradle.kts                 # Module includes with findProject renames
├── gradle.properties                   # Gradle JVM args (Xmx, file-system-watching)
├── gradle/
│   └── libs.versions.toml              # Centralized version catalog
├── .gitignore                          # Java/Gradle/IDE/OS ignores
│
├── server/                             # Main application module (bootJar enabled)
│   ├── build.gradle.kts
│   └── src/
│       ├── main/
│       │   ├── java/{pkg}/server/
│       │   │   ├── {Name}Application.java
│       │   │   └── exception/
│       │   │       └── ServerException.java
│       │   └── resources/
│       │       └── application.yml
│       └── test/
│           └── java/{pkg}/server/
│               └── {Name}ApplicationTests.java
│
├── api-gateway/                        # API layer library module
│   ├── build.gradle.kts
│   └── src/
│       ├── main/
│       │   └── java/{pkg}/gateway/
│       │       └── exception/
│       │           └── ApiGatewayException.java
│       └── test/
│           └── java/{pkg}/gateway/
│
├── common/                             # Parent module for shared libraries
│   ├── build.gradle.kts
│   └── exception/                      # Exception handling library
│       ├── build.gradle.kts
│       └── src/
│           ├── main/
│           │   └── java/{pkg}/common/exception/
│           │       ├── {Name}Exception.java
│           │       ├── ResourceNotFoundException.java
│           │       ├── ValidationException.java
│           │       ├── BadRequestException.java
│           │       ├── ServiceException.java
│           │       ├── config/
│           │       │   └── ExceptionHandlingConfig.java
│           │       ├── handler/
│           │       │   └── GlobalExceptionHandler.java
│           │       └── model/
│           │           ├── ErrorCode.java
│           │           ├── ErrorCategory.java
│           │           └── ErrorResponse.java
│           └── test/
│               └── java/{pkg}/common/exception/
```

## Module Roles

| Module | Type | Role |
|--------|------|------|
| `server` | Application | Main Spring Boot application. Produces `bootJar`. Entry point. |
| `api-gateway` | Library | API controllers, request/response DTOs, validation. |
| `common:exception` | Library | Shared exception hierarchy, global handler, error models. |
| `common` | Parent | Container for common sub-modules. No source code of its own. |

## Module Dependency Graph

```
server
├── api-gateway
│   └── common:exception
└── common:exception
```

- `server` depends on both `api-gateway` and `common:exception`
- `api-gateway` depends on `common:exception`
- `common:exception` has no project dependencies (only Spring Boot starters)

## Gradle Multi-Module Patterns

### `settings.gradle.kts`

```kotlin
rootProject.name = "project-name"

include(
    "server",
    "api-gateway",
    "common",
    "common:exception"
)

// Rename nested modules for cleaner dependency references
findProject(":common:exception")?.name = "exception"
```

The `findProject` rename allows Gradle to resolve `:common:exception` correctly when it's a nested sub-project.

### Root `build.gradle.kts`

```kotlin
plugins {
    java
    checkstyle
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(libs.versions.javaVersion.get())
    }
}

// Root project doesn't need tests
tasks.withType<Test> {
    enabled = false
}
```

### Library Module Pattern (bootJar disabled)

```kotlin
// This module is a library, not a bootable application
tasks.getByName<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar") {
    enabled = false
}

tasks.getByName<Jar>("jar") {
    enabled = true
}
```

All modules except `server` use this pattern. It prevents Spring Boot from trying to package the module as an executable JAR.

### Application Module Pattern (bootJar enabled)

```kotlin
springBoot {
    mainClass.set("{basePackage}.server.{Name}Application")
}

tasks.named<BootJar>("bootJar") {
    mainClass.set(springBoot.mainClass)
    layered { enabled = true }
}
```

Only the `server` module enables `bootJar`.

### Version Catalog Usage

All modules reference dependencies through the version catalog:

```kotlin
dependencies {
    implementation(libs.springboot.web)          // Uses catalog alias
    implementation(project(":common:exception")) // Inter-module dependency
}
```

## Application Configuration

### `@SpringBootApplication` Setup

```java
@SpringBootApplication
@ComponentScan(basePackages = "{basePackage}")
@EntityScan(basePackages = "{basePackage}")
public class {Name}Application {
    public static void main(String[] args) {
        SpringApplication.run({Name}Application.class, args);
    }
}
```

- `@ComponentScan` with explicit base package ensures Spring discovers beans in all modules
- `@EntityScan` ensures JPA entities from all modules are found
- Boot 4 uses `org.springframework.boot.persistence.autoconfigure.EntityScan`

### `application.yml` Structure

```yaml
spring:
  application:
    name: {project-name}
  profiles:
    active: local

server:
  port: 8080
```
