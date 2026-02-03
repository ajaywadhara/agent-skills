# Testing Migration Reference

Complete guide for migrating test infrastructure from Spring Boot 3.x to 4.x.

---

## Overview

Spring Boot 4.0 testing changes include:
- `@MockBean`/`@SpyBean` replaced with `@MockitoBean`/`@MockitoSpyBean`
- JUnit 6 support (backward compatible with JUnit 5)
- Testcontainers 2.0
- `RestTestClient` replaces `TestRestTemplate`
- Explicit auto-configuration annotations required

---

## MockBean Migration

### Basic Replacement

```java
// Spring Boot 3.x
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;

@SpringBootTest
class ServiceTest {
    @MockBean
    private ExternalService externalService;

    @SpyBean
    private CacheService cacheService;
}

// Spring Boot 4.x
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;

@SpringBootTest
class ServiceTest {
    @MockitoBean
    private ExternalService externalService;

    @MockitoSpyBean
    private CacheService cacheService;
}
```

### Key Differences

| Feature | `@MockBean` (3.x) | `@MockitoBean` (4.x) |
|---------|-------------------|----------------------|
| Package | `org.springframework.boot.test.mock.mockito` | `org.springframework.test.context.bean.override.mockito` |
| In `@Configuration` | Supported | **NOT Supported** |
| Field only | No | Yes |
| Bean scopes | Singleton only | All scopes (new!) |

### Shared Mocks Pattern

**Old Approach (3.x) - Mocks in Configuration:**
```java
@TestConfiguration
static class MockConfig {
    @MockBean
    private UserService userService;

    @MockBean
    private PaymentService paymentService;
}

@SpringBootTest
@Import(MockConfig.class)
class ApplicationTest {}
```

**New Approach (4.x) - Type-level annotation:**
```java
// Option 1: Direct on test class
@SpringBootTest
@MockitoBean(types = {UserService.class, PaymentService.class})
class ApplicationTest {}

// Option 2: Custom annotation for reuse
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@MockitoBean(types = {UserService.class, PaymentService.class})
public @interface CommonMocks {}

@SpringBootTest
@CommonMocks
class ApplicationTest {}
```

### Non-Singleton Bean Mocking (New in 4.x)

```java
// Now works with prototype and custom scopes
@SpringBootTest
class PrototypeBeanTest {
    @MockitoBean
    private PrototypeScopedService service;  // Was not possible in 3.x
}
```

---

## @SpringBootTest Changes

### MockMvc Not Auto-Configured

```java
// Spring Boot 3.x - MockMvc available automatically
@SpringBootTest
class ControllerTest {
    @Autowired
    private MockMvc mockMvc;  // Worked automatically
}

// Spring Boot 4.x - Explicit annotation required
@SpringBootTest
@AutoConfigureMockMvc
class ControllerTest {
    @Autowired
    private MockMvc mockMvc;
}
```

### RestTestClient (New)

```java
// Spring Boot 3.x - TestRestTemplate
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class ApiTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void testEndpoint() {
        ResponseEntity<String> response = restTemplate.getForEntity("/api/data", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
}

// Spring Boot 4.x - RestTestClient (recommended)
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class ApiTest {
    @Autowired
    private RestTestClient restTestClient;

    @Test
    void testEndpoint() {
        restTestClient.get()
            .uri("/api/data")
            .exchange()
            .expectStatus().isOk()
            .expectBody(String.class)
            .value(body -> assertThat(body).contains("expected"));
    }
}

// Spring Boot 4.x - With MockMvc backend
@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureRestTestClient
class ApiTest {
    @Autowired
    private RestTestClient restTestClient;  // Uses MockMvc internally
}
```

### TestRestTemplate Migration

```java
// Old location
import org.springframework.boot.test.web.client.TestRestTemplate;

// New location
import org.springframework.boot.resttestclient.TestRestTemplate;

// Required dependency
// spring-boot-resttestclient (runtime)
// spring-boot-restclient (compile)
```

---

## HtmlUnit Configuration

### Attribute Restructuring

```java
// Spring Boot 3.x
@AutoConfigureMockMvc(
    webClientEnabled = false,
    webDriverEnabled = false
)

// Spring Boot 4.x
@AutoConfigureMockMvc(
    htmlUnit = @HtmlUnit(
        webClient = false,
        webDriver = false
    )
)
```

---

## JUnit 6 Support

### Migration from JUnit 5

JUnit 6 is mostly backward compatible with JUnit 5:

```java
// JUnit 5 - continues to work
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;

@SpringBootTest
class MyTest {
    @BeforeEach
    void setUp() {}

    @Test
    @DisplayName("Should work correctly")
    void testSomething() {}
}
```

### JUnit 6 New Features

```java
// Enhanced @Nested support
@SpringBootTest
class ParentTest {
    @Nested
    @DisplayName("When user is authenticated")
    class AuthenticatedTests {
        @BeforeEach
        void authenticateUser() {}

        @Test
        void canAccessProtectedResource() {}
    }
}

// JSpecify null safety annotations
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;
```

### JUnit 4 Removal

JUnit 4 is completely removed. If you have JUnit 4 tests:

```java
// JUnit 4 - NOT SUPPORTED
import org.junit.Test;
import org.junit.Before;
import org.junit.runner.RunWith;

// Must migrate to JUnit 5/6
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
```

---

## Testcontainers 2.0

### Module Name Changes

```java
// Testcontainers 1.x
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.containers.MongoDBContainer;

// Testcontainers 2.x - same imports, but check module names
// testcontainers-postgres → testcontainers-postgresql
// etc.
```

### Service Connection Enhancements

```java
// Spring Boot 4.x - New MongoDB Atlas Local support
@SpringBootTest
@Testcontainers
class MongoTest {
    @Container
    @ServiceConnection
    static MongoDBAtlasLocalContainer mongo = new MongoDBAtlasLocalContainer("mongodb/mongodb-atlas-local:7");
}

// Standard containers - unchanged
@SpringBootTest
@Testcontainers
class DatabaseTest {
    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Container
    @ServiceConnection
    static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.5.0"));
}
```

### JUnit 4 Support Removed

Testcontainers 2.0 removes JUnit 4 support entirely. Use JUnit 5/6:

```java
// Use @Testcontainers from JUnit 5 extension
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.junit.jupiter.Container;

@SpringBootTest
@Testcontainers
class IntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
}
```

---

## Slice Tests

### Required Test Starters

```java
// If testing web layer
@WebMvcTest(UserController.class)
class UserControllerTest {}
// Requires: spring-boot-starter-webmvc-test

// If testing JPA layer
@DataJpaTest
class UserRepositoryTest {}
// Requires: spring-boot-starter-data-jpa-test

// If testing MongoDB layer
@DataMongoTest
class DocumentRepositoryTest {}
// Requires: spring-boot-starter-data-mongodb-test
```

### Example Slice Test

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        when(userService.findById(1L)).thenReturn(new User(1L, "John"));

        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}
```

---

## Test Context Caching

### Auto-Pausing (New in 4.x)

Spring Boot 4.0 automatically pauses cached test contexts when not in use, improving resource management for large test suites.

### Context Configuration

```java
// Unique context per test class
@SpringBootTest(properties = "test.property=unique-value")
class UniqueContextTest {}

// Shared context (same configuration = same context)
@SpringBootTest
class SharedContextTest1 {}

@SpringBootTest
class SharedContextTest2 {}  // Shares context with SharedContextTest1
```

---

## Mockito Configuration

### Using MockitoExtension

```java
// For unit tests (no Spring context)
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class UnitTest {
    @Mock
    private Repository repository;

    @InjectMocks
    private Service service;

    @Test
    void test() {
        when(repository.find(1L)).thenReturn(Optional.of(new Entity()));
        assertThat(service.get(1L)).isNotNull();
    }
}
```

### @Mock vs @MockitoBean

| Annotation | Use Case | Spring Context |
|------------|----------|----------------|
| `@Mock` | Unit tests | No |
| `@MockitoBean` | Integration tests | Yes |

```java
// Unit test - no Spring
@ExtendWith(MockitoExtension.class)
class UnitTest {
    @Mock
    private Dependency dependency;
}

// Integration test - with Spring
@SpringBootTest
class IntegrationTest {
    @MockitoBean
    private Dependency dependency;  // Replaces bean in context
}
```

---

## Test Properties

### Configuration

```java
// Inline properties
@SpringBootTest(properties = {
    "spring.datasource.url=jdbc:h2:mem:test",
    "logging.level.root=WARN"
})

// Properties file
@TestPropertySource("/test.properties")

// YAML (new in Spring Boot 4)
@TestPropertySource(locations = "/test.yml")
```

### Deprecated Property

```yaml
# Old
spring:
  test:
    observability: true

# New
spring:
  test:
    metrics:
      export: true
    tracing:
      export: true
```

---

## Migration Checklist

- [ ] Replace `@MockBean` with `@MockitoBean`
- [ ] Replace `@SpyBean` with `@MockitoSpyBean`
- [ ] Move mocks from `@Configuration` to test class or custom annotation
- [ ] Add `@AutoConfigureMockMvc` where MockMvc is needed
- [ ] Add `@AutoConfigureRestTestClient` for RestTestClient
- [ ] Update HtmlUnit configuration to nested `@HtmlUnit` annotation
- [ ] Migrate JUnit 4 tests to JUnit 5/6
- [ ] Update Testcontainers to 2.x
- [ ] Add appropriate test starters for slice tests
- [ ] Update TestRestTemplate imports if still using
- [ ] Remove JUnit 4 dependencies
- [ ] Verify all tests pass
