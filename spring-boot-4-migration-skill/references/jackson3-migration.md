# Jackson 3 Migration Reference

Complete guide for migrating from Jackson 2 to Jackson 3 in Spring Boot 4.

---

## Overview

Spring Boot 4.0 uses Jackson 3 as the default JSON library. Jackson 3 brings:
- New package structure (`tools.jackson.*`)
- Immutable `JsonMapper` (replaces mutable `ObjectMapper`)
- Unchecked exceptions (no more `JsonProcessingException`)
- Changed default behaviors

---

## Package Changes

### Core Databind Classes

```java
// Jackson 2 imports
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.Module;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.fasterxml.jackson.databind.ObjectReader;

// Jackson 3 imports
import tools.jackson.databind.ObjectMapper;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.SerializationFeature;
import tools.jackson.databind.DeserializationFeature;
import tools.jackson.databind.ValueSerializer;
import tools.jackson.databind.ValueDeserializer;
import tools.jackson.databind.JacksonModule;
import tools.jackson.databind.ObjectWriter;
import tools.jackson.databind.ObjectReader;
```

### Core Classes

```java
// Jackson 2
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonFactory;

// Jackson 3
import tools.jackson.core.JsonParser;
import tools.jackson.core.JsonGenerator;
import tools.jackson.core.JsonFactory;
```

### Annotations - UNCHANGED

**Important:** Jackson annotations remain in the original package:

```java
// These DO NOT change - still use com.fasterxml.jackson.annotation
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
```

### Maven Coordinates

```xml
<!-- Jackson 2 (old) -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>

<!-- Jackson 3 (new) -->
<dependency>
    <groupId>tools.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>

<!-- Annotations - still uses old group ID -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-annotations</artifactId>
</dependency>
```

---

## Class Renames

### Spring Boot Classes

| Jackson 2 (Boot 3.x) | Jackson 3 (Boot 4.x) |
|----------------------|----------------------|
| `@JsonComponent` | `@JacksonComponent` |
| `@JsonMixin` | `@JacksonMixin` |
| `JsonObjectSerializer` | `ObjectValueSerializer` |
| `JsonObjectDeserializer` | `ObjectValueDeserializer` |
| `Jackson2ObjectMapperBuilder` | `JsonMapper.builder()` |
| `Jackson2ObjectMapperBuilderCustomizer` | `JsonMapperBuilderCustomizer` |

### Code Examples

**Custom Serializer:**
```java
// Jackson 2 (Boot 3.x)
@JsonComponent
public class MoneySerializer extends JsonObjectSerializer<Money> {
    @Override
    protected void serializeObject(Money value, JsonGenerator gen, SerializerProvider provider) {
        gen.writeStringField("amount", value.getAmount().toString());
        gen.writeStringField("currency", value.getCurrency().getCurrencyCode());
    }
}

// Jackson 3 (Boot 4.x)
@JacksonComponent
public class MoneySerializer extends ObjectValueSerializer<Money> {
    @Override
    protected void serializeFields(Money value, JsonGenerator gen, SerializerProvider provider) {
        gen.writeStringProperty("amount", value.getAmount().toString());
        gen.writeStringProperty("currency", value.getCurrency().getCurrencyCode());
    }
}
```

**Custom Deserializer:**
```java
// Jackson 2 (Boot 3.x)
@JsonComponent
public class MoneyDeserializer extends JsonObjectDeserializer<Money> {
    @Override
    protected Money deserializeObject(JsonParser parser, DeserializationContext context, ObjectCodec codec, JsonNode tree) {
        String amount = nullSafeValue(tree.get("amount"), String.class);
        String currency = nullSafeValue(tree.get("currency"), String.class);
        return new Money(new BigDecimal(amount), Currency.getInstance(currency));
    }
}

// Jackson 3 (Boot 4.x)
@JacksonComponent
public class MoneyDeserializer extends ObjectValueDeserializer<Money> {
    @Override
    protected Money deserializeFromObject(JsonParser parser, DeserializationContext context) {
        JsonNode tree = parser.readValueAsTree();
        String amount = tree.get("amount").asText();
        String currency = tree.get("currency").asText();
        return new Money(new BigDecimal(amount), Currency.getInstance(currency));
    }
}
```

**ObjectMapper Configuration:**
```java
// Jackson 2 (Boot 3.x)
@Bean
public ObjectMapper objectMapper() {
    return Jackson2ObjectMapperBuilder.json()
        .featuresToEnable(SerializationFeature.INDENT_OUTPUT)
        .featuresToDisable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
        .build();
}

// Jackson 3 (Boot 4.x) - Using JsonMapperBuilderCustomizer (recommended)
@Bean
public JsonMapperBuilderCustomizer jsonMapperCustomizer() {
    return builder -> builder
        .enable(SerializationFeature.INDENT_OUTPUT)
        .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
}

// Jackson 3 (Boot 4.x) - Direct builder usage
@Bean
public JsonMapper jsonMapper() {
    return JsonMapper.builder()
        .enable(SerializationFeature.INDENT_OUTPUT)
        .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
        .build();
}
```

---

## Default Behavior Changes

### Changed Defaults

| Feature | Jackson 2 Default | Jackson 3 Default | Impact |
|---------|-------------------|-------------------|--------|
| `MapperFeature.SORT_PROPERTIES_ALPHABETICALLY` | `false` | `true` | JSON property order changes |
| `SerializationFeature.WRITE_DATES_AS_TIMESTAMPS` | `true` | `false` | Dates serialize as ISO-8601 strings |
| `DeserializationFeature.FAIL_ON_NULL_FOR_PRIMITIVES` | `false` | `true` | Null to primitive fails |
| `DeserializationFeature.FAIL_ON_TRAILING_TOKENS` | `false` | `true` | Extra content after JSON fails |

### Locale Serialization

```java
// Jackson 2 serialized Locale.CHINA as:
"zh_CN"

// Jackson 3 serializes Locale.CHINA as (IETF BCP 47 Language Tag):
"zh-CN"
```

### Date/Time Serialization

```java
// Jackson 2 default (timestamps)
{"createdAt": 1704067200000}

// Jackson 3 default (ISO-8601)
{"createdAt": "2024-01-01T00:00:00Z"}
```

---

## Compatibility Mode

### Use Jackson 2 Defaults

To minimize behavior changes during migration:

```yaml
# application.yml
spring:
  jackson:
    use-jackson2-defaults: true
```

This aligns JsonMapper defaults with Jackson 2 behavior from Boot 3.x.

### Disable Auto Module Detection

Jackson 3 auto-detects and registers all classpath modules (Jackson 2 only did "well-known" ones):

```yaml
spring:
  jackson:
    find-and-add-modules: false
```

---

## Keeping Jackson 2 (Temporary)

For applications not ready to migrate JSON handling:

### Add Jackson 2 Module

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-jackson2</artifactId>
</dependency>
```

### Configure Preferred Mapper

```yaml
# For Spring MVC
spring:
  http:
    converters:
      preferred-json-mapper: jackson2

# For WebFlux
spring:
  http:
    codecs:
      preferred-json-mapper: jackson2
```

### Jackson 2 Properties

Use `spring.jackson2.*` namespace (equivalent to `spring.jackson` in Boot 3.5):

```yaml
spring:
  jackson2:
    serialization:
      INDENT_OUTPUT: true
    deserialization:
      FAIL_ON_UNKNOWN_PROPERTIES: false
```

**Note:** `spring-boot-jackson2` is deprecated and will be removed in a future release.

---

## Exception Handling

### Unchecked Exceptions

Jackson 3 uses unchecked exceptions:

```java
// Jackson 2 - checked exception
try {
    String json = objectMapper.writeValueAsString(object);
} catch (JsonProcessingException e) {
    // Handle checked exception
}

// Jackson 3 - unchecked exception
try {
    String json = jsonMapper.writeValueAsString(object);
} catch (JacksonException e) {
    // Handle unchecked exception (RuntimeException)
}

// Jackson 3 - can also use in lambdas without try-catch
List<String> jsons = objects.stream()
    .map(jsonMapper::writeValueAsString)
    .toList();
```

---

## Module Registration

### Jackson 2 (Boot 3.x)

```java
@Bean
public ObjectMapper objectMapper() {
    ObjectMapper mapper = new ObjectMapper();
    mapper.registerModule(new JavaTimeModule());
    mapper.registerModule(new ParameterNamesModule());
    return mapper;
}
```

### Jackson 3 (Boot 4.x)

```java
// Auto-detection is enabled by default
// All modules on classpath are registered automatically

// To add custom module:
@Bean
public JsonMapperBuilderCustomizer customModules() {
    return builder -> builder.addModule(new MyCustomModule());
}

// Or create a JacksonModule bean
@Bean
public JacksonModule myCustomModule() {
    return new MyCustomModule();
}
```

---

## Spring Security Jackson Integration

### Jackson 2

```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModules(SecurityJackson2Modules.getModules(classLoader));
```

### Jackson 3

```java
JsonMapper.Builder builder = JsonMapper.builder();
SecurityJacksonModules.configure(builder);
JsonMapper mapper = builder.build();
```

---

## Testing with Jackson 3

### Test Configuration

```java
@SpringBootTest
class JacksonTest {
    @Autowired
    private JsonMapper jsonMapper;

    @Test
    void serializesCorrectly() {
        MyObject obj = new MyObject("test");
        String json = jsonMapper.writeValueAsString(obj);
        assertThat(json).isEqualTo("{\"name\":\"test\"}");
    }
}
```

### Custom ObjectMapper in Tests

```java
@TestConfiguration
static class TestJacksonConfig {
    @Bean
    public JsonMapperBuilderCustomizer testCustomizer() {
        return builder -> builder.enable(SerializationFeature.INDENT_OUTPUT);
    }
}
```

---

## OpenRewrite Recipe

Automate Jackson 2 to 3 migration:

```bash
# Maven
./mvnw rewrite:run -Drewrite.activeRecipes=org.openrewrite.java.jackson.UpgradeJackson_2_3

# Gradle
./gradlew rewriteRun -Drewrite.activeRecipes=org.openrewrite.java.jackson.UpgradeJackson_2_3
```

This recipe handles:
- Package import changes
- Maven coordinate updates
- Common API migrations

---

## Migration Checklist

- [ ] Update import statements (`com.fasterxml.jackson.databind` → `tools.jackson.databind`)
- [ ] Rename `@JsonComponent` to `@JacksonComponent`
- [ ] Rename `@JsonMixin` to `@JacksonMixin`
- [ ] Update custom serializers to extend `ObjectValueSerializer`
- [ ] Update custom deserializers to extend `ObjectValueDeserializer`
- [ ] Replace `Jackson2ObjectMapperBuilderCustomizer` with `JsonMapperBuilderCustomizer`
- [ ] Update exception handling from checked to unchecked
- [ ] Test date/time serialization format
- [ ] Test property ordering if tests depend on it
- [ ] Test Locale serialization if applicable
- [ ] Verify null handling for primitives
