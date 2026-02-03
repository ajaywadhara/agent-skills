# Observability Migration Reference

Complete guide for migrating observability (metrics, tracing, logging) from Spring Boot 3.x to 4.x.

---

## Overview

Spring Boot 4.0 introduces:
- New `spring-boot-starter-opentelemetry` for unified observability
- OTLP (OpenTelemetry Protocol) as primary export format
- Simplified dependency management
- Decoupled from Actuator (observability without full Actuator)

---

## New OpenTelemetry Starter

### Before (3.x) - Multiple Dependencies

```xml
<!-- Spring Boot 3.x - Multiple dependencies needed -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-otlp</artifactId>
</dependency>
```

### After (4.x) - Single Starter

```xml
<!-- Spring Boot 4.x - Single starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

This starter includes:
- Micrometer tracing bridge for OpenTelemetry
- OTLP exporters for metrics and traces
- OpenTelemetry SDK auto-configuration
- Automatic instrumentation for HTTP, JDBC, etc.

---

## Configuration

### Basic OTLP Export

```yaml
management:
  otlp:
    metrics:
      export:
        url: http://localhost:4318/v1/metrics
        enabled: true
    tracing:
      endpoint: http://localhost:4318/v1/traces

  opentelemetry:
    tracing:
      export:
        otlp:
          endpoint: http://localhost:4318/v1/traces
```

### Service Identification

```yaml
management:
  opentelemetry:
    resource:
      attributes:
        service.name: my-service
        service.version: 1.0.0
        deployment.environment: production
```

### Sampling Configuration

```yaml
management:
  tracing:
    sampling:
      probability: 1.0  # 100% sampling
```

---

## Property Changes

### Renamed Properties

```yaml
# Old (3.x)
management:
  tracing:
    enabled: true

# New (4.x)
management:
  tracing:
    export:
      enabled: true
```

### Test Properties

```yaml
# Old (3.x)
spring:
  test:
    observability: true

# New (4.x)
spring:
  test:
    metrics:
      export: true
    tracing:
      export: true
```

---

## Automatic Instrumentation

With `spring-boot-starter-opentelemetry`, automatic instrumentation for:

- **HTTP Server** - All controller endpoints
- **HTTP Client** - RestTemplate, RestClient, WebClient
- **JDBC** - Database queries
- **Logging** - Trace/span IDs in logs

### Verify Instrumentation

```java
@RestController
public class TestController {
    private static final Logger log = LoggerFactory.getLogger(TestController.class);

    @GetMapping("/test")
    public String test() {
        // Trace ID automatically included in logs
        log.info("Processing request");
        return "OK";
    }
}
```

Log output includes trace context:
```
2025-01-15 10:30:00.123 INFO [my-service,abc123def456,xyz789] TestController : Processing request
```

---

## Observability Annotations

### Enable Annotation Scanning

```yaml
management:
  observations:
    annotations:
      enabled: true
```

### Required Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aspectj</artifactId>
</dependency>
```

### Available Annotations

```java
import io.micrometer.observation.annotation.Observed;
import io.micrometer.core.annotation.Timed;
import io.micrometer.core.annotation.Counted;

@Service
public class MyService {

    // Creates observation (both metric and trace)
    @Observed(name = "my.operation", contextualName = "my-operation")
    public void observedOperation() {}

    // Creates timer metric
    @Timed(value = "my.timed.operation", description = "Time for operation")
    public void timedOperation() {}

    // Creates counter metric
    @Counted(value = "my.operation.count", description = "Count of operations")
    public void countedOperation() {}
}
```

---

## Micrometer Integration

### How It Works

Spring Boot uses Micrometer as the observability API internally:

```
Application Code
       ↓
Micrometer Observation API
       ↓
micrometer-tracing-bridge-otel
       ↓
OpenTelemetry SDK
       ↓
OTLP Exporter
       ↓
Observability Backend (Grafana, Jaeger, etc.)
```

### Custom Meters

```java
@Component
public class CustomMetrics {
    private final MeterRegistry registry;

    public CustomMetrics(MeterRegistry registry) {
        this.registry = registry;
    }

    public void recordBusinessMetric(double value) {
        registry.gauge("business.metric", value);
    }

    public void countEvent() {
        registry.counter("business.events").increment();
    }
}
```

---

## Redis Observability Change

### Command Latency Recording

```java
// Old (3.x)
MicrometerCommandLatencyRecorder recorder;

// New (4.x)
MicrometerTracing tracing;
```

### Configuration

```yaml
# Redis observability auto-configured with spring-boot-starter-data-redis
spring:
  data:
    redis:
      lettuce:
        pool:
          enabled: true
```

---

## Actuator Independence

### Observability Without Full Actuator

In Spring Boot 4.x, you can have observability without the full Actuator module:

```xml
<!-- Observability only -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>

<!-- No need for spring-boot-starter-actuator for basic observability -->
```

### With Actuator Endpoints

```xml
<!-- Full observability + management endpoints -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

---

## Health Indicators

### SSL Certificate Health

```yaml
# Old behavior - threshold-based status
# STATUS: WILL_EXPIRE_SOON

# New behavior - status is VALID, expiring certs listed separately
# STATUS: VALID
# expiringChains: [list of expiring certificates]
```

### Health Probes (Default Enabled)

```yaml
# Liveness and readiness probes enabled by default
management:
  endpoint:
    health:
      probes:
        enabled: true  # default in 4.x

# Disable if not using Kubernetes
management:
  endpoint:
    health:
      probes:
        enabled: false
```

---

## Logging Changes

### Default Charset

Logback now uses UTF-8 by default (aligned with Log4j2):

```yaml
# If you need different charset
logging:
  charset:
    console: ISO-8859-1
    file: UTF-8
```

### Console Logging Control

```yaml
logging:
  console:
    enabled: true  # can disable console output
```

### Structured Logging (JSON)

```yaml
logging:
  structured:
    format:
      console: json
      file: json
```

---

## Grafana LGTM Stack Integration

### Complete Configuration

```yaml
management:
  otlp:
    metrics:
      export:
        url: http://localhost:4318/v1/metrics
    tracing:
      endpoint: http://localhost:4318/v1/traces

  opentelemetry:
    resource:
      attributes:
        service.name: ${spring.application.name}

  tracing:
    sampling:
      probability: 1.0

  observations:
    annotations:
      enabled: true

# Loki for logs (via logback appender)
logging:
  structured:
    format:
      console: json
```

### Docker Compose Example

```yaml
version: '3.8'
services:
  otel-collector:
    image: otel/opentelemetry-collector:latest
    ports:
      - "4317:4317"  # gRPC
      - "4318:4318"  # HTTP
    volumes:
      - ./otel-config.yaml:/etc/otelcol/config.yaml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

  tempo:
    image: grafana/tempo:latest
    ports:
      - "3200:3200"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
```

---

## Migration Checklist

- [ ] Replace individual Micrometer/OTel dependencies with `spring-boot-starter-opentelemetry`
- [ ] Update `management.tracing.enabled` to `management.tracing.export.enabled`
- [ ] Update `spring.test.observability` to separate metrics/tracing properties
- [ ] Add `spring-boot-starter-aspectj` if using observability annotations
- [ ] Enable `management.observations.annotations.enabled` if using `@Observed`
- [ ] Update Redis observability code (`MicrometerCommandLatencyRecorder` → `MicrometerTracing`)
- [ ] Configure OTLP endpoints for metrics and traces
- [ ] Review health probe configuration (enabled by default)
- [ ] Update SSL certificate health monitoring expectations
- [ ] Configure logging charset if non-UTF-8 needed
- [ ] Test trace context propagation in logs
- [ ] Verify metrics export to backend
- [ ] Verify traces visible in tracing backend
