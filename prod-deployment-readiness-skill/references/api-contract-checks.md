# API Contract Checks

Detailed patterns for detecting breaking API changes that affect downstream consumers.

---

## Breaking Change Detection Per Stack

### Java/Spring Boot

```java
// Controller changes to detect:

// BLOCKER: Endpoint removed
// Was: @GetMapping("/api/v1/users/{id}")
// Now: method deleted or path changed

// BLOCKER: Required field added to request
public record CreateUserRequest(
    String name,
    String email,
    String phone  // NEW required field - breaks existing clients
) {}

// WARNING: Response field removed
public record UserResponse(
    Long id,
    String name
    // String email  <-- REMOVED - may break consumers
) {}

// WARNING: Path parameter renamed
// Was: @PathVariable("userId") Long userId
// Now: @PathVariable("id") Long id
// (if using name-based binding)

// WARNING: HTTP method changed
// Was: @PostMapping("/api/v1/users/search")
// Now: @GetMapping("/api/v1/users/search")
```

### Detection Patterns (Java)

```regex
# Endpoint removal: look for deleted @*Mapping annotations
(?i)@(Get|Post|Put|Delete|Patch)Mapping\s*\(

# Request body changes: look for modified record/class in DTO package
(?i)(record|class)\s+\w+(Request|Dto|Command)\s*\(

# Response changes: look for modified response types
(?i)(record|class)\s+\w+(Response|Dto|View)\s*\(

# Path changes
(?i)@RequestMapping\s*\(\s*["'][^"']+["']
```

### Node.js (Express/Fastify/NestJS)

```javascript
// Route changes to detect:

// BLOCKER: Route removed
// Was: router.get('/api/v1/users/:id', getUser)
// Now: line deleted

// BLOCKER: Required body field added
// Was: const { name, email } = req.body
// Now: const { name, email, phone } = req.body
//      if (!phone) throw new BadRequestError()

// WARNING: Response shape changed
// Was: res.json({ id, name, email })
// Now: res.json({ id, name })  // email removed
```

### Detection Patterns (Node.js)

```regex
# Route definitions
(router|app)\.(get|post|put|delete|patch)\s*\(
@(Get|Post|Put|Delete|Patch)\s*\(

# Request validation changes
(body|query|params)\s*\.\s*\w+
Joi\.object\s*\(
z\.object\s*\(
```

### Python (Django/Flask/FastAPI)

```python
# Endpoint changes to detect:

# BLOCKER: URL pattern removed (Django)
# Was: path('api/v1/users/<int:pk>/', UserView.as_view())
# Now: line deleted

# BLOCKER: Required field added (FastAPI/Pydantic)
# Was: class CreateUser(BaseModel): name: str; email: str
# Now: class CreateUser(BaseModel): name: str; email: str; phone: str

# WARNING: Response model changed
# Was: class UserResponse(BaseModel): id: int; name: str; email: str
# Now: class UserResponse(BaseModel): id: int; name: str
```

---

## OpenAPI/Swagger Diff Analysis

### When OpenAPI Spec is Available

If the project has `openapi.yml`, `openapi.json`, `swagger.yml`, or `swagger.json`:

1. **Compare old vs new spec** (from git diff)
2. **Check for breaking changes:**

| Change | Severity | Reason |
|--------|----------|--------|
| Path removed | BLOCKER | Consumers lose access |
| Required parameter added | BLOCKER | Existing requests fail |
| Response property removed | WARNING | Consumers may depend on it |
| Enum value removed | BLOCKER | Existing values rejected |
| Type changed (e.g., string -> integer) | BLOCKER | Parsing failures |
| New optional parameter | INFO | Backward-compatible |
| New response property | INFO | Backward-compatible |
| New path added | INFO | No impact on existing consumers |

### OpenAPI Files to Watch

```
openapi.yml / openapi.yaml / openapi.json
swagger.yml / swagger.yaml / swagger.json
api-docs/**
src/main/resources/static/swagger/**
```

---

## gRPC / Protobuf Backward Compatibility

### Breaking Changes in Proto Files

```protobuf
// BLOCKER: Field number reused
message User {
  // Was: string email = 2;
  // Now: string phone = 2;  // BREAKS all existing clients
}

// BLOCKER: Field type changed
message User {
  // Was: string id = 1;
  // Now: int64 id = 1;  // Incompatible wire format
}

// BLOCKER: Required field semantics changed (proto3 -> explicit presence)

// WARNING: Field removed (should be reserved)
message User {
  string name = 1;
  // string email = 2;  // REMOVED - should use 'reserved 2;'
}

// INFO: New field added (backward-compatible)
message User {
  string name = 1;
  string email = 2;
  string phone = 3;  // New field, safe
}
```

### Proto Compatibility Rules

| Change | Compatible? | Severity |
|--------|------------|----------|
| Add new field | Yes | INFO |
| Remove field (with reserved) | Yes | WARNING |
| Remove field (without reserved) | No | BLOCKER |
| Rename field | Yes (wire uses numbers) | INFO |
| Change field number | No | BLOCKER |
| Change field type | No | BLOCKER |
| Add enum value | Yes | INFO |
| Remove enum value | No | BLOCKER |
| Rename service/RPC | No | BLOCKER |

---

## GraphQL Schema Evolution

### Breaking Changes in GraphQL

```graphql
# BLOCKER: Field removed from type
type User {
  id: ID!
  name: String!
  # email: String!  <-- REMOVED, breaks queries requesting email
}

# BLOCKER: Non-null added to existing nullable field
# Was: phone: String
# Now: phone: String!  <-- Existing data may have nulls

# BLOCKER: Argument added as required
# Was: users(limit: Int): [User!]!
# Now: users(limit: Int, filter: FilterInput!): [User!]!

# WARNING: Type changed
# Was: age: Int
# Now: age: String

# INFO: New field added (safe)
type User {
  id: ID!
  name: String!
  avatar: String  # New optional field
}
```

---

## Versioning Strategy Validation

### Check for Versioning When Breaking Changes Found

If breaking changes detected, verify versioning is in place:

| Strategy | Detection | Check |
|----------|-----------|-------|
| URL versioning | `/api/v1/`, `/api/v2/` | New version path exists alongside old |
| Header versioning | `Accept: application/vnd.api.v2+json` | Version handling in middleware |
| Query param | `?version=2` | Version parameter handling |

### Severity Rules

- BLOCKER: Breaking change without any versioning strategy
- WARNING: Breaking change with versioning but old version removed simultaneously
- INFO: Breaking change with proper versioning (old version still available)

---

## Consumer Impact Checklist

When breaking API changes are found, generate this checklist:

- [ ] All known consumers identified
- [ ] Consumers notified of breaking change
- [ ] Migration guide provided for consumers
- [ ] Deprecation period set (minimum 1 release cycle)
- [ ] Old endpoint still available during transition
- [ ] Monitoring on old endpoint to track consumer migration
- [ ] Timeline for old endpoint removal documented
