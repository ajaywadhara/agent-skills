# HTTP Standards & RFCs Reference

## Key RFCs for API Design

### RFC 9110 - HTTP Semantics (2022)
Supersedes RFC 7231. Defines HTTP methods, status codes, and headers.

### RFC 9111 - HTTP Caching (2022)
Cache-Control, ETag, conditional requests.

### RFC 7807 - Problem Details for HTTP APIs (2016)
Standard error response format. See main SKILL.md for implementation.

### RFC 8288 - Web Linking (2017)
Link header format for pagination and related resources.

### RFC 6585 - Additional HTTP Status Codes (2012)
Defines 428, 429, 431, 511.

### RFC 7396 - JSON Merge Patch (2014)
Standard for PATCH request bodies.

### RFC 6902 - JSON Patch (2013)
Alternative PATCH format with operations array.

---

## Method Semantics (RFC 9110)

### Safe Methods
Do not modify server state. Clients can cache and prefetch.
- GET, HEAD, OPTIONS, TRACE

### Idempotent Methods
Multiple identical requests = same result as single request.
- GET, HEAD, PUT, DELETE, OPTIONS, TRACE
- Note: POST and PATCH are NOT idempotent

### Cacheable Methods
Responses may be cached by default.
- GET, HEAD
- POST responses cacheable only with explicit headers

---

## Content Negotiation

### Request Headers
```
Accept: application/json, application/xml;q=0.9, */*;q=0.8
Accept-Language: en-US, en;q=0.9
Accept-Encoding: gzip, deflate, br
```

### Response Headers
```
Content-Type: application/json; charset=utf-8
Content-Language: en-US
Content-Encoding: gzip
Vary: Accept, Accept-Language
```

---

## Conditional Requests

### ETag-Based (Strong Validation)
```
# Response includes ETag
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"

# Subsequent GET with cache validation
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
# Returns 304 Not Modified if unchanged

# PUT/PATCH with optimistic locking
If-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
# Returns 412 Precondition Failed if changed
```

### Last-Modified (Weak Validation)
```
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT

If-Modified-Since: Wed, 21 Oct 2024 07:28:00 GMT
If-Unmodified-Since: Wed, 21 Oct 2024 07:28:00 GMT
```

---

## Link Header (RFC 8288)

### Pagination Links
```
Link: <https://api.example.com/users?cursor=abc123>; rel="next",
      <https://api.example.com/users?cursor=xyz789>; rel="prev",
      <https://api.example.com/users>; rel="first"
```

### Standard Relations
- `self` - Current resource
- `next` - Next page
- `prev` - Previous page
- `first` - First page
- `last` - Last page
- `collection` - Parent collection
- `item` - Item in collection

---

## Cache-Control Directives

### Response Directives
```
# Public caching for 1 hour
Cache-Control: public, max-age=3600

# Private (browser only), revalidate
Cache-Control: private, no-cache

# Never cache
Cache-Control: no-store

# Stale-while-revalidate pattern
Cache-Control: max-age=60, stale-while-revalidate=300
```

### Request Directives
```
Cache-Control: no-cache          # Force revalidation
Cache-Control: no-store          # Don't cache response
Cache-Control: max-age=0         # Want fresh response
```

---

## CORS Headers

### Simple Requests
```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: X-Request-Id, X-RateLimit-Remaining
```

### Preflight Response (OPTIONS)
```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH
Access-Control-Allow-Headers: Authorization, Content-Type, X-Request-Id
Access-Control-Max-Age: 86400
```

---

## Rate Limiting Headers

### Standard Pattern (Draft RFC)
```
X-RateLimit-Limit: 100           # Requests allowed per window
X-RateLimit-Remaining: 45        # Requests remaining
X-RateLimit-Reset: 1704067200    # Unix timestamp of reset
Retry-After: 60                  # Seconds to wait (on 429)
```

### IETF Draft Standard
```
RateLimit-Limit: 100
RateLimit-Remaining: 45
RateLimit-Reset: 60              # Seconds until reset (not timestamp)
```

---

## Content Types

### Standard Types
```
application/json                           # JSON response
application/problem+json                   # RFC 7807 errors
application/merge-patch+json               # RFC 7396 PATCH
application/json-patch+json                # RFC 6902 PATCH
application/x-www-form-urlencoded          # Form data
multipart/form-data                        # File uploads
```

### Vendor Types
```
application/vnd.api+json                   # JSON:API
application/hal+json                       # HAL
application/vnd.example.v1+json            # Versioned custom type
```
