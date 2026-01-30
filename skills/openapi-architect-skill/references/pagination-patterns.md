# Pagination Patterns

## Comparison of Approaches

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Cursor-based** | Consistent, performant, handles real-time | No random access, opaque cursors | Large datasets, real-time data |
| **Offset-based** | Simple, random access | Inconsistent on changes, slow for large offsets | Small datasets, admin UIs |
| **Keyset** | Performant, consistent | Requires sortable unique key | Time-series, logs |
| **Page-based** | User-friendly | Same issues as offset | Simple UIs |

---

## Cursor-Based Pagination (Recommended)

### Implementation

```yaml
paths:
  /orders:
    get:
      summary: List orders
      parameters:
        - name: cursor
          in: query
          schema:
            type: string
          description: Opaque cursor from previous response
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: direction
          in: query
          schema:
            type: string
            enum: [forward, backward]
            default: forward
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'

components:
  schemas:
    OrderListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Order'
        pagination:
          $ref: '#/components/schemas/CursorPagination'

    CursorPagination:
      type: object
      properties:
        next_cursor:
          type: string
          nullable: true
          description: Cursor for next page, null if no more
          example: eyJpZCI6MTIzNH0
        prev_cursor:
          type: string
          nullable: true
          description: Cursor for previous page
        has_more:
          type: boolean
          description: Whether more results exist
```

### Response Example

```json
{
  "data": [
    {"id": "order-1", "amount": 100},
    {"id": "order-2", "amount": 200}
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6Im9yZGVyLTIiLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0xNSJ9",
    "prev_cursor": null,
    "has_more": true
  }
}
```

### Cursor Encoding

Encode cursor data as base64 JSON:
```json
// Decoded cursor
{
  "id": "order-2",
  "created_at": "2024-01-15T10:30:00Z"
}
// Encoded: eyJpZCI6Im9yZGVyLTIiLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0xNVQxMDozMDowMFoifQ
```

---

## Offset-Based Pagination

### Implementation

```yaml
paths:
  /users:
    get:
      parameters:
        - name: offset
          in: query
          schema:
            type: integer
            minimum: 0
            default: 0
          description: Number of items to skip
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        200:
          headers:
            X-Total-Count:
              schema:
                type: integer
              description: Total number of items
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'

components:
  schemas:
    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          type: object
          properties:
            total:
              type: integer
              example: 1000
            offset:
              type: integer
              example: 20
            limit:
              type: integer
              example: 20
```

### Page-Based Variant

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

# Response
{
  "data": [...],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total_pages": 50,
    "total_count": 1000
  }
}
```

---

## Keyset Pagination

### Best for Time-Series Data

```yaml
paths:
  /events:
    get:
      parameters:
        - name: after
          in: query
          schema:
            type: string
            format: date-time
          description: Return events after this timestamp
        - name: after_id
          in: query
          schema:
            type: string
          description: Tiebreaker for same timestamp
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
```

### Query Pattern
```sql
SELECT * FROM events
WHERE (created_at, id) > (:after, :after_id)
ORDER BY created_at ASC, id ASC
LIMIT :limit + 1  -- Fetch one extra to detect has_more
```

---

## Link Headers (RFC 8288)

### Include with Any Pagination Style

```yaml
responses:
  200:
    headers:
      Link:
        schema:
          type: string
        description: RFC 8288 pagination links
        example: |
          <https://api.example.com/orders?cursor=abc>; rel="next",
          <https://api.example.com/orders>; rel="first"
```

### Generating Links

```
Link: <https://api.example.com/orders?cursor=xyz>; rel="next",
      <https://api.example.com/orders?cursor=abc>; rel="prev",
      <https://api.example.com/orders>; rel="first"
```

---

## Filtering with Pagination

### Combine Parameters

```yaml
paths:
  /orders:
    get:
      parameters:
        # Pagination
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
        # Filters
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, shipped, delivered]
        - name: created_after
          in: query
          schema:
            type: string
            format: date-time
        - name: customer_id
          in: query
          schema:
            type: string
            format: uuid
```

### Filter in Cursor

Include filters in cursor to maintain consistency:
```json
{
  "id": "order-123",
  "filters": {
    "status": "pending",
    "customer_id": "cust-456"
  }
}
```

---

## Sorting with Pagination

### Cursor Must Include Sort Fields

```yaml
parameters:
  - name: sort
    in: query
    schema:
      type: string
      enum:
        - created_at
        - -created_at
        - amount
        - -amount
    default: -created_at
    description: Sort field (prefix - for descending)
```

### Cursor Contains Sort Context

```json
{
  "id": "order-123",
  "sort": {
    "field": "amount",
    "direction": "desc",
    "value": 150.00
  }
}
```

---

## Performance Considerations

### Offset Pagination Issues

```sql
-- This gets slower as offset increases
SELECT * FROM orders
ORDER BY created_at
OFFSET 100000 LIMIT 20;  -- Must scan 100,020 rows!
```

### Cursor Pagination Solution

```sql
-- Constant performance regardless of position
SELECT * FROM orders
WHERE created_at < :cursor_created_at
ORDER BY created_at DESC
LIMIT 20;  -- Uses index, scans only 20 rows
```

### Index Requirements

```sql
-- For cursor pagination by created_at
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- For keyset pagination with tiebreaker
CREATE INDEX idx_orders_created_id ON orders(created_at DESC, id DESC);
```

---

## Infinite Scroll / Load More

### Response Format

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "abc123",
    "has_more": true
  }
}
```

### Client Implementation

```javascript
// Initial load
GET /items?limit=20

// Load more
GET /items?cursor={next_cursor}&limit=20

// Continue until has_more: false
```

---

## Total Count Considerations

### When to Include

- **Include:** Admin UIs, dashboards, small datasets
- **Avoid:** Large datasets (COUNT is expensive)

### Alternatives to Exact Count

```json
{
  "meta": {
    "has_more": true,
    "estimated_total": 10000  // Approximate
  }
}
```

### Separate Endpoint for Count

```yaml
paths:
  /orders:
    get:
      # Returns paginated data, no count

  /orders/count:
    get:
      summary: Get order count (expensive)
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  count:
                    type: integer
```
