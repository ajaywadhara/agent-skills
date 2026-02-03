# Code Smells Reference

## Method-Level Smells

### Long Method (>20 lines)
```java
// ❌ SMELL: Method doing too much
public OrderResult processOrder(Order order) {
    // Validate order (10 lines)
    if (order.getItems() == null || order.getItems().isEmpty()) {
        throw new InvalidOrderException("No items");
    }
    // ... more validation
    
    // Calculate totals (15 lines)
    BigDecimal subtotal = BigDecimal.ZERO;
    for (OrderItem item : order.getItems()) {
        // ... calculation logic
    }
    
    // Apply discounts (20 lines)
    // ...
    
    // Process payment (15 lines)
    // ...
    
    // Send notifications (10 lines)
    // ...
    
    return result;
}

// ✅ REFACTOR: Extract methods
public OrderResult processOrder(Order order) {
    validateOrder(order);
    BigDecimal total = calculateTotal(order);
    BigDecimal finalPrice = applyDiscounts(order, total);
    PaymentResult payment = processPayment(order, finalPrice);
    sendNotifications(order, payment);
    return buildResult(order, payment);
}
```

---

### Too Many Parameters (>4)
```java
// ❌ SMELL: Too many parameters
public User createUser(String firstName, String lastName, String email, 
                       String phone, String address, String city, 
                       String state, String zip, String country) {
    // ...
}

// ✅ REFACTOR: Use parameter object
public User createUser(CreateUserRequest request) {
    // ...
}

@Builder
public class CreateUserRequest {
    private String firstName;
    private String lastName;
    private String email;
    private ContactInfo contactInfo;
    private Address address;
}
```

---

### Feature Envy
```java
// ❌ SMELL: Method uses another object's data excessively
public class OrderPrinter {
    public String formatOrder(Order order) {
        return String.format("Order #%d: %s - %d items - $%.2f - %s",
            order.getId(),
            order.getCustomer().getName(),
            order.getItems().size(),
            order.getItems().stream()
                .mapToDouble(i -> i.getPrice() * i.getQuantity())
                .sum(),
            order.getStatus());
    }
}

// ✅ REFACTOR: Move method to the class it envies
public class Order {
    public String format() {
        return String.format("Order #%d: %s - %d items - $%.2f - %s",
            id, customer.getName(), items.size(), calculateTotal(), status);
    }
    
    public BigDecimal calculateTotal() {
        return items.stream()
            .map(OrderItem::getLineTotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

---

### Boolean Blindness
```java
// ❌ SMELL: What does true/false mean?
orderService.process(order, true, false, true);

// ✅ REFACTOR: Use enums or builder
orderService.process(order, ProcessingOptions.builder()
    .priority(Priority.HIGH)
    .sendNotification(false)
    .validateInventory(true)
    .build());
```

---

## Class-Level Smells

### God Class
```java
// ❌ SMELL: Class does everything
public class OrderManager {
    public Order createOrder() { }
    public void validateOrder() { }
    public void calculateTax() { }
    public void applyDiscount() { }
    public void processPayment() { }
    public void updateInventory() { }
    public void sendConfirmationEmail() { }
    public void sendSMS() { }
    public void generateInvoice() { }
    public void generateReport() { }
    public void exportToExcel() { }
    // ... 50+ more methods
}

// ✅ REFACTOR: Single Responsibility
public class OrderService { }
public class OrderValidator { }
public class PricingService { }
public class PaymentService { }
public class InventoryService { }
public class NotificationService { }
public class InvoiceGenerator { }
public class ReportGenerator { }
```

---

### Data Class (Anemic Domain Model)
```java
// ❌ SMELL: Only getters/setters, no behavior
public class Order {
    private Long id;
    private List<OrderItem> items;
    private OrderStatus status;
    private BigDecimal total;
    
    // Only getters and setters...
}

// Business logic scattered in services
public class OrderService {
    public void addItem(Order order, Product product, int quantity) { }
    public BigDecimal calculateTotal(Order order) { }
    public boolean canCancel(Order order) { }
}

// ✅ REFACTOR: Rich domain model
public class Order {
    private Long id;
    private List<OrderItem> items;
    private OrderStatus status;
    
    public void addItem(Product product, int quantity) {
        validateCanModify();
        items.add(new OrderItem(product, quantity));
    }
    
    public BigDecimal calculateTotal() {
        return items.stream()
            .map(OrderItem::getLineTotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    public boolean canCancel() {
        return status == OrderStatus.PENDING || status == OrderStatus.CONFIRMED;
    }
    
    public void cancel() {
        if (!canCancel()) {
            throw new IllegalStateException("Cannot cancel order in status: " + status);
        }
        this.status = OrderStatus.CANCELLED;
    }
}
```

---

### Inappropriate Intimacy
```java
// ❌ SMELL: Classes know too much about each other
public class Order {
    private Customer customer;
    
    public String getCustomerFullAddress() {
        return customer.getStreet() + ", " + 
               customer.getCity() + ", " + 
               customer.getState() + " " + 
               customer.getZipCode();
    }
}

// ✅ REFACTOR: Ask, don't tell
public class Customer {
    public String getFullAddress() {
        return address.format();
    }
}

public class Order {
    public String getShippingAddress() {
        return customer.getFullAddress();
    }
}
```

---

### Refused Bequest
```java
// ❌ SMELL: Subclass doesn't use inherited behavior
public class Bird {
    public void fly() { }
    public void eat() { }
    public void sleep() { }
}

public class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
    }
}

// ✅ REFACTOR: Use composition or interface segregation
public interface Eater { void eat(); }
public interface Sleeper { void sleep(); }
public interface Flyer { void fly(); }

public class Penguin implements Eater, Sleeper {
    // No fly method!
}
```

---

## Architecture Smells

### Circular Dependencies
```java
// ❌ SMELL: A depends on B, B depends on A
@Service
public class OrderService {
    @Autowired
    private CustomerService customerService;
}

@Service
public class CustomerService {
    @Autowired
    private OrderService orderService;  // Circular!
}

// ✅ REFACTOR: Extract common functionality
@Service
public class OrderService {
    @Autowired
    private CustomerQueryService customerQueryService;
}

@Service
public class CustomerService {
    @Autowired
    private OrderQueryService orderQueryService;
}

// Or use events
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher events;
    
    public void completeOrder(Order order) {
        // ...
        events.publishEvent(new OrderCompletedEvent(order));
    }
}
```

---

### Layer Violation
```java
// ❌ SMELL: Controller directly accesses repository
@RestController
public class OrderController {
    @Autowired
    private OrderRepository orderRepository;  // Skip service layer!
    
    @GetMapping("/orders/{id}")
    public Order getOrder(@PathVariable Long id) {
        return orderRepository.findById(id).orElseThrow();
    }
}

// ✅ REFACTOR: Proper layering
@RestController
public class OrderController {
    @Autowired
    private OrderService orderService;
    
    @GetMapping("/orders/{id}")
    public OrderDTO getOrder(@PathVariable Long id) {
        return orderService.findById(id);
    }
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    
    public OrderDTO findById(Long id) {
        return orderRepository.findById(id)
            .map(OrderDTO::from)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }
}
```

---

### Hardcoded Dependencies
```java
// ❌ SMELL: Hardcoded implementation
public class OrderService {
    private PaymentProcessor processor = new StripePaymentProcessor();
    
    public void processPayment(Order order) {
        processor.charge(order.getTotal());
    }
}

// ✅ REFACTOR: Dependency injection
public class OrderService {
    private final PaymentProcessor processor;
    
    public OrderService(PaymentProcessor processor) {
        this.processor = processor;
    }
}
```

---

## Naming Smells

### Vague Names
```java
// ❌ SMELL: Meaningless names
public class DataManager {
    public Object process(Object data) { }
    public void handle(Object item) { }
    public Object get(String id) { }
}

int temp, temp2;
String str;
Object obj;

// ✅ REFACTOR: Meaningful names
public class OrderProcessor {
    public ProcessedOrder process(RawOrder order) { }
}

int retryCount, maxAttempts;
String customerEmail;
Order pendingOrder;
```

---

### Inconsistent Naming
```java
// ❌ SMELL: Inconsistent conventions
public class UserService {
    public User getUser(Long id) { }
    public User fetchUserById(Long userId) { }
    public User retrieveUserByIdentifier(Long identifier) { }
    public User findByUserId(Long user_id) { }
}

// ✅ REFACTOR: Consistent pattern
public class UserService {
    public User findById(Long id) { }
    public Optional<User> findByEmail(String email) { }
    public List<User> findByStatus(UserStatus status) { }
    public List<User> findAll() { }
}
```

---

## Variable Declaration Style

### Use `final var` for Local Variables

**Principle:** Use `final var` for local variables to:
1. Enforce immutability (prevents reassignment)
2. Reduce visual clutter (type inference)
3. Force descriptive variable names (since type isn't visible)

```java
// ❌ SMELL: Explicit type with final - redundant and verbose
final HttpStatus status = HttpStatus.OK;
final String message = "Success";
final List<User> users = userRepository.findAll();
final Optional<Order> order = orderRepository.findById(id);
final UserResponseDTO response = mapper.toDTO(user);

// ✅ BETTER: Use final var with descriptive names
final var httpStatus = HttpStatus.OK;
final var successMessage = "Success";
final var activeUsers = userRepository.findAll();
final var existingOrder = orderRepository.findById(id);
final var userResponse = mapper.toDTO(user);
```

### Variable Naming with `var`

Since `var` hides the type, variable names must be more descriptive:

```java
// ❌ BAD: Vague names become worse with var
final var s = HttpStatus.OK;           // What is 's'?
final var list = findAll();            // List of what?
final var result = process(order);     // What kind of result?
final var dto = convert(user);         // DTO for what?

// ✅ GOOD: Descriptive names compensate for hidden type
final var responseStatus = HttpStatus.OK;
final var pendingOrders = orderRepository.findByStatus(PENDING);
final var paymentResult = paymentService.process(order);
final var userProfileDto = userMapper.toProfileDto(user);
```

### When NOT to Use `var`

```java
// ❌ Don't use var when type isn't obvious from context
final var value = getValue();           // Type unclear
final var data = parse(input);          // What type is data?
final var x = calculate();              // Completely opaque

// ✅ Use explicit type when it aids readability
final BigDecimal calculatedTax = taxService.calculate(order);
final CompletableFuture<Result> asyncResult = executeAsync();
final Map<String, List<OrderItem>> groupedItems = groupByCategory(items);
```

### `final var` Patterns by Context

**Method Return Values:**
```java
// ✅ GOOD
final var savedOrder = orderRepository.save(order);
final var validationErrors = validator.validate(request);
final var accessToken = authService.generateToken(user);
```

**Stream Operations:**
```java
// ✅ GOOD
final var totalAmount = orders.stream()
    .map(Order::getAmount)
    .reduce(BigDecimal.ZERO, BigDecimal::add);

final var activeUserEmails = users.stream()
    .filter(User::isActive)
    .map(User::getEmail)
    .collect(Collectors.toList());
```

**Object Creation:**
```java
// ✅ GOOD - Type is clear from constructor/builder
final var newOrder = new Order(customer, items);
final var orderRequest = OrderRequest.builder()
    .customerId(customerId)
    .items(items)
    .build();
```

**Loop Variables:**
```java
// ✅ GOOD
for (final var order : orders) {
    processOrder(order);
}

// ✅ GOOD - Entry iteration
for (final var entry : orderMap.entrySet()) {
    log.info("Order {}: {}", entry.getKey(), entry.getValue());
}
```

### Why `final` Matters

```java
// ❌ BAD: Mutable local variable - can be reassigned accidentally
var status = HttpStatus.OK;
// ... 50 lines later ...
status = HttpStatus.CREATED;  // Was this intentional?

// ✅ GOOD: Immutable - compiler prevents reassignment
final var status = HttpStatus.OK;
// ... 50 lines later ...
status = HttpStatus.CREATED;  // ❌ Compile error!
```

### Summary Table

| Context | Recommendation | Example |
|---------|---------------|---------|
| Method return values | `final var` + descriptive name | `final var savedUser = repo.save(user)` |
| Object instantiation | `final var` (type obvious) | `final var config = new Config()` |
| Builder results | `final var` | `final var request = Request.builder()...build()` |
| Stream results | `final var` + descriptive name | `final var activeCount = stream.filter(...).count()` |
| Primitives/Strings | `final var` OK if name is clear | `final var maxRetries = 3` |
| Complex generics | Consider explicit type | `final Map<K, List<V>> grouped = ...` |
| Unclear context | Use explicit type | `final BigDecimal tax = calculate()` |

---

## Code Quality Metrics

### Cyclomatic Complexity

| Score | Risk Level | Action |
|-------|------------|--------|
| 1-10 | Low | Acceptable |
| 11-20 | Moderate | Consider refactoring |
| 21-50 | High | Must refactor |
| 50+ | Very High | Critical - split immediately |

```java
// Complexity 12 - each decision point adds 1
public void process(Order order) {
    if (order == null) return;                    // +1
    if (order.getItems().isEmpty()) return;       // +1
    
    for (OrderItem item : order.getItems()) {     // +1
        if (item.getQuantity() <= 0) continue;    // +1
        
        switch (item.getType()) {                 // +3 (3 cases)
            case PHYSICAL: 
                if (item.requiresShipping()) { }  // +1
                break;
            case DIGITAL: 
                if (item.hasDownloadLimit()) { }  // +1
                break;
            case SERVICE:
                break;
        }
    }
    
    if (order.hasDiscount() && order.isValidDiscount()) {  // +2
        applyDiscount(order);
    }
}
```

---

### Lines of Code Guidelines

| Element | Recommended Max |
|---------|----------------|
| Method | 20-30 lines |
| Class | 200-300 lines |
| File | 500 lines |
| Package | 15-20 classes |

---

## Detection Summary

| Smell | Detection Signal |
|-------|-----------------|
| Long Method | >20 lines, multiple comments, nested conditions |
| God Class | >10 dependencies, >20 methods, mixed responsibilities |
| Feature Envy | Excessive use of other object's getters |
| Data Class | Only getters/setters, no business logic |
| Circular Dependency | Bidirectional @Autowired |
| Layer Violation | Controller → Repository direct access |
| Boolean Blindness | Methods with multiple boolean parameters |
| Vague Names | data, manager, handler, processor without context |
| Verbose Type Declaration | `final HttpStatus status` instead of `final var httpStatus` |
| Mutable Local Variables | Non-final local variables that could be final |
