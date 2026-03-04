# Spring Boot 4 Migration Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/skills.sh-available-blue)](https://skills.sh)

Migrate your Spring Boot applications from **3.x to 4.x** with step-by-step, AI-guided assistance — no guesswork, no missed breaking changes.

---

## Why Use This Skill?

Spring Boot 4 is a **major upgrade** — it brings Spring Framework 7, Spring Security 7, Jackson 3, Hibernate 7.1, Jakarta EE 11, and JUnit 6, all at once. That's a lot of moving parts.

Here's why this skill matters:

| Challenge | Without This Skill | With This Skill |
|-----------|--------------------|-----------------|
| **Breaking changes** | Discover them one at a time via compile errors | Get a complete checklist of every change upfront |
| **Package renames** | Manually search and replace across the codebase | AI applies all renames automatically |
| **Starter changes** | `starter-web` silently deprecated? You won't know until runtime | Clear mapping: `starter-web` → `starter-webmvc` |
| **Security DSL** | `.and()` chaining removed — security configs won't compile | Lambda-style DSL rewrites applied for you |
| **Jackson 3** | New package (`tools.jackson`), renamed annotations | Automated import rewrites and annotation updates |
| **Test breakage** | `@MockBean` removed — every test file needs updates | Bulk migration to `@MockitoBean` / `@MockitoSpyBean` |
| **Migration order** | Which change should come first? No clear guidance | 10 sequenced phases, each with verification steps |

**Bottom line:** What could take days of research and trial-and-error becomes a guided, phase-by-phase migration that your AI assistant executes with you.

---

## Installation

### Using npx (Recommended)

Install this skill with a single command — no global packages required:

```bash
# Install just this skill
npx skills add ajaywadhara/agent-skills/spring-boot-4-migration-skill
```

Or install the entire Agent Skills collection:

```bash
# Install all skills from the repository
npx skills add ajaywadhara/agent-skills
```

### Manual Installation

If you prefer to install manually:

```bash
# Clone the repository
git clone https://github.com/ajaywadhara/agent-skills.git

# Copy to your project's skills directory (Claude Code)
mkdir -p .claude/skills
cp -r agent-skills/spring-boot-4-migration-skill .claude/skills/

# Or install globally (available across all projects)
mkdir -p ~/.claude/skills
cp -r agent-skills/spring-boot-4-migration-skill ~/.claude/skills/
```

---

## Usage

Once installed, just tell your AI assistant what you need. The skill activates automatically.

```
"Migrate to Spring Boot 4"
"Upgrade from Spring Boot 3.x"
"Help with Jackson 3 migration"
"Migrate Security to Spring Security 7"
"Fix my tests for Spring Boot 4"
"What changed in Spring Boot 4?"
```

---

## What's Covered

The skill guides you through **10 migration phases**, executed in order:

| Phase | What It Does |
|-------|-------------|
| **1. Pre-Migration** | Validates you're on Spring Boot 3.5.x, fixes deprecations, ensures tests pass |
| **2. Build Files** | Updates parent/plugin versions, remaps starters, sets Java 21 |
| **3. Properties** | Renames deprecated config keys (`spring.dao.*` → `spring.persistence.*`, etc.) |
| **4. Jackson 3** | Migrates from `com.fasterxml.jackson` to `tools.jackson`, renames annotations |
| **5. API Changes** | Applies package relocations and removed API replacements |
| **6. Security 7** | Rewrites security DSL from `.and()` chaining to lambda style |
| **7. Testing** | Migrates `@MockBean` → `@MockitoBean`, updates MockMvc config |
| **8. Observability** | Switches to unified `starter-opentelemetry` |
| **9. Framework 7** | Updates to JSpecify null annotations, applies Spring Framework 7 changes |
| **10. Verification** | Runs tests, checks actuator, removes compatibility bridges |

### Migration Strategies

Choose the approach that fits your team:

- **Gradual (6 tracks)** — Use compatibility bridges for incremental adoption. Ideal for large codebases or teams that can't freeze development.
- **All-at-once (10 phases)** — Execute sequentially in a dedicated sprint. Best for smaller codebases.

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Java | 17+ (21+ recommended) |
| Kotlin | 2.2+ |
| Maven | 3.6.3+ |
| Gradle | 8.14+ |

---

## Key Changes at a Glance

| Area | What Changed |
|------|-------------|
| **Starters** | `starter-web` → `starter-webmvc`, `starter-aop` → `starter-aspectj` |
| **Jackson** | `com.fasterxml.jackson` → `tools.jackson` |
| **Security** | `.and()` removed, lambda DSL only, `antMatchers` → `requestMatchers` |
| **Testing** | `@MockBean` → `@MockitoBean`, `@SpyBean` → `@MockitoSpyBean` |
| **Undertow** | Removed — use Jetty instead |
| **Observability** | New unified `starter-opentelemetry` |
| **Null Safety** | `@Nullable` → `org.jspecify.annotations.Nullable` |
| **Database** | `starter-flyway` and `starter-liquibase` now required explicitly |

---

## New Features in Spring Boot 4

Beyond migration changes, Spring Boot 4 and Spring Framework 7 introduce powerful new capabilities you can adopt immediately after upgrading.

### HTTP Interface Clients

Zero-boilerplate declarative HTTP clients using `@ImportHttpServices` — no more manual `RestClient` bean wiring.

```java
@Configuration
@ImportHttpServices(TodoService.class)
public class HttpClientConfig {
    // That's it — Spring handles all bean registration
}

@HttpExchange(url = "https://api.example.com", accept = "application/json")
public interface TodoService {
    @GetExchange("/todos")
    List<Todo> getAllTodos();

    @PostExchange("/todos")
    Todo createTodo(@RequestBody Todo todo);
}
```

### Programmatic Bean Registration

The new `BeanRegistrar` interface replaces verbose `BeanDefinitionRegistryPostProcessor` with a clean, AOT-compatible API.

```java
public class MessageServiceRegistrar implements BeanRegistrar {
    @Override
    public void register(BeanRegistry registry, Environment env) {
        String type = env.getProperty("app.message-type", "email");
        switch (type) {
            case "email" -> registry.registerBean("messageService", EmailMessageService.class);
            case "sms" -> registry.registerBean("messageService", SmsMessageService.class);
        }
    }
}
```

### First-Class API Versioning

Built-in `version` attribute in request mappings with media type parameter versioning and RFC-compliant deprecation headers.

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping(version = "1.0")
    public UserDTOv1 getUserV1(@PathVariable Long id) { /* ... */ }

    @GetMapping(version = "2.0")
    public UserDTOv2 getUserV2(@PathVariable Long id) { /* ... */ }
}

// Configuration
@Configuration
public class ApiConfig implements WebMvcConfigurer {
    @Override
    public void configureApiVersioning(ApiVersionConfigurer configurer) {
        configurer.useMediaTypeParameterVersioning();
    }
}
```

### Native Resilience (`@Retryable` & `@ConcurrencyLimit`)

Built-in resilience in Spring Framework 7 core — no more Spring Retry or external libraries needed.

```java
@Configuration
@EnableResilientMethods
public class ResilienceConfig {}

@Retryable(maxAttempts = 4, delay = 500, multiplier = 2.0, jitter = 100)
public String fetchData(String id) { /* retries with exponential backoff */ }

@ConcurrencyLimit(2)
public String heavyOperation(String taskId) { /* max 2 concurrent executions */ }
```

### REST Test Client

`RestTestClient` provides a single unified API for unit, integration, and E2E tests — replacing the need to switch between `MockMvc`, `WebTestClient`, and `TestRestTemplate`.

```java
// Unit test — no Spring context
RestTestClient.bindToController(new TodoController(mockService)).build();

// Slice test — with MockMvc
RestTestClient.bindToMockMvc(mockMvc).build();

// Integration test — full context
RestTestClient.bindToApplicationContext(context).build();

// E2E test — real HTTP
RestTestClient.bindToServer().baseUrl("http://localhost:" + port).build();
```

### MockMvcTester

Server-side testing with native AssertJ integration alongside RestTestClient:

| Scenario | Use MockMvcTester | Use RestTestClient |
|----------|-------------------|--------------------|
| File uploads / multipart | ✅ | |
| Handler inspection | ✅ | |
| Same tests for mock + real HTTP | | ✅ |
| Multiple content types (XML, etc.) | | ✅ |

### Spring Data AOT Repositories

Compile-time query generation delivers **50-70% faster startup**, build-time validation, and GraalVM native image readiness.

```java
public interface CoffeeRepository extends CrudRepository<Coffee, Long> {
    // SQL generated at compile-time, not runtime
    List<Coffee> findByNameContainingIgnoreCase(String name);
}
```

Enable with Maven:
```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>process-aot</id>
            <goals><goal>process-aot</goal></goals>
        </execution>
    </executions>
</plugin>
```

### Spring Security MFA

Declarative multi-factor authentication with `@EnableMultiFactorAuthentication` and One-Time Token (OTT) support.

```java
@Configuration
@EnableWebSecurity
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
public class SecurityConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(Customizer.withDefaults())
            .build();
    }
}
```

### Modular Auto-Configuration

The monolithic `spring-boot-autoconfigure` JAR is now split into focused modules. Features that "just worked" before now require explicit dependencies.

```xml
<!-- Quick migration — restore 3.x behavior -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-autoconfigure-classic</artifactId>
</dependency>

<!-- Recommended — explicit modular dependencies -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-restclient</artifactId>
</dependency>
```

| Missing Feature | Add This Dependency |
|-----------------|---------------------|
| RestClient | `spring-boot-starter-restclient` |
| H2 Console | `spring-boot-starter-h2-console` |
| JPA/Hibernate | `spring-boot-autoconfigure-data-jpa` |
| Flyway | Appropriate Flyway starter |

### Jackson 3 — Additional New Features

Beyond the package rename (`com.fasterxml` → `tools.jackson`), Jackson 3 brings:

| Feature | Jackson 2 | Jackson 3 |
|---------|-----------|-----------|
| Date format | Numeric timestamp | ISO-8601 string (default) |
| Exceptions | Checked | Unchecked (better for lambdas/streams) |
| Configuration | Mutable | Immutable builders |
| JSON View filtering | `MappingJacksonValue` | `hint()` method |

### JMS Client API

Modern fluent `JmsClient` API replaces verbose `JmsTemplate` for Apache Artemis messaging.

```java
// Fire-and-forget
jmsClient.send("orders.queue").withBody(order);

// With QoS
jmsClient.send("orders.queue")
    .withPriority(9)
    .withTimeToLive(Duration.ofMinutes(5))
    .withBody(order);

// Request-reply
OrderConfirmation confirmation = jmsClient.requestAndReceive("orders.queue")
    .withBody(order)
    .convertTo(OrderConfirmation.class);
```

---

## OpenRewrite Automation

The skill also supports automated refactoring via OpenRewrite:

```bash
# Maven
mvn rewrite:run

# Gradle
./gradlew rewriteRun
```

Recipe: `org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0`

---

## Compatibility

This skill works with any AI assistant that supports the Agent Skills format:

- **Claude Code**
- **GitHub Copilot**
- **Cursor**
- **Cline**
- Other compatible AI coding tools

---

## License

MIT — see [LICENSE](../LICENSE) for details.

---

## Author

**Ajay Wadhara** — [@ajaywadhara](https://github.com/ajaywadhara)

Found this useful? [⭐ Star the repo](https://github.com/ajaywadhara/agent-skills) to help others discover it!
