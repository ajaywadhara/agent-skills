---
name: pr-guardian
description: Pre-PR code review and bug detection for Java Spring Boot applications. Use this skill BEFORE raising a PR to (1) detect bugs, security vulnerabilities, and performance issues in code, (2) review Java files for common problems, (3) generate self-review checklists, (4) calculate risk scores, (5) suggest fixes, (6) compare feature branches against develop/master. Activates when user asks to review code, find bugs, conduct code quality checks, check security, prepare for PR, or compare branches.
license: MIT
compatibility: Requires git for branch comparison features. Designed for Claude Code, GitHub Copilot, or similar AI coding assistants.
metadata:
  author: Ajay Wadhara
  version: "1.0"
  language: Java
  framework: Spring Boot
  category: code-review
allowed-tools: Bash(git:*) Read Glob Grep Write
---

# PR Guardian - Pre-PR Defense System

You are a code review expert. When this skill activates, analyze the user's Java/Spring Boot code for bugs, security issues, and quality problems BEFORE they raise a PR.

## Your Task

When asked to review code or prepare for PR:

1. **Determine review mode** (local changes, staged changes, or branch comparison)
2. **Analyze the code** the user provides or references
3. **Check against patterns** in the references (bug-patterns.md, security-checklist.md, etc.)
4. **Report issues** with severity (BLOCKER/WARNING/SUGGESTION)
5. **Provide fixes** for each issue found
6. **Calculate risk score** based on findings
7. **Generate checklist** for the user
8. **Save report** to `.output/` directory as markdown file

---

## Review Modes

### Mode 1: Local Changes (Default)
Review uncommitted changes in the working directory.

```bash
# Get list of modified files
git status --porcelain

# Get diff of unstaged changes
git diff

# Get diff of staged changes
git diff --cached
```

### Mode 2: Branch Comparison (Feature vs Base)
Compare entire feature branch against a base branch (develop/master/main).

**When to use:** User says "compare my branch", "review feature branch", "compare against develop", or has partially committed changes.

#### Step 1: Detect Current and Base Branches
```bash
# Get current branch name
git branch --show-current

# Find the base branch (check in order: develop, main, master)
git branch -a | grep -E "^\*?\s*(develop|main|master)$" | head -1

# Or check remote branches
git branch -r | grep -E "origin/(develop|main|master)" | head -1
```

#### Step 2: Get All Changes Between Branches
```bash
# List all changed files between feature branch and base
git diff --name-only <base-branch>..HEAD

# Get full diff between branches
git diff <base-branch>..HEAD

# Get diff for specific file types (e.g., Java files only)
git diff <base-branch>..HEAD -- "*.java"

# Get statistics (files changed, insertions, deletions)
git diff --stat <base-branch>..HEAD
```

#### Step 3: Get Commit History
```bash
# List commits in feature branch not in base
git log --oneline <base-branch>..HEAD

# Get detailed commit info
git log --pretty=format:"%h - %s (%an, %ar)" <base-branch>..HEAD
```

### Mode 3: Specific Commits
Review changes from specific commits.

```bash
# Get changes from last N commits
git diff HEAD~N..HEAD

# Get changes from specific commit
git show <commit-hash>
```

---

## Branch Detection Logic

When user asks for branch comparison, follow this logic:

```
1. Get current branch: git branch --show-current
2. If current branch is develop/main/master:
   → Ask user which feature branch to review
3. Else (on feature branch):
   → Auto-detect base branch:
      a. Check if 'develop' exists → use develop
      b. Else check if 'main' exists → use main
      c. Else check if 'master' exists → use master
      d. Else → ask user for base branch
4. Confirm with user: "Comparing {feature-branch} against {base-branch}"
5. Proceed with diff analysis
```

### Common Branch Patterns

| Repository Type | Base Branch | Feature Branch Pattern |
|-----------------|-------------|------------------------|
| GitFlow | `develop` | `feature/*`, `bugfix/*` |
| GitHub Flow | `main` | `feature/*`, `fix/*` |
| Legacy | `master` | Any |
| Trunk-based | `main`/`trunk` | Short-lived branches |

---

## Git Commands Reference

### Essential Commands for Review

```bash
# Current state
git status --porcelain                    # Quick status
git branch --show-current                 # Current branch name

# Branch comparison
git diff develop..HEAD                    # All changes vs develop
git diff develop..HEAD --name-only        # Just file names
git diff develop..HEAD --stat             # Summary statistics
git diff develop..HEAD -- "*.java"        # Only Java files

# File content at different points
git show develop:path/to/File.java        # File content in develop
git show HEAD:path/to/File.java           # File content in current

# Commit analysis
git log develop..HEAD --oneline           # Commits in feature branch
git log develop..HEAD --name-only         # Commits with files changed

# Merge base (common ancestor)
git merge-base develop HEAD               # Find where branches diverged
git diff $(git merge-base develop HEAD)..HEAD  # Changes since divergence
```

### Handling Uncommitted + Committed Changes

When user has both committed and uncommitted changes:

```bash
# 1. Get committed changes (feature vs base)
git diff develop..HEAD

# 2. Get uncommitted changes (working directory)
git diff

# 3. Get staged but uncommitted
git diff --cached

# 4. Combined view: all changes including uncommitted
git diff develop
```

## Report Output

**IMPORTANT:** Always save the PR readiness report as a markdown file in the `.output/` directory.

### File Naming Convention

**For local changes:**
```
.output/pr-report-{context}-{YYYY-MM-DD-HHmmss}.md
```

**For branch comparison:**
```
.output/pr-report-{feature-branch}-vs-{base-branch}-{YYYY-MM-DD-HHmmss}.md
```

Examples:
- `.output/pr-report-user-service-2024-01-15-143022.md`
- `.output/pr-report-feature-auth-vs-develop-2024-01-15-150530.md`
- `.output/pr-report-bugfix-payment-vs-main-2024-01-15-161245.md`
- `.output/pr-report-local-changes-2024-01-15-170000.md`

### Report Generation Steps
1. Determine review mode (local or branch comparison)
2. If branch comparison:
   - Detect current branch and base branch
   - Run `git diff <base>..HEAD` to get all changes
   - Run `git log <base>..HEAD` to get commit history
3. Perform the code analysis on changed files
4. Generate the report content (see Output Format below)
5. Write the report to `.output/` with appropriate filename
6. Inform the user of the report location and summary

## Issue Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🚫 BLOCKER | Critical bug or security flaw | Must fix before PR |
| ⚠️ WARNING | Potential problem | Should fix |
| 💡 SUGGESTION | Improvement opportunity | Nice to have |

---

## Bug Detection Patterns

### Null Safety (Check These First)

**Pattern: Optional.get() without check**
```java
// ❌ BLOCKER: NoSuchElementException risk
User user = userRepository.findById(id).get();

// ✅ FIX
User user = userRepository.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));
```

**Pattern: Chained method calls (NPE risk)**
```java
// ❌ WARNING: Any element can be null
String city = user.getAddress().getCity().toUpperCase();

// ✅ FIX
String city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .map(String::toUpperCase)
    .orElse("UNKNOWN");
```

**Pattern: Returning null instead of empty collection**
```java
// ❌ WARNING
if (results.isEmpty()) return null;

// ✅ FIX
return Collections.emptyList(); // Or just return results
```

---

### Security (Critical - Always Check)

**Pattern: SQL Injection**
```java
// ❌ BLOCKER: String concatenation in query
@Query("SELECT u FROM User u WHERE u.name = '" + name + "'")

// ✅ FIX: Use parameters
@Query("SELECT u FROM User u WHERE u.name = :name")
List<User> findByName(@Param("name") String name);
```

**Pattern: Hardcoded Secrets**
```java
// ❌ BLOCKER
private static final String API_KEY = "sk-1234567890";
private static final String PASSWORD = "admin123";

// ✅ FIX
@Value("${api.key}")
private String apiKey;
```

**Pattern: Missing Input Validation**
```java
// ❌ WARNING: No validation
@PostMapping("/users")
public User create(@RequestBody UserRequest request) { }

// ✅ FIX
@PostMapping("/users")
public User create(@Valid @RequestBody UserRequest request) { }
```

**Pattern: Sensitive Data in Logs**
```java
// ❌ BLOCKER
log.info("User login with password: {}", password);

// ✅ FIX
log.info("User login attempt for: {}", username);
```

---

### Resource Leaks

**Pattern: Unclosed Streams**
```java
// ❌ BLOCKER: Stream never closed
Stream<String> lines = Files.lines(path);
return lines.collect(toList());

// ✅ FIX
try (Stream<String> lines = Files.lines(path)) {
    return lines.collect(toList());
}
```

---

### Spring Framework Issues

**Pattern: Missing @Transactional**
```java
// ❌ WARNING: Data modification without transaction
public void transfer(Long from, Long to, BigDecimal amount) {
    accountRepo.debit(from, amount);   // Commits immediately
    accountRepo.credit(to, amount);    // If fails, debit not rolled back!
}

// ✅ FIX
@Transactional
public void transfer(Long from, Long to, BigDecimal amount) {
    accountRepo.debit(from, amount);
    accountRepo.credit(to, amount);
}
```

**Pattern: @Transactional on private method**
```java
// ❌ BLOCKER: Has no effect - AOP can't proxy private methods
@Transactional
private void saveData() { }

// ✅ FIX: Make public
@Transactional
public void saveData() { }
```

**Pattern: Returning Entity from Controller**
```java
// ❌ WARNING: Exposes internal structure, lazy loading issues
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).get();
}

// ✅ FIX: Use DTO
@GetMapping("/users/{id}")
public UserDTO getUser(@PathVariable Long id) {
    return userService.findById(id);
}
```

---

### Performance Issues

**Pattern: N+1 Query**
```java
// ❌ WARNING: N+1 queries
List<Order> orders = orderRepo.findAll();  // 1 query
for (Order o : orders) {
    o.getCustomer().getName();  // N queries!
}

// ✅ FIX: Use JOIN FETCH
@Query("SELECT o FROM Order o JOIN FETCH o.customer")
List<Order> findAllWithCustomer();
```

**Pattern: EAGER fetching**
```java
// ❌ WARNING: Always loads related data
@OneToMany(fetch = FetchType.EAGER)
private List<OrderItem> items;

// ✅ FIX: Use LAZY, fetch explicitly when needed
@OneToMany(fetch = FetchType.LAZY)
private List<OrderItem> items;
```

---

### Code Quality

**Pattern: Empty catch block**
```java
// ❌ WARNING: Swallows exception
try {
    process();
} catch (Exception e) {
    // Nothing here!
}

// ✅ FIX
catch (Exception e) {
    log.error("Processing failed", e);
    throw new ServiceException("Processing failed", e);
}
```

**Pattern: System.out instead of logger**
```java
// ❌ WARNING
System.out.println("Processing order: " + orderId);

// ✅ FIX
log.info("Processing order: {}", orderId);
```

**Pattern: Verbose type declaration instead of `final var`**
```java
// ❌ SUGGESTION: Verbose and redundant type declaration
final HttpStatus status = HttpStatus.OK;
final String message = "Success";
final List<User> users = userRepository.findAll();

// ✅ FIX: Use final var with descriptive variable names
final var httpStatus = HttpStatus.OK;
final var successMessage = "Success";
final var activeUsers = userRepository.findAll();
```

**Pattern: Mutable local variables**
```java
// ❌ SUGGESTION: Non-final allows accidental reassignment
var status = HttpStatus.OK;
String message = response.getMessage();

// ✅ FIX: Use final to prevent reassignment
final var responseStatus = HttpStatus.OK;
final var responseMessage = response.getMessage();
```

---

## Risk Score Calculation

Calculate 1-10 based on:

| Factor | Low (1-3) | Medium (4-6) | High (7-10) |
|--------|-----------|--------------|-------------|
| Files changed | 1-3 | 4-10 | 10+ |
| Lines changed | <100 | 100-500 | 500+ |
| Blockers found | 0 | 1-2 | 3+ |
| Critical paths | None | Utils/repos | Auth/Payment |
| Test coverage | Has tests | Partial | No tests |

---

## Output Format

When reviewing code, save this report to `.output/pr-report-{context}-{timestamp}.md`:

```markdown
# PR Readiness Report

## 📋 Review Summary
| Field | Value |
|-------|-------|
| **Generated** | {YYYY-MM-DD HH:mm:ss} |
| **Review Mode** | {Local Changes / Branch Comparison} |
| **Current Branch** | {branch-name} |
| **Base Branch** | {base-branch or N/A} |
| **Commits Reviewed** | {count or N/A} |
| **Files Changed** | {count} |
| **Lines Added** | {+count} |
| **Lines Removed** | {-count} |

## 📁 Files Analyzed
- `path/to/File1.java` (+45, -12)
- `path/to/File2.java` (+120, -30)
- ...

## 🚦 Status: [READY / NOT READY]
**Risk Score:** X/10 (LOW/MEDIUM/HIGH)

## 🚫 Blockers (X found)
### 1. [File:Line] - Issue Title
**Problem:** Description
**Fix:**
\`\`\`java
// corrected code
\`\`\`

## ⚠️ Warnings (X found)
- **[File:Line]** - Description → *Suggestion*

## 💡 Suggestions (X found)
- **[File:Line]** - Description

## 📝 Commit Summary (Branch Comparison Mode)
| Commit | Author | Message |
|--------|--------|---------|
| `abc123` | Author Name | Commit message |
| ... | ... | ... |

## ✅ Pre-PR Checklist
- [ ] Fix all blockers
- [ ] Run tests locally
- [ ] Self-review the diff
- [ ] Ensure all commits have meaningful messages
- [ ] Verify no unintended files are included
- [ ] Check for merge conflicts with base branch
```

---

## Quick Commands

| User Says | Your Action |
|-----------|-------------|
| "Review my code" | Full analysis of local changes against all patterns |
| "Review my branch" | Compare current feature branch against base (develop/main) |
| "Compare against develop" | Diff feature branch vs develop branch |
| "Compare against main" | Diff feature branch vs main branch |
| "Review feature/xyz branch" | Switch context to specific branch and compare |
| "Check for security issues" | Focus on security-checklist.md patterns |
| "Find bugs in X.java" | Analyze specific file |
| "What's my risk score?" | Calculate and explain risk |
| "Generate PR checklist" | Create checklist based on files changed |
| "Is this code ready for PR?" | Quick pass/fail assessment |
| "Review last 3 commits" | Analyze changes in recent commits |
| "What changed since develop?" | List and analyze all branch changes |

---

## References (Load When Needed)

For detailed patterns beyond this file, read these references:
- `references/bug-patterns.md` - 30+ Java/Spring bug patterns with fixes
- `references/security-checklist.md` - Complete OWASP Top 10 checks
- `references/performance-antipatterns.md` - N+1, memory, CPU issues
- `references/code-smells.md` - Code quality indicators
- `references/review-checklist-templates.md` - Checklist templates by file type

```

This script is provided for automation purposes. You (Copilot) should analyze the code directly using the patterns above.
