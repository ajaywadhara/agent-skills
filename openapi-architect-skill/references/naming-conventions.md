# API Naming Conventions

## URL Path Naming

### Rules

| Rule | Good | Bad |
|------|------|-----|
| Use nouns, not verbs | `/orders` | `/getOrders`, `/createOrder` |
| Use plural nouns | `/users` | `/user` |
| Use lowercase | `/order-items` | `/OrderItems`, `/orderItems` |
| Use hyphens for multi-word | `/order-items` | `/order_items`, `/orderitems` |
| No trailing slashes | `/users` | `/users/` |
| No file extensions | `/users/123` | `/users/123.json` |

### Resource Hierarchy

```
# Collection
GET /users

# Item in collection
GET /users/{userId}

# Sub-resource (belongs to parent)
GET /users/{userId}/orders

# Item in sub-resource
GET /users/{userId}/orders/{orderId}

# Limit nesting to 2 levels
# Instead of: /users/{id}/orders/{id}/items/{id}
# Use: /order-items/{id}
```

### Actions as Sub-Resources

```
# State transitions
POST /orders/{orderId}/cancel
POST /orders/{orderId}/ship
POST /users/{userId}/activate

# Processes
POST /reports/{reportId}/generate
POST /emails/{emailId}/send

# Calculations (can be GET if no side effects)
GET /orders/{orderId}/total
POST /carts/{cartId}/checkout
```

---

## Path Parameters

### Naming

```yaml
# Use camelCase for parameter names
/users/{userId}
/orders/{orderId}/items/{itemId}

# Be specific
/users/{userId}      # Good
/users/{id}          # OK if unambiguous
/users/{user}        # Bad - confusing
```

### Type Indication (Optional)

```yaml
# Include type hint when helpful
/posts/{postSlug}           # String slug
/users/{userId}             # UUID
/products/{productSku}      # SKU code
```

---

## Query Parameters

### Naming Conventions

```yaml
# Use snake_case for query params
?created_after=2024-01-01
?order_by=created_at
?include_deleted=true

# Or camelCase (be consistent)
?createdAfter=2024-01-01
?orderBy=created_at
```

### Common Parameters

| Purpose | Parameter | Example |
|---------|-----------|---------|
| Pagination | `cursor`, `limit`, `offset`, `page`, `per_page` | `?limit=20&cursor=abc` |
| Sorting | `sort`, `order_by` | `?sort=-created_at` |
| Filtering | Field name or prefixed | `?status=active&created_after=2024-01-01` |
| Field selection | `fields` | `?fields=id,name,email` |
| Expansion | `expand`, `include` | `?expand=orders,profile` |
| Search | `q`, `query`, `search` | `?q=john` |

### Filter Operators

```yaml
# Equality (default)
?status=active

# Multiple values
?status=active,pending
?status[]=active&status[]=pending

# Comparison (option 1: suffix)
?price_gte=100&price_lte=500
?created_after=2024-01-01

# Comparison (option 2: bracketed)
?price[gte]=100&price[lte]=500
?created[after]=2024-01-01
```

---

## Request/Response Body Fields

### JSON Field Naming

**Use snake_case (Recommended for most APIs):**
```json
{
  "user_id": "123",
  "first_name": "John",
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

**Or camelCase (Common in JavaScript ecosystems):**
```json
{
  "userId": "123",
  "firstName": "John",
  "createdAt": "2024-01-15T10:30:00Z",
  "isActive": true
}
```

**Be consistent within your API.**

### Boolean Fields

```json
// Use is_, has_, can_, should_ prefixes
{
  "is_active": true,
  "is_verified": false,
  "has_orders": true,
  "can_edit": true,
  "should_notify": false
}

// Avoid negatives
"is_active": true      // Good
"is_not_deleted": true // Bad - double negative
```

### Date/Time Fields

```json
{
  // Use _at suffix for timestamps
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z",
  "deleted_at": null,

  // Use _on suffix for dates only
  "birth_date": "1990-05-20",
  "due_on": "2024-02-01",

  // Use _until, _from for ranges
  "valid_from": "2024-01-01",
  "valid_until": "2024-12-31"
}
```

### ID Fields

```json
{
  // Primary ID
  "id": "550e8400-e29b-41d4-a716-446655440000",

  // Foreign keys - use resource_id pattern
  "user_id": "user-123",
  "order_id": "order-456",

  // External IDs
  "external_id": "EXT-789",
  "stripe_customer_id": "cus_abc123"
}
```

---

## Schema Naming (OpenAPI)

### Resource Schemas

```yaml
components:
  schemas:
    # Core resources (singular, PascalCase)
    User:
    Order:
    Product:

    # Nested/embedded objects
    Address:
    Money:

    # Request bodies
    CreateUserRequest:
    UpdateUserRequest:

    # Response wrappers (if needed)
    UserResponse:
    UserListResponse:

    # Enums
    OrderStatus:
    PaymentMethod:
```

### Avoid Redundancy

```yaml
# Bad - redundant "User" in field names
User:
  properties:
    user_id:
    user_name:
    user_email:

# Good - context is clear from schema name
User:
  properties:
    id:
    name:
    email:
```

---

## Operation IDs

### Naming Pattern

```yaml
# Pattern: {verb}{Resource}
# or: {verb}{Resource}{Qualifier}

paths:
  /users:
    get:
      operationId: listUsers
    post:
      operationId: createUser

  /users/{userId}:
    get:
      operationId: getUser
    put:
      operationId: updateUser
    delete:
      operationId: deleteUser

  /users/{userId}/orders:
    get:
      operationId: listUserOrders
    post:
      operationId: createUserOrder
```

### Common Verbs

| Action | Verb | Example |
|--------|------|---------|
| Get one | `get` | `getUser` |
| Get many | `list` | `listUsers` |
| Create | `create` | `createUser` |
| Full update | `update` or `replace` | `updateUser` |
| Partial update | `patch` | `patchUser` |
| Delete | `delete` | `deleteUser` |
| Action | Action name | `activateUser`, `cancelOrder` |
| Search | `search` | `searchUsers` |

---

## Header Naming

### Custom Headers

```yaml
# Use X- prefix (deprecated but common)
X-Request-Id: abc-123
X-API-Key: sk_live_xxx
X-RateLimit-Remaining: 95

# Or without prefix (modern)
Request-Id: abc-123
Api-Key: sk_live_xxx
RateLimit-Remaining: 95
```

### Standard Headers

```
# Use exact standard names
Authorization: Bearer xxx
Content-Type: application/json
Accept: application/json
If-Match: "etag-value"
If-None-Match: "etag-value"
```

---

## Error Codes

### Application Error Codes

```yaml
# Pattern: RESOURCE_ERROR or ERROR_DESCRIPTION
components:
  schemas:
    ErrorCode:
      type: string
      enum:
        # Validation errors
        - VALIDATION_ERROR
        - INVALID_FORMAT
        - REQUIRED_FIELD
        - MAX_LENGTH_EXCEEDED

        # Resource errors
        - USER_NOT_FOUND
        - ORDER_NOT_FOUND
        - RESOURCE_ALREADY_EXISTS

        # Business logic
        - INSUFFICIENT_BALANCE
        - ORDER_ALREADY_SHIPPED
        - PAYMENT_DECLINED

        # Auth errors
        - INVALID_CREDENTIALS
        - TOKEN_EXPIRED
        - INSUFFICIENT_PERMISSIONS
```

---

## Versioning in Names

### URL Versioning

```yaml
servers:
  - url: https://api.example.com/v1
  - url: https://api.example.com/v2
```

### Schema Versioning

```yaml
# Avoid version in schema names
User:        # Good
UserV2:      # Bad - use separate spec version

# If must coexist
UserLegacy:  # Acceptable for migration
```

---

## Abbreviations

### Acceptable Abbreviations

```
id    - identifier
url   - uniform resource locator
uri   - uniform resource identifier
api   - application programming interface
http  - hypertext transfer protocol
ip    - internet protocol
sku   - stock keeping unit
```

### Avoid Unclear Abbreviations

```yaml
# Bad
usr_nm, ord_cnt, prod_desc

# Good
user_name, order_count, product_description
```
