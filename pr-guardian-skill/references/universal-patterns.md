# Universal Bug Patterns (Language Agnostic)

## Null/Reference Safety

### Dereferencing Without Null Check
```java
// All languages: accessing property/method on potentially null value
user.getAddress().getCity()  // NPE if any element null
```
**Fix:** Use null-safe operators or defensive checks:
- Java: `Optional.ofNullable(user).map(User::getAddress)...`
- Kotlin: `user?.address?.city`
- JavaScript: `user?.address?.city`
- Python: `getattr(getattr(user, 'address', None), 'city', None)`

### Returning Null Instead of Empty Collection
```java
if (items.isEmpty()) return null;  // Forces null checks on callers
```
**Fix:** Return empty collection/list/array

---

## Resource Management

### Unclosed Resources
```java
Stream<String> lines = Files.lines(path);  // Never closed
return lines.collect(toList());
```
**Fix:** Use try-with-resources or defer to caller with explicit cleanup

### Connection Leaks
```java
Connection conn = dataSource.getConnection();
// Exception here = leaked connection
```
**Fix:** Always use try-finally or equivalent resource management

---

## Concurrency

### Race Conditions
```java
if (!map.containsKey(key)) {
    map.put(key, value);  // Another thread may have put first
}
```
**Fix:** Use atomic operations: `map.computeIfAbsent(key, k -> value)`

### Shared Mutable State
```java
private int counter = 0;
public void increment() { counter++; }  // Not thread-safe
```
**Fix:** Use atomic types or synchronization

---

## Security

### Injection Vulnerabilities

| Type | Pattern | Fix |
|------|---------|-----|
| SQL | String concat in queries | Parameterized queries |
| Command | User input in shell commands | Allowlist validation |
| LDAP | Unescaped user input | Escape special chars |
| Path Traversal | User input in file paths | Validate/sanitize |

### Hardcoded Secrets
```java
private static final String API_KEY = "sk-live-abc123";
private static final String PASSWORD = "admin123";
```
**Fix:** Externalize to environment variables or secret manager

### Sensitive Data in Logs
```java
log.info("User login: {} with password: {}", username, password);
```
**Fix:** Never log credentials, PII, or sensitive data

### Missing Input Validation
```java
public void process(UserInput input) {  // No validation
    database.query(input.getValue());
}
```
**Fix:** Validate at boundary: type, length, format, allowlist

---

## Error Handling

### Swallowing Exceptions
```java
try {
    process();
} catch (Exception e) {
    // Silent failure
}
```
**Fix:** Log and handle or rethrow

### Catching Too Broad
```java
catch (Exception e) {  // Catches everything including NPE
    return defaultValue;
}
```
**Fix:** Catch specific exceptions

---

## Logic Errors

### Off-by-One
```java
for (int i = 0; i < items.size() - 1; i++)  // Skips last element
```
**Fix:** `< items.size()` not `< items.size() - 1`

### Floating Point Comparison
```java
if (price == 19.99)  // May fail due to precision
```
**Fix:** Use epsilon comparison or decimal types

### Object Identity vs Equality
```java
if (a == b)  // Reference comparison for objects
```
**Fix:** Use `.equals()` or language equivalent

---

## Code Quality

### Magic Numbers
```java
if (status == 3)  // What does 3 mean?
```
**Fix:** Use named constants

### Dead Code
```java
if (false) { thisNeverRuns(); }
return x; x = 5;  // Unreachable
```
**Fix:** Remove unreachable code

### Long Methods/Functions
> 50-100 lines typically indicates need for refactoring

**Fix:** Extract methods, single responsibility

### Duplicate Code
> Same logic in multiple places

**Fix:** Extract to shared function/module

---

## Performance

### N+1 Queries
```java
for (Order order : orders) {
    order.getCustomer().getName();  // Query per iteration
}
```
**Fix:** Eager load or batch fetch related data

### Inefficient Collection Operations
```java
list.contains(item)  // O(n) for ArrayList
```
**Fix:** Use Set for O(1) lookups

### Premature Optimization
> Complex code for hypothetical performance gains

**Fix:** Profile first, optimize where actually needed