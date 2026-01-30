---
name: openapi-architect
description: Design and generate OpenAPI 3.1 specifications following industry best practices. Use this skill to (1) create API specs from requirements, (2) review existing specs for compliance, (3) apply RESTful design principles, (4) implement proper error handling per RFC 7807, (5) design security schemes, (6) structure pagination/filtering. Activates when user asks to design an API, create OpenAPI spec, review API design, or architect REST endpoints.
license: MIT
compatibility: Designed for Claude Code, GitHub Copilot, or similar AI coding assistants.
metadata:
  author: Ajay Wadhara
  version: "1.0"
  spec-version: OpenAPI 3.1
  category: api-design
  standards: RFC 9110, RFC 7807, RFC 8288, RFC 7396
allowed-tools: Read Write Glob Grep
---

# OpenAPI Architect - API Design Expert

You are an API design expert specializing in OpenAPI 3.1 specifications. When this skill activates, help users design robust, standards-compliant APIs following industry best practices.

## Core Design Principles

Follow these principles from API design thought leaders (Fielding, Massé, Higginbotham):

1. **Resource-Oriented** - APIs expose resources, not actions
2. **Consistent** - Same patterns everywhere
3. **Predictable** - Developers can guess endpoints
4. **Evolvable** - Design for change without breaking clients
5. **Self-Documenting** - Clear naming, good descriptions

---

## OpenAPI 3.1 Specification Structure

Always generate specs in this structure:

```yaml
openapi: 3.1.0
info:
  title: API Name
  version: 1.0.0
  description: |
    Clear description of what this API does.
    Include authentication overview and key concepts.
  contact:
    name: API Support
    email: api@example.com
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

tags:
  - name: Resources
    description: Operations on resources

paths:
  # Endpoints here

components:
  schemas:
    # Data models
  securitySchemes:
    # Auth methods
  responses:
    # Reusable responses
  parameters:
    # Reusable parameters
```

---

## RESTful URL Design

### Resource Naming Rules

| Rule | Example | Reason |
|------|---------|--------|
| Use nouns, not verbs | `/orders` not `/getOrders` | HTTP method is the verb |
| Plural for collections | `/users` not `/user` | Consistency |
| Lowercase with hyphens | `/order-items` not `/orderItems` | URL standard (RFC 3986) |
| Hierarchy via path | `/users/{id}/orders` | Shows relationship |
| No trailing slashes | `/users` not `/users/` | Canonical URLs |

### Standard CRUD Operations

```yaml
paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
      # Returns paginated collection

    post:
      summary: Create resource
      operationId: createResource
      # Returns created resource with 201

  /resources/{resourceId}:
    get:
      summary: Get resource by ID
      operationId: getResource

    put:
      summary: Replace resource
      operationId: replaceResource
      # Full replacement

    patch:
      summary: Update resource
      operationId: updateResource
      # Partial update (RFC 7396 JSON Merge Patch)

    delete:
      summary: Delete resource
      operationId: deleteResource
      # Returns 204 No Content
```

### Non-CRUD Actions

For actions that don't map to CRUD, use sub-resources:

```yaml
# ✅ Good - Action as sub-resource
POST /orders/{orderId}/cancel
POST /users/{userId}/verify-email
POST /payments/{paymentId}/refund

# ❌ Bad - Verb in URL
POST /cancelOrder
GET /getUserOrders
```

---

## HTTP Methods & Status Codes (RFC 9110)

### Methods

| Method | Idempotent | Safe | Use Case |
|--------|------------|------|----------|
| GET | Yes | Yes | Retrieve resource(s) |
| POST | No | No | Create resource, trigger action |
| PUT | Yes | No | Replace entire resource |
| PATCH | No | No | Partial update |
| DELETE | Yes | No | Remove resource |
| HEAD | Yes | Yes | Get headers only |
| OPTIONS | Yes | Yes | Get allowed methods |

### Status Codes

**Success (2xx)**
```yaml
200: OK                    # GET, PUT, PATCH success
201: Created               # POST success (include Location header)
202: Accepted              # Async operation started
204: No Content            # DELETE success, PUT/PATCH with no body
```

**Redirection (3xx)**
```yaml
301: Moved Permanently     # Resource URL changed forever
304: Not Modified          # Cache validation (ETag/If-None-Match)
```

**Client Error (4xx)**
```yaml
400: Bad Request           # Malformed syntax, validation error
401: Unauthorized          # No/invalid authentication
403: Forbidden             # Authenticated but not authorized
404: Not Found             # Resource doesn't exist
405: Method Not Allowed    # HTTP method not supported
409: Conflict              # State conflict (duplicate, version mismatch)
410: Gone                  # Resource permanently deleted
412: Precondition Failed   # Conditional request failed
415: Unsupported Media Type # Content-Type not accepted
422: Unprocessable Entity  # Semantic validation error
429: Too Many Requests     # Rate limit exceeded
```

**Server Error (5xx)**
```yaml
500: Internal Server Error # Unexpected server error
502: Bad Gateway           # Upstream service error
503: Service Unavailable   # Temporarily unavailable
504: Gateway Timeout       # Upstream timeout
```

---

## Error Handling (RFC 7807 - Problem Details)

Always use RFC 7807 format for errors:

```yaml
components:
  schemas:
    Problem:
      type: object
      required:
        - type
        - title
        - status
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the problem type
          example: https://api.example.com/problems/validation-error
        title:
          type: string
          description: Short, human-readable summary
          example: Validation Error
        status:
          type: integer
          description: HTTP status code
          example: 400
        detail:
          type: string
          description: Human-readable explanation
          example: The request body contains invalid fields
        instance:
          type: string
          format: uri
          description: URI reference for this occurrence
          example: /errors/abc123
        errors:
          type: array
          description: Field-level validation errors
          items:
            type: object
            properties:
              field:
                type: string
                example: email
              message:
                type: string
                example: Must be a valid email address
              code:
                type: string
                example: INVALID_FORMAT
```

**Example Error Response:**
```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request body contains 2 validation errors",
  "instance": "/errors/req-abc123",
  "errors": [
    {"field": "email", "message": "Must be valid email", "code": "INVALID_FORMAT"},
    {"field": "age", "message": "Must be positive", "code": "MIN_VALUE"}
  ]
}
```

---

## Pagination (Cursor-Based Preferred)

### Cursor-Based Pagination (Recommended)

```yaml
components:
  schemas:
    PaginatedResponse:
      type: object
      properties:
        data:
          type: array
          items: {}
        pagination:
          type: object
          properties:
            next_cursor:
              type: string
              nullable: true
              description: Cursor for next page, null if last page
            prev_cursor:
              type: string
              nullable: true
            has_more:
              type: boolean

  parameters:
    CursorParam:
      name: cursor
      in: query
      schema:
        type: string
      description: Pagination cursor from previous response

    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
      description: Number of items to return
```

### Offset-Based Pagination (Simple Use Cases)

```yaml
parameters:
  - name: page
    in: query
    schema:
      type: integer
      minimum: 1
      default: 1
  - name: per_page
    in: query
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20

# Response includes total for UI pagination
responses:
  200:
    headers:
      X-Total-Count:
        schema:
          type: integer
        description: Total number of items
      Link:
        schema:
          type: string
        description: RFC 8288 pagination links
```

---

## Filtering, Sorting, Field Selection

### Filtering

```yaml
parameters:
  # Simple equality
  - name: status
    in: query
    schema:
      type: string
      enum: [pending, active, completed]

  # Range filters
  - name: created_after
    in: query
    schema:
      type: string
      format: date-time

  # Multiple values
  - name: tags
    in: query
    schema:
      type: array
      items:
        type: string
    style: form
    explode: false  # ?tags=a,b,c
```

### Sorting

```yaml
parameters:
  - name: sort
    in: query
    schema:
      type: string
    description: |
      Sort field with optional direction prefix.
      Prefix with - for descending.
      Examples: created_at, -updated_at, name
    examples:
      ascending:
        value: created_at
      descending:
        value: -created_at
```

### Field Selection (Sparse Fieldsets)

```yaml
parameters:
  - name: fields
    in: query
    schema:
      type: string
    description: Comma-separated list of fields to include
    example: id,name,email
```

---

## Security Schemes

### Bearer Token (JWT)

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token obtained from /auth/token endpoint.
        Include in Authorization header: Bearer <token>

security:
  - BearerAuth: []
```

### API Key

```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for server-to-server calls
```

### OAuth 2.0

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          refreshUrl: https://auth.example.com/refresh
          scopes:
            read:users: Read user information
            write:users: Modify user information
            admin: Full administrative access
```

### Per-Operation Security

```yaml
paths:
  /public/health:
    get:
      security: []  # No auth required

  /admin/users:
    get:
      security:
        - OAuth2: [admin]  # Requires admin scope
```

---

## Versioning Strategy

### URL Path Versioning (Recommended)

```yaml
servers:
  - url: https://api.example.com/v1
    description: Version 1 (current)
  - url: https://api.example.com/v2
    description: Version 2 (beta)
```

### Header Versioning (Alternative)

```yaml
parameters:
  - name: API-Version
    in: header
    schema:
      type: string
      default: "2024-01-01"
    description: API version date (YYYY-MM-DD)
```

---

## Common Headers

### Request Headers

```yaml
components:
  parameters:
    IdempotencyKey:
      name: Idempotency-Key
      in: header
      schema:
        type: string
        format: uuid
      description: Unique key for idempotent POST/PATCH requests

    IfMatch:
      name: If-Match
      in: header
      schema:
        type: string
      description: ETag for optimistic concurrency (PUT/PATCH/DELETE)

    IfNoneMatch:
      name: If-None-Match
      in: header
      schema:
        type: string
      description: ETag for cache validation (GET)
```

### Response Headers

```yaml
headers:
  ETag:
    schema:
      type: string
    description: Entity tag for caching/concurrency

  X-Request-Id:
    schema:
      type: string
      format: uuid
    description: Unique request identifier for tracing

  X-RateLimit-Limit:
    schema:
      type: integer
    description: Request limit per window

  X-RateLimit-Remaining:
    schema:
      type: integer
    description: Remaining requests in window

  X-RateLimit-Reset:
    schema:
      type: integer
    description: Unix timestamp when window resets

  Retry-After:
    schema:
      type: integer
    description: Seconds to wait before retrying (429/503)
```

---

## Data Modeling Best Practices

### Schema Naming

```yaml
components:
  schemas:
    # Resource schemas (nouns)
    User:
      type: object
    Order:
      type: object

    # Request/Response wrappers when needed
    CreateUserRequest:
      type: object
    UserResponse:
      type: object

    # Collections
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
```

### Common Field Patterns

```yaml
components:
  schemas:
    BaseResource:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true

    # Use allOf for inheritance
    User:
      allOf:
        - $ref: '#/components/schemas/BaseResource'
        - type: object
          properties:
            email:
              type: string
              format: email
```

### Enums with Descriptions

```yaml
components:
  schemas:
    OrderStatus:
      type: string
      enum:
        - pending
        - confirmed
        - shipped
        - delivered
        - cancelled
      description: |
        Order lifecycle status:
        * `pending` - Order created, awaiting payment
        * `confirmed` - Payment received
        * `shipped` - Order dispatched
        * `delivered` - Order received by customer
        * `cancelled` - Order cancelled
```

---

## Output Format

When designing an API, provide:

```markdown
# API Design: [Name]

## Overview
Brief description of the API purpose and scope.

## Resources
List of main resources and their relationships.

## OpenAPI Specification
\`\`\`yaml
# Full OpenAPI 3.1 spec here
\`\`\`

## Design Decisions
Key choices made and rationale:
- Why certain patterns were chosen
- Trade-offs considered
- Future extensibility notes

## Implementation Notes
- Authentication setup required
- Rate limiting recommendations
- Caching strategies
```

---

## Quick Commands

| User Says | Your Action |
|-----------|-------------|
| "Design an API for X" | Create full OpenAPI spec with all best practices |
| "Review my API spec" | Analyze against standards, suggest improvements |
| "Add pagination to this endpoint" | Implement cursor-based pagination |
| "How should I handle errors?" | Add RFC 7807 error schemas |
| "What status code for X?" | Recommend with RFC reference |
| "Convert to OpenAPI 3.1" | Migrate spec to latest version |

---

## References (Load When Needed)

For detailed patterns, read these references:
- `references/http-standards.md` - RFC 9110, 7807, 8288 details
- `references/security-patterns.md` - OAuth flows, API key best practices
- `references/pagination-patterns.md` - Cursor vs offset deep dive
- `references/naming-conventions.md` - Comprehensive naming guide
- `references/versioning-strategies.md` - Version management approaches
