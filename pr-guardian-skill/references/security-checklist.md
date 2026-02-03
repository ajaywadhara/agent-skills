# Security Checklist Reference

## OWASP Top 10 Checks

### A01: Broken Access Control

#### Missing Authorization
```java
// ❌ VULNERABLE: No authorization check
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
    // Any authenticated user can access any user's data!
}

// ✅ SECURE
@GetMapping("/users/{id}")
@PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
}
```

#### Insecure Direct Object Reference (IDOR)
```java
// ❌ VULNERABLE: User-controlled ID without ownership check
@DeleteMapping("/orders/{orderId}")
public void deleteOrder(@PathVariable Long orderId) {
    orderRepository.deleteById(orderId); // Can delete any order!
}

// ✅ SECURE
@DeleteMapping("/orders/{orderId}")
public void deleteOrder(@PathVariable Long orderId, @AuthenticationPrincipal User user) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    if (!order.getUserId().equals(user.getId())) {
        throw new AccessDeniedException("Not your order");
    }
    orderRepository.delete(order);
}
```

#### Privilege Escalation
```java
// ❌ VULNERABLE: User can set their own role
@PutMapping("/users/{id}")
public User updateUser(@PathVariable Long id, @RequestBody UserUpdateRequest request) {
    User user = userRepository.findById(id).orElseThrow();
    user.setRole(request.getRole()); // Can make themselves admin!
    return userRepository.save(user);
}

// ✅ SECURE: Separate admin endpoint for role changes
@PutMapping("/users/{id}")
public User updateUser(@PathVariable Long id, @RequestBody UserUpdateRequest request) {
    User user = userRepository.findById(id).orElseThrow();
    user.setName(request.getName()); // Only safe fields
    user.setEmail(request.getEmail());
    // Role change requires admin endpoint
    return userRepository.save(user);
}
```

---

### A02: Cryptographic Failures

#### Weak Hashing
```java
// ❌ VULNERABLE: MD5/SHA1 for passwords
String hashedPassword = DigestUtils.md5Hex(password);

// ✅ SECURE: Use BCrypt
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);
}
```

#### Hardcoded Secrets
```java
// ❌ VULNERABLE: Secrets in code
private static final String API_KEY = "sk-live-abc123xyz";
private static final String JWT_SECRET = "mysecretkey";

// ✅ SECURE: Use externalized config
@Value("${api.key}")
private String apiKey;

@Value("${jwt.secret}")
private String jwtSecret;
```

#### Weak Encryption
```java
// ❌ VULNERABLE: DES is broken
Cipher cipher = Cipher.getInstance("DES");

// ✅ SECURE: Use AES-256-GCM
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
```

#### Sensitive Data in Logs
```java
// ❌ VULNERABLE: Logging sensitive data
log.info("User login: {} with password: {}", username, password);
log.debug("Credit card: {}", creditCardNumber);

// ✅ SECURE: Mask sensitive data
log.info("User login: {}", username);
log.debug("Credit card: ****{}", last4Digits);
```

---

### A03: Injection

#### SQL Injection
```java
// ❌ VULNERABLE: String concatenation
@Query("SELECT u FROM User u WHERE u.name = '" + name + "'")
List<User> findByName(String name);

// Or in native query
String sql = "SELECT * FROM users WHERE name = '" + name + "'";

// ✅ SECURE: Parameterized queries
@Query("SELECT u FROM User u WHERE u.name = :name")
List<User> findByName(@Param("name") String name);

// Or with JdbcTemplate
jdbcTemplate.query("SELECT * FROM users WHERE name = ?", 
    new Object[]{name}, userRowMapper);
```

#### LDAP Injection
```java
// ❌ VULNERABLE
String filter = "(uid=" + username + ")";

// ✅ SECURE: Escape special characters
String filter = "(uid=" + LdapEncoder.filterEncode(username) + ")";
```

#### Command Injection
```java
// ❌ VULNERABLE
Runtime.getRuntime().exec("ping " + userInput);

// ✅ SECURE: Use ProcessBuilder with separate arguments
ProcessBuilder pb = new ProcessBuilder("ping", "-c", "1", hostname);
// And validate hostname is actually a hostname
if (!hostname.matches("^[a-zA-Z0-9.-]+$")) {
    throw new IllegalArgumentException("Invalid hostname");
}
```

#### SpEL Injection
```java
// ❌ VULNERABLE: User input in SpEL
ExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression(userInput);
Object value = exp.getValue();

// ✅ SECURE: Use SimpleEvaluationContext (restricted)
SimpleEvaluationContext context = SimpleEvaluationContext
    .forReadOnlyDataBinding()
    .build();
Object value = exp.getValue(context);
```

---

### A04: Insecure Design

#### Missing Rate Limiting
```java
// ❌ VULNERABLE: No rate limiting
@PostMapping("/login")
public LoginResponse login(@RequestBody LoginRequest request) {
    return authService.login(request); // Brute force possible
}

// ✅ SECURE: Add rate limiting
@PostMapping("/login")
@RateLimiter(name = "login", fallbackMethod = "loginFallback")
public LoginResponse login(@RequestBody LoginRequest request) {
    return authService.login(request);
}

// Or use bucket4j
Bucket bucket = Bucket.builder()
    .addLimit(Bandwidth.classic(5, Refill.intervally(5, Duration.ofMinutes(1))))
    .build();
```

#### Missing Input Validation
```java
// ❌ VULNERABLE: No validation
@PostMapping("/transfer")
public void transfer(@RequestBody TransferRequest request) {
    // amount could be negative, stealing money!
    accountService.transfer(request);
}

// ✅ SECURE: Comprehensive validation
public class TransferRequest {
    @NotNull
    private Long fromAccountId;
    
    @NotNull
    private Long toAccountId;
    
    @NotNull
    @Positive
    @Digits(integer = 10, fraction = 2)
    private BigDecimal amount;
}
```

---

### A05: Security Misconfiguration

#### Debug Mode in Production
```yaml
# ❌ VULNERABLE
spring:
  devtools:
    restart:
      enabled: true  # Should be disabled in prod
  h2:
    console:
      enabled: true  # H2 console exposed

# ✅ SECURE: Use profiles
# application-prod.yml
spring:
  devtools:
    restart:
      enabled: false
  h2:
    console:
      enabled: false
```

#### Missing Security Headers
```java
// ✅ SECURE: Configure security headers
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.headers(headers -> headers
            .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
            .frameOptions(frame -> frame.deny())
            .xssProtection(xss -> xss.block(true))
            .contentTypeOptions(Customizer.withDefaults())
            .httpStrictTransportSecurity(hsts -> hsts
                .includeSubDomains(true)
                .maxAgeInSeconds(31536000))
        );
        return http.build();
    }
}
```

#### Default Credentials
```java
// ❌ VULNERABLE: Default credentials
spring.datasource.username=sa
spring.datasource.password=

// ✅ SECURE: Strong, externalized credentials
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}
```

---

### A06: Vulnerable Components

#### Dependency Scanning
```xml
<!-- Add OWASP dependency check -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>9.0.9</version>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
    </configuration>
</plugin>
```

#### Known Vulnerable Libraries
```xml
<!-- ❌ VULNERABLE: Known CVEs -->
<dependency>
    <groupId>log4j</groupId>
    <artifactId>log4j</artifactId>
    <version>1.2.17</version> <!-- CVE-2021-44228 -->
</dependency>

<!-- ✅ SECURE: Use patched version -->
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.21.1</version>
</dependency>
```

---

### A07: Authentication Failures

#### Session Fixation
```java
// ✅ SECURE: Change session ID on login
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.sessionManagement(session -> session
        .sessionFixation().newSession()
        .maximumSessions(1)
        .maxSessionsPreventsLogin(true)
    );
    return http.build();
}
```

#### Weak Password Policy
```java
// ✅ SECURE: Strong password validation
public class PasswordValidator {
    private static final Pattern PATTERN = Pattern.compile(
        "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!])(?=\\S+$).{12,}$"
    );
    
    public boolean isValid(String password) {
        return PATTERN.matcher(password).matches();
    }
}
```

#### Missing Account Lockout
```java
// ✅ SECURE: Implement lockout
@Service
public class LoginAttemptService {
    private final LoadingCache<String, Integer> attemptsCache;
    
    private static final int MAX_ATTEMPTS = 5;
    
    public void loginFailed(String key) {
        int attempts = attemptsCache.getUnchecked(key);
        attemptsCache.put(key, attempts + 1);
    }
    
    public boolean isBlocked(String key) {
        return attemptsCache.getUnchecked(key) >= MAX_ATTEMPTS;
    }
}
```

---

### A08: Data Integrity Failures

#### Missing CSRF Protection
```java
// ✅ SECURE: Enable CSRF
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.csrf(csrf -> csrf
        .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
    );
    return http.build();
}
```

#### JWT Without Signature Verification
```java
// ❌ VULNERABLE: Not verifying signature
Claims claims = Jwts.parser()
    .parseClaimsJwt(token)  // parseClaimsJWT doesn't verify!
    .getBody();

// ✅ SECURE: Verify signature
Claims claims = Jwts.parser()
    .setSigningKey(secretKey)
    .parseClaimsJws(token)  // parseClaimsJWS verifies
    .getBody();
```

---

### A09: Logging and Monitoring Failures

#### Insufficient Logging
```java
// ✅ SECURE: Log security-relevant events
@Service
public class AuditService {
    private final Logger auditLog = LoggerFactory.getLogger("AUDIT");
    
    public void logLoginSuccess(String username, String ip) {
        auditLog.info("LOGIN_SUCCESS user={} ip={}", username, ip);
    }
    
    public void logLoginFailure(String username, String ip, String reason) {
        auditLog.warn("LOGIN_FAILURE user={} ip={} reason={}", username, ip, reason);
    }
    
    public void logAccessDenied(String username, String resource) {
        auditLog.warn("ACCESS_DENIED user={} resource={}", username, resource);
    }
}
```

---

### A10: Server-Side Request Forgery (SSRF)

#### Unvalidated URL
```java
// ❌ VULNERABLE: User controls URL
@GetMapping("/fetch")
public String fetchUrl(@RequestParam String url) {
    return restTemplate.getForObject(url, String.class);
    // Can access internal services: http://localhost:8080/admin
}

// ✅ SECURE: Validate URL
@GetMapping("/fetch")
public String fetchUrl(@RequestParam String url) {
    URL parsedUrl = new URL(url);
    if (!ALLOWED_HOSTS.contains(parsedUrl.getHost())) {
        throw new SecurityException("Host not allowed");
    }
    if (isInternalAddress(parsedUrl.getHost())) {
        throw new SecurityException("Internal addresses not allowed");
    }
    return restTemplate.getForObject(url, String.class);
}
```

---

## Secret Detection Patterns

### Common Secret Patterns
```
AWS Access Key:      AKIA[0-9A-Z]{16}
AWS Secret Key:      [0-9a-zA-Z/+=]{40}
GitHub Token:        ghp_[0-9a-zA-Z]{36}
Slack Token:         xox[baprs]-[0-9a-zA-Z-]{10,}
Google API Key:      AIza[0-9A-Za-z-_]{35}
Stripe Key:          sk_live_[0-9a-zA-Z]{24}
RSA Private Key:     -----BEGIN RSA PRIVATE KEY-----
Generic Password:    password\s*=\s*["'][^"']+["']
JWT Secret:          jwt[_-]?secret\s*=\s*["'][^"']+["']
```

### Files to Scan
- `application.yml`, `application.properties`
- `docker-compose.yml`
- `.env`, `.env.local`
- `bootstrap.yml`
- Any file with `config`, `secret`, `credential` in name

---

## Security Review Checklist

### Authentication
- [ ] Passwords hashed with BCrypt/Argon2
- [ ] Secure session management
- [ ] Account lockout implemented
- [ ] Password policy enforced
- [ ] MFA available for sensitive operations

### Authorization
- [ ] All endpoints have authorization checks
- [ ] No IDOR vulnerabilities
- [ ] Role-based access control implemented
- [ ] Principle of least privilege followed

### Input Validation
- [ ] All inputs validated
- [ ] Parameterized queries used
- [ ] File upload restrictions
- [ ] Rate limiting implemented

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS for data in transit
- [ ] No sensitive data in logs
- [ ] Secure cookie flags set

### Configuration
- [ ] Debug mode disabled
- [ ] Default credentials changed
- [ ] Security headers configured
- [ ] CORS properly configured
