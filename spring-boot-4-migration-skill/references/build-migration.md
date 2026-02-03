# Build File Migration Reference

Complete guide for migrating Maven and Gradle build files from Spring Boot 3.x to 4.x.

---

## Maven Migration

### Parent POM Update

```xml
<!-- Before (3.x) -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.6</version>
    <relativePath/>
</parent>

<!-- After (4.x) -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.0.0</version>
    <relativePath/>
</parent>
```

### Java Version

```xml
<properties>
    <!-- Minimum: 17, Recommended: 21 -->
    <java.version>21</java.version>
</properties>
```

### Kotlin Version (if applicable)

```xml
<properties>
    <kotlin.version>2.2.20</kotlin.version>
</properties>
```

### Plugin Updates

```xml
<!-- Spring Boot Maven Plugin - no version needed if using parent -->
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
</plugin>

<!-- CycloneDX - minimum 3.0.0 -->
<plugin>
    <groupId>org.cyclonedx</groupId>
    <artifactId>cyclonedx-maven-plugin</artifactId>
    <version>3.0.0</version>
</plugin>
```

### Optional Dependencies in Uber Jars

Optional dependencies are no longer included by default:

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
        <!-- Include optional dependencies if needed -->
        <includeOptional>true</includeOptional>
    </configuration>
</plugin>
```

### Removed: Classic Loader Implementation

Remove this if present:
```xml
<!-- REMOVE THIS -->
<configuration>
    <loaderImplementation>CLASSIC</loaderImplementation>
</configuration>
```

---

## Gradle Migration

### Plugin Version Update

**Groovy DSL (build.gradle):**
```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '4.0.0'
    id 'io.spring.dependency-management' version '1.1.7'
}
```

**Kotlin DSL (build.gradle.kts):**
```kotlin
plugins {
    java
    id("org.springframework.boot") version "4.0.0"
    id("io.spring.dependency-management") version "1.1.7"
}
```

### Java Toolchain

**Groovy DSL:**
```groovy
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

**Kotlin DSL:**
```kotlin
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}
```

### Kotlin Configuration (if applicable)

```kotlin
plugins {
    kotlin("jvm") version "2.2.20"
    kotlin("plugin.spring") version "2.2.20"
}
```

### Gradle Version Requirements

- Minimum: Gradle 8.14
- Supported: Gradle 9.x

Check and update wrapper:
```bash
./gradlew wrapper --gradle-version=8.14
# or for Gradle 9
./gradlew wrapper --gradle-version=9.0
```

---

## Starter Dependency Changes

This section provides a comprehensive reference of all starter changes in Spring Boot 4.x, organized by category.

---

### Web & API Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-web` | `spring-boot-starter-webmvc` | **RENAMED** | Spring MVC applications (Servlet-based) |
| `spring-boot-starter-webflux` | `spring-boot-starter-webflux` | Unchanged | Reactive web applications |
| `spring-boot-starter-web-services` | `spring-boot-starter-webservices` | **RENAMED** | SOAP web services |
| `spring-boot-starter-graphql` | `spring-boot-starter-graphql` | Unchanged | GraphQL API support |
| `spring-boot-starter-hateoas` | `spring-boot-starter-hateoas` | Unchanged | Hypermedia REST APIs |
| `spring-boot-starter-jersey` | `spring-boot-starter-jersey` | Unchanged | JAX-RS with Jersey |
| `spring-boot-starter-rsocket` | `spring-boot-starter-rsocket` | Unchanged | RSocket messaging |

```xml
<!-- Web MVC Migration -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- After (4.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
</dependency>
```

---

### Security Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-security` | `spring-boot-starter-security` | Unchanged | Core Spring Security |
| `spring-boot-starter-oauth2-client` | `spring-boot-starter-security-oauth2-client` | **RENAMED** | OAuth2/OIDC login |
| `spring-boot-starter-oauth2-resource-server` | `spring-boot-starter-security-oauth2-resource-server` | **RENAMED** | JWT/Opaque token resource server |
| `spring-boot-starter-oauth2-authorization-server` | `spring-boot-starter-security-oauth2-authorization-server` | **RENAMED** | OAuth2 authorization server |
| N/A | `spring-boot-starter-security-test` | **NEW** | Security testing annotations |
| `spring-boot-starter-saml2-service-provider` | `spring-boot-starter-security-saml2-service-provider` | **RENAMED** | SAML 2.0 service provider |

```xml
<!-- Security Migration Examples -->

<!-- OAuth2 Client -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>

<!-- After (4.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-client</artifactId>
</dependency>

<!-- OAuth2 Resource Server -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>

<!-- After (4.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-resource-server</artifactId>
</dependency>

<!-- NEW: Security Test Starter (required for @WithMockUser, etc.) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

---

### Database & Data Access Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-data-jpa` | `spring-boot-starter-data-jpa` | Unchanged | JPA with Hibernate 7.1 |
| `spring-boot-starter-data-jdbc` | `spring-boot-starter-data-jdbc` | Unchanged | Spring Data JDBC |
| `spring-boot-starter-data-mongodb` | `spring-boot-starter-data-mongodb` | Unchanged | MongoDB support |
| `spring-boot-starter-data-mongodb-reactive` | `spring-boot-starter-data-mongodb-reactive` | Unchanged | Reactive MongoDB |
| `spring-boot-starter-data-redis` | `spring-boot-starter-data-redis` | Unchanged | Redis support |
| `spring-boot-starter-data-redis-reactive` | `spring-boot-starter-data-redis-reactive` | Unchanged | Reactive Redis |
| `spring-boot-starter-data-elasticsearch` | `spring-boot-starter-data-elasticsearch` | Updated | Uses Rest5Client |
| `spring-boot-starter-data-cassandra` | `spring-boot-starter-data-cassandra` | Unchanged | Cassandra support |
| `spring-boot-starter-data-cassandra-reactive` | `spring-boot-starter-data-cassandra-reactive` | Unchanged | Reactive Cassandra |
| `spring-boot-starter-data-couchbase` | `spring-boot-starter-data-couchbase` | Unchanged | Couchbase support |
| `spring-boot-starter-data-couchbase-reactive` | `spring-boot-starter-data-couchbase-reactive` | Unchanged | Reactive Couchbase |
| `spring-boot-starter-data-neo4j` | `spring-boot-starter-data-neo4j` | Unchanged | Neo4j graph database |
| `spring-boot-starter-data-r2dbc` | `spring-boot-starter-data-r2dbc` | Unchanged | Reactive relational DB |
| `spring-boot-starter-data-ldap` | `spring-boot-starter-data-ldap` | Unchanged | LDAP support |
| `spring-boot-starter-data-rest` | `spring-boot-starter-data-rest` | Unchanged | REST repositories |
| `spring-boot-starter-jdbc` | `spring-boot-starter-jdbc` | Unchanged | Plain JDBC |
| N/A | `spring-boot-starter-flyway` | **NEW** | Flyway migrations |
| N/A | `spring-boot-starter-liquibase` | **NEW** | Liquibase migrations |

```xml
<!-- Database Migration Tools - NOW REQUIRE STARTERS -->

<!-- Flyway -->
<!-- Before (3.x) - Direct dependency -->
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>

<!-- After (4.x) - Use starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-flyway</artifactId>
</dependency>

<!-- Liquibase -->
<!-- Before (3.x) - Direct dependency -->
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>

<!-- After (4.x) - Use starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-liquibase</artifactId>
</dependency>
```

---

### Messaging Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-amqp` | `spring-boot-starter-amqp` | Unchanged | RabbitMQ support |
| `spring-boot-starter-kafka` | `spring-boot-starter-kafka` | Unchanged | Apache Kafka |
| `spring-boot-starter-kafka-streams` | `spring-boot-starter-kafka-streams` | Unchanged | Kafka Streams |
| `spring-boot-starter-pulsar` | `spring-boot-starter-pulsar` | Updated | Apache Pulsar (reactive removed) |
| `spring-boot-starter-pulsar-reactive` | N/A | **REMOVED** | Use imperative API instead |
| `spring-boot-starter-activemq` | `spring-boot-starter-activemq` | Unchanged | ActiveMQ Classic |
| `spring-boot-starter-artemis` | `spring-boot-starter-artemis` | Unchanged | ActiveMQ Artemis |
| `spring-boot-starter-integration` | `spring-boot-starter-integration` | Unchanged | Spring Integration |
| `spring-boot-starter-websocket` | `spring-boot-starter-websocket` | Unchanged | WebSocket support |
| `spring-boot-starter-jooq` | `spring-boot-starter-jooq` | Unchanged | jOOQ support |

```xml
<!-- Pulsar - Reactive support removed -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-pulsar-reactive</artifactId>
</dependency>

<!-- After (4.x) - Use imperative API -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-pulsar</artifactId>
</dependency>
```

---

### Batch & Scheduling Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-batch` | `spring-boot-starter-batch` | Unchanged | Spring Batch core |
| N/A | `spring-boot-starter-batch-jdbc` | **NEW** | Batch with JDBC metadata |
| N/A | `spring-boot-starter-batch-mongodb` | **NEW** | Batch with MongoDB metadata |
| `spring-boot-starter-quartz` | `spring-boot-starter-quartz` | Unchanged | Quartz scheduler |

```xml
<!-- Spring Batch with Database - NOW REQUIRES SEPARATE STARTER -->
<!-- Before (3.x) - Included with spring-boot-starter-batch + JDBC -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-batch</artifactId>
</dependency>

<!-- After (4.x) - Explicit starter for JDBC metadata -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-batch</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-batch-jdbc</artifactId>
</dependency>
```

---

### Observability & Monitoring Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-actuator` | `spring-boot-starter-actuator` | Unchanged | Production-ready features |
| N/A | `spring-boot-starter-opentelemetry` | **NEW** | OpenTelemetry integration |
| N/A | `spring-boot-starter-opentelemetry-tracing` | **NEW** | OTel tracing only |
| N/A | `spring-boot-starter-opentelemetry-metrics` | **NEW** | OTel metrics only |

```xml
<!-- OpenTelemetry - NEW UNIFIED STARTER -->
<!-- Before (3.x) - Multiple dependencies needed -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>

<!-- After (4.x) - Single starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

---

### Serialization & JSON Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-json` | `spring-boot-starter-json` | Updated | Now uses Jackson 3.x |
| N/A | `spring-boot-starter-kotlin-serialization` | **NEW** | Kotlin serialization |
| N/A | `spring-boot-jackson2` | **NEW** | Jackson 2 compatibility bridge |

```xml
<!-- Jackson 2 Compatibility Bridge (temporary migration aid) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-jackson2</artifactId>
</dependency>

<!-- Kotlin Serialization - NEW STARTER -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-kotlin-serialization</artifactId>
</dependency>
```

---

### AOP & Infrastructure Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-aop` | `spring-boot-starter-aspectj` | **RENAMED** | AspectJ AOP support |
| `spring-boot-starter-validation` | `spring-boot-starter-validation` | Unchanged | Bean Validation (Hibernate Validator) |
| `spring-boot-starter-cache` | `spring-boot-starter-cache` | Unchanged | Caching abstraction |
| `spring-boot-starter-mail` | `spring-boot-starter-mail` | Unchanged | Email support |
| `spring-boot-starter-freemarker` | `spring-boot-starter-freemarker` | Unchanged | FreeMarker templates |
| `spring-boot-starter-thymeleaf` | `spring-boot-starter-thymeleaf` | Unchanged | Thymeleaf templates |
| `spring-boot-starter-mustache` | `spring-boot-starter-mustache` | Unchanged | Mustache templates |
| `spring-boot-starter-groovy-templates` | `spring-boot-starter-groovy-templates` | Unchanged | Groovy templates |

```xml
<!-- AOP Migration -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>

<!-- After (4.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aspectj</artifactId>
</dependency>
```

---

### Session Management Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-session-core` | `spring-session-core` | Unchanged | Core session support |
| `spring-session-jdbc` | `spring-session-jdbc` | Unchanged | JDBC session store |
| `spring-session-data-redis` | `spring-session-data-redis` | Unchanged | Redis session store |
| `spring-session-hazelcast` | N/A | **REMOVED** | Now managed by Hazelcast team |
| `spring-session-mongodb` | N/A | **REMOVED** | Now managed by MongoDB team |

```xml
<!-- Hazelcast Session - Now external -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.session</groupId>
    <artifactId>spring-session-hazelcast</artifactId>
</dependency>

<!-- After (4.x) - Use Hazelcast-provided module -->
<dependency>
    <groupId>com.hazelcast</groupId>
    <artifactId>hazelcast-spring-session</artifactId>
    <version>${hazelcast.version}</version>
</dependency>
```

---

### Servlet Container Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-tomcat` | `spring-boot-starter-tomcat` | Unchanged | Tomcat 11 (default) |
| `spring-boot-starter-jetty` | `spring-boot-starter-jetty` | Unchanged | Jetty 12.1+ |
| `spring-boot-starter-undertow` | N/A | **REMOVED** | Not compatible with Servlet 6.1 |
| N/A | `spring-boot-starter-netty` | **NEW** | Netty for WebFlux |

```xml
<!-- Undertow - REMOVED, migrate to Tomcat or Jetty -->
<!-- Before (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>

<!-- After (4.x) - Use Jetty as alternative to Tomcat -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

---

### Testing Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-boot-starter-test` | `spring-boot-starter-test` | Updated | JUnit 6, Mockito 6, AssertJ 4 |
| N/A | `spring-boot-starter-test-classic` | **NEW** | Migration bridge for tests |
| N/A | `spring-boot-starter-security-test` | **NEW** | Security testing (required) |
| N/A | `spring-boot-starter-webmvc-test` | **NEW** | WebMvc slice tests |
| N/A | `spring-boot-starter-webflux-test` | **NEW** | WebFlux slice tests |
| N/A | `spring-boot-starter-data-jpa-test` | **NEW** | JPA slice tests |
| N/A | `spring-boot-starter-data-jdbc-test` | **NEW** | JDBC slice tests |
| N/A | `spring-boot-starter-data-mongodb-test` | **NEW** | MongoDB slice tests |
| N/A | `spring-boot-starter-data-redis-test` | **NEW** | Redis slice tests |

```xml
<!-- Test Dependencies -->
<!-- Core test starter (updated) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- Security test starter (NEW - required for @WithMockUser, etc.) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- WebMVC test starter (NEW - for @WebMvcTest) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- Data JPA test starter (NEW - for @DataJpaTest) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- Classic test bridge for gradual migration -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test-classic</artifactId>
    <scope>test</scope>
</dependency>
```

---

### Cloud & Distributed Starters

| Old Starter (3.x) | New Starter (4.x) | Status | Notes |
|-------------------|-------------------|--------|-------|
| `spring-cloud-starter-*` | `spring-cloud-starter-*` | Check compatibility | Use Spring Cloud 2025.x |
| `spring-boot-starter-docker-compose` | `spring-boot-starter-docker-compose` | Unchanged | Docker Compose support |

**Note:** Spring Cloud releases are independent. Ensure you use a Spring Cloud version compatible with Spring Boot 4.x (typically Spring Cloud 2025.x or later).

---

### Migration Starters (Temporary)

These starters help with gradual migration and should be removed once migration is complete:

| Starter | Purpose | Remove After |
|---------|---------|--------------|
| `spring-boot-starter-classic` | All 3.x auto-configurations | Full migration |
| `spring-boot-starter-test-classic` | All 3.x test configurations | Test migration |
| `spring-boot-jackson2` | Jackson 2.x compatibility | Jackson 3 migration |

```xml
<!-- Gradual Migration Support -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-classic</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test-classic</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-jackson2</artifactId>
</dependency>
```

---

### Quick Reference: All Renamed Starters

| Category | Old Name (3.x) | New Name (4.x) |
|----------|----------------|----------------|
| Web | `spring-boot-starter-web` | `spring-boot-starter-webmvc` |
| Web | `spring-boot-starter-web-services` | `spring-boot-starter-webservices` |
| Security | `spring-boot-starter-oauth2-client` | `spring-boot-starter-security-oauth2-client` |
| Security | `spring-boot-starter-oauth2-resource-server` | `spring-boot-starter-security-oauth2-resource-server` |
| Security | `spring-boot-starter-oauth2-authorization-server` | `spring-boot-starter-security-oauth2-authorization-server` |
| Security | `spring-boot-starter-saml2-service-provider` | `spring-boot-starter-security-saml2-service-provider` |
| AOP | `spring-boot-starter-aop` | `spring-boot-starter-aspectj` |

### Quick Reference: All New Required Starters

| If Using | Add Starter |
|----------|-------------|
| Flyway migrations | `spring-boot-starter-flyway` |
| Liquibase migrations | `spring-boot-starter-liquibase` |
| `@WithMockUser` / security tests | `spring-boot-starter-security-test` |
| Spring Batch with database | `spring-boot-starter-batch-jdbc` |
| Spring Batch with MongoDB | `spring-boot-starter-batch-mongodb` |
| OpenTelemetry | `spring-boot-starter-opentelemetry` |
| Kotlin serialization | `spring-boot-starter-kotlin-serialization` |

### Quick Reference: All Removed Starters

| Removed Starter | Reason | Alternative |
|-----------------|--------|-------------|
| `spring-boot-starter-undertow` | Servlet 6.1 incompatible | `spring-boot-starter-jetty` |
| `spring-boot-starter-pulsar-reactive` | Reactive API dropped | `spring-boot-starter-pulsar` |
| `spring-session-hazelcast` | External management | Hazelcast-provided module |
| `spring-session-mongodb` | External management | MongoDB-provided module |

---

## Modular Architecture

### Module Naming Convention

| Component | Pattern | Example |
|-----------|---------|---------|
| Main module | `spring-boot-<technology>` | `spring-boot-graphql` |
| Root package | `org.springframework.boot.<technology>` | `org.springframework.boot.graphql` |
| Starter POM | `spring-boot-starter-<technology>` | `spring-boot-starter-graphql` |
| Test module | `spring-boot-<technology>-test` | `spring-boot-graphql-test` |
| Test starter | `spring-boot-starter-<technology>-test` | `spring-boot-starter-graphql-test` |

### Classic Starters (Migration Aid)

For gradual migration, use classic starters to maintain old classpath:

```xml
<!-- Runtime dependency - all auto-configuration available -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-classic</artifactId>
</dependency>

<!-- Test dependency - all test auto-configuration available -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test-classic</artifactId>
    <scope>test</scope>
</dependency>
```

**Important:** Classic starters are temporary. Plan to remove them and use specific starters.

---

## Removed Dependencies

### Undertow (Not Compatible with Servlet 6.1)

```xml
<!-- REMOVE - Not supported in Boot 4 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>

<!-- Use Tomcat (default) or Jetty instead -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

### Spring Session Storage Backends

```xml
<!-- REMOVE - Now managed by Hazelcast team -->
<dependency>
    <groupId>org.springframework.session</groupId>
    <artifactId>spring-session-hazelcast</artifactId>
</dependency>

<!-- REMOVE - Now managed by MongoDB team -->
<dependency>
    <groupId>org.springframework.session</groupId>
    <artifactId>spring-session-mongodb</artifactId>
</dependency>
```

### Reactive Pulsar

```xml
<!-- REMOVE - Reactive support dropped -->
<dependency>
    <groupId>org.springframework.pulsar</groupId>
    <artifactId>spring-pulsar-reactive</artifactId>
</dependency>
```

### Elasticsearch Low-Level Client

```xml
<!-- REMOVE - Replaced with Rest5Client -->
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-client</artifactId>
</dependency>
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-client-sniffer</artifactId>
</dependency>

<!-- USE - Consolidated client -->
<dependency>
    <groupId>co.elastic.clients</groupId>
    <artifactId>elasticsearch-java</artifactId>
</dependency>
```

### Hibernate Dependencies Renamed

```xml
<!-- REMOVE -->
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-jpamodelgen</artifactId>
</dependency>

<!-- USE -->
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-processor</artifactId>
</dependency>

<!-- REMOVED - No longer published -->
<!-- hibernate-proxool -->
<!-- hibernate-vibur -->
```

---

## Version Properties

If overriding managed versions, update property names:

```xml
<properties>
    <!-- Spring Authorization Server is now part of Spring Security -->
    <!-- OLD: spring-authorization-server.version -->
    <!-- NEW: Use spring-security.version -->
    <spring-security.version>7.0.0</spring-security.version>
</properties>
```

---

## BOM (Bill of Materials) for Non-Parent Usage

If not using spring-boot-starter-parent:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>4.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**Gradle:**
```groovy
dependencyManagement {
    imports {
        mavenBom "org.springframework.boot:spring-boot-dependencies:4.0.0"
    }
}
```

---

## Native Image Support

### GraalVM Requirements

- Minimum: GraalVM 25+

### Native Build Plugin

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

### Removed: Fully Executable JARs

Launch scripts for "fully executable" JARs are removed. Use alternatives:

```bash
# Standard Java launch
java -jar myapp.jar

# Gradle application plugin
./gradlew run
```

---

## Verification Commands

After migration, verify build:

**Maven:**
```bash
# Clean and compile
./mvnw clean compile

# Run tests
./mvnw test

# Package
./mvnw package

# Check for dependency issues
./mvnw dependency:tree
```

**Gradle:**
```bash
# Clean and compile
./gradlew clean compileJava

# Run tests
./gradlew test

# Build
./gradlew build

# Check dependencies
./gradlew dependencies
```
