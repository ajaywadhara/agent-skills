# Spring Boot 4 Dependencies Reference

## Version Catalog (`gradle/libs.versions.toml`)

The scaffolder generates a Gradle version catalog with these dependency versions:

### Versions

| Dependency | Version | Notes |
|-----------|---------|-------|
| Spring Boot | 4.0.0 | Boot 4.x release |
| Spring Boot Gradle Plugin | 4.0.0 | Must match Boot version |
| Spring Dependency Management | 1.1.7 | `io.spring.dependency-management` plugin |
| Java | 21 | Minimum for Boot 4 |
| Lombok | 1.18.36 | Annotation processor |
| PostgreSQL Driver | 42.7.2 | JDBC driver |

### Generated `libs.versions.toml`

```toml
[versions]
spring-boot = "4.0.0"
spring-boot-gradle-plugin = "4.0.0"
spring-dm-plugin = "1.1.7"
javaVersion = "21"
lombokVersion = "1.18.36"
postgresqlVersion = "42.7.2"

[libraries]
springboot-dependencies = { module = "org.springframework.boot:spring-boot-dependencies", version.ref = "spring-boot" }
springboot-web = { module = "org.springframework.boot:spring-boot-starter-webmvc" }
springboot-actuator = { module = "org.springframework.boot:spring-boot-starter-actuator" }
springboot-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
springboot-validation = { module = "org.springframework.boot:spring-boot-starter-validation" }
springboot-security = { module = "org.springframework.boot:spring-boot-starter-security" }
springboot-test = { module = "org.springframework.boot:spring-boot-starter-test" }
springboot-webmvc-test = { module = "org.springframework.boot:spring-boot-starter-webmvc-test" }
springboot-devtools = { module = "org.springframework.boot:spring-boot-devtools" }
spring-boot-configuration-processor = { module = "org.springframework.boot:spring-boot-configuration-processor" }
postgresql = { module = "org.postgresql:postgresql", version.ref = "postgresqlVersion" }
lombok = { module = "org.projectlombok:lombok", version.ref = "lombokVersion" }
junitplatform-launcher = { module = "org.junit.platform:junit-platform-launcher" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot-gradle-plugin" }
spring-dm = { id = "io.spring.dependency-management", version.ref = "spring-dm-plugin" }
```

## Boot 4 Specifics

### Starter Renames

| Boot 3.x | Boot 4.x |
|----------|----------|
| `spring-boot-starter-web` | `spring-boot-starter-webmvc` |
| `spring-boot-starter-aop` | `spring-boot-starter-aspectj` |
| `spring-boot-starter-web-services` | `spring-boot-starter-webservices` |

The scaffolder uses `starter-webmvc` (Boot 4 convention), not `starter-web`.

### EntityScan Import Change

```java
// Boot 3.x
import org.springframework.boot.autoconfigure.domain.EntityScan;

// Boot 4.x
import org.springframework.boot.persistence.autoconfigure.EntityScan;
```

## Module Dependency Breakdown

### `server` module
- `spring-boot-starter-webmvc` — Web MVC
- `spring-boot-starter-actuator` — Health/metrics endpoints
- `spring-boot-starter-data-jpa` — JPA/Hibernate
- `spring-boot-starter-test` — Test framework
- `spring-boot-starter-webmvc-test` — MockMvc testing
- `spring-boot-devtools` — Dev-time reloading
- `postgresql` — Database driver (runtime)
- Project dependencies: `:api-gateway`, `:common:exception`

### `api-gateway` module
- `spring-boot-starter-webmvc` — Web MVC
- `spring-boot-starter-validation` — Bean validation
- `spring-boot-starter-test` — Test framework
- `lombok` — Boilerplate reduction
- Project dependency: `:common:exception`

### `common:exception` module
- `spring-boot-starter-webmvc` — Web MVC (for `@RestControllerAdvice`)
- `spring-boot-starter-validation` — Bean validation (for constraint violation handling)
- `spring-boot-starter-security` — Security (for `AccessDeniedException` handling)
- `spring-boot-configuration-processor` — Config metadata
- `spring-boot-starter-test` — Test framework
- `lombok` — Boilerplate reduction
