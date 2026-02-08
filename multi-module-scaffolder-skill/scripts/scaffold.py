#!/usr/bin/env python3
"""
Multi-Module Scaffolder — Spring Boot 4 Project Generator

Generates a complete multi-module Gradle project with:
- server module (Spring Boot application)
- api-gateway module (library)
- common:exception module (exception handling framework)
- Gradle version catalog (libs.versions.toml)
- Production-grade exception hierarchy with GlobalExceptionHandler

Usage:
    python3 scaffold.py --name my-app --package com.example.myapp --output-dir /path/to/output
"""

import argparse
import os
import re
import sys


# ─── ANSI Colors ─────────────────────────────────────────────────────────────

class Color:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# ─── Name Conversion Helpers ─────────────────────────────────────────────────

def kebab_to_pascal(name: str) -> str:
    """Convert kebab-case to PascalCase: 'my-app' -> 'MyApp'"""
    return "".join(word.capitalize() for word in name.split("-"))


def kebab_to_package_segment(name: str) -> str:
    """Convert kebab-case to package segment: 'my-app' -> 'myapp'"""
    return name.replace("-", "")


def package_to_path(package: str) -> str:
    """Convert package to directory path: 'com.example.myapp' -> 'com/example/myapp'"""
    return package.replace(".", "/")


# ─── Validation ──────────────────────────────────────────────────────────────

def validate_project_name(name: str) -> bool:
    """Validate kebab-case project name."""
    return bool(re.match(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$", name))


def validate_package(package: str) -> bool:
    """Validate Java package name."""
    return bool(re.match(r"^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$", package))


# ─── File Content Templates ──────────────────────────────────────────────────

def root_build_gradle(group: str) -> str:
    return f'''plugins {{
    java
    checkstyle
}}

group = "{group}"
version = "1.0.0"

java {{
    toolchain {{
        languageVersion = JavaLanguageVersion.of(libs.versions.javaVersion.get())
    }}
}}

repositories {{
    mavenCentral()
}}

// Root project doesn't need tests
tasks.withType<Test> {{
    enabled = false
}}
'''


def settings_gradle(project_name: str) -> str:
    return f'''rootProject.name = "{project_name}"

include(
    "server",
    "api-gateway",
    "common",
    "common:exception"
)

findProject(":server")?.name = "server"
findProject(":api-gateway")?.name = "api-gateway"
findProject(":common")?.name = "common"
findProject(":common:exception")?.name = "exception"
'''


def gradle_properties() -> str:
    return '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
'''


def libs_versions_toml() -> str:
    return '''[versions]
spring-boot = "4.0.0"
spring-boot-gradle-plugin = "4.0.0"
spring-dm-plugin = "1.1.7"
javaVersion = "21"
lombokVersion = "1.18.36"
postgresqlVersion = "42.7.2"

[libraries]
springboot-dependencies = { module = "org.springframework.boot:spring-boot-dependencies", version.ref = "spring-boot" }
springboot-web = { module = "org.springframework.boot:spring-boot-starter-webmvc" }
springboot-actuator = { module = "org.springframework.boot:spring-boot-starter-actuator" }
springboot-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
springboot-validation = { module = "org.springframework.boot:spring-boot-starter-validation" }
springboot-security = { module = "org.springframework.boot:spring-boot-starter-security" }
springboot-test = { module = "org.springframework.boot:spring-boot-starter-test" }
springboot-webmvc-test = { module = "org.springframework.boot:spring-boot-starter-webmvc-test" }
springboot-devtools = { module = "org.springframework.boot:spring-boot-devtools" }
spring-boot-configuration-processor = { module = "org.springframework.boot:spring-boot-configuration-processor" }
postgresql = { module = "org.postgresql:postgresql", version.ref = "postgresqlVersion" }
lombok = { module = "org.projectlombok:lombok", version.ref = "lombokVersion" }
junitplatform-launcher = { module = "org.junit.platform:junit-platform-launcher" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot-gradle-plugin" }
spring-dm = { id = "io.spring.dependency-management", version.ref = "spring-dm-plugin" }
'''


def gitignore() -> str:
    return '''# Compiled class files
*.class

# Log files
*.log

# Package files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# IDE
.idea/
*.iml
*.iws
*.ipr
.vscode/
.settings/
.project
.classpath
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Output
.output/
'''


# ─── Server Module ───────────────────────────────────────────────────────────

def server_build_gradle(base_package: str, pascal_name: str) -> str:
    return f'''import org.springframework.boot.gradle.tasks.bundling.BootJar
import org.springframework.boot.gradle.tasks.run.BootRun

plugins {{
    java
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dm)
}}

java {{
    toolchain {{
        languageVersion = JavaLanguageVersion.of(libs.versions.javaVersion.get())
    }}
}}

springBoot {{
    mainClass.set("{base_package}.server.{pascal_name}Application")
    version = rootProject.version
}}

tasks.named<BootJar>("bootJar") {{
    mainClass.set(springBoot.mainClass)
    layered {{
        enabled = true
    }}
}}

repositories {{
    mavenCentral()
}}

dependencies {{
    implementation(project(":api-gateway"))
    implementation(project(":common:exception"))
    implementation(libs.springboot.dependencies)
    implementation(libs.springboot.actuator)
    implementation(libs.springboot.data.jpa)
    implementation(libs.springboot.web)
    developmentOnly(libs.springboot.devtools)

    runtimeOnly(libs.postgresql)

    testImplementation(libs.springboot.test)
    testImplementation(libs.springboot.webmvc.test)
    testRuntimeOnly(libs.junitplatform.launcher)
}}

tasks.withType<Test> {{
    useJUnitPlatform()
}}

tasks.bootJar {{
    enabled = true
    mainClass.set(springBoot.mainClass)
}}

tasks.jar {{
    enabled = true
}}

tasks.register("localRun", BootRun::class) {{
    group = "Application"
    description = "Runs the application with local profile"
    mainClass.set("{base_package}.server.{pascal_name}Application")
    classpath = sourceSets["main"].runtimeClasspath
    environment("SPRING_PROFILES_ACTIVE", "local")
}}
'''


def application_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.server;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {{"{base_package}"}})
@EntityScan(basePackages = {{"{base_package}"}})
public class {pascal_name}Application {{

    private static final Logger log = LoggerFactory.getLogger({pascal_name}Application.class);

    public static void main(String[] args) {{
        log.info("Initializing {pascal_name} server");
        SpringApplication.run({pascal_name}Application.class, args);
    }}
}}
'''


def application_tests_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.server;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class {pascal_name}ApplicationTests {{

    @Test
    void contextLoads() {{
    }}
}}
'''


def application_yml(project_name: str) -> str:
    return f'''spring:
  application:
    name: {project_name}
  profiles:
    active: local

server:
  port: 8080

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when-authorized

logging:
  level:
    root: INFO
'''


def server_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.server.exception;

import {base_package}.common.exception.{pascal_name}Exception;
import {base_package}.common.exception.model.ErrorCode;

/**
 * Exception for server module specific errors.
 */
public class ServerException extends {pascal_name}Exception {{

    public ServerException(ErrorCode errorCode) {{
        super(errorCode);
    }}

    public ServerException(ErrorCode errorCode, String message) {{
        super(errorCode, message);
    }}

    public ServerException(ErrorCode errorCode, String message, Throwable cause) {{
        super(errorCode, message, cause);
    }}
}}
'''


# ─── API Gateway Module ──────────────────────────────────────────────────────

def gateway_build_gradle() -> str:
    return '''plugins {
    java
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dm)
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(libs.versions.javaVersion.get())
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(project(":common:exception"))
    implementation(libs.springboot.web)
    implementation(libs.springboot.validation)
    implementation(libs.springboot.actuator)

    compileOnly(libs.lombok)
    annotationProcessor(libs.lombok)

    testImplementation(libs.springboot.test)
    testImplementation(libs.springboot.webmvc.test)
    testRuntimeOnly(libs.junitplatform.launcher)
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.getByName<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar") {
    enabled = false
}

tasks.getByName<Jar>("jar") {
    enabled = true
}
'''


def gateway_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.gateway.exception;

import {base_package}.common.exception.{pascal_name}Exception;
import {base_package}.common.exception.model.ErrorCode;

/**
 * Exception for API gateway module specific errors.
 */
public class ApiGatewayException extends {pascal_name}Exception {{

    public ApiGatewayException(ErrorCode errorCode) {{
        super(errorCode);
    }}

    public ApiGatewayException(ErrorCode errorCode, String message) {{
        super(errorCode, message);
    }}

    public ApiGatewayException(ErrorCode errorCode, String message, Throwable cause) {{
        super(errorCode, message, cause);
    }}
}}
'''


# ─── Common Module ───────────────────────────────────────────────────────────

def common_build_gradle() -> str:
    return '''plugins {
    java
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dm)
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(libs.versions.javaVersion.get())
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(libs.springboot.web)
    implementation(libs.springboot.validation)

    testImplementation(libs.springboot.test)
    testRuntimeOnly(libs.junitplatform.launcher)
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.getByName<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar") {
    enabled = false
}

tasks.getByName<Jar>("jar") {
    enabled = true
}
'''


def exception_build_gradle() -> str:
    return '''plugins {
    java
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dm)
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(libs.versions.javaVersion.get())
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(libs.springboot.web)
    implementation(libs.springboot.validation)
    implementation(libs.springboot.security)
    implementation(libs.spring.boot.configuration.processor)

    compileOnly(libs.lombok)
    annotationProcessor(libs.lombok)

    testImplementation(libs.springboot.test)
    testRuntimeOnly(libs.junitplatform.launcher)
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.getByName<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar") {
    enabled = false
}

tasks.getByName<Jar>("jar") {
    enabled = true
}
'''


# ─── Exception Classes ───────────────────────────────────────────────────────

def base_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.common.exception;

import {base_package}.common.exception.model.ErrorCode;

import java.util.HashMap;
import java.util.Map;

/**
 * Base exception class for all application-specific exceptions.
 * This class includes fields for the error code and any additional details.
 */
public class {pascal_name}Exception extends RuntimeException {{

    private final ErrorCode errorCode;
    private final Map<String, Object> details;

    /**
     * Constructs a new {pascal_name}Exception with the specified error code.
     *
     * @param errorCode The error code
     */
    public {pascal_name}Exception(ErrorCode errorCode) {{
        super(errorCode.getDefaultMessage());
        this.errorCode = errorCode;
        this.details = new HashMap<>();
    }}

    /**
     * Constructs a new {pascal_name}Exception with the specified error code and message.
     *
     * @param errorCode The error code
     * @param message The error message
     */
    public {pascal_name}Exception(ErrorCode errorCode, String message) {{
        super(message);
        this.errorCode = errorCode;
        this.details = new HashMap<>();
    }}

    /**
     * Constructs a new {pascal_name}Exception with the specified error code, message, and cause.
     *
     * @param errorCode The error code
     * @param message The error message
     * @param cause The cause of the exception
     */
    public {pascal_name}Exception(ErrorCode errorCode, String message, Throwable cause) {{
        super(message, cause);
        this.errorCode = errorCode;
        this.details = new HashMap<>();
    }}

    /**
     * Gets the error code.
     *
     * @return The error code
     */
    public ErrorCode getErrorCode() {{
        return errorCode;
    }}

    /**
     * Gets the details map.
     *
     * @return The details map
     */
    public Map<String, Object> getDetails() {{
        return details;
    }}

    /**
     * Adds a detail to the details map.
     *
     * @param key The detail key
     * @param value The detail value
     * @return This exception for fluent chaining
     */
    public {pascal_name}Exception addDetail(String key, Object value) {{
        this.details.put(key, value);
        return this;
    }}
}}
'''


def resource_not_found_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.common.exception;

import {base_package}.common.exception.model.ErrorCode;

/**
 * Exception thrown when a requested resource is not found.
 */
public class ResourceNotFoundException extends {pascal_name}Exception {{

    /**
     * Constructs a new ResourceNotFoundException with the default message.
     */
    public ResourceNotFoundException() {{
        super(ErrorCode.RESOURCE_NOT_FOUND);
    }}

    /**
     * Constructs a new ResourceNotFoundException with the specified message.
     *
     * @param message The error message
     */
    public ResourceNotFoundException(String message) {{
        super(ErrorCode.RESOURCE_NOT_FOUND, message);
    }}

    /**
     * Constructs a new ResourceNotFoundException with the specified resource type and identifier.
     *
     * @param resourceType The type of resource that was not found
     * @param identifier The identifier of the resource that was not found
     */
    public ResourceNotFoundException(String resourceType, Object identifier) {{
        super(ErrorCode.RESOURCE_NOT_FOUND,
              String.format("%s with identifier '%s' not found", resourceType, identifier));
        addDetail("resourceType", resourceType);
        addDetail("identifier", identifier);
    }}

    /**
     * Constructs a new ResourceNotFoundException with the specified message and cause.
     *
     * @param message The error message
     * @param cause The cause of the exception
     */
    public ResourceNotFoundException(String message, Throwable cause) {{
        super(ErrorCode.RESOURCE_NOT_FOUND, message, cause);
    }}
}}
'''


def validation_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.common.exception;

import {base_package}.common.exception.model.ErrorCode;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Exception thrown when validation errors occur.
 */
public class ValidationException extends {pascal_name}Exception {{

    private final List<ValidationError> validationErrors;

    /**
     * Constructs a new ValidationException with the default message.
     */
    public ValidationException() {{
        super(ErrorCode.VALIDATION_ERROR);
        this.validationErrors = new ArrayList<>();
    }}

    /**
     * Constructs a new ValidationException with the specified message.
     *
     * @param message The error message
     */
    public ValidationException(String message) {{
        super(ErrorCode.VALIDATION_ERROR, message);
        this.validationErrors = new ArrayList<>();
    }}

    /**
     * Constructs a new ValidationException with the specified validation errors.
     *
     * @param validationErrors The validation errors
     */
    public ValidationException(List<ValidationError> validationErrors) {{
        super(ErrorCode.VALIDATION_ERROR, "Validation failed");
        this.validationErrors = validationErrors;
        addDetail("validationErrors", validationErrors);
    }}

    /**
     * Constructs a new ValidationException with the specified message and validation errors.
     *
     * @param message The error message
     * @param validationErrors The validation errors
     */
    public ValidationException(String message, List<ValidationError> validationErrors) {{
        super(ErrorCode.VALIDATION_ERROR, message);
        this.validationErrors = validationErrors;
        addDetail("validationErrors", validationErrors);
    }}

    /**
     * Constructs a new ValidationException with the specified message and cause.
     *
     * @param message The error message
     * @param cause The cause of the exception
     */
    public ValidationException(String message, Throwable cause) {{
        super(ErrorCode.VALIDATION_ERROR, message, cause);
        this.validationErrors = new ArrayList<>();
    }}

    /**
     * Gets the validation errors.
     *
     * @return The validation errors
     */
    public List<ValidationError> getValidationErrors() {{
        return validationErrors;
    }}

    /**
     * Adds a validation error.
     *
     * @param field The field that failed validation
     * @param message The error message
     * @return This exception
     */
    public ValidationException addValidationError(String field, String message) {{
        this.validationErrors.add(new ValidationError(field, message));
        addDetail("validationErrors", validationErrors);
        return this;
    }}

    /**
     * Adds validation errors from a map.
     *
     * @param errors The map of field names to error messages
     * @return This exception
     */
    public ValidationException addValidationErrors(Map<String, String> errors) {{
        errors.forEach(this::addValidationError);
        return this;
    }}

    /**
     * Represents a validation error for a specific field.
     */
    public static class ValidationError {{
        private final String field;
        private final String message;

        public ValidationError(String field, String message) {{
            this.field = field;
            this.message = message;
        }}

        public String getField() {{
            return field;
        }}

        public String getMessage() {{
            return message;
        }}
    }}
}}
'''


def bad_request_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.common.exception;

import {base_package}.common.exception.model.ErrorCode;

/**
 * Exception thrown when a request is invalid or malformed.
 */
public class BadRequestException extends {pascal_name}Exception {{

    /**
     * Constructs a new BadRequestException with the default message.
     */
    public BadRequestException() {{
        super(ErrorCode.INVALID_REQUEST);
    }}

    /**
     * Constructs a new BadRequestException with the specified message.
     *
     * @param message The error message
     */
    public BadRequestException(String message) {{
        super(ErrorCode.INVALID_REQUEST, message);
    }}

    /**
     * Constructs a new BadRequestException with the specified message and cause.
     *
     * @param message The error message
     * @param cause The cause of the exception
     */
    public BadRequestException(String message, Throwable cause) {{
        super(ErrorCode.INVALID_REQUEST, message, cause);
    }}

    /**
     * Constructs a new BadRequestException with the specified field and reason.
     *
     * @param field The field that is invalid
     * @param reason The reason why the field is invalid
     */
    public BadRequestException(String field, String reason) {{
        super(ErrorCode.INVALID_REQUEST, String.format("Invalid value for field '%s': %s", field, reason));
        addDetail("field", field);
        addDetail("reason", reason);
    }}
}}
'''


def service_exception_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.common.exception;

import {base_package}.common.exception.model.ErrorCode;

/**
 * Exception thrown when errors occur during service operations.
 * This can include external service errors, business logic errors, etc.
 */
public class ServiceException extends {pascal_name}Exception {{

    /**
     * Constructs a new ServiceException with the specified error code.
     *
     * @param errorCode The error code
     */
    public ServiceException(ErrorCode errorCode) {{
        super(errorCode);
    }}

    /**
     * Constructs a new ServiceException with the specified error code and message.
     *
     * @param errorCode The error code
     * @param message The error message
     */
    public ServiceException(ErrorCode errorCode, String message) {{
        super(errorCode, message);
    }}

    /**
     * Constructs a new ServiceException with the specified error code, message, and cause.
     *
     * @param errorCode The error code
     * @param message The error message
     * @param cause The cause of the exception
     */
    public ServiceException(ErrorCode errorCode, String message, Throwable cause) {{
        super(errorCode, message, cause);
    }}

    /**
     * Constructs a new ServiceException for an external service error.
     *
     * @param serviceName The name of the external service
     * @param message The error message
     * @return A new ServiceException
     */
    public static ServiceException externalServiceError(String serviceName, String message) {{
        ServiceException exception = new ServiceException(ErrorCode.EXTERNAL_SERVICE_ERROR, message);
        exception.addDetail("serviceName", serviceName);
        return exception;
    }}

    /**
     * Constructs a new ServiceException for a database error.
     *
     * @param message The error message
     * @param cause The cause of the exception
     * @return A new ServiceException
     */
    public static ServiceException databaseError(String message, Throwable cause) {{
        return new ServiceException(ErrorCode.DATABASE_ERROR, message, cause);
    }}
}}
'''


# ─── Model Classes ───────────────────────────────────────────────────────────

def error_category_java(base_package: str) -> str:
    return f'''package {base_package}.common.exception.model;

/**
 * Enum defining broad categories for error codes.
 */
public enum ErrorCategory {{
    GENERAL,
    VALIDATION,
    AUTHENTICATION,
    AUTHORIZATION,
    RESOURCE,
    EXTERNAL_SERVICE
}}
'''


def error_code_java(base_package: str) -> str:
    return f'''package {base_package}.common.exception.model;

/**
 * Enum defining standard error codes for the application.
 * Each error code has a unique code, a default message, and a category.
 */
public enum ErrorCode {{
    // General errors
    INTERNAL_SERVER_ERROR("ERR-001", "An unexpected error occurred", ErrorCategory.GENERAL),
    SERVICE_UNAVAILABLE("ERR-002", "The service is currently unavailable", ErrorCategory.GENERAL),

    // Validation errors
    VALIDATION_ERROR("ERR-100", "Validation failed", ErrorCategory.VALIDATION),
    INVALID_REQUEST("ERR-101", "Invalid request", ErrorCategory.VALIDATION),
    MISSING_REQUIRED_FIELD("ERR-102", "Required field is missing", ErrorCategory.VALIDATION),
    INVALID_FORMAT("ERR-103", "Invalid format", ErrorCategory.VALIDATION),

    // Authentication/Authorization errors
    UNAUTHORIZED("ERR-200", "Unauthorized access", ErrorCategory.AUTHENTICATION),
    FORBIDDEN("ERR-201", "Access forbidden", ErrorCategory.AUTHORIZATION),
    INVALID_CREDENTIALS("ERR-202", "Invalid credentials", ErrorCategory.AUTHENTICATION),
    TOKEN_EXPIRED("ERR-203", "Token has expired", ErrorCategory.AUTHENTICATION),

    // Resource errors
    RESOURCE_NOT_FOUND("ERR-300", "Resource not found", ErrorCategory.RESOURCE),
    RESOURCE_ALREADY_EXISTS("ERR-301", "Resource already exists", ErrorCategory.RESOURCE),
    RESOURCE_CONFLICT("ERR-302", "Resource conflict", ErrorCategory.RESOURCE),

    // External service errors
    EXTERNAL_SERVICE_ERROR("ERR-500", "External service error", ErrorCategory.EXTERNAL_SERVICE),
    DATABASE_ERROR("ERR-502", "Database error", ErrorCategory.EXTERNAL_SERVICE);

    private final String code;
    private final String defaultMessage;
    private final ErrorCategory category;

    ErrorCode(String code, String defaultMessage, ErrorCategory category) {{
        this.code = code;
        this.defaultMessage = defaultMessage;
        this.category = category;
    }}

    /**
     * Gets the error code.
     *
     * @return The error code
     */
    public String getCode() {{
        return code;
    }}

    /**
     * Gets the default error message.
     *
     * @return The default error message
     */
    public String getDefaultMessage() {{
        return defaultMessage;
    }}

    /**
     * Gets the error category.
     *
     * @return The error category
     */
    public ErrorCategory getCategory() {{
        return category;
    }}
}}
'''


def error_response_java(base_package: str) -> str:
    return f'''package {base_package}.common.exception.model;

import java.time.OffsetDateTime;
import java.util.Map;

/**
 * Standard error response model for all API errors.
 * This record provides a consistent structure for error responses across the application.
 *
 * @param timestamp The time when the error occurred
 * @param status The HTTP status code
 * @param error The error type
 * @param code The specific error code
 * @param category The error category
 * @param message The error message
 * @param path The path of the request that caused the error
 * @param details Additional details about the error
 */
public record ErrorResponse(
    OffsetDateTime timestamp,
    int status,
    String error,
    String code,
    String category,
    String message,
    String path,
    Map<String, Object> details
) {{
    /**
     * Creates a builder for ErrorResponse.
     *
     * @return A new builder instance
     */
    public static Builder builder() {{
        return new Builder();
    }}

    /**
     * Builder class for ErrorResponse.
     */
    public static class Builder {{
        private OffsetDateTime timestamp = OffsetDateTime.now();
        private int status;
        private String error;
        private String code;
        private String category;
        private String message;
        private String path;
        private Map<String, Object> details;

        public Builder status(int status) {{
            this.status = status;
            return this;
        }}

        public Builder error(String error) {{
            this.error = error;
            return this;
        }}

        public Builder code(String code) {{
            this.code = code;
            return this;
        }}

        public Builder category(String category) {{
            this.category = category;
            return this;
        }}

        public Builder message(String message) {{
            this.message = message;
            return this;
        }}

        public Builder path(String path) {{
            this.path = path;
            return this;
        }}

        public Builder details(Map<String, Object> details) {{
            this.details = details;
            return this;
        }}

        public ErrorResponse build() {{
            return new ErrorResponse(timestamp, status, error, code, category, message, path, details);
        }}
    }}
}}
'''


# ─── Handler & Config ────────────────────────────────────────────────────────

def exception_handling_config_java(base_package: str) -> str:
    return f'''package {base_package}.common.exception.config;

import {base_package}.common.exception.handler.GlobalExceptionHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

/**
 * Configuration class for exception handling.
 * Import this configuration to enable the GlobalExceptionHandler in any module.
 */
@Configuration
@Import(GlobalExceptionHandler.class)
public class ExceptionHandlingConfig {{
}}
'''


def global_exception_handler_java(base_package: str, pascal_name: str) -> str:
    return f'''package {base_package}.common.exception.handler;

import {base_package}.common.exception.BadRequestException;
import {base_package}.common.exception.ResourceNotFoundException;
import {base_package}.common.exception.ServiceException;
import {base_package}.common.exception.ValidationException;
import {base_package}.common.exception.{pascal_name}Exception;
import {base_package}.common.exception.model.ErrorCode;
import {base_package}.common.exception.model.ErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authorization.AuthorizationDeniedException;
import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.NoHandlerFoundException;

import java.util.ArrayList;
import java.util.List;

/**
 * Global exception handler for the application.
 * This class handles all exceptions and returns standardized error responses.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {{

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * Handles {pascal_name}Exception and its subclasses.
     */
    @ExceptionHandler({pascal_name}Exception.class)
    public ResponseEntity<ErrorResponse> handle{pascal_name}Exception({pascal_name}Exception ex, HttpServletRequest request) {{
        HttpStatus status = getStatusForErrorCode(ex.getErrorCode());

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(status.value())
                .error(status.getReasonPhrase())
                .code(ex.getErrorCode().getCode())
                .category(ex.getErrorCode().getCategory().name())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .details(ex.getDetails())
                .build();

        log.error("{pascal_name}Exception [{{}}]: {{}}", ex.getErrorCode().getCode(), ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, status);
    }}

    /**
     * Handles ResourceNotFoundException.
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(
            ResourceNotFoundException ex, HttpServletRequest request) {{

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.NOT_FOUND.value())
                .error(HttpStatus.NOT_FOUND.getReasonPhrase())
                .code(ex.getErrorCode().getCode())
                .category(ex.getErrorCode().getCategory().name())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .details(ex.getDetails())
                .build();

        log.error("ResourceNotFoundException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }}

    /**
     * Handles ValidationException.
     */
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            ValidationException ex, HttpServletRequest request) {{

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(ex.getErrorCode().getCode())
                .category(ex.getErrorCode().getCategory().name())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .details(ex.getDetails())
                .build();

        log.error("ValidationException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles BadRequestException.
     */
    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<ErrorResponse> handleBadRequestException(
            BadRequestException ex, HttpServletRequest request) {{

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(ex.getErrorCode().getCode())
                .category(ex.getErrorCode().getCategory().name())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .details(ex.getDetails())
                .build();

        log.error("BadRequestException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles ServiceException.
     */
    @ExceptionHandler(ServiceException.class)
    public ResponseEntity<ErrorResponse> handleServiceException(
            ServiceException ex, HttpServletRequest request) {{

        HttpStatus status = getStatusForErrorCode(ex.getErrorCode());

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(status.value())
                .error(status.getReasonPhrase())
                .code(ex.getErrorCode().getCode())
                .category(ex.getErrorCode().getCategory().name())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .details(ex.getDetails())
                .build();

        log.error("ServiceException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, status);
    }}

    /**
     * Handles MethodArgumentNotValidException.
     * Thrown when @Valid validation fails on a method argument.
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleMethodArgumentNotValidException(
            MethodArgumentNotValidException ex, HttpServletRequest request) {{

        List<ValidationException.ValidationError> validationErrors = new ArrayList<>();

        for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {{
            validationErrors.add(new ValidationException.ValidationError(
                    fieldError.getField(), fieldError.getDefaultMessage()));
        }}

        ValidationException validationException = new ValidationException(
                "Validation failed for request", validationErrors);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(validationException.getErrorCode().getCode())
                .category(validationException.getErrorCode().getCategory().name())
                .message(validationException.getMessage())
                .path(request.getRequestURI())
                .details(validationException.getDetails())
                .build();

        log.error("MethodArgumentNotValidException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles BindException.
     * Thrown when binding errors occur.
     */
    @ExceptionHandler(BindException.class)
    public ResponseEntity<ErrorResponse> handleBindException(
            BindException ex, HttpServletRequest request) {{

        List<ValidationException.ValidationError> validationErrors = new ArrayList<>();

        for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {{
            validationErrors.add(new ValidationException.ValidationError(
                    fieldError.getField(), fieldError.getDefaultMessage()));
        }}

        ValidationException validationException = new ValidationException(
                "Binding errors occurred", validationErrors);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(validationException.getErrorCode().getCode())
                .category(validationException.getErrorCode().getCategory().name())
                .message(validationException.getMessage())
                .path(request.getRequestURI())
                .details(validationException.getDetails())
                .build();

        log.error("BindException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles ConstraintViolationException.
     * Thrown when @Validated validation fails.
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolationException(
            ConstraintViolationException ex, HttpServletRequest request) {{

        ValidationException validationException = new ValidationException(
                "Constraint violations occurred");

        ex.getConstraintViolations().forEach(violation -> {{
            String propertyPath = violation.getPropertyPath().toString();
            String field = propertyPath.substring(propertyPath.lastIndexOf('.') + 1);
            validationException.addValidationError(field, violation.getMessage());
        }});

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(validationException.getErrorCode().getCode())
                .category(validationException.getErrorCode().getCategory().name())
                .message(validationException.getMessage())
                .path(request.getRequestURI())
                .details(validationException.getDetails())
                .build();

        log.error("ConstraintViolationException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles MissingServletRequestParameterException.
     * Thrown when a required request parameter is missing.
     */
    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<ErrorResponse> handleMissingServletRequestParameterException(
            MissingServletRequestParameterException ex, HttpServletRequest request) {{

        BadRequestException badRequestException = new BadRequestException(
                String.format("Required parameter '%s' of type '%s' is missing",
                        ex.getParameterName(), ex.getParameterType()));
        badRequestException.addDetail("parameterName", ex.getParameterName());
        badRequestException.addDetail("parameterType", ex.getParameterType());

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(badRequestException.getErrorCode().getCode())
                .category(badRequestException.getErrorCode().getCategory().name())
                .message(badRequestException.getMessage())
                .path(request.getRequestURI())
                .details(badRequestException.getDetails())
                .build();

        log.error("MissingServletRequestParameterException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles MethodArgumentTypeMismatchException.
     * Thrown when a method argument is not the expected type.
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleMethodArgumentTypeMismatchException(
            MethodArgumentTypeMismatchException ex, HttpServletRequest request) {{

        BadRequestException badRequestException = new BadRequestException(
                String.format("Parameter '%s' should be of type '%s'",
                        ex.getName(), ex.getRequiredType().getSimpleName()));

        badRequestException.addDetail("parameterName", ex.getName());
        badRequestException.addDetail("requiredType", ex.getRequiredType().getSimpleName());
        if (ex.getValue() != null) {{
            badRequestException.addDetail("providedValue", ex.getValue().toString());
        }}

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(badRequestException.getErrorCode().getCode())
                .category(badRequestException.getErrorCode().getCategory().name())
                .message(badRequestException.getMessage())
                .path(request.getRequestURI())
                .details(badRequestException.getDetails())
                .build();

        log.error("MethodArgumentTypeMismatchException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles HttpMessageNotReadableException.
     * Thrown when the request body is invalid.
     */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(
            HttpMessageNotReadableException ex, HttpServletRequest request) {{

        String detailedMessage = "Invalid request body format";

        Throwable cause = ex.getCause();
        if (cause != null) {{
            detailedMessage = cause.getMessage();
            if (detailedMessage != null && detailedMessage.contains("at [Source:")) {{
                detailedMessage = detailedMessage.substring(0, detailedMessage.indexOf("at [Source:")).trim();
            }}
        }}

        BadRequestException badRequestException = new BadRequestException("Invalid request body");
        badRequestException.addDetail("parseError", detailedMessage);

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .code(badRequestException.getErrorCode().getCode())
                .category(badRequestException.getErrorCode().getCategory().name())
                .message("Invalid request body format")
                .path(request.getRequestURI())
                .details(badRequestException.getDetails())
                .build();

        log.error("HttpMessageNotReadableException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }}

    /**
     * Handles NoHandlerFoundException.
     * Thrown when no handler is found for the request.
     */
    @ExceptionHandler(NoHandlerFoundException.class)
    public ResponseEntity<ErrorResponse> handleNoHandlerFoundException(
            NoHandlerFoundException ex, HttpServletRequest request) {{

        ResourceNotFoundException resourceNotFoundException = new ResourceNotFoundException(
                String.format("No handler found for %s %s", ex.getHttpMethod(), ex.getRequestURL()));

        resourceNotFoundException.addDetail("httpMethod", ex.getHttpMethod());
        resourceNotFoundException.addDetail("requestURL", ex.getRequestURL());

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.NOT_FOUND.value())
                .error(HttpStatus.NOT_FOUND.getReasonPhrase())
                .code(resourceNotFoundException.getErrorCode().getCode())
                .category(resourceNotFoundException.getErrorCode().getCategory().name())
                .message(resourceNotFoundException.getMessage())
                .path(request.getRequestURI())
                .details(resourceNotFoundException.getDetails())
                .build();

        log.error("NoHandlerFoundException: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }}

    /**
     * Handles AuthorizationDeniedException and AccessDeniedException.
     */
    @ExceptionHandler({{AuthorizationDeniedException.class, AccessDeniedException.class}})
    public ResponseEntity<ErrorResponse> handleAccessDeniedException(
            Exception ex, HttpServletRequest request) {{

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.FORBIDDEN.value())
                .error(HttpStatus.FORBIDDEN.getReasonPhrase())
                .code(ErrorCode.FORBIDDEN.getCode())
                .category(ErrorCode.FORBIDDEN.getCategory().name())
                .message(ErrorCode.FORBIDDEN.getDefaultMessage())
                .path(request.getRequestURI())
                .build();

        log.warn("Access denied for {{}} {{}}: {{}}", request.getMethod(), request.getRequestURI(), ex.getMessage());

        return new ResponseEntity<>(errorResponse, HttpStatus.FORBIDDEN);
    }}

    /**
     * Handles all other exceptions.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex, HttpServletRequest request) {{
        ServiceException serviceException = new ServiceException(
                ErrorCode.INTERNAL_SERVER_ERROR,
                "An unexpected error occurred",
                ex);

        serviceException.addDetail("exceptionType", ex.getClass().getSimpleName());
        if (ex.getMessage() != null) {{
            serviceException.addDetail("exceptionMessage", ex.getMessage());
        }}

        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
                .code(serviceException.getErrorCode().getCode())
                .category(serviceException.getErrorCode().getCategory().name())
                .message(serviceException.getMessage())
                .path(request.getRequestURI())
                .details(serviceException.getDetails())
                .build();

        log.error("Unhandled exception: {{}}", ex.getMessage(), ex);

        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }}

    /**
     * Gets the HTTP status for the given error code.
     *
     * @param errorCode The error code
     * @return The HTTP status
     */
    private HttpStatus getStatusForErrorCode(ErrorCode errorCode) {{
        return switch (errorCode) {{
            case RESOURCE_NOT_FOUND -> HttpStatus.NOT_FOUND;
            case VALIDATION_ERROR, INVALID_REQUEST, MISSING_REQUIRED_FIELD, INVALID_FORMAT -> HttpStatus.BAD_REQUEST;
            case UNAUTHORIZED, INVALID_CREDENTIALS, TOKEN_EXPIRED -> HttpStatus.UNAUTHORIZED;
            case FORBIDDEN -> HttpStatus.FORBIDDEN;
            case SERVICE_UNAVAILABLE -> HttpStatus.SERVICE_UNAVAILABLE;
            default -> HttpStatus.INTERNAL_SERVER_ERROR;
        }};
    }}
}}
'''


# ─── File Generation ─────────────────────────────────────────────────────────

def write_file(path: str, content: str) -> None:
    """Write content to a file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def scaffold(project_name: str, base_package: str, output_dir: str) -> None:
    """Generate the complete multi-module project."""
    pascal_name = kebab_to_pascal(project_name)
    pkg_path = package_to_path(base_package)
    project_dir = os.path.join(output_dir, project_name)

    if os.path.exists(project_dir):
        print(f"{Color.RED}Error: Directory '{project_dir}' already exists.{Color.RESET}")
        sys.exit(1)

    # Derive group from base package (everything before the last segment)
    parts = base_package.rsplit(".", 1)
    group = parts[0] if len(parts) > 1 else base_package

    files_created = 0
    dirs_created = set()

    def create(rel_path: str, content: str) -> None:
        nonlocal files_created
        full_path = os.path.join(project_dir, rel_path)
        write_file(full_path, content)
        files_created += 1
        dirs_created.add(os.path.dirname(full_path))

    # ── Root files ────────────────────────────────────────────────────────
    create("build.gradle.kts", root_build_gradle(group))
    create("settings.gradle.kts", settings_gradle(project_name))
    create("gradle.properties", gradle_properties())
    create("gradle/libs.versions.toml", libs_versions_toml())
    create(".gitignore", gitignore())

    # ── Server module ─────────────────────────────────────────────────────
    create("server/build.gradle.kts",
           server_build_gradle(base_package, pascal_name))
    create(f"server/src/main/java/{pkg_path}/server/{pascal_name}Application.java",
           application_java(base_package, pascal_name))
    create(f"server/src/main/java/{pkg_path}/server/exception/ServerException.java",
           server_exception_java(base_package, pascal_name))
    create("server/src/main/resources/application.yml",
           application_yml(project_name))
    create(f"server/src/test/java/{pkg_path}/server/{pascal_name}ApplicationTests.java",
           application_tests_java(base_package, pascal_name))

    # ── API Gateway module ────────────────────────────────────────────────
    create("api-gateway/build.gradle.kts", gateway_build_gradle())
    create(f"api-gateway/src/main/java/{pkg_path}/gateway/exception/ApiGatewayException.java",
           gateway_exception_java(base_package, pascal_name))
    # Create empty test directory marker
    create(f"api-gateway/src/test/java/{pkg_path}/gateway/.gitkeep", "")

    # ── Common module ─────────────────────────────────────────────────────
    create("common/build.gradle.kts", common_build_gradle())

    # ── Common:Exception module ───────────────────────────────────────────
    create("common/exception/build.gradle.kts", exception_build_gradle())

    # Exception classes
    exc_base = f"common/exception/src/main/java/{pkg_path}/common/exception"
    create(f"{exc_base}/{pascal_name}Exception.java",
           base_exception_java(base_package, pascal_name))
    create(f"{exc_base}/ResourceNotFoundException.java",
           resource_not_found_exception_java(base_package, pascal_name))
    create(f"{exc_base}/ValidationException.java",
           validation_exception_java(base_package, pascal_name))
    create(f"{exc_base}/BadRequestException.java",
           bad_request_exception_java(base_package, pascal_name))
    create(f"{exc_base}/ServiceException.java",
           service_exception_java(base_package, pascal_name))

    # Config
    create(f"{exc_base}/config/ExceptionHandlingConfig.java",
           exception_handling_config_java(base_package))

    # Handler
    create(f"{exc_base}/handler/GlobalExceptionHandler.java",
           global_exception_handler_java(base_package, pascal_name))

    # Models
    create(f"{exc_base}/model/ErrorCategory.java",
           error_category_java(base_package))
    create(f"{exc_base}/model/ErrorCode.java",
           error_code_java(base_package))
    create(f"{exc_base}/model/ErrorResponse.java",
           error_response_java(base_package))

    # Empty test directory marker
    create(f"common/exception/src/test/java/{pkg_path}/common/exception/.gitkeep", "")

    # ── Print Summary ─────────────────────────────────────────────────────
    print()
    print(f"{Color.BOLD}{Color.GREEN}Project '{project_name}' created successfully!{Color.RESET}")
    print()
    print(f"{Color.CYAN}Location:{Color.RESET} {project_dir}")
    print(f"{Color.CYAN}Package:{Color.RESET}  {base_package}")
    print(f"{Color.CYAN}Modules:{Color.RESET}  server, api-gateway, common:exception")
    print(f"{Color.CYAN}Files:{Color.RESET}    {files_created} files in {len(dirs_created)} directories")
    print()
    print(f"{Color.BOLD}Generated structure:{Color.RESET}")
    print(f"  {project_name}/")
    print(f"  {Color.BLUE}├── build.gradle.kts{Color.RESET}")
    print(f"  {Color.BLUE}├── settings.gradle.kts{Color.RESET}")
    print(f"  {Color.BLUE}├── gradle.properties{Color.RESET}")
    print(f"  {Color.BLUE}├── gradle/libs.versions.toml{Color.RESET}")
    print(f"  {Color.BLUE}├── .gitignore{Color.RESET}")
    print(f"  {Color.YELLOW}├── server/{Color.RESET}")
    print(f"  │   ├── build.gradle.kts")
    print(f"  │   └── src/main/java/.../{pascal_name}Application.java")
    print(f"  {Color.YELLOW}├── api-gateway/{Color.RESET}")
    print(f"  │   ├── build.gradle.kts")
    print(f"  │   └── src/main/java/.../ApiGatewayException.java")
    print(f"  {Color.YELLOW}└── common/exception/{Color.RESET}")
    print(f"      ├── build.gradle.kts")
    print(f"      └── src/main/java/.../")
    print(f"          ├── {pascal_name}Exception.java")
    print(f"          ├── ResourceNotFoundException.java")
    print(f"          ├── ValidationException.java")
    print(f"          ├── BadRequestException.java")
    print(f"          ├── ServiceException.java")
    print(f"          ├── config/ExceptionHandlingConfig.java")
    print(f"          ├── handler/GlobalExceptionHandler.java")
    print(f"          └── model/ErrorCode.java, ErrorCategory.java, ErrorResponse.java")
    print()
    print(f"{Color.BOLD}Exception hierarchy:{Color.RESET}")
    print(f"  RuntimeException")
    print(f"  └── {pascal_name}Exception")
    print(f"      ├── ResourceNotFoundException")
    print(f"      ├── ValidationException")
    print(f"      ├── BadRequestException")
    print(f"      ├── ServiceException")
    print(f"      ├── ServerException (server module)")
    print(f"      └── ApiGatewayException (api-gateway module)")
    print()


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a multi-module Spring Boot 4 Gradle project"
    )
    parser.add_argument(
        "--name", required=True,
        help="Project name in kebab-case (e.g., my-app)"
    )
    parser.add_argument(
        "--package", required=True,
        help="Base Java package (e.g., com.example.myapp)"
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Parent directory where the project will be created"
    )
    args = parser.parse_args()

    # Validate inputs
    if not validate_project_name(args.name):
        print(f"{Color.RED}Error: Invalid project name '{args.name}'. "
              f"Must be kebab-case (e.g., my-app).{Color.RESET}")
        sys.exit(1)

    if not validate_package(args.package):
        print(f"{Color.RED}Error: Invalid package '{args.package}'. "
              f"Must be a valid Java package (e.g., com.example.myapp).{Color.RESET}")
        sys.exit(1)

    if not os.path.isdir(args.output_dir):
        print(f"{Color.RED}Error: Output directory '{args.output_dir}' does not exist.{Color.RESET}")
        sys.exit(1)

    scaffold(args.name, args.package, args.output_dir)


if __name__ == "__main__":
    main()
