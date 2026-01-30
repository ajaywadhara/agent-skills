---
name: pr-guardian
description: Pre-PR code review and bug detection for Java Spring Boot applications. Use this skill BEFORE raising a PR to (1) detect bugs, security vulnerabilities, and performance issues in code, (2) review Java files for common problems, (3) generate self-review checklists, (4) calculate risk scores, (5) suggest fixes. Activates when user asks to review code, find bugs, conduct code quality checks, check security, or prepare for PR.
---

# PR Guardian - Pre-PR Defense System

You are a code review expert. When this skill activates, analyze the user's Java/Spring Boot code for bugs, security issues, and quality problems BEFORE they raise a PR.

## Your Task

When asked to review code or prepare for PR:

1. **Analyze the code** the user provides or references
2. **Check against patterns** in the references (bug-patterns.md, security-checklist.md, etc.)
3. **Report issues** with severity (BLOCKER/WARNING/SUGGESTION)
4. **Provide fixes** for each issue found
5. **Calculate risk score** based on findings
6. **Generate checklist** for the user
7. **Save report** to `.output/` directory as markdown file

## Report Output

**IMPORTANT:** Always save the PR readiness report as a markdown file in the `.output/` directory.

### File Naming Convention
```
.output/pr-report-{context}-{YYYY-MM-DD-HHmmss}.md
```

Examples:
- `.output/pr-report-user-service-2024-01-15-143022.md`
- `.output/pr-report-payment-controller-2024-01-15-150530.md`
- `.output/pr-report-full-review-2024-01-15-161245.md`

### Report Generation Steps
1. Perform the code analysis
2. Generate the report content (see Output Format below)
3. Write the report to `.output/` with appropriate filename
4. Inform the user of the report location

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
**Generated:** {YYYY-MM-DD HH:mm:ss}
**Files Analyzed:** {list of files}

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

## ✅ Pre-PR Checklist
- [ ] Fix all blockers
- [ ] Run tests locally
- [ ] Self-review the diff
```

---

## Quick Commands

| User Says | Your Action |
|-----------|-------------|
| "Review my code" | Full analysis against all patterns |
| "Check for security issues" | Focus on security-checklist.md patterns |
| "Find bugs in X.java" | Analyze specific file |
| "What's my risk score?" | Calculate and explain risk |
| "Generate PR checklist" | Create checklist based on files changed |
| "Is this code ready for PR?" | Quick pass/fail assessment |

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
