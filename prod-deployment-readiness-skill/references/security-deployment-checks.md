# Security Deployment Checks

Detailed patterns for detecting security-impacting changes that need extra deployment care.

---

## Auth/AuthZ Change Detection

### Java/Spring Security

```java
// BLOCKER: Security filter chain modified
@Bean
SecurityFilterChain filterChain(HttpSecurity http) {
    // Check for:
    // - .permitAll() added to previously authenticated endpoints
    // - .csrf().disable() added
    // - .cors().disable() added
    // - Authorization rules changed
    // - Authentication mechanism changed
}

// BLOCKER: Method security removed
// Was: @PreAuthorize("hasRole('ADMIN')")
// Now: annotation removed

// WARNING: New endpoint without security annotation
@GetMapping("/api/admin/data")  // No @PreAuthorize or @Secured
public Data getAdminData() { }
```

### Detection Patterns (Java)

```regex
# Security configuration changes
SecurityFilterChain
WebSecurityConfigurer
@EnableWebSecurity
@EnableMethodSecurity
@PreAuthorize
@Secured
@RolesAllowed

# Dangerous patterns
\.permitAll\(\)
\.csrf\(\)\.disable\(\)
\.cors\(\)\.disable\(\)
\.headers\(\)\.frameOptions\(\)\.disable\(\)
\.anonymous\(\)
```

### Node.js (Express/Passport/Auth0)

```javascript
// Check for:
// - Middleware removed from route
// - passport.authenticate removed
// - JWT verification removed
// - Role check removed

// BLOCKER: Auth middleware removed from route
// Was: router.get('/admin', requireAuth, requireAdmin, handler)
// Now: router.get('/admin', handler)

// WARNING: Token expiry changed
jwt.sign(payload, secret, { expiresIn: '30d' })  // Was '1h'
```

### Python (Django/Flask)

```python
# Django
# BLOCKER: @login_required removed
# BLOCKER: permission_classes changed to AllowAny
# WARNING: authentication_classes changed

# Flask
# BLOCKER: @auth.login_required removed
# BLOCKER: Flask-Login @login_required removed
```

---

## CORS Configuration Analysis

### Dangerous CORS Patterns

| Pattern | Severity | Description |
|---------|----------|-------------|
| `Access-Control-Allow-Origin: *` in prod | BLOCKER | Any origin can make requests |
| `Access-Control-Allow-Credentials: true` with wildcard origin | BLOCKER | Security vulnerability |
| CORS allowed origins expanded | WARNING | Verify new origins are trusted |
| CORS allowed methods expanded | WARNING | New HTTP methods accessible |
| CORS allowed headers expanded | INFO | New headers accepted |
| CORS config removed entirely | WARNING | May break legitimate cross-origin requests |

### Detection Per Stack

```java
// Spring Boot
@CrossOrigin(origins = "*")  // BLOCKER
cors.allowedOrigins("*")     // BLOCKER
cors.allowCredentials(true)  // Check if combined with wildcard
```

```javascript
// Express/Node.js
cors({ origin: '*' })              // BLOCKER
cors({ origin: true })             // BLOCKER (reflects any origin)
cors({ credentials: true })        // Check if combined with wildcard
app.use(cors())                    // WARNING: default allows all
```

```python
# Django
CORS_ALLOW_ALL_ORIGINS = True      # BLOCKER
CORS_ORIGIN_ALLOW_ALL = True       # BLOCKER (deprecated name)
CORS_ALLOW_CREDENTIALS = True      # Check if combined with allow all
```

---

## CSP (Content Security Policy) Changes

### Patterns to Watch

| Change | Severity | Description |
|--------|----------|-------------|
| CSP header removed | BLOCKER | No XSS protection |
| `unsafe-inline` added to script-src | WARNING | XSS risk increased |
| `unsafe-eval` added | WARNING | Code injection risk |
| Wildcard domain in CSP | WARNING | Too permissive |
| `frame-ancestors` relaxed | WARNING | Clickjacking risk |
| New domain added to connect-src | INFO | New external connection allowed |

---

## Secret Rotation Requirements

### When to Flag Secret Rotation

| Change | Severity | Action |
|--------|----------|--------|
| Auth provider changed | WARNING | Rotate all tokens/keys for old provider |
| JWT signing key config changed | WARNING | All existing tokens will be invalid |
| Database credentials config changed | WARNING | Ensure new credentials are provisioned |
| API key reference changed | WARNING | Ensure new key is active before deploy |
| OAuth client ID/secret changed | WARNING | Re-register with OAuth provider |
| Encryption key reference changed | BLOCKER | Data encrypted with old key must be re-encrypted or dual-key support added |

---

## TLS / Certificate Changes

### Patterns to Check

| Change | Severity | Description |
|--------|----------|-------------|
| TLS verification disabled | BLOCKER | MITM attack risk |
| Certificate path changed | WARNING | Cert must exist at new path |
| SSL/TLS version changed | WARNING | Compatibility with clients |
| Trust store modified | WARNING | May reject or accept different certs |
| Self-signed cert added to trust | WARNING | Only acceptable for internal services |

### Detection Patterns

```regex
# Java
SSLContext\.getInstance
TrustManager
setHostnameVerifier
verify.*return\s+true  # BLOCKER: hostname verification bypass

# Node.js
rejectUnauthorized:\s*false  # BLOCKER
NODE_TLS_REJECT_UNAUTHORIZED.*0  # BLOCKER

# Python
verify\s*=\s*False  # BLOCKER (requests library)
ssl\._create_unverified_context  # BLOCKER
```

---

## New External Integration Security

When a new external service integration is detected:

### Impact Assessment Checklist

- [ ] Data classification: What data flows to/from this service?
- [ ] Authentication: How is the integration authenticated?
- [ ] TLS: Is the connection encrypted in transit?
- [ ] Data residency: Where does the external service store data?
- [ ] Fallback: What happens if the external service is down?
- [ ] Rate limiting: Are we protected from abuse?
- [ ] Logging: Are requests/responses logged (without secrets)?

### Detection

```regex
# New HTTP client URLs
https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
RestTemplate|WebClient|HttpClient
fetch\(|axios\.|request\(
requests\.(get|post|put|delete)\(
```

Flag as WARNING when new external domain appears in changed code.
