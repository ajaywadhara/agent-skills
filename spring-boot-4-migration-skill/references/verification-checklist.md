# Migration Verification Checklist

Complete checklist for verifying Spring Boot 3.x to 4.x migration.

---

## Pre-Migration Verification

### Baseline Checks

- [ ] Currently on Spring Boot 3.5.x (latest patch)
- [ ] All deprecation warnings addressed
- [ ] Full test suite passes
- [ ] Application starts and runs correctly
- [ ] Git branch created for migration
- [ ] Dependencies documented

### Environment Requirements

- [ ] Java 17+ installed (21+ recommended)
- [ ] Maven 3.6.3+ or Gradle 8.14+
- [ ] Kotlin 2.2+ (if using Kotlin)
- [ ] GraalVM 25+ (if using native images)

---

## Build File Verification

### Version Updates

- [ ] Spring Boot parent/plugin version is 4.0.x
- [ ] Java version property set to 17 or 21
- [ ] Kotlin version is 2.2+ (if applicable)
- [ ] Gradle wrapper version is 8.14+ or 9.x

### Starter Changes

- [ ] `spring-boot-starter-web` → `spring-boot-starter-webmvc`
- [ ] `spring-boot-starter-web-services` → `spring-boot-starter-webservices`
- [ ] OAuth2 starters have `security-` prefix
- [ ] `spring-boot-starter-aop` → `spring-boot-starter-aspectj`

### New Required Starters

- [ ] `spring-boot-starter-flyway` (if using Flyway)
- [ ] `spring-boot-starter-liquibase` (if using Liquibase)
- [ ] `spring-boot-starter-security-test` (if using `@WithMockUser`)
- [ ] `spring-boot-starter-batch-jdbc` (if using Spring Batch with DB)
- [ ] Test starters for each technology under test

### Removed Dependencies

- [ ] No Undertow dependency
- [ ] No JUnit 4 dependency
- [ ] No Spring Session Hazelcast/MongoDB (now external)
- [ ] No Reactive Pulsar

---

## Code Verification

### Package Imports

- [ ] `@EntityScan` from `org.springframework.boot.persistence.autoconfigure`
- [ ] `EnvironmentPostProcessor` from `org.springframework.boot`
- [ ] `BootstrapRegistry` from `org.springframework.boot.bootstrap`
- [ ] JSpecify annotations instead of `org.springframework.lang.*`
- [ ] Jackson 3 imports (`tools.jackson.*`)

### Testing Annotations

- [ ] `@MockBean` → `@MockitoBean`
- [ ] `@SpyBean` → `@MockitoSpyBean`
- [ ] Mocks not in `@Configuration` classes
- [ ] `@AutoConfigureMockMvc` added where needed
- [ ] `@AutoConfigureRestTestClient` for RestTestClient
- [ ] HtmlUnit config uses nested `@HtmlUnit` annotation

### Security Configuration

- [ ] No `.and()` chaining in HttpSecurity
- [ ] Using `authorizeHttpRequests()` not `authorizeRequests()`
- [ ] Using `requestMatchers()` not `antMatchers()`
- [ ] Lambda-style configuration throughout

### Jackson Configuration

- [ ] `@JsonComponent` → `@JacksonComponent`
- [ ] `@JsonMixin` → `@JacksonMixin`
- [ ] Custom serializers extend `ObjectValueSerializer`
- [ ] Custom deserializers extend `ObjectValueDeserializer`
- [ ] Using `JsonMapperBuilderCustomizer` for customization

---

## Property Verification

### Renamed Properties

- [ ] `spring.persistence.exceptiontranslation.enabled` (not `dao`)
- [ ] `spring.session.data.redis.*` (not `session.redis`)
- [ ] `management.tracing.export.enabled` (not `tracing.enabled`)
- [ ] `management.health.mongodb.enabled` (not `mongo`)
- [ ] Jackson properties under `spring.jackson.json.*`

### Removed Properties

- [ ] No SignalFX properties
- [ ] No template engine `enabled` properties (use dependencies instead)

### New Properties (if needed)

- [ ] `logging.console.enabled` for console logging control
- [ ] `spring.devtools.livereload.enabled` (disabled by default now)
- [ ] `management.endpoint.health.probes.enabled` awareness

---

## Compilation & Build

### Successful Compilation

```bash
# Maven
./mvnw clean compile

# Gradle
./gradlew clean compileJava
```

- [ ] No compilation errors
- [ ] No unresolved imports
- [ ] All deprecated API calls updated

### Successful Test Build

```bash
# Maven
./mvnw test-compile

# Gradle
./gradlew compileTestJava
```

- [ ] Test classes compile
- [ ] Test dependencies resolved

---

## Test Execution

### Unit Tests

```bash
# Maven
./mvnw test

# Gradle
./gradlew test
```

- [ ] All unit tests pass
- [ ] No JUnit 4 errors
- [ ] MockitoBean/MockitoSpyBean work correctly

### Integration Tests

```bash
# Maven
./mvnw verify

# Gradle
./gradlew integrationTest
```

- [ ] All integration tests pass
- [ ] Testcontainers 2.x compatible
- [ ] Database tests work

---

## Runtime Verification

### Application Startup

```bash
# Maven
./mvnw spring-boot:run

# Gradle
./gradlew bootRun
```

- [ ] Application starts without errors
- [ ] No missing bean errors
- [ ] No auto-configuration failures
- [ ] Startup time acceptable

### Actuator Endpoints

```bash
curl http://localhost:8080/actuator/health
curl http://localhost:8080/actuator/info
```

- [ ] Health endpoint responds
- [ ] Liveness probe: `/actuator/health/liveness`
- [ ] Readiness probe: `/actuator/health/readiness`

### API Endpoints

- [ ] All REST endpoints accessible
- [ ] Authentication/Authorization works
- [ ] JSON serialization correct (dates, etc.)
- [ ] Request validation works

### Database Operations

- [ ] Connections established
- [ ] Queries execute correctly
- [ ] Transactions work
- [ ] Entity mapping correct

### Messaging (if applicable)

- [ ] Kafka consumers/producers work
- [ ] RabbitMQ listeners work
- [ ] JMS operations work

### Scheduled Tasks (if applicable)

- [ ] `@Scheduled` methods execute
- [ ] Cron expressions work
- [ ] No timing issues

---

## Security Verification

### Authentication

- [ ] Login/logout works
- [ ] JWT validation works (if using)
- [ ] OAuth2 flows work (if using)
- [ ] Session management correct

### Authorization

- [ ] Role-based access works
- [ ] Method security (`@PreAuthorize`) works
- [ ] URL-based security works

---

## Observability Verification

### Metrics

- [ ] Metrics exported correctly
- [ ] Custom metrics work
- [ ] `@Timed`/`@Counted` annotations work

### Tracing

- [ ] Traces exported correctly
- [ ] Trace IDs in logs
- [ ] Distributed tracing works

### Logging

- [ ] Log levels correct
- [ ] Structured logging works (if enabled)
- [ ] Log rotation works

---

## Bridge Cleanup (Post-Migration)

### Compatibility Bridges to Remove

- [ ] Remove `spring-boot-starter-classic`
- [ ] Remove `spring-boot-starter-test-classic`
- [ ] Remove `spring-boot-jackson2`
- [ ] Remove `spring-security-access` (if using)

### After Bridge Removal

- [ ] Re-run all verifications
- [ ] Confirm no runtime errors
- [ ] Performance acceptable

---

## Documentation Updates

- [ ] README updated with new requirements
- [ ] Migration notes documented
- [ ] Breaking changes documented
- [ ] Runbook updated (if applicable)

---

## Final Sign-off

- [ ] All FAIL items resolved
- [ ] All WARN items reviewed
- [ ] All BRIDGE items have removal plan
- [ ] Stakeholder approval obtained
- [ ] Ready for deployment

---

## Quick Verification Commands

```bash
# Run automated verification script
./scripts/verify-migration.sh

# Quick compile check
./mvnw clean compile -q && echo "Compile: OK" || echo "Compile: FAILED"

# Quick test check
./mvnw test -q && echo "Tests: OK" || echo "Tests: FAILED"

# Dependency tree (check for conflicts)
./mvnw dependency:tree > deps.txt

# Find deprecated imports
grep -r "org.springframework.boot.test.mock.mockito" --include="*.java" src/

# Find Jackson 2 imports
grep -r "com.fasterxml.jackson.databind" --include="*.java" src/

# Find javax imports
grep -r "import javax\." --include="*.java" src/ | grep -v "javax.crypto\|javax.net"
```
