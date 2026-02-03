# Pre-Migration Reference

Complete guide for preparing Spring Boot 3.x applications for migration to 4.x.

---

## Upgrade Path

### Recommended Path

```
Spring Boot 2.x
      ↓
Spring Boot 3.0.x → 3.5.x (incremental)
      ↓
Spring Boot 3.5.x (latest patch)
      ↓
Spring Boot 4.0.x
```

**Do not skip directly from 2.x or 3.0-3.4 to 4.0.**

### Why 3.5.x First?

1. **Deprecation Warnings**: 3.5.x deprecates APIs removed in 4.0
2. **Migration Bridges**: Some bridges introduced in 3.5
3. **Stable Foundation**: Latest 3.x features before major upgrade
4. **Smaller Jumps**: Easier to debug issues

---

## Environment Preparation

### Java Version

```bash
# Check current version
java -version

# Required: Java 17+
# Recommended: Java 21 (LTS)

# Install Java 21 (example using SDKMAN)
sdk install java 21-tem
sdk use java 21-tem
```

### Build Tool Version

**Maven:**
```bash
# Check version
mvn -version

# Required: 3.6.3+
# Update wrapper
mvn wrapper:wrapper -Dmaven=3.9.6
```

**Gradle:**
```bash
# Check version
./gradlew --version

# Required: 8.14+
# Update wrapper
./gradlew wrapper --gradle-version=8.14
```

### Kotlin Version (if applicable)

```bash
# Required: 2.2+
kotlin -version
```

---

## Code Preparation

### Fix Deprecation Warnings

**Enable deprecation warnings:**

```xml
<!-- Maven -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <compilerArgs>
            <arg>-Xlint:deprecation</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

```groovy
// Gradle
tasks.withType(JavaCompile) {
    options.deprecation = true
}
```

**Build and review warnings:**
```bash
./mvnw clean compile 2>&1 | grep -i deprecat
```

### Common Deprecations to Fix

| Deprecated (3.x) | Replacement |
|------------------|-------------|
| `@MockBean` | `@MockitoBean` (available in 3.4+) |
| `@SpyBean` | `@MockitoSpyBean` (available in 3.4+) |
| `ObjectMapper` direct construction | `Jackson2ObjectMapperBuilder` |
| `authorizeRequests()` | `authorizeHttpRequests()` |
| `antMatchers()` | `requestMatchers()` |
| `.and()` in Security DSL | Lambda configuration |

---

## Dependency Audit

### Generate Dependency Report

```bash
# Maven
./mvnw dependency:tree > dependencies.txt
./mvnw versions:display-dependency-updates > updates.txt

# Gradle
./gradlew dependencies > dependencies.txt
./gradlew dependencyUpdates > updates.txt
```

### Check for Incompatible Dependencies

**Known incompatible in 4.0:**
- Undertow (any version)
- JUnit 4
- Spring Session Hazelcast (community version)
- Spring Session MongoDB (community version)
- Spock Framework (pre-Groovy 5 compatibility)

### Check Third-Party Library Compatibility

For each significant dependency, check:
1. Does it support Jakarta EE 11?
2. Does it support Spring Boot 4 / Spring Framework 7?
3. Is there a newer version?

---

## Test Suite Preparation

### Ensure High Test Coverage

```bash
# Run with coverage
./mvnw test jacoco:report
```

- Aim for 70%+ line coverage
- Critical paths should have integration tests

### Update Test Dependencies

```xml
<!-- Ensure using JUnit 5 -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>

<!-- Remove JUnit 4 -->
<!-- <dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
</dependency> -->
```

### Migrate JUnit 4 Tests

```java
// JUnit 4
import org.junit.Test;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class MyTest {
    @Before
    public void setUp() {}

    @Test
    public void testSomething() {}
}

// JUnit 5
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
// No @RunWith needed with @SpringBootTest

@SpringBootTest
class MyTest {
    @BeforeEach
    void setUp() {}

    @Test
    void testSomething() {}
}
```

---

## Configuration Preparation

### Audit Properties

Review all property files:
- `application.yml`
- `application.properties`
- `application-*.yml` (profiles)
- `bootstrap.yml` (if using)

### Document Custom Configurations

List all:
- `@Configuration` classes
- `@Bean` definitions
- Property bindings
- Auto-configuration exclusions

### Check for XML Configuration

XML configuration is less common but should be migrated:

```java
// If using @ImportResource
@ImportResource("classpath:legacy-config.xml")

// Consider migrating to Java config
@Configuration
public class LegacyConfig {
    // Migrate beans here
}
```

---

## Security Audit

### Review Security Configuration

```java
// Ensure using modern DSL
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        // Use lambda style
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .anyRequest().authenticated()
        )
        // Use Customizer.withDefaults() or lambda
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

### Check for Deprecated Security APIs

- `WebSecurityConfigurerAdapter` (removed in 6.0)
- `antMatchers()` (use `requestMatchers()`)
- `authorizeRequests()` (use `authorizeHttpRequests()`)
- `.and()` chaining

---

## Database Preparation

### Hibernate/JPA

Check entity mappings:
```java
// Ensure using jakarta.persistence
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class MyEntity {
    @Id
    private Long id;
}
```

### Flyway/Liquibase

- Document current migration state
- Ensure all migrations applied
- No pending migrations

---

## Create Migration Branch

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b spring-boot-4-migration

# Create initial commit
git commit --allow-empty -m "Start Spring Boot 4 migration"
```

---

## Backup and Rollback Plan

### Backup Strategies

1. **Git Branch**: Keep main branch stable
2. **Database Snapshots**: If schema changes needed
3. **Configuration Backup**: Export current configs

### Rollback Steps

If migration fails:
```bash
# Return to stable branch
git checkout main

# If deployed, revert deployment
# (deployment-specific commands)
```

---

## Migration Checklist

### Environment Ready

- [ ] Java 17+ installed (21+ recommended)
- [ ] Maven 3.6.3+ or Gradle 8.14+
- [ ] Kotlin 2.2+ (if using)
- [ ] IDE updated (IntelliJ 2025.3+, Eclipse with Spring Tools)

### Codebase Ready

- [ ] On Spring Boot 3.5.x (latest patch)
- [ ] All deprecation warnings fixed
- [ ] All tests passing (70%+ coverage)
- [ ] JUnit 5 (no JUnit 4)
- [ ] Modern Security DSL (lambda style)
- [ ] jakarta.* packages (not javax.*)

### Dependencies Ready

- [ ] Dependency audit complete
- [ ] No incompatible dependencies
- [ ] Third-party compatibility verified

### Documentation Ready

- [ ] Current configurations documented
- [ ] Custom beans documented
- [ ] Breaking changes identified
- [ ] Rollback plan in place

### Team Ready

- [ ] Team aware of migration
- [ ] Migration timeline agreed
- [ ] Testing resources allocated

---

## Estimated Effort

| Application Size | Estimated Time |
|------------------|----------------|
| Small (< 10 controllers) | 1-2 days |
| Medium (10-50 controllers) | 3-5 days |
| Large (50+ controllers) | 1-2 weeks |
| Enterprise (multiple modules) | 2-4 weeks |

Factors affecting time:
- Number of deprecated APIs used
- Custom Jackson configuration
- Complex security setup
- Native image support
- Test coverage (lower = more risk/time)
