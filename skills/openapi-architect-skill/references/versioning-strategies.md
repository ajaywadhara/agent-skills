# API Versioning Strategies

## Overview of Approaches

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URL Path** | `/v1/users` | Clear, cacheable, easy routing | URL pollution, harder redirects |
| **Query Parameter** | `/users?version=1` | Optional, easy testing | Not RESTful, cache issues |
| **Header** | `API-Version: 1` | Clean URLs, flexible | Hidden, harder debugging |
| **Content Type** | `Accept: application/vnd.api.v1+json` | RESTful, granular | Complex, tooling issues |
| **Date-based** | `API-Version: 2024-01-15` | Clear timeline | Requires documentation |

---

## URL Path Versioning (Recommended)

### Implementation

```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0

servers:
  - url: https://api.example.com/v1
    description: Version 1 (stable)
  - url: https://api.example.com/v2
    description: Version 2 (current)
```

### Best Practices

```yaml
# Major versions only in URL
/v1/users    # Major version 1
/v2/users    # Major version 2

# Minor/patch versions in response headers
# X-API-Version: 1.2.3

# Never
/v1.2/users  # Bad - too granular
/v1.2.3/users  # Bad - patch in URL
```

### Routing Setup

```
https://api.example.com/v1/* → API v1 service
https://api.example.com/v2/* → API v2 service
```

---

## Header-Based Versioning

### Custom Header

```yaml
components:
  parameters:
    ApiVersion:
      name: API-Version
      in: header
      required: false
      schema:
        type: string
        default: "2"
        enum: ["1", "2"]
      description: API version (defaults to latest stable)
```

### Request Example

```http
GET /users HTTP/1.1
Host: api.example.com
API-Version: 2
```

### Date-Based Header (Stripe Style)

```yaml
components:
  parameters:
    ApiVersion:
      name: Stripe-Version
      in: header
      schema:
        type: string
        pattern: '^\d{4}-\d{2}-\d{2}$'
        default: "2024-01-15"
      description: |
        API version date. Each version is backwards-compatible
        with all requests since that date.
```

---

## Content Negotiation Versioning

### Accept Header

```yaml
# Request
Accept: application/vnd.myapi.v2+json

# Response
Content-Type: application/vnd.myapi.v2+json
```

### OpenAPI Definition

```yaml
paths:
  /users:
    get:
      responses:
        200:
          content:
            application/vnd.myapi.v1+json:
              schema:
                $ref: '#/components/schemas/UserV1'
            application/vnd.myapi.v2+json:
              schema:
                $ref: '#/components/schemas/UserV2'
```

---

## Version Lifecycle

### Stages

```
Alpha → Beta → Stable → Deprecated → Sunset
```

### Documentation

```yaml
info:
  title: My API
  version: 2.0.0
  x-api-status: stable
  x-deprecation-date: null
  x-sunset-date: null

# For deprecated version:
info:
  title: My API
  version: 1.0.0
  x-api-status: deprecated
  x-deprecation-date: "2024-01-01"
  x-sunset-date: "2024-07-01"
  description: |
    ⚠️ **DEPRECATED**: This version will be removed on 2024-07-01.
    Please migrate to v2. See migration guide: https://docs.example.com/migrate
```

### Deprecation Headers

```yaml
components:
  headers:
    Deprecation:
      schema:
        type: string
        format: date-time
      description: When this version was deprecated
      example: "Wed, 01 Jan 2024 00:00:00 GMT"

    Sunset:
      schema:
        type: string
        format: date-time
      description: When this version will be removed
      example: "Mon, 01 Jul 2024 00:00:00 GMT"

    Link:
      schema:
        type: string
      description: Link to successor version
      example: '<https://api.example.com/v2/users>; rel="successor-version"'
```

### Response Example

```http
HTTP/1.1 200 OK
Deprecation: Wed, 01 Jan 2024 00:00:00 GMT
Sunset: Mon, 01 Jul 2024 00:00:00 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

---

## Breaking vs Non-Breaking Changes

### Non-Breaking (No Version Bump)

- Adding new endpoints
- Adding optional request fields
- Adding response fields
- Adding new enum values (if clients ignore unknown)
- Adding optional headers
- Relaxing validation (accepting more)
- Bug fixes that match documented behavior

### Breaking (Requires New Version)

- Removing endpoints
- Removing or renaming fields
- Changing field types
- Changing response structure
- Adding required request fields
- Tightening validation
- Changing authentication
- Changing error formats
- Changing URL structure

---

## Migration Strategies

### Parallel Running

```yaml
servers:
  - url: https://api.example.com/v1
    description: Version 1 (deprecated, until 2024-07-01)
  - url: https://api.example.com/v2
    description: Version 2 (current)
```

### Feature Flags (Internal)

```yaml
# Same endpoint, different behavior based on version
/users:
  get:
    parameters:
      - name: API-Version
        in: header
    # Implementation checks version and returns appropriate format
```

### Gradual Rollout

```
Week 1: v2 available, v1 default
Week 4: v2 default, v1 available
Week 8: v1 deprecated warning
Week 16: v1 sunset
```

---

## Version Communication

### Documentation

```markdown
# API Changelog

## v2.0.0 (2024-01-15)

### Breaking Changes
- Renamed `user_name` to `username` in User schema
- Removed `GET /users/{id}/settings` (use `GET /settings`)

### New Features
- Added `GET /users/{id}/preferences`
- Added pagination to all list endpoints

### Migration Guide
1. Update field name: `user_name` → `username`
2. Update settings endpoint: `/users/{id}/settings` → `/settings`
```

### In-API Communication

```yaml
paths:
  /version:
    get:
      summary: Get API version info
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  current_version:
                    type: string
                    example: "2"
                  supported_versions:
                    type: array
                    items:
                      type: object
                      properties:
                        version:
                          type: string
                        status:
                          type: string
                          enum: [current, stable, deprecated, sunset]
                        sunset_date:
                          type: string
                          format: date
                          nullable: true
```

---

## Per-Resource Versioning

### When to Use

For large APIs where only some resources change:

```yaml
paths:
  /v1/users:     # Users still on v1
  /v2/orders:    # Orders upgraded to v2
  /v1/products:  # Products still on v1
```

### Considerations

- More complex routing
- Harder to understand compatibility
- Better for incremental migration

---

## Semantic Versioning for APIs

### Version Number Meaning

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, no API changes
  │     └──────── New features, backwards compatible
  └────────────── Breaking changes
```

### Exposure

```yaml
info:
  version: 2.1.3  # Full semver in spec

servers:
  - url: https://api.example.com/v2  # Major only in URL

# Response header for full version
X-API-Version: 2.1.3
```

---

## Best Practices Summary

1. **Use URL path versioning** for simplicity and clarity
2. **Version on major changes only** - don't over-version
3. **Plan for deprecation** from day one
4. **Communicate clearly** - changelog, headers, docs
5. **Give migration time** - minimum 6 months deprecation
6. **Support at least 2 versions** simultaneously
7. **Use feature flags** internally for gradual rollout
8. **Monitor version usage** to plan sunset timing
9. **Provide migration tools** - guides, codemods, examples
10. **Never remove without warning** - deprecate first
