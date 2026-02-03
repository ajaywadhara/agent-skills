# Property Changes Reference

Complete guide for configuration property changes from Spring Boot 3.x to 4.x.

---

## Property Renames

### Core Framework

| Old Property (3.x) | New Property (4.x) |
|--------------------|---------------------|
| `spring.dao.exceptiontranslation.enabled` | `spring.persistence.exceptiontranslation.enabled` |

### Observability & Tracing

| Old Property (3.x) | New Property (4.x) |
|--------------------|---------------------|
| `management.tracing.enabled` | `management.tracing.export.enabled` |
| `spring.test.observability` | `spring.test.metrics.export` and `spring.test.tracing.export` |

### MongoDB

| Old Property (3.x) | New Property (4.x) |
|--------------------|---------------------|
| `management.health.mongo.enabled` | `management.health.mongodb.enabled` |
| `management.metrics.mongo.command.enabled` | `management.metrics.mongodb.command.enabled` |
| `management.metrics.mongo.connectionpool.enabled` | `management.metrics.mongodb.connectionpool.enabled` |

**New MongoDB Core Properties:**
```yaml
spring:
  mongodb:
    host: localhost
    port: 27017
    database: mydb
    username: user
    password: secret
    authentication-database: admin
    replica-set-name: rs0
    uri: mongodb://localhost:27017/mydb
    protocol: mongodb
    additional-hosts: host2:27017,host3:27017
    representation:
      uuid: standard  # or java-legacy
    ssl:
      enabled: true
      bundle: my-ssl-bundle
```

### Spring Session

| Old Property (3.x) | New Property (4.x) |
|--------------------|---------------------|
| `spring.session.redis.*` | `spring.session.data.redis.*` |
| `spring.session.mongodb.*` | `spring.session.data.mongodb.*` |

### Kafka

| Old Property (3.x) | New Property (4.x) |
|--------------------|---------------------|
| `spring.kafka.retry.topic.backoff.random` | `spring.kafka.retry.topic.backoff.jitter` |

### Jackson

JSON-specific properties moved under `json` namespace:

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

### Hibernate Naming Strategy

```yaml
# Value change
spring:
  jpa:
    hibernate:
      naming:
        # Old value
        implicit-strategy: org.springframework.boot.orm.jpa.hibernate.SpringImplicitNamingStrategy
        # New value
        implicit-strategy: org.springframework.boot.hibernate.SpringImplicitNamingStrategy
```

---

## Removed Properties

### SignalFX (No Longer Supported)

All SignalFX properties removed:
```yaml
# REMOVED - Delete these
management:
  metrics:
    export:
      signalfx:
        access-token: xxx
        batch-size: 10000
        connect-timeout: 1s
        enabled: true
        published-histogram-type: cumulative
        read-timeout: 10s
        source: host
        step: 10s
        uri: https://ingest.signalfx.com
```

### Template Engine `enabled` Properties

These properties are deprecated and will be removed:
```yaml
# DEPRECATED - No longer needed
spring:
  freemarker:
    enabled: true
  groovy:
    template:
      enabled: true
  mustache:
    enabled: true
  thymeleaf:
    enabled: true
```

To disable a template engine, simply don't include its dependency.

---

## New Properties

### Elasticsearch API Key

```yaml
spring:
  elasticsearch:
    api-key: your-api-key-here
```

### Tomcat Static Cache

```yaml
server:
  tomcat:
    resource:
      cache-max-size: 10MB
```

### MongoDB Representations

```yaml
spring:
  mongodb:
    representation:
      uuid: standard  # standard, java-legacy
  data:
    mongodb:
      representation:
        big-decimal: decimal128  # decimal128, string
```

### Console Logging Control

```yaml
logging:
  console:
    enabled: true  # false to disable console logging
```

### DevTools LiveReload

```yaml
# Disabled by default in 4.x
spring:
  devtools:
    livereload:
      enabled: true  # must explicitly enable
```

### API Versioning

```yaml
spring:
  mvc:
    apiversion:
      enabled: true
      use:
        header: API-Version
        # or
        parameter: version
        # or
        path: true
```

### Observability Annotations

```yaml
management:
  observations:
    annotations:
      enabled: true  # enables @Observed, @Timed, @Counted, @NewSpan
```

### Health Probes

```yaml
# Enabled by default in 4.x, disable if not needed
management:
  endpoint:
    health:
      probes:
        enabled: false
```

---

## Jackson 2 Compatibility Properties

For temporary Jackson 2 support:

```yaml
spring:
  jackson:
    use-jackson2-defaults: true  # align with Boot 3.x behavior
    find-and-add-modules: false  # disable auto module detection

  http:
    converters:
      preferred-json-mapper: jackson2  # for Spring MVC
    codecs:
      preferred-json-mapper: jackson2  # for WebFlux

# Jackson 2 specific properties (deprecated)
spring:
  jackson2:
    serialization:
      INDENT_OUTPUT: true
    deserialization:
      FAIL_ON_UNKNOWN_PROPERTIES: false
```

---

## Property Profiles

### Profile-Specific Changes

Update all profile-specific files:
- `application.yml`
- `application-dev.yml`
- `application-prod.yml`
- `application-test.yml`

### Environment Variables

Remember to update environment variable names:

```bash
# Old
SPRING_DAO_EXCEPTIONTRANSLATION_ENABLED=true

# New
SPRING_PERSISTENCE_EXCEPTIONTRANSLATION_ENABLED=true
```

---

## Migration Using Properties Migrator

### Add Migrator Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

### How It Works

1. Add dependency temporarily
2. Start application
3. Check logs for property migration suggestions
4. Update properties based on warnings
5. Remove dependency after migration

### Sample Output

```
Property 'spring.dao.exceptiontranslation.enabled' is deprecated and should be replaced with 'spring.persistence.exceptiontranslation.enabled'.
Property 'management.health.mongo.enabled' is deprecated and should be replaced with 'management.health.mongodb.enabled'.
```

---

## OpenRewrite Automation

### Run Property Migration Recipe

**Maven:**
```bash
./mvnw rewrite:run -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.SpringBootProperties_4_0
```

**Gradle:**
```bash
./gradlew rewriteRun -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.SpringBootProperties_4_0
```

This automatically updates:
- `application.properties`
- `application.yml`
- `application-*.properties`
- `application-*.yml`

---

## Complete Example

### Before (3.x)

```yaml
spring:
  dao:
    exceptiontranslation:
      enabled: true
  session:
    redis:
      namespace: myapp
  kafka:
    retry:
      topic:
        backoff:
          random: 0.5
  jackson:
    read:
      ACCEPT_FLOAT_AS_INT: true

management:
  tracing:
    enabled: true
  health:
    mongo:
      enabled: true
  metrics:
    export:
      signalfx:
        enabled: true
```

### After (4.x)

```yaml
spring:
  persistence:
    exceptiontranslation:
      enabled: true
  session:
    data:
      redis:
        namespace: myapp
  kafka:
    retry:
      topic:
        backoff:
          jitter: 0.5
  jackson:
    json:
      read:
        ACCEPT_FLOAT_AS_INT: true

management:
  tracing:
    export:
      enabled: true
  endpoint:
    health:
      probes:
        enabled: true
  health:
    mongodb:
      enabled: true
  # SignalFX removed - use alternative metrics backend

logging:
  console:
    enabled: true
```

---

## Verification

After updating properties:

```bash
# Start application and check for warnings
./mvnw spring-boot:run

# Check actuator for configuration
curl http://localhost:8080/actuator/configprops

# Check environment
curl http://localhost:8080/actuator/env
```

---

## Migration Checklist

- [ ] Rename `spring.dao.exceptiontranslation.enabled`
- [ ] Rename MongoDB health/metrics properties
- [ ] Rename Spring Session properties
- [ ] Rename Kafka retry backoff property
- [ ] Move Jackson read/write properties under `json` namespace
- [ ] Update Hibernate naming strategy value
- [ ] Remove SignalFX properties
- [ ] Review deprecated template engine `enabled` properties
- [ ] Add new MongoDB representation properties if needed
- [ ] Update environment variables
- [ ] Update all profile-specific files
- [ ] Run properties migrator to verify
- [ ] Remove properties migrator dependency
