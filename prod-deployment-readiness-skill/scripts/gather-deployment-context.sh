#!/bin/bash

# Production Deployment Readiness - Context Gathering Script
# Gathers git context quickly for deployment readiness analysis
#
# Usage: ./gather-deployment-context.sh <base-ref> <target-ref>
# Example: ./gather-deployment-context.sh main HEAD
#          ./gather-deployment-context.sh v1.2.0 v1.3.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Counters
CONFIG_COUNT=0
MIGRATION_COUNT=0
API_COUNT=0
INFRA_COUNT=0
TEST_COUNT=0
DEPS_COUNT=0
SECURITY_COUNT=0
OTHER_COUNT=0
WARN_COUNT=0
PASS_COUNT=0

# Output functions
header() {
    echo ""
    echo -e "${BOLD}=============================================="
    echo "$1"
    echo -e "==============================================${NC}"
}

subheader() {
    echo -e "\n${CYAN}--- $1 ---${NC}"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    WARN_COUNT=$((WARN_COUNT + 1))
}

fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Validate arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage: $0 <base-ref> <target-ref>${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 main HEAD              # Compare current branch against main"
    echo "  $0 develop HEAD            # Compare current branch against develop"
    echo "  $0 v1.2.0 v1.3.0          # Compare two tags"
    echo "  $0 HEAD~5 HEAD             # Last 5 commits"
    exit 1
fi

BASE_REF="$1"
TARGET_REF="$2"

# Validate refs exist
if ! git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
    fail "Base ref '$BASE_REF' does not exist"
    exit 1
fi

if ! git rev-parse --verify "$TARGET_REF" >/dev/null 2>&1; then
    fail "Target ref '$TARGET_REF' does not exist"
    exit 1
fi

# ============================================
# Project Type Detection
# ============================================
header "Project Type Detection"

STACK="unknown"
if [ -f "pom.xml" ] || [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    STACK="java"
    pass "Detected: Java/Spring Boot"
    if [ -f "pom.xml" ]; then
        info "Build tool: Maven"
    else
        info "Build tool: Gradle"
    fi
fi

if [ -f "package.json" ]; then
    if [ "$STACK" != "unknown" ]; then
        warn "Multiple stacks detected (also Node.js)"
    else
        STACK="nodejs"
        pass "Detected: Node.js"
    fi
    if [ -f "yarn.lock" ]; then
        info "Package manager: Yarn"
    elif [ -f "pnpm-lock.yaml" ]; then
        info "Package manager: pnpm"
    else
        info "Package manager: npm"
    fi
fi

if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "Pipfile" ]; then
    if [ "$STACK" != "unknown" ] && [ "$STACK" != "java" ] && [ "$STACK" != "nodejs" ]; then
        warn "Multiple stacks detected (also Python)"
    elif [ "$STACK" = "unknown" ]; then
        STACK="python"
        pass "Detected: Python"
    fi
    if [ -f "pyproject.toml" ]; then
        info "Project config: pyproject.toml"
    elif [ -f "Pipfile" ]; then
        info "Package manager: pipenv"
    fi
fi

if [ "$STACK" = "unknown" ]; then
    warn "Could not auto-detect project type"
fi

# ============================================
# Diff Statistics
# ============================================
header "Diff Statistics: $BASE_REF..$TARGET_REF"

DIFF_STAT=$(git diff --stat "$BASE_REF".."$TARGET_REF" 2>/dev/null | tail -1)
if [ -n "$DIFF_STAT" ]; then
    info "$DIFF_STAT"
else
    info "No changes detected between $BASE_REF and $TARGET_REF"
    exit 0
fi

TOTAL_FILES=$(git diff --name-only "$BASE_REF".."$TARGET_REF" 2>/dev/null | wc -l | tr -d ' ')
info "Total files changed: $TOTAL_FILES"

# ============================================
# Changed Files by Category
# ============================================
header "Changed Files by Category"

ALL_FILES=$(git diff --name-only "$BASE_REF".."$TARGET_REF" 2>/dev/null)

# Configuration files
subheader "Configuration & Environment"
while IFS= read -r file; do
    if [[ "$file" =~ \.(yml|yaml|properties|env|toml|json)$ ]] && [[ "$file" =~ (config|application|settings|\.env) ]]; then
        echo "  $file"
        CONFIG_COUNT=$((CONFIG_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$CONFIG_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    info "Config files changed: $CONFIG_COUNT"
fi

# Database migrations
subheader "Database Migrations"
while IFS= read -r file; do
    if [[ "$file" =~ (migration|migrate|flyway|liquibase|alembic|prisma/migrations|knex|db/migrate) ]]; then
        echo "  $file"
        MIGRATION_COUNT=$((MIGRATION_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$MIGRATION_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    warn "Migration files changed: $MIGRATION_COUNT"
fi

# API files (controllers, routes, endpoints)
subheader "API / Endpoint Files"
while IFS= read -r file; do
    if [[ "$file" =~ (Controller|controller|Route|route|router|endpoint|api/|views\.py|urls\.py) ]]; then
        echo "  $file"
        API_COUNT=$((API_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$API_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    info "API files changed: $API_COUNT"
fi

# Infrastructure files
subheader "Infrastructure"
while IFS= read -r file; do
    if [[ "$file" =~ (Dockerfile|docker-compose|\.tf$|\.tfvars$|k8s/|kubernetes/|helm/|\.github/workflows|Jenkinsfile|\.gitlab-ci|cloudbuild) ]]; then
        echo "  $file"
        INFRA_COUNT=$((INFRA_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$INFRA_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    warn "Infrastructure files changed: $INFRA_COUNT"
fi

# Dependency files
subheader "Dependencies"
while IFS= read -r file; do
    if [[ "$file" =~ (pom\.xml|build\.gradle|package\.json|package-lock|yarn\.lock|pnpm-lock|requirements\.txt|pyproject\.toml|Pipfile|poetry\.lock|libs\.versions\.toml) ]]; then
        echo "  $file"
        DEPS_COUNT=$((DEPS_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$DEPS_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    info "Dependency files changed: $DEPS_COUNT"
fi

# Security-related files
subheader "Security-Related"
while IFS= read -r file; do
    if [[ "$file" =~ (Security|security|Auth|auth|Permission|permission|Cors|cors|Csp|csp) ]]; then
        echo "  $file"
        SECURITY_COUNT=$((SECURITY_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$SECURITY_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    warn "Security files changed: $SECURITY_COUNT"
fi

# Test files
subheader "Test Files"
while IFS= read -r file; do
    if [[ "$file" =~ (Test|test|Spec|spec|__tests__) ]]; then
        echo "  $file"
        TEST_COUNT=$((TEST_COUNT + 1))
    fi
done <<< "$ALL_FILES"
if [ "$TEST_COUNT" -eq 0 ]; then
    echo "  (none)"
else
    info "Test files changed: $TEST_COUNT"
fi

# ============================================
# Commit Log
# ============================================
header "Commit Log: $BASE_REF..$TARGET_REF"

COMMIT_COUNT=$(git log --oneline "$BASE_REF".."$TARGET_REF" 2>/dev/null | wc -l | tr -d ' ')
info "Total commits: $COMMIT_COUNT"
echo ""
git log --pretty=format:"  %C(yellow)%h%C(reset) %s %C(blue)(%an, %ar)%C(reset)" "$BASE_REF".."$TARGET_REF" 2>/dev/null
echo ""

# ============================================
# Quick Checks
# ============================================
header "Quick Deployment Checks"

# Check for destructive SQL patterns
subheader "Destructive SQL Operations"
DESTRUCTIVE=$(git diff "$BASE_REF".."$TARGET_REF" 2>/dev/null | grep -iE '^\+.*(DROP TABLE|DROP COLUMN|TRUNCATE|DELETE FROM.*[^W]HERE)' | head -5)
if [ -n "$DESTRUCTIVE" ]; then
    warn "Destructive SQL operations detected:"
    echo "$DESTRUCTIVE" | while IFS= read -r line; do
        echo -e "  ${RED}$line${NC}"
    done
else
    pass "No destructive SQL operations found"
fi

# Check for secret patterns
subheader "Potential Secrets"
SECRETS=$(git diff "$BASE_REF".."$TARGET_REF" 2>/dev/null | grep -iE '^\+.*(password|secret|api_key|apikey|token|private_key)\s*[:=]' | grep -v '^\+\+\+' | grep -v 'example\|placeholder\|changeme\|TODO\|FIXME' | head -5)
if [ -n "$SECRETS" ]; then
    warn "Potential secrets in diff:"
    echo "$SECRETS" | while IFS= read -r line; do
        echo -e "  ${RED}$line${NC}"
    done
else
    pass "No obvious secrets detected in diff"
fi

# Check for debug/dev flags in config
subheader "Debug/Dev Configuration"
DEBUG_FLAGS=$(git diff "$BASE_REF".."$TARGET_REF" 2>/dev/null | grep -iE '^\+.*(debug\s*[:=]\s*true|DEBUG\s*=\s*True|NODE_ENV.*development|ddl-auto.*create)' | head -5)
if [ -n "$DEBUG_FLAGS" ]; then
    warn "Debug/dev configuration detected:"
    echo "$DEBUG_FLAGS" | while IFS= read -r line; do
        echo -e "  ${YELLOW}$line${NC}"
    done
else
    pass "No debug/dev flags detected in changes"
fi

# Check for SNAPSHOT/pre-release versions
subheader "Unstable Dependencies"
SNAPSHOTS=$(git diff "$BASE_REF".."$TARGET_REF" 2>/dev/null | grep -iE '^\+.*(SNAPSHOT|alpha|beta|rc[0-9]|canary|next\.)' | grep -v '^\+\+\+' | head -5)
if [ -n "$SNAPSHOTS" ]; then
    warn "Unstable dependency versions detected:"
    echo "$SNAPSHOTS" | while IFS= read -r line; do
        echo -e "  ${YELLOW}$line${NC}"
    done
else
    pass "No unstable dependency versions detected"
fi

# ============================================
# Summary
# ============================================
header "Context Gathering Summary"

echo ""
echo -e "  ${BOLD}Comparison:${NC}       $BASE_REF..$TARGET_REF"
echo -e "  ${BOLD}Stack:${NC}            $STACK"
echo -e "  ${BOLD}Files Changed:${NC}    $TOTAL_FILES"
echo -e "  ${BOLD}Commits:${NC}          $COMMIT_COUNT"
echo ""
echo -e "  ${BOLD}Categories Affected:${NC}"
[ "$CONFIG_COUNT" -gt 0 ] && echo -e "    ${YELLOW}*${NC} Configuration: $CONFIG_COUNT files"
[ "$MIGRATION_COUNT" -gt 0 ] && echo -e "    ${RED}*${NC} Migrations: $MIGRATION_COUNT files"
[ "$API_COUNT" -gt 0 ] && echo -e "    ${YELLOW}*${NC} API/Endpoints: $API_COUNT files"
[ "$INFRA_COUNT" -gt 0 ] && echo -e "    ${RED}*${NC} Infrastructure: $INFRA_COUNT files"
[ "$DEPS_COUNT" -gt 0 ] && echo -e "    ${YELLOW}*${NC} Dependencies: $DEPS_COUNT files"
[ "$SECURITY_COUNT" -gt 0 ] && echo -e "    ${RED}*${NC} Security: $SECURITY_COUNT files"
[ "$TEST_COUNT" -gt 0 ] && echo -e "    ${GREEN}*${NC} Tests: $TEST_COUNT files"
echo ""
echo -e "  ${GREEN}PASS:${NC} $PASS_COUNT"
echo -e "  ${YELLOW}WARN:${NC} $WARN_COUNT"
echo ""

if [ "$WARN_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}$WARN_COUNT warning(s) found — run full deployment readiness analysis for details.${NC}"
else
    echo -e "${GREEN}Quick checks passed — run full deployment readiness analysis for comprehensive review.${NC}"
fi
