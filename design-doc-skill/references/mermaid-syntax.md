# Mermaid Diagram Syntax Reference

Complete syntax reference for all diagram types used in design documents. Load this file when you need exact syntax for constructing diagrams.

---

## 1. Flowchart

Use for: pipelines, decision trees, process flows, deployment steps.

### Directions

| Direction | Keyword |
|-----------|---------|
| Top to Bottom | `flowchart TD` or `flowchart TB` |
| Left to Right | `flowchart LR` |
| Bottom to Top | `flowchart BT` |
| Right to Left | `flowchart RL` |

### Node Shapes

```mermaid
flowchart TD
    A[Rectangle]           %% Standard process
    B(Rounded)             %% Start/end
    C([Stadium])           %% Terminal
    D[[Subroutine]]        %% Subroutine/subprocess
    E[(Database)]          %% Cylinder — database/storage
    F((Circle))            %% Connector/junction
    G{Diamond}             %% Decision
    H{{Hexagon}}           %% Preparation step
```

### Arrow Types

```mermaid
flowchart LR
    A --> B                %% Solid arrow
    C --- D                %% Solid line (no arrow)
    E -.-> F               %% Dotted arrow
    G ==> H                %% Thick arrow
    I -- "label" --> J     %% Labeled arrow
    K -. "label" .-> L     %% Labeled dotted arrow
```

### Subgraphs

```mermaid
flowchart TD
    subgraph Backend["Backend Services"]
        A[API Gateway] --> B[Auth Service]
        A --> C[Core Service]
    end
    subgraph Data["Data Layer"]
        D[(PostgreSQL)]
        E[(Redis)]
    end
    C --> D
    C --> E
```

### Styling

```mermaid
flowchart TD
    A[Service]:::primary --> B[(DB)]:::secondary
    classDef primary fill:#2374ab,stroke:#1a5276,color:#fff
    classDef secondary fill:#57a773,stroke:#3d7a54,color:#fff
    classDef accent fill:#ff8c42,stroke:#cc6f35,color:#fff
    classDef error fill:#d64045,stroke:#a33033,color:#fff
```

---

## 2. Sequence Diagram

Use for: API flows, user journeys, service interactions, authentication flows.

### Participants and Arrow Types

| Arrow | Meaning |
|-------|---------|
| `->>`  | Solid with arrowhead (synchronous request) |
| `-->>`  | Dashed with arrowhead (asynchronous/response) |
| `->`   | Solid without arrowhead |
| `-->`  | Dashed without arrowhead |
| `-x`   | Solid with cross (failed/rejected) |
| `--x`  | Dashed with cross |

### Complete Example (All Control Blocks)

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant S as Server
    participant DB as Database

    C ->> +S: POST /orders
    alt Valid Request
        S ->> DB: INSERT order
        DB -->> S: order_id
        S -->> -C: 201 Created
    else Invalid Request
        S -->> C: 400 Bad Request
    end

    opt Send Notification
        S ->> S: Queue email
    end

    loop Retry up to 3 times
        S ->> DB: Check status
    end

    par Parallel Operations
        S ->> DB: Update inventory
    and
        S ->> DB: Log audit event
    end

    Note over C,S: Connection established via TLS
    Note right of DB: Read replica used for queries
```

Key features: `autonumber` adds step numbers, `+`/`-` on participants controls activation lifelines, `alt/else/end` for branching, `opt` for optional, `loop` for repetition, `par/and` for parallel, `Note over/right of` for annotations.

---

## 3. Entity Relationship Diagram (ERD)

Use for: data models, database schemas, domain models.

### Relationship Types

| Syntax | Meaning |
|--------|---------|
| `\|\|--\|\|` | One to one |
| `\|\|--o{` | One to zero or more |
| `\|\|--\|{` | One to one or more |
| `o\|--o{` | Zero or one to zero or more |

### Example

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        uuid id PK
        string email UK
        string name
        timestamp created_at
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        uuid id PK
        uuid user_id FK
        enum status
        decimal total
    }
    ORDER_ITEM }|--|| PRODUCT : references
    ORDER_ITEM {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal unit_price
    }
    PRODUCT {
        uuid id PK
        string name
        decimal price
        int stock
    }
```

### Field Annotations

| Annotation | Meaning |
|------------|---------|
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |

Supported types: `string`, `int`, `uuid`, `decimal`, `boolean`, `timestamp`, `date`, `text`, `enum`, `json`

---

## 4. C4 Diagrams

Use for: system architecture at different zoom levels.

### C4 Context Diagram

Shows the system in its environment — people and external systems.

```mermaid
C4Context
    title System Context — Order Management
    Person(customer, "Customer", "Places and tracks orders")
    Person(admin, "Admin", "Manages products and orders")
    System(oms, "Order Management System", "Handles order lifecycle")
    System_Ext(payment, "Payment Gateway", "Processes payments")
    System_Ext(shipping, "Shipping Provider", "Handles delivery")
    Rel(customer, oms, "Places orders", "HTTPS")
    Rel(admin, oms, "Manages", "HTTPS")
    Rel(oms, payment, "Processes payments", "REST")
    Rel(oms, shipping, "Creates shipments", "REST")
```

### C4 Container Diagram

Shows the deployable units within the system boundary.

```mermaid
C4Container
    title Container Diagram — Order Management
    Person(customer, "Customer", "End user")
    System_Boundary(oms, "Order Management System") {
        Container(web, "Web App", "React", "Customer-facing SPA")
        Container(api, "API Service", "Spring Boot", "Core business logic")
        Container(worker, "Worker", "Spring Boot", "Async job processing")
        ContainerDb(db, "Database", "PostgreSQL", "Persistent storage")
        ContainerQueue(queue, "Message Queue", "RabbitMQ", "Event bus")
    }
    System_Ext(payment, "Payment Gateway", "Stripe")
    Rel(customer, web, "Uses", "HTTPS")
    Rel(web, api, "Calls", "REST/JSON")
    Rel(api, db, "Reads/writes", "JDBC")
    Rel(api, queue, "Publishes events", "AMQP")
    Rel(worker, queue, "Consumes events", "AMQP")
    Rel(api, payment, "Charges", "REST")
```

### C4 Elements Reference

| Element | Usage |
|---------|-------|
| `Person(alias, label, desc)` | Human actor |
| `System(alias, label, desc)` | Your system |
| `System_Ext(alias, label, desc)` | External system |
| `System_Boundary(alias, label)` | System boundary |
| `Container(alias, label, tech, desc)` | Deployable unit |
| `ContainerDb(alias, label, tech, desc)` | Database container |
| `ContainerQueue(alias, label, tech, desc)` | Message queue container |
| `Container_Boundary(alias, label)` | Container boundary |
| `Component(alias, label, tech, desc)` | Internal component |
| `Rel(from, to, label, tech)` | Relationship |

Use `C4Component` with `Container_Boundary` and `Component()` for component-level diagrams inside a container.

---

## 5. State Diagram

Use for: order lifecycles, workflow states, session management, entity status tracking.

### Basic Syntax

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted : submit()
    Submitted --> UnderReview : assign_reviewer()
    UnderReview --> Approved : approve()
    UnderReview --> Rejected : reject()
    Rejected --> Draft : revise()
    Approved --> Published : publish()
    Published --> [*]
```

### Advanced Features

```mermaid
stateDiagram-v2
    [*] --> Active
    state Active {
        [*] --> Idle
        Idle --> Processing : new_request
        Processing --> Idle : complete
        Processing --> Error : failure
        Error --> Idle : retry
    }
    Active --> Suspended : suspend()
    Suspended --> Active : resume()
    Active --> [*] : terminate()

    state check <<choice>>
    Processing --> check : evaluate
    check --> Approved : if valid
    check --> Rejected : if invalid

    note right of Active
        Composite state with
        internal transitions.
    end note
```

Key features: `[*]` for start/end, `state Name { }` for composite states, `<<choice>>` for conditional branching, `<<fork>>`/`<<join>>` for parallel states, `note right of` for annotations, `state "Long Name" as Alias` for aliasing.

---

## 6. Class Diagram

Use for: domain models, service interfaces, DTO structures, component contracts.

### Syntax and Visibility

| Symbol | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

### Relationships

| Syntax | Meaning |
|--------|---------|
| `A <\|-- B` | B inherits from A |
| `A *-- B` | A composed of B (strong ownership) |
| `A o-- B` | A aggregates B (weak ownership) |
| `A --> B` | A uses/depends on B |
| `A ..\|> B` | A implements B |
| `A ..> B` | A depends on B (dashed) |

### Example

```mermaid
classDiagram
    class OrderRepository {
        <<interface>>
        +findById(id) Optional~Order~
        +save(order) Order
    }
    class JpaOrderRepository {
        +findById(id) Optional~Order~
        +save(order) Order
    }
    class Order {
        -UUID id
        -OrderStatus status
        -BigDecimal total
        +submit() void
        +cancel() void
    }
    class OrderItem {
        -UUID id
        -int quantity
        -BigDecimal unitPrice
        +subtotal() BigDecimal
    }
    OrderRepository <|.. JpaOrderRepository
    Order "1" --> "*" OrderItem : contains
```

Annotations: `<<interface>>`, `<<abstract>>`, `<<service>>`, `<<enumeration>>`. Generics: `class ApiResponse~T~`.

---

## 7. Styling Reference

### Themes

```
%%{init: {'theme': 'default'}}%%
```

Available: `default`, `dark`, `forest`, `neutral`, `base`

### Color Palette

| Role | classDef |
|------|----------|
| Primary | `fill:#2374ab,stroke:#1a5276,color:#fff` |
| Secondary | `fill:#57a773,stroke:#3d7a54,color:#fff` |
| Accent | `fill:#ff8c42,stroke:#cc6f35,color:#fff` |
| Error | `fill:#d64045,stroke:#a33033,color:#fff` |
| Neutral | `fill:#e8e8e8,stroke:#bbb,color:#333` |

Apply with: `A[Node]:::primary` and `classDef primary fill:#2374ab,stroke:#1a5276,color:#fff`

### Subgraph Styling

```mermaid
flowchart TD
    subgraph Backend["Backend Services"]
        style Backend fill:#f0f4f8,stroke:#2374ab,stroke-width:2px
        A[API] --> B[Worker]
    end
```

### Tips for Clean Diagrams

1. **Limit nodes** — Keep under 12-15 nodes per diagram. Split if larger.
2. **Consistent direction** — `TD` for hierarchical, `LR` for process flows.
3. **Label all arrows** — Unlabeled arrows are ambiguous.
4. **Use subgraphs** — Group related nodes to reduce visual clutter.
5. **Short labels** — 2-4 words on nodes. Detail in surrounding text.
