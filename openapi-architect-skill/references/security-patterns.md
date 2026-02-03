# API Security Patterns

## Authentication Methods

### 1. Bearer Token (JWT)

**Best For:** Mobile apps, SPAs, microservices

```yaml
securitySchemes:
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

**JWT Best Practices:**
- Short expiration (15-60 minutes)
- Use refresh tokens for long sessions
- Include minimal claims (sub, iat, exp, scope)
- Validate signature, issuer, audience
- Use RS256 or ES256 (asymmetric) for distributed systems

**Token Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2g...",
  "scope": "read:users write:users"
}
```

---

### 2. OAuth 2.0 Flows

**Authorization Code (Web Apps)**
```yaml
OAuth2AuthCode:
  type: oauth2
  flows:
    authorizationCode:
      authorizationUrl: https://auth.example.com/authorize
      tokenUrl: https://auth.example.com/token
      refreshUrl: https://auth.example.com/refresh
      scopes:
        read: Read access
        write: Write access
```

**Client Credentials (Machine-to-Machine)**
```yaml
OAuth2ClientCredentials:
  type: oauth2
  flows:
    clientCredentials:
      tokenUrl: https://auth.example.com/token
      scopes:
        api:full: Full API access
```

**PKCE (Mobile/SPA)**
Always use PKCE for public clients:
- Generate code_verifier (random string)
- Create code_challenge = BASE64URL(SHA256(code_verifier))
- Send code_challenge in authorization request
- Send code_verifier in token request

---

### 3. API Keys

**Best For:** Server-to-server, public APIs with rate limits

```yaml
ApiKeyHeader:
  type: apiKey
  in: header
  name: X-API-Key

ApiKeyQuery:
  type: apiKey
  in: query
  name: api_key  # Less secure, visible in logs
```

**Best Practices:**
- Prefix keys for identification: `sk_live_`, `pk_test_`
- Hash keys in database (store only hash)
- Support key rotation (multiple active keys)
- Bind to IP allowlist when possible
- Different keys for test/production

---

### 4. Mutual TLS (mTLS)

**Best For:** High-security B2B, zero-trust networks

```yaml
securitySchemes:
  MutualTLS:
    type: mutualTLS
    description: Client certificate required
```

---

## Authorization Patterns

### Scope-Based Access

```yaml
paths:
  /users:
    get:
      security:
        - OAuth2: [read:users]
    post:
      security:
        - OAuth2: [write:users]

  /admin/settings:
    get:
      security:
        - OAuth2: [admin]
```

### Role-Based (RBAC)

```yaml
components:
  schemas:
    TokenClaims:
      properties:
        roles:
          type: array
          items:
            type: string
            enum: [user, admin, super_admin]
```

### Resource-Based

Check ownership in business logic:
```
GET /users/{userId}/orders
# Verify: token.sub == userId OR token.roles.includes('admin')
```

---

## Security Headers

### Recommended Response Headers

```yaml
components:
  headers:
    SecurityHeaders:
      description: Standard security headers
      # Include in all responses:
      # Strict-Transport-Security: max-age=31536000; includeSubDomains
      # X-Content-Type-Options: nosniff
      # X-Frame-Options: DENY
      # Content-Security-Policy: default-src 'none'
      # X-Request-Id: <uuid>
```

**Header Details:**

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000` | Force HTTPS |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `X-XSS-Protection` | `0` | Disable (causes issues) |
| `Content-Security-Policy` | `default-src 'none'` | For API responses |

---

## Input Validation

### OpenAPI Schema Validation

```yaml
components:
  schemas:
    CreateUser:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
          maxLength: 255
        name:
          type: string
          minLength: 1
          maxLength: 100
          pattern: '^[a-zA-Z\s\-]+$'
        age:
          type: integer
          minimum: 0
          maximum: 150
        website:
          type: string
          format: uri
          pattern: '^https://'
```

### Validation Rules to Enforce

1. **Type validation** - Reject wrong types
2. **Format validation** - email, uri, uuid, date-time
3. **Length limits** - Prevent overflow attacks
4. **Pattern matching** - Whitelist allowed characters
5. **Enum validation** - Reject unknown values
6. **Required fields** - Reject incomplete data

---

## Rate Limiting

### Strategies

| Strategy | Use Case | Example |
|----------|----------|---------|
| Fixed Window | Simple | 100 req/minute |
| Sliding Window | Smoother | 100 req/60 seconds rolling |
| Token Bucket | Bursts OK | 100 tokens, refill 10/sec |
| Leaky Bucket | Steady rate | Process 10 req/sec max |

### Response Headers

```yaml
components:
  headers:
    RateLimitHeaders:
      X-RateLimit-Limit:
        schema:
          type: integer
        description: Requests allowed per window
      X-RateLimit-Remaining:
        schema:
          type: integer
        description: Requests remaining
      X-RateLimit-Reset:
        schema:
          type: integer
        description: Seconds until reset
```

### 429 Response

```yaml
responses:
  TooManyRequests:
    description: Rate limit exceeded
    headers:
      Retry-After:
        schema:
          type: integer
        description: Seconds to wait
    content:
      application/problem+json:
        schema:
          $ref: '#/components/schemas/Problem'
        example:
          type: https://api.example.com/problems/rate-limit
          title: Rate Limit Exceeded
          status: 429
          detail: You have exceeded 100 requests per minute
```

---

## Sensitive Data Handling

### Never Expose in Responses

- Passwords (even hashed)
- Internal IDs when UUIDs available
- Stack traces in production
- Database error details
- Infrastructure info (server names, IPs)

### Audit Logging

Log these events (without sensitive data):
- Authentication attempts (success/failure)
- Authorization failures
- Resource creation/modification/deletion
- Admin actions
- Rate limit hits

### PII Considerations

```yaml
components:
  schemas:
    User:
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
          description: PII - handle per GDPR/CCPA
          x-pii: true
        ssn:
          type: string
          writeOnly: true  # Never returned in responses
          x-sensitive: true
```

---

## OWASP API Security Top 10

| Risk | Mitigation |
|------|------------|
| Broken Object Level Auth | Verify ownership on every request |
| Broken Authentication | Strong auth, rate limit, MFA |
| Broken Object Property Auth | Use DTOs, never expose internals |
| Unrestricted Resource Consumption | Rate limits, pagination limits |
| Broken Function Level Auth | Check permissions per endpoint |
| Unrestricted Access to Business Flows | Rate limit sensitive operations |
| Server Side Request Forgery | Validate/allowlist URLs |
| Security Misconfiguration | Secure defaults, no debug in prod |
| Improper Inventory Management | Document all endpoints, deprecate properly |
| Unsafe Consumption of APIs | Validate all external API responses |
