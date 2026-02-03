#!/bin/bash

# Spring Boot 4.x Migration Verification Script
# This script performs comprehensive checks after migration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0
BRIDGE_COUNT=0

# Output functions
pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASS_COUNT++))
}

fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAIL_COUNT++))
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARN_COUNT++))
}

bridge() {
    echo -e "${BLUE}[BRIDGE]${NC} $1"
    ((BRIDGE_COUNT++))
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

header() {
    echo ""
    echo "=============================================="
    echo "$1"
    echo "=============================================="
}

# Detect build tool
detect_build_tool() {
    if [ -f "pom.xml" ]; then
        BUILD_TOOL="maven"
        BUILD_CMD="./mvnw"
        [ ! -f "./mvnw" ] && BUILD_CMD="mvn"
    elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
        BUILD_TOOL="gradle"
        BUILD_CMD="./gradlew"
        [ ! -f "./gradlew" ] && BUILD_CMD="gradle"
    else
        fail "No pom.xml or build.gradle found"
        exit 1
    fi
    info "Detected build tool: $BUILD_TOOL"
}

# Check Java version
check_java_version() {
    header "Checking Java Version"

    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)

    if [ "$JAVA_VERSION" -ge 17 ]; then
        pass "Java version $JAVA_VERSION meets minimum requirement (17+)"
    else
        fail "Java version $JAVA_VERSION does not meet minimum requirement (17+)"
    fi

    if [ "$JAVA_VERSION" -ge 21 ]; then
        pass "Java version $JAVA_VERSION meets recommended version (21+)"
    else
        warn "Java version $JAVA_VERSION - consider upgrading to 21+"
    fi
}

# Check Spring Boot version
check_boot_version() {
    header "Checking Spring Boot Version"

    if [ "$BUILD_TOOL" = "maven" ]; then
        VERSION=$(grep -A2 'spring-boot-starter-parent' pom.xml | grep '<version>' | sed 's/.*>\([^<]*\)<.*/\1/' | head -1)
    else
        VERSION=$(grep "org.springframework.boot" build.gradle* | grep -oP "version '\K[^']+" | head -1)
        [ -z "$VERSION" ] && VERSION=$(grep "org.springframework.boot" build.gradle* | grep -oP 'version "\K[^"]+' | head -1)
    fi

    if [[ "$VERSION" == 4.* ]]; then
        pass "Spring Boot version $VERSION is 4.x"
    elif [[ "$VERSION" == 3.5.* ]]; then
        warn "Spring Boot version $VERSION - ready for upgrade to 4.x"
    else
        fail "Spring Boot version $VERSION - upgrade to 3.5.x first, then to 4.x"
    fi
}

# Check for deprecated starters
check_deprecated_starters() {
    header "Checking for Deprecated Starters"

    DEPRECATED_STARTERS=(
        "spring-boot-starter-web[^m]"  # but not webmvc
        "spring-boot-starter-web-services"
        "spring-boot-starter-oauth2-client[^-]"
        "spring-boot-starter-oauth2-resource-server[^-]"
        "spring-boot-starter-aop"
        "spring-boot-starter-undertow"
    )

    for starter in "${DEPRECATED_STARTERS[@]}"; do
        if grep -rq "$starter" pom.xml build.gradle* 2>/dev/null; then
            warn "Found deprecated starter pattern: $starter - consider updating"
        fi
    done

    # Check for classic starters (bridges)
    if grep -rq "spring-boot-starter-classic" pom.xml build.gradle* 2>/dev/null; then
        bridge "Using spring-boot-starter-classic (migration bridge)"
    fi

    if grep -rq "spring-boot-starter-test-classic" pom.xml build.gradle* 2>/dev/null; then
        bridge "Using spring-boot-starter-test-classic (migration bridge)"
    fi

    if grep -rq "spring-boot-jackson2" pom.xml build.gradle* 2>/dev/null; then
        bridge "Using spring-boot-jackson2 (Jackson 2 compatibility bridge)"
    fi
}

# Check for old imports
check_old_imports() {
    header "Checking for Old Imports"

    # Jackson 2 imports
    if grep -rq "com.fasterxml.jackson.databind" --include="*.java" src/ 2>/dev/null; then
        warn "Found Jackson 2 databind imports - migrate to tools.jackson.databind"
    else
        pass "No Jackson 2 databind imports found"
    fi

    # Old Spring annotations
    if grep -rq "org.springframework.lang.Nullable" --include="*.java" src/ 2>/dev/null; then
        warn "Found org.springframework.lang.Nullable - migrate to org.jspecify.annotations.Nullable"
    fi

    # Old MockBean imports
    if grep -rq "org.springframework.boot.test.mock.mockito.MockBean" --include="*.java" src/ 2>/dev/null; then
        warn "Found old @MockBean import - migrate to @MockitoBean"
    else
        pass "No old @MockBean imports found"
    fi

    # Old EntityScan
    if grep -rq "org.springframework.boot.autoconfigure.domain.EntityScan" --include="*.java" src/ 2>/dev/null; then
        warn "Found old @EntityScan import - migrate to org.springframework.boot.persistence.autoconfigure.EntityScan"
    fi

    # javax packages
    if grep -rq "import javax\." --include="*.java" src/ 2>/dev/null | grep -v "javax.crypto\|javax.net\|javax.xml" | head -1; then
        warn "Found javax.* imports - ensure migration to jakarta.*"
    fi
}

# Check for deprecated properties
check_deprecated_properties() {
    header "Checking for Deprecated Properties"

    DEPRECATED_PROPS=(
        "spring.dao.exceptiontranslation"
        "spring.session.redis\\."
        "spring.session.mongodb\\."
        "management.tracing.enabled[^.]"
        "management.health.mongo.enabled"
        "management.metrics.mongo\\."
        "spring.kafka.retry.topic.backoff.random"
    )

    for prop in "${DEPRECATED_PROPS[@]}"; do
        if grep -rq "$prop" src/main/resources/ 2>/dev/null; then
            warn "Found deprecated property: $prop"
        fi
    done

    pass "Property check complete"
}

# Check for removed features
check_removed_features() {
    header "Checking for Removed Features"

    # Undertow
    if grep -rq "undertow" pom.xml build.gradle* 2>/dev/null; then
        fail "Undertow dependency found - NOT SUPPORTED in Boot 4. Use Tomcat or Jetty."
    else
        pass "No Undertow dependency (removed in Boot 4)"
    fi

    # JUnit 4
    if grep -rq "junit:junit" pom.xml build.gradle* 2>/dev/null; then
        fail "JUnit 4 dependency found - NOT SUPPORTED. Migrate to JUnit 5/6."
    elif grep -rq "import org.junit.Test" --include="*.java" src/ 2>/dev/null; then
        fail "JUnit 4 imports found - migrate to JUnit Jupiter"
    else
        pass "No JUnit 4 detected"
    fi

    # Spock
    if grep -rq "spockframework" pom.xml build.gradle* 2>/dev/null; then
        warn "Spock Framework found - verify Groovy 5 compatibility"
    fi
}

# Compile check
check_compilation() {
    header "Checking Compilation"

    info "Running compilation..."

    if [ "$BUILD_TOOL" = "maven" ]; then
        if $BUILD_CMD clean compile -q 2>/dev/null; then
            pass "Compilation successful"
        else
            fail "Compilation failed - check errors above"
        fi
    else
        if $BUILD_CMD clean compileJava -q 2>/dev/null; then
            pass "Compilation successful"
        else
            fail "Compilation failed - check errors above"
        fi
    fi
}

# Test check
check_tests() {
    header "Checking Tests"

    info "Running tests..."

    if [ "$BUILD_TOOL" = "maven" ]; then
        if $BUILD_CMD test -q 2>/dev/null; then
            pass "All tests passed"
        else
            fail "Some tests failed - check errors above"
        fi
    else
        if $BUILD_CMD test -q 2>/dev/null; then
            pass "All tests passed"
        else
            fail "Some tests failed - check errors above"
        fi
    fi
}

# Application startup check
check_startup() {
    header "Checking Application Startup"

    info "This check requires manual verification:"
    echo "  1. Run: $BUILD_CMD spring-boot:run (Maven) or $BUILD_CMD bootRun (Gradle)"
    echo "  2. Verify application starts without errors"
    echo "  3. Check actuator health: curl http://localhost:8080/actuator/health"
    echo "  4. Stop the application"
    warn "Manual startup verification required"
}

# Summary
print_summary() {
    header "Migration Verification Summary"

    echo ""
    echo -e "  ${GREEN}PASS:${NC}   $PASS_COUNT"
    echo -e "  ${RED}FAIL:${NC}   $FAIL_COUNT"
    echo -e "  ${YELLOW}WARN:${NC}   $WARN_COUNT"
    echo -e "  ${BLUE}BRIDGE:${NC} $BRIDGE_COUNT"
    echo ""

    if [ $FAIL_COUNT -eq 0 ]; then
        if [ $BRIDGE_COUNT -eq 0 ]; then
            echo -e "${GREEN}Migration verification complete - Ready for production!${NC}"
        else
            echo -e "${YELLOW}Migration in progress - $BRIDGE_COUNT compatibility bridge(s) in use${NC}"
            echo "Plan to remove bridges before final release."
        fi
    else
        echo -e "${RED}Migration incomplete - $FAIL_COUNT issue(s) must be resolved${NC}"
    fi

    if [ $WARN_COUNT -gt 0 ]; then
        echo -e "${YELLOW}$WARN_COUNT warning(s) should be reviewed${NC}"
    fi
}

# Main execution
main() {
    echo "Spring Boot 4.x Migration Verification"
    echo "========================================"

    detect_build_tool
    check_java_version
    check_boot_version
    check_deprecated_starters
    check_old_imports
    check_deprecated_properties
    check_removed_features

    # Optional: uncomment to run compilation and tests
    # check_compilation
    # check_tests

    check_startup
    print_summary

    # Exit with error if any failures
    [ $FAIL_COUNT -gt 0 ] && exit 1
    exit 0
}

main "$@"
