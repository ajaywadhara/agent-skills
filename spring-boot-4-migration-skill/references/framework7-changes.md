# Spring Framework 7 Changes Reference

Complete guide for Spring Framework 7 changes affecting Spring Boot 4 applications.

---

## Overview

Spring Framework 7.0 brings:
- Jakarta EE 11 alignment (Servlet 6.1, JPA 3.2, Validation 3.1)
- JSpecify null safety annotations
- Resilience features (@Retryable, @ConcurrencyLimit)
- Spring Retry integration into core
- API versioning support
- GraalVM 25 and AOT improvements

---

## Jakarta EE 11 Requirements

### Minimum Versions

| Specification | Version | Notes |
|---------------|---------|-------|
| Jakarta Servlet | 6.1 | Tomcat 11+, Jetty 12.1+ |
| Jakarta WebSocket | 2.2 | |
| Jakarta Validation | 3.1 | |
| Jakarta Persistence | 3.2 | Hibernate 7.1+ |
| Jakarta Annotations | 3.0 | |

### Servlet Container Requirements

```xml
<!-- Tomcat 11 (default in Boot 4) -->
<!-- Automatically included with spring-boot-starter-webmvc -->

<!-- Jetty 12.1 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>

<!-- Undertow - NOT SUPPORTED (removed) -->
```

### Jakarta Package Migration

If still using `javax.*` packages:

```java
// Old (javax)
import javax.persistence.Entity;
import javax.validation.constraints.NotNull;
import javax.servlet.http.HttpServletRequest;

// New (jakarta)
import jakarta.persistence.Entity;
import jakarta.validation.constraints.NotNull;
import jakarta.servlet.http.HttpServletRequest;
```

---

## JSpecify Null Safety

### Migration from Spring Annotations

```java
// Old - Spring's nullability annotations
import org.springframework.lang.Nullable;
import org.springframework.lang.NonNull;

public class Service {
    @Nullable
    public String getValue() { return null; }

    public void process(@NonNull String input) {}
}

// New - JSpecify annotations
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;

public class Service {
    public @Nullable String getValue() { return null; }

    public void process(@NonNull String input) {}
}
```

### JSpecify Features

```java
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.NullUnmarked;
import org.jspecify.annotations.Nullable;

// Mark entire package as non-null by default
@NullMarked
package com.example.service;

// Override for specific classes
@NullUnmarked
public class LegacyService {}

// Generic types
public class Container<@Nullable T> {
    private T value;
}
```

### IDE Support

- IntelliJ IDEA 2025.3+: Compile-time warnings for null violations
- Eclipse with Spring Tools: Full JSpecify support

### Kotlin Impact

JSpecify annotations affect Kotlin's platform type inference:

```kotlin
// Java method with @Nullable
fun javaMethod(): String?  // Kotlin sees as nullable

// Java method with @NonNull
fun javaMethod(): String  // Kotlin sees as non-null
```

---

## Resilience Features

### @Retryable (from Spring Retry)

```java
import org.springframework.core.retry.annotation.Retryable;
import org.springframework.core.retry.annotation.Backoff;
import org.springframework.core.retry.annotation.Recover;

@Service
public class ResilientService {

    @Retryable(
        retryFor = {RemoteServiceException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000, multiplier = 2)
    )
    public String fetchData() {
        // May throw RemoteServiceException
        return remoteService.call();
    }

    @Recover
    public String fallback(RemoteServiceException e) {
        return "default";
    }
}
```

### @ConcurrencyLimit (New)

```java
import org.springframework.core.concurrency.ConcurrencyLimit;

@Service
public class RateLimitedService {

    @ConcurrencyLimit(permits = 10)
    public void limitedOperation() {
        // Only 10 concurrent executions allowed
    }

    @ConcurrencyLimit(permits = 5, timeout = "5s")
    public void limitedWithTimeout() {
        // Wait up to 5 seconds for permit
    }
}
```

### Enable Resilience Features

```java
@Configuration
@EnableRetry  // If using Spring Retry
public class ResilienceConfig {}
```

Or use auto-configuration:

```yaml
spring:
  retry:
    enabled: true
```

---

## Path Matching Changes

### AntPathMatcher Deprecated

```java
// Old - AntPathMatcher (deprecated)
AntPathMatcher matcher = new AntPathMatcher();
boolean matches = matcher.match("/api/**", "/api/users");

// New - PathPatternParser (preferred)
PathPatternParser parser = new PathPatternParser();
PathPattern pattern = parser.parse("/api/**");
boolean matches = pattern.matches(PathContainer.parsePath("/api/users"));
```

### Configuration

```yaml
spring:
  mvc:
    pathmatch:
      matching-strategy: path_pattern_parser  # default in 4.x
```

### Removed Behaviors

- Suffix pattern matching removed
- Trailing slash matching removed by default

```yaml
# If you need trailing slash matching
spring:
  mvc:
    servlet:
      path: /
    pathmatch:
      use-trailing-slash-match: true  # deprecated, avoid if possible
```

---

## Hibernate 7.1 Changes

### Dependency Rename

```xml
<!-- Old -->
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-jpamodelgen</artifactId>
</dependency>

<!-- New -->
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-processor</artifactId>
</dependency>
```

### Removed Dependencies

```xml
<!-- These are no longer published -->
<!-- hibernate-proxool -->
<!-- hibernate-vibur -->
```

### JPA 3.2 Features

```java
// New JPA 3.2 features available
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    // JPA 3.2 - Improved type inference
    @ElementCollection
    private Set<String> tags;
}
```

---

## Logging Changes

### spring-jcl Removed

```java
// Old - spring-jcl
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

// Still works - use commons-logging directly
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

// Or use SLF4J (recommended)
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
```

### Dependency

```xml
<!-- spring-jcl removed, use commons-logging if needed -->
<dependency>
    <groupId>commons-logging</groupId>
    <artifactId>commons-logging</artifactId>
</dependency>
```

---

## GraalVM Native Image

### Requirements

- GraalVM 25 or later
- Updated AOT processing

### RuntimeHints Registration

```java
@SpringBootApplication
@ImportRuntimeHints(MyApplication.MyRuntimeHints.class)
public class MyApplication {

    static class MyRuntimeHints implements RuntimeHintsRegistrar {
        @Override
        public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
            // Reflection hints
            hints.reflection().registerType(MyClass.class,
                MemberCategory.INVOKE_DECLARED_CONSTRUCTORS,
                MemberCategory.INVOKE_DECLARED_METHODS);

            // Resource hints
            hints.resources().registerPattern("config/*.json");

            // Proxy hints
            hints.proxies().registerJdkProxy(MyInterface.class);
        }
    }
}
```

### Build Configuration

**Maven:**
```xml
<plugin>
    <groupId>org.graalvm.buildtools</groupId>
    <artifactId>native-maven-plugin</artifactId>
</plugin>
```

**Gradle:**
```groovy
plugins {
    id 'org.graalvm.buildtools.native' version '0.10.4'
}
```

### Build Native Image

```bash
# Maven
./mvnw -Pnative native:compile

# Gradle
./gradlew nativeCompile
```

---

## HTTP Interface Clients

### Declarative HTTP Clients

```java
// Define interface
public interface UserClient {
    @GetExchange("/users/{id}")
    User getUser(@PathVariable Long id);

    @PostExchange("/users")
    User createUser(@RequestBody User user);

    @DeleteExchange("/users/{id}")
    void deleteUser(@PathVariable Long id);
}

// Create client
@Configuration
public class ClientConfig {
    @Bean
    public UserClient userClient(RestClient.Builder builder) {
        RestClient restClient = builder
            .baseUrl("https://api.example.com")
            .build();

        return HttpServiceProxyFactory
            .builderFor(RestClientAdapter.create(restClient))
            .build()
            .createClient(UserClient.class);
    }
}
```

### Auto-Configuration

```yaml
spring:
  http:
    client:
      # Configure HTTP client defaults
      connect-timeout: 5s
      read-timeout: 30s
```

---

## Validation Changes

### Jakarta Validation 3.1

```java
import jakarta.validation.constraints.*;

public class CreateUserRequest {
    @NotBlank
    @Size(min = 2, max = 100)
    private String name;

    @Email
    @NotNull
    private String email;

    // New in Validation 3.1 - improved container element validation
    @NotEmpty
    private List<@NotBlank String> roles;
}
```

---

## Migration Checklist

- [ ] Verify servlet container compatibility (Tomcat 11+, Jetty 12.1+)
- [ ] Complete javax.* to jakarta.* migration
- [ ] Update Spring nullability annotations to JSpecify
- [ ] Review Kotlin code for JSpecify impact
- [ ] Update AntPathMatcher to PathPatternParser if using directly
- [ ] Rename hibernate-jpamodelgen to hibernate-processor
- [ ] Remove hibernate-proxool/vibur if used
- [ ] Update logging if using spring-jcl directly
- [ ] Review resilience patterns (@Retryable, @ConcurrencyLimit)
- [ ] Update GraalVM to version 25+
- [ ] Register RuntimeHints for native image if applicable
- [ ] Test HTTP interface clients
- [ ] Verify validation constraints work correctly
