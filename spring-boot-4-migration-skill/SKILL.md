---
name: spring-boot-4-migration-skill
description: A comprehensive, modular skill for migrating Spring Boot applications from 3.x to 4.x.
---

# Spring Boot 4.x Migration Skill

A comprehensive, modular skill for migrating Spring Boot applications from 3.x to 4.x.

## Activation Patterns

This skill activates when the user mentions:
- "Migrate to Spring Boot 4"
- "Upgrade Spring Boot 3 to 4"
- "Spring Boot 4 migration"
- "Update to Boot 4"
- "Spring Boot 4.x upgrade"
- "Modernize Spring Boot application"

---

## Pre-Migration Assessment

Before starting migration, perform these checks:

### 1. Toolchain Verification

```bash
# Check Java version (17+ required, 21+ recommended)
java -version

# Check build tool version
mvn -version  # Maven 3.6.3+ required
gradle -version  # Gradle 8.14+ required (9.x supported)

# Check Kotlin version if applicable (2.2+ required)
kotlin -version
```

### 2. Current Version Assessment

**For Maven:**
```bash
grep -E '<version>.*</version>' pom.xml | head -20
grep 'spring-boot' pom.xml
```

**For Gradle:**
```bash
grep -E "springBoot|org.springframework.boot" build.gradle* settings.gradle*
```

### 3. Upgrade Path Determination

| Current Version | Recommended Path |
|-----------------|------------------|
| 3.0.x - 3.4.x | First upgrade to 3.5.x, then to 4.0.x |
| 3.5.x | Direct upgrade to 4.0.x |
| 2.x or earlier | Upgrade to 3.5.x first (separate migration) |

---

## Migration Strategies

### Strategy A: Gradual Migration

Uses compatibility bridges for incremental adoption. Teams can work on six independent tracks:

1. **Starters Track** - Migrate to modular starters
2. **Jackson Track** - Migrate from Jackson 2 to 3
3. **Properties Track** - Update configuration properties
4. **Security Track** - Migrate to Spring Security 7
5. **Testing Track** - Update test infrastructure
6. **Framework Track** - Address Spring Framework 7 changes

**Enable bridges:**
```xml
<!-- Maven: Add to pom.xml for gradual migration -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-classic</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test-classic</artifactId>
    <scope>test</scope>
</dependency>
```

```groovy
// Gradle: Add to build.gradle for gradual migration
implementation 'org.springframework.boot:spring-boot-starter-classic'
testImplementation 'org.springframework.boot:spring-boot-starter-test-classic'
```

### Strategy B: All-at-Once Migration

Execute all 10 phases sequentially. Best for smaller codebases or dedicated migration sprints.

---

## Migration Phases

### Phase 1: Pre-Migration Preparation

**Actions:**
1. Ensure on latest 3.5.x version
2. Fix all deprecation warnings
3. Run full test suite - must pass
4. Create backup/branch

**Commands:**
```bash
# Create migration branch
git checkout -b spring-boot-4-migration

# Run tests to establish baseline
./mvnw clean test  # Maven
./gradlew clean test  # Gradle
```

**Reference:** [pre-migration.md](references/pre-migration.md)

---

### Phase 2: Build File Migration

**Maven Changes:**
```xml
<!-- Update parent version -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.0.0</version>
</parent>

<!-- Update Java version -->
<properties>
    <java.version>21</java.version>
</properties>
```

**Gradle Changes:**
```groovy
plugins {
    id 'org.springframework.boot' version '4.0.0'
    id 'io.spring.dependency-management' version '1.1.7'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

**Starter Changes by Category:**

*Web & API:*
| Old Starter | New Starter |
|-------------|-------------|
| `spring-boot-starter-web` | `spring-boot-starter-webmvc` |
| `spring-boot-starter-web-services` | `spring-boot-starter-webservices` |

*Security:*
| Old Starter | New Starter |
|-------------|-------------|
| `spring-boot-starter-oauth2-client` | `spring-boot-starter-security-oauth2-client` |
| `spring-boot-starter-oauth2-resource-server` | `spring-boot-starter-security-oauth2-resource-server` |
| `spring-boot-starter-oauth2-authorization-server` | `spring-boot-starter-security-oauth2-authorization-server` |
| `spring-boot-starter-saml2-service-provider` | `spring-boot-starter-security-saml2-service-provider` |
| N/A | `spring-boot-starter-security-test` (NEW - required for @WithMockUser) |

*Database & Migrations:*
| Old Starter | New Starter |
|-------------|-------------|
| `flyway-core` (direct) | `spring-boot-starter-flyway` (NEW starter) |
| `liquibase-core` (direct) | `spring-boot-starter-liquibase` (NEW starter) |

*Batch:*
| Old Starter | New Starter |
|-------------|-------------|
| N/A | `spring-boot-starter-batch-jdbc` (NEW - required for DB metadata) |
| N/A | `spring-boot-starter-batch-mongodb` (NEW - for MongoDB metadata) |

*Observability:*
| Old Starter | New Starter |
|-------------|-------------|
| Multiple OTel deps | `spring-boot-starter-opentelemetry` (NEW unified starter) |

*AOP:*
| Old Starter | New Starter |
|-------------|-------------|
| `spring-boot-starter-aop` | `spring-boot-starter-aspectj` |

*Serialization:*
| Old Starter | New Starter |
|-------------|-------------|
| N/A | `spring-boot-starter-kotlin-serialization` (NEW) |

*Servlet Containers:*
| Old Starter | New Starter |
|-------------|-------------|
| `spring-boot-starter-undertow` | REMOVED - use `spring-boot-starter-jetty` |

*Testing:*
| Old Starter | New Starter |
|-------------|-------------|
| N/A | `spring-boot-starter-webmvc-test` (NEW) |
| N/A | `spring-boot-starter-data-jpa-test` (NEW) |
| N/A | `spring-boot-starter-data-mongodb-test` (NEW) |

*Session (Removed - Now External):*
| Old Starter | Alternative |
|-------------|-------------|
| `spring-session-hazelcast` | Hazelcast-provided module |
| `spring-session-mongodb` | MongoDB-provided module |

*Migration Bridges (Temporary):*
| Starter | Purpose |
|---------|---------|
| `spring-boot-starter-classic` | All 3.x auto-configurations |
| `spring-boot-starter-test-classic` | All 3.x test configurations |
| `spring-boot-jackson2` | Jackson 2.x compatibility |

**Reference:** [build-migration.md](references/build-migration.md) - Complete starter reference with examples

---

### Phase 3: Property Migration

**Renamed Properties:**

| Old Property | New Property |
|--------------|--------------|
| `spring.dao.exceptiontranslation.enabled` | `spring.persistence.exceptiontranslation.enabled` |
| `spring.session.redis.*` | `spring.session.data.redis.*` |
| `spring.session.mongodb.*` | `spring.session.data.mongodb.*` |
| `management.tracing.enabled` | `management.tracing.export.enabled` |
| `management.health.mongo.enabled` | `management.health.mongodb.enabled` |
| `management.metrics.mongo.*` | `management.metrics.mongodb.*` |
| `spring.kafka.retry.topic.backoff.random` | `spring.kafka.retry.topic.backoff.jitter` |

**Jackson Property Restructuring:**
```yaml
# Old (3.x)
spring:
  jackson:
    read:
      ACCEPT_FLOAT_AS_INT: true
    write:
      INDENT_OUTPUT: true

# New (4.x)
spring:
  jackson:
    json:
      read:
        ACCEPT_FLOAT_AS_INT: true
      write:
        INDENT_OUTPUT: true
```
**Reference:** [property-changes.md](references/property-changes.md)

---

### Phase 4: Jackson 3 Migration

**Package Changes:**
```java
// Old imports (Jackson 2)
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

// New imports (Jackson 3)
import tools.jackson.databind.ObjectMapper;
import tools.jackson.databind.JsonNode;

// EXCEPTION: Annotations stay the same
import com.fasterxml.jackson.annotation.JsonProperty;  // Unchanged
```

**Class Renames:**
```java
// Old
@JsonComponent
public class MySerializer extends JsonObjectSerializer<MyType> {}

// New
@JacksonComponent
public class MySerializer extends ObjectValueSerializer<MyType> {}
```

**Builder Pattern Changes:**
```java
// Old (3.x)
ObjectMapper mapper = Jackson2ObjectMapperBuilder.json()
    .featuresToEnable(SerializationFeature.INDENT_OUTPUT)
    .build();

// New (4.x)
JsonMapper mapper = JsonMapper.builder()
    .enable(StreamWriteFeature.INDENT_OUTPUT)
    .build();

// Or use Spring's customizer
@Bean
public JsonMapperBuilderCustomizer customizer() {
    return builder -> builder.enable(StreamWriteFeature.INDENT_OUTPUT);
}
```

**Default Behavior Changes:**

| Feature | Jackson 2 Default | Jackson 3 Default |
|---------|-------------------|-------------------|
| `SORT_PROPERTIES_ALPHABETICALLY` | false | true |
| `WRITE_DATES_AS_TIMESTAMPS` | true | false (ISO-8601) |
| `FAIL_ON_NULL_FOR_PRIMITIVES` | false | true |
| `FAIL_ON_TRAILING_TOKENS` | false | true |

**Temporary Jackson 2 Compatibility:**
```yaml
# Keep Jackson 2 behavior during migration
spring:
  jackson:
    use-jackson2-defaults: true
```

**Reference:** [jackson3-migration.md](references/jackson3-migration.md)

---

### Phase 5: Package and API Relocations

**Key Package Moves:**

| Old Package | New Package |
|-------------|-------------|
| `org.springframework.boot.autoconfigure.domain.EntityScan` | `org.springframework.boot.persistence.autoconfigure.EntityScan` |
| `org.springframework.boot.env.EnvironmentPostProcessor` | `org.springframework.boot.EnvironmentPostProcessor` |
| `org.springframework.boot.BootstrapRegistry` | `org.springframework.boot.bootstrap.BootstrapRegistry` |
| `org.springframework.boot.test.web.client.TestRestTemplate` | `org.springframework.boot.resttestclient.TestRestTemplate` |
| `org.springframework.boot.test.autoconfigure.properties.PropertyMapping` | `org.springframework.boot.test.context.PropertyMapping` |

**Removed APIs:**

```java
// PropertyMapper - removed method
// Old
PropertyMapper map = PropertyMapper.get().alwaysApplyingNotNull();

// New - use always() for null handling
PropertyMapper map = PropertyMapper.get();
map.from(source::getValue).always().to(destination::setValue);
```

**Reference:** [api-changes.md](references/api-changes.md)

---

### Phase 6: Spring Security 7 Migration

**DSL Changes:**
```java
// Old (Security 6.x) - and() chaining
http
    .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
    .and()
    .formLogin();

// New (Security 7.x) - Lambda only
http
    .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
    .formLogin(Customizer.withDefaults());
```

**Authorization Changes:**
```java
// Old - authorizeRequests
http.authorizeRequests()
    .antMatchers("/api/**").hasRole("USER");

// New - authorizeHttpRequests with requestMatchers
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/**").hasRole("USER"));
```

**Request Matcher Updates:**
```java
// Old - AntPathRequestMatcher
new AntPathRequestMatcher("/api/**")

// New - PathPatternRequestMatcher (preferred)
PathPatternRequestMatcher.pathPattern("/api/**")
```

**Jackson Module for Security:**
```java
// Old (Jackson 2)
ObjectMapper mapper = new ObjectMapper();
mapper.registerModules(SecurityJackson2Modules.getModules(classLoader));

// New (Jackson 3)
JsonMapper.Builder builder = JsonMapper.builder();
SecurityJacksonModules.configure(builder);
JsonMapper mapper = builder.build();
```

**Reference:** [security7-migration.md](references/security7-migration.md)

---

### Phase 7: Testing Infrastructure Migration

**MockBean/SpyBean Replacement:**
```java
// Old (deprecated in 3.4, removed in 4.0)
@MockBean
private UserService userService;

@SpyBean
private OrderService orderService;

// New
@MockitoBean
private UserService userService;

@MockitoSpyBean
private OrderService orderService;
```

**Shared Mocks (No Longer in @Configuration):**
```java
// Old - mocks in @TestConfiguration
@TestConfiguration
static class MockConfig {
    @MockBean UserService userService;
}

// New - annotation on test class
@SpringBootTest
@MockitoBean(types = {UserService.class, OrderService.class})
class ApplicationTests {
}

// Or create custom annotation
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@MockitoBean(types = {UserService.class})
public @interface SharedMocks {}
```

**@SpringBootTest Changes:**
```java
// Old - MockMvc auto-configured
@SpringBootTest
class MyTest {
    @Autowired MockMvc mockMvc;  // Was auto-configured
}

// New - Explicit configuration required
@SpringBootTest
@AutoConfigureMockMvc
class MyTest {
    @Autowired MockMvc mockMvc;
}

// For RestTestClient
@SpringBootTest
@AutoConfigureRestTestClient
class MyTest {
    @Autowired RestTestClient restTestClient;
}
```

**HtmlUnit Configuration:**
```java
// Old
@AutoConfigureMockMvc(webClientEnabled = false, webDriverEnabled = false)

// New
@AutoConfigureMockMvc(htmlUnit = @HtmlUnit(webClient = false, webDriver = false))
```

**JUnit 6 Migration:**
- Most JUnit 5 code works unchanged
- Remove JUnit 4 dependencies entirely
- Update Testcontainers to 2.x

**Reference:** [testing-migration.md](references/testing-migration.md)

---

### Phase 8: Observability Migration

**New OpenTelemetry Starter:**
```xml
<!-- Replace individual Micrometer/OTel dependencies -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

**Configuration:**
```yaml
management:
  otlp:
    metrics:
      export:
        url: http://localhost:4318/v1/metrics
  opentelemetry:
    tracing:
      export:
        otlp:
          endpoint: http://localhost:4318/v1/traces
  observations:
    annotations:
      enabled: true  # Enable @Observed, @Timed, @Counted
```

**Redis Observability Change:**
```java
// Old
MicrometerCommandLatencyRecorder recorder;

// New
MicrometerTracing tracing;
```

**Reference:** [observability-migration.md](references/observability-migration.md)

---

### Phase 9: Spring Framework 7 Changes

**JSpecify Null Safety:**
```java
// Old Spring annotations
import org.springframework.lang.Nullable;
import org.springframework.lang.NonNull;

// New JSpecify annotations
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;
```

**Resilience (from Spring Retry):**
```java
// Retry moved to Spring Framework core
import org.springframework.core.retry.Retryable;

@Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000))
public String fetchData() { ... }

// New concurrency limit
@ConcurrencyLimit(permits = 10)
public void limitedOperation() { ... }
```

**Hibernate 7.1 Changes:**
```xml
<!-- Dependency rename -->
<!-- Old -->
<artifactId>hibernate-jpamodelgen</artifactId>
<!-- New -->
<artifactId>hibernate-processor</artifactId>
```

**Reference:** [framework7-changes.md](references/framework7-changes.md)

---

### Phase 10: Verification and Cleanup

**Run Verification Script:**
```bash
./scripts/verify-migration.sh
```

**Manual Verification Checklist:**

- [ ] Application starts without errors
- [ ] All tests pass
- [ ] Actuator endpoints respond (`/actuator/health`)
- [ ] Authentication/Authorization works
- [ ] API endpoints respond correctly
- [ ] Database operations work
- [ ] Message queue operations work (if applicable)
- [ ] Scheduled tasks execute (if applicable)
- [ ] No deprecation warnings in critical paths

**Remove Compatibility Bridges:**
```xml
<!-- Remove after full migration -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-classic</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-jackson2</artifactId>
</dependency>
```

**Reference:** [verification-checklist.md](references/verification-checklist.md)

---

## Automation with OpenRewrite

**Maven:**
```xml
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>6.28.0</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-spring</artifactId>
            <version>6.23.0</version>
        </dependency>
    </dependencies>
</plugin>
```

Run: `mvn rewrite:run`

**Gradle:**
```groovy
plugins {
    id 'org.openrewrite.rewrite' version '7.3.0'
}

rewrite {
    activeRecipe('org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0')
}

dependencies {
    rewrite 'org.openrewrite.recipe:rewrite-spring:6.23.0'
}
```

Run: `./gradlew rewriteRun`

---

## Rollback Strategy

If migration fails:

1. **Immediate Rollback:**
   ```bash
   git checkout main  # or your stable branch
   ```

2. **Partial Rollback (if using bridges):**
   - Keep `spring-boot-starter-classic`
   - Revert specific failing modules
   - Continue incremental migration

3. **Document Blockers:**
   - Note which phase failed
   - Capture error messages
   - Check compatibility matrix for dependencies

---

## Support Timeline

| Version | OSS Support Until | Commercial Support Until |
|---------|-------------------|--------------------------|
| Spring Boot 3.4 | December 2025 | - |
| Spring Boot 3.5 | June 2026 | June 2032 |
| Spring Boot 4.0 | November 2026 | November 2032 |

---

## Quick Reference

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

**Servlet Containers:**
- Tomcat 11+
- Jetty 12.1+
- Undertow: **NOT SUPPORTED** (removed)
