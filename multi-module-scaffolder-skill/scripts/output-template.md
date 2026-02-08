# Project Scaffolded Successfully

## Summary

| | |
|---|---|
| **Project** | `{project_name}` |
| **Package** | `{base_package}` |
| **Java** | 21 |
| **Spring Boot** | 4.0.0 |
| **Modules** | `server`, `api-gateway`, `common:exception` |

## Generated File Tree

```
{project_name}/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── gradle/libs.versions.toml
├── .gitignore
│
├── server/
│   ├── build.gradle.kts
│   └── src/
│       ├── main/java/{pkg_path}/server/
│       │   ├── {pascal_name}Application.java
│       │   └── exception/
│       │       └── ServerException.java
│       ├── main/resources/
│       │   └── application.yml
│       └── test/java/{pkg_path}/server/
│           └── {pascal_name}ApplicationTests.java
│
├── api-gateway/
│   ├── build.gradle.kts
│   └── src/main/java/{pkg_path}/gateway/
│       └── exception/
│           └── ApiGatewayException.java
│
└── common/
    ├── build.gradle.kts
    └── exception/
        ├── build.gradle.kts
        └── src/main/java/{pkg_path}/common/exception/
            ├── {pascal_name}Exception.java
            ├── ResourceNotFoundException.java
            ├── ValidationException.java
            ├── BadRequestException.java
            ├── ServiceException.java
            ├── config/
            │   └── ExceptionHandlingConfig.java
            ├── handler/
            │   └── GlobalExceptionHandler.java
            └── model/
                ├── ErrorCode.java
                ├── ErrorCategory.java
                └── ErrorResponse.java
```

## Exception Hierarchy

```
RuntimeException
└── {pascal_name}Exception (common:exception)
    ├── ResourceNotFoundException      — "User with identifier '123' not found"
    ├── ValidationException            — field-level errors with ValidationError list
    ├── BadRequestException            — "Invalid value for field 'email': must not be empty"
    ├── ServiceException               — static factories: externalServiceError(), databaseError()
    ├── ServerException (server)       — server module specific errors
    └── ApiGatewayException (gateway)  — API gateway module specific errors
```

## Module Dependency Graph

```
server ──► api-gateway ──► common:exception
  │                              ▲
  └──────────────────────────────┘
```

## Next Steps

1. **Initialize Git**
   ```bash
   cd {project_name}
   git init
   git add .
   git commit -m "Initial project scaffold"
   ```

2. **Add Gradle Wrapper** (requires Gradle 8.14+ installed)
   ```bash
   cd {project_name}
   gradle wrapper --gradle-version 8.14
   ```

3. **Import in IDE**
   - Open the `{project_name}` directory in IntelliJ IDEA
   - Select "Import Gradle Project" when prompted
   - Wait for Gradle sync to complete

4. **Run the Application**
   ```bash
   ./gradlew :server:bootRun
   ```
   Or use the local run task:
   ```bash
   ./gradlew :server:localRun
   ```

5. **Add Your Domain Code**
   - Add controllers to `api-gateway`
   - Add services and repositories to `server`
   - Add domain-specific error codes to `ErrorCode.java`
   - Add domain-specific exceptions extending `{pascal_name}Exception`
