# API and Package Changes Reference

Complete guide for API changes, package relocations, and removed classes from Spring Boot 3.x to 4.x.

---

## Package Relocations

### Core Classes

| Old Location (3.x) | New Location (4.x) |
|--------------------|---------------------|
| `org.springframework.boot.env.EnvironmentPostProcessor` | `org.springframework.boot.EnvironmentPostProcessor` |
| `org.springframework.boot.BootstrapRegistry` | `org.springframework.boot.bootstrap.BootstrapRegistry` |
| `org.springframework.boot.BootstrapContext` | `org.springframework.boot.bootstrap.BootstrapContext` |
| `org.springframework.boot.BootstrapRegistryInitializer` | `org.springframework.boot.bootstrap.BootstrapRegistryInitializer` |

### Persistence

| Old Location (3.x) | New Location (4.x) |
|--------------------|---------------------|
| `org.springframework.boot.autoconfigure.domain.EntityScan` | `org.springframework.boot.persistence.autoconfigure.EntityScan` |

### HTTP Converters

| Old Location (3.x) | New Location (4.x) |
|--------------------|---------------------|
| `org.springframework.boot.http.converter.autoconfigure.HttpMessageConverters` | Deprecated, use customizers |

### Testing

| Old Location (3.x) | New Location (4.x) |
|--------------------|---------------------|
| `org.springframework.boot.test.web.client.TestRestTemplate` | `org.springframework.boot.resttestclient.TestRestTemplate` |
| `org.springframework.boot.test.autoconfigure.properties.PropertyMapping` | `org.springframework.boot.test.context.PropertyMapping` |
| `PropertyMapping.Skip` | `org.springframework.boot.test.context.PropertyMapping.Skip` |

---

## spring.factories Updates

If you have custom `META-INF/spring.factories`, update entries:

```properties
# Old
org.springframework.boot.env.EnvironmentPostProcessor=\
  com.example.MyEnvironmentPostProcessor

# New
org.springframework.boot.EnvironmentPostProcessor=\
  com.example.MyEnvironmentPostProcessor
```

---

## Removed APIs

### PropertyMapper

```java
// REMOVED - alwaysApplyingNotNull()
// Old
PropertyMapper mapper = PropertyMapper.get().alwaysApplyingNotNull();
map.from(source::getValue).to(destination::setValue);

// New - Use always() for explicit null handling
PropertyMapper mapper = PropertyMapper.get();

// This won't call destination.setValue(null) if source returns null
map.from(source::getValue).to(destination::setValue);

// This WILL call destination.setValue(null) if source returns null
map.from(source::getValue).always().to(destination::setValue);
```

### MockitoTestExecutionListener

```java
// REMOVED
org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener

// Use instead
org.mockito.junit.jupiter.MockitoExtension
```

### Classic Uber-Jar Loader

```xml
<!-- REMOVE from Maven configuration -->
<configuration>
    <loaderImplementation>CLASSIC</loaderImplementation>
</configuration>
```

### Executable Launch Scripts

Fully executable JAR support removed. No replacement - use standard `java -jar`.

---

## Deprecated APIs

### HttpMessageConverters

```java
// DEPRECATED
org.springframework.boot.http.converter.autoconfigure.HttpMessageConverters

// Use customizers instead
@Bean
public ClientHttpMessageConvertersCustomizer clientCustomizer() {
    return converters -> {
        // customize client-side converters
    };
}

@Bean
public ServerHttpMessageConvertersCustomizer serverCustomizer() {
    return converters -> {
        // customize server-side converters
    };
}
```

### OperationMethod Constructor

```java
// DEPRECATED
new OperationMethod(Method method, OperationType operationType)

// Use the new constructor with additional parameters
```

---

## Actuator Changes

### Nullable Annotations

```java
// Old - Using Spring's Nullable
import org.springframework.lang.Nullable;

@ReadOperation
public String getValue(@Nullable String param) {}

// New - Using JSpecify
import org.jspecify.annotations.Nullable;

@ReadOperation
public String getValue(@Nullable String param) {}

// Or use OptionalParameter
@ReadOperation
public String getValue(OptionalParameter<String> param) {}
```

### Health Endpoint Changes

Liveness and readiness probes enabled by default:

```java
// Access liveness/readiness
// GET /actuator/health/liveness
// GET /actuator/health/readiness

// Disable if not needed
// management.endpoint.health.probes.enabled=false
```

---

## Web Framework Changes

### PathRequest - Static Resources

```java
// New font location added to common locations
// /fonts/** now included

// To exclude fonts:
pathRequest.toStaticResources()
    .atCommonLocations()
    .excluding(StaticResourceLocation.FONTS);
```

### API Versioning

```java
// New in Spring Boot 4 - Built-in API versioning
@RestController
@RequestMapping("/api")
public class UserController {

    @GetMapping(value = "/users", version = "1.0")
    public List<UserV1> getUsersV1() {}

    @GetMapping(value = "/users", version = "2.0")
    public List<UserV2> getUsersV2() {}
}

// Configure versioning strategy
// application.yml:
// spring.mvc.apiversion.use.header: API-Version
```

---

## Messaging Changes

### Kafka StreamsBuilderFactoryBeanCustomizer

```java
// REMOVED
org.springframework.boot.autoconfigure.kafka.StreamsBuilderFactoryBeanCustomizer

// Use Spring Kafka's configurer
import org.springframework.kafka.config.StreamsBuilderFactoryBeanConfigurer;

@Bean
public StreamsBuilderFactoryBeanConfigurer kafkaStreamsConfigurer() {
    return factoryBean -> {
        // configure
    };
}
```

### AMQP Retry Customizers

```java
// REMOVED - Single customizer
org.springframework.boot.autoconfigure.amqp.RabbitRetryTemplateCustomizer

// NEW - Separate customizers for template and listener
@Bean
public RabbitTemplateRetrySettingsCustomizer templateRetryCustomizer() {
    return settings -> settings.setMaxAttempts(5);
}

@Bean
public RabbitListenerRetrySettingsCustomizer listenerRetryCustomizer() {
    return settings -> settings.setMaxAttempts(3);
}
```

---

## Elasticsearch Changes

### RestClient → Rest5Client

```java
// Old
import org.elasticsearch.client.RestClient;
import org.springframework.boot.autoconfigure.elasticsearch.RestClientBuilderCustomizer;

@Bean
public RestClientBuilderCustomizer customizer() {
    return builder -> {
        // customize
    };
}

// New
import co.elastic.clients.transport.rest5_client.Rest5Client;
import org.springframework.boot.autoconfigure.elasticsearch.Rest5ClientBuilderCustomizer;

@Bean
public Rest5ClientBuilderCustomizer customizer() {
    return builder -> {
        // customize
    };
}
```

---

## Spring Batch Changes

### Default Behavior

Spring Batch now operates in-memory by default (no database required):

```java
// To restore database persistence, add starter
// spring-boot-starter-batch-jdbc
```

---

## Spring Retry Migration

Spring Retry features moving to Spring Framework:

```java
// Old - Spring Retry
import org.springframework.retry.annotation.Retryable;
import org.springframework.retry.annotation.Backoff;

// New - Spring Framework core (preferred)
import org.springframework.core.retry.Retryable;
import org.springframework.core.retry.Backoff;

// If still using Spring Retry, add explicit version
```

---

## JSpecify Nullability

### Migration from Spring Annotations

```java
// Old
import org.springframework.lang.Nullable;
import org.springframework.lang.NonNull;

// New
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;
```

### Kotlin Impact

JSpecify annotations affect Kotlin nullability inference. Review Kotlin code for potential issues.

---

## Module Package Structure

Each module now has dedicated root package:

```
org.springframework.boot.<module>

Examples:
- org.springframework.boot.webmvc
- org.springframework.boot.graphql
- org.springframework.boot.data.jpa
- org.springframework.boot.security
```

### Import Updates

```java
// Check imports for auto-configuration classes
// Old
import org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration;

// New (check exact package)
import org.springframework.boot.webmvc.autoconfigure.WebMvcAutoConfiguration;
```

---

## Migration Checklist

- [ ] Update `EnvironmentPostProcessor` imports and spring.factories
- [ ] Update `BootstrapRegistry` imports
- [ ] Update `@EntityScan` import
- [ ] Update `TestRestTemplate` import
- [ ] Update `PropertyMapping` import
- [ ] Replace `PropertyMapper.alwaysApplyingNotNull()` with `always()`
- [ ] Remove `MockitoTestExecutionListener` usage
- [ ] Remove classic loader configuration
- [ ] Update `HttpMessageConverters` to customizers
- [ ] Update actuator nullable annotations to JSpecify
- [ ] Update Kafka `StreamsBuilderFactoryBeanCustomizer`
- [ ] Update AMQP retry customizers
- [ ] Update Elasticsearch `RestClientBuilderCustomizer`
- [ ] Add Spring Batch JDBC starter if using database
- [ ] Update Spring Retry imports if applicable
- [ ] Update all JSpecify nullability annotations
- [ ] Review modular package imports
