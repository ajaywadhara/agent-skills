# Java/Spring Boot Bug Patterns Reference

## Null Safety Bugs

### 1. Optional Misuse
```java
// ❌ BUG: Optional.get() without check
User user = userRepository.findById(id).get(); // NoSuchElementException

// ✅ FIX
User user = userRepository.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));
```

### 2. Chained Null Dereference
```java
// ❌ BUG: Any element in chain can be null
String city = user.getAddress().getCity().toUpperCase();

// ✅ FIX
String city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .map(String::toUpperCase)
    .orElse("UNKNOWN");
```

### 3. Collection Null vs Empty
```java
// ❌ BUG: Returns null instead of empty collection
public List<Order> findOrders(Long userId) {
    List<Order> orders = repository.findByUserId(userId);
    if (orders.isEmpty()) return null;  // Don't return null!
    return orders;
}

// ✅ FIX
public List<Order> findOrders(Long userId) {
    return repository.findByUserId(userId); // Return empty list, not null
}
```

### 4. Primitive Wrapper Unboxing
```java
// ❌ BUG: NullPointerException on unboxing
public void process(Integer count) {
    int value = count; // NPE if count is null
    for (int i = 0; i < value; i++) { }
}

// ✅ FIX
public void process(Integer count) {
    int value = count != null ? count : 0;
    for (int i = 0; i < value; i++) { }
}
```

---

## Resource Management Bugs

### 5. Unclosed Stream
```java
// ❌ BUG: Stream resource leak
public long countLines(Path path) throws IOException {
    return Files.lines(path).count(); // Stream never closed!
}

// ✅ FIX
public long countLines(Path path) throws IOException {
    try (Stream<String> lines = Files.lines(path)) {
        return lines.count();
    }
}
```

### 6. Connection Leak
```java
// ❌ BUG: Connection not returned to pool
public User findUser(Long id) {
    Connection conn = dataSource.getConnection();
    // If exception occurs here, connection leaks
    PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
    // ...
}

// ✅ FIX
public User findUser(Long id) {
    try (Connection conn = dataSource.getConnection();
         PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?")) {
        ps.setLong(1, id);
        // ...
    }
}
```

### 7. EntityManager Leak
```java
// ❌ BUG: EntityManager not closed in non-managed context
public void processInBackground() {
    EntityManager em = entityManagerFactory.createEntityManager();
    em.getTransaction().begin();
    // If exception, transaction and EM leak
}

// ✅ FIX
public void processInBackground() {
    EntityManager em = entityManagerFactory.createEntityManager();
    try {
        em.getTransaction().begin();
        // work
        em.getTransaction().commit();
    } catch (Exception e) {
        em.getTransaction().rollback();
        throw e;
    } finally {
        em.close();
    }
}
```

---

## Concurrency Bugs

### 8. Check-Then-Act Race Condition
```java
// ❌ BUG: Race condition
public void createIfNotExists(String key, Object value) {
    if (!map.containsKey(key)) {     // Thread A: true
        map.put(key, value);          // Thread B already put different value
    }
}

// ✅ FIX
public void createIfNotExists(String key, Object value) {
    map.computeIfAbsent(key, k -> value);
}
```

### 9. Non-Atomic Compound Operation
```java
// ❌ BUG: counter++ is not atomic
private int counter = 0;
public void increment() {
    counter++; // Read-modify-write: not thread-safe
}

// ✅ FIX
private AtomicInteger counter = new AtomicInteger(0);
public void increment() {
    counter.incrementAndGet();
}
```

### 10. Double-Checked Locking Without Volatile
```java
// ❌ BUG: Instance may be partially constructed
private static Singleton instance;
public static Singleton getInstance() {
    if (instance == null) {
        synchronized (Singleton.class) {
            if (instance == null) {
                instance = new Singleton(); // May be visible before fully constructed
            }
        }
    }
    return instance;
}

// ✅ FIX
private static volatile Singleton instance;
// Or use holder pattern
private static class Holder {
    static final Singleton INSTANCE = new Singleton();
}
public static Singleton getInstance() {
    return Holder.INSTANCE;
}
```

### 11. Unsynchronized Lazy Initialization
```java
// ❌ BUG: Multiple threads may initialize
private List<String> cache;
public List<String> getCache() {
    if (cache == null) {
        cache = loadFromDatabase(); // Called multiple times
    }
    return cache;
}

// ✅ FIX
private volatile List<String> cache;
public List<String> getCache() {
    List<String> result = cache;
    if (result == null) {
        synchronized (this) {
            result = cache;
            if (result == null) {
                cache = result = loadFromDatabase();
            }
        }
    }
    return result;
}
```

---

## Spring-Specific Bugs

### 12. Missing @Transactional
```java
// ❌ BUG: No transaction, each call is separate
public void transferMoney(Long from, Long to, BigDecimal amount) {
    accountRepository.debit(from, amount);  // Commits
    accountRepository.credit(to, amount);   // If fails, debit not rolled back!
}

// ✅ FIX
@Transactional
public void transferMoney(Long from, Long to, BigDecimal amount) {
    accountRepository.debit(from, amount);
    accountRepository.credit(to, amount);
}
```

### 13. @Transactional on Private Method
```java
// ❌ BUG: @Transactional ignored on private methods
@Transactional
private void saveData(Data data) {  // Won't work - AOP can't proxy private
    repository.save(data);
}

// ✅ FIX
@Transactional
public void saveData(Data data) {
    repository.save(data);
}
```

### 14. Self-Invocation Bypasses Proxy
```java
// ❌ BUG: Transaction not applied
@Service
public class OrderService {
    public void processOrder(Order order) {
        validate(order);
        saveOrder(order); // Direct call bypasses proxy!
    }
    
    @Transactional
    public void saveOrder(Order order) {
        repository.save(order);
    }
}

// ✅ FIX: Inject self or extract to separate service
@Service
public class OrderService {
    @Autowired
    private OrderService self; // Proxy-aware self reference
    
    public void processOrder(Order order) {
        validate(order);
        self.saveOrder(order); // Goes through proxy
    }
}
```

### 15. @Async Without @EnableAsync
```java
// ❌ BUG: Runs synchronously
@Service
public class EmailService {
    @Async
    public void sendEmail(String to, String body) {
        // Runs synchronously if @EnableAsync missing!
    }
}

// ✅ FIX: Add to configuration
@Configuration
@EnableAsync
public class AsyncConfig { }
```

### 16. Returning Entity from Controller
```java
// ❌ BUG: Exposes internal structure, lazy loading issues
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
    // May expose password, lazy loading outside transaction
}

// ✅ FIX: Use DTO
@GetMapping("/users/{id}")
public UserDTO getUser(@PathVariable Long id) {
    User user = userRepository.findById(id).orElseThrow();
    return new UserDTO(user.getId(), user.getName(), user.getEmail());
}
```

---

## Exception Handling Bugs

### 17. Swallowing Exceptions
```java
// ❌ BUG: Exception swallowed, failure hidden
public void processFile(Path path) {
    try {
        Files.readAllLines(path);
    } catch (IOException e) {
        // Silent failure - bug goes unnoticed
    }
}

// ✅ FIX
public void processFile(Path path) {
    try {
        Files.readAllLines(path);
    } catch (IOException e) {
        log.error("Failed to process file: {}", path, e);
        throw new ProcessingException("File processing failed", e);
    }
}
```

### 18. Catching Generic Exception
```java
// ❌ BUG: Catches everything including programming errors
try {
    processOrder(order);
} catch (Exception e) {  // Catches NullPointerException, etc.
    return defaultOrder();
}

// ✅ FIX: Catch specific exceptions
try {
    processOrder(order);
} catch (OrderValidationException | PaymentException e) {
    log.warn("Order processing failed: {}", e.getMessage());
    return defaultOrder();
}
```

### 19. Exception in Finally
```java
// ❌ BUG: Finally exception masks original
try {
    processData();
} finally {
    closeConnection(); // If this throws, original exception lost
}

// ✅ FIX
try {
    processData();
} finally {
    try {
        closeConnection();
    } catch (Exception e) {
        log.warn("Failed to close connection", e);
    }
}
```

---

## Collection Bugs

### 20. ConcurrentModificationException
```java
// ❌ BUG: Modifying while iterating
for (User user : users) {
    if (user.isInactive()) {
        users.remove(user); // ConcurrentModificationException
    }
}

// ✅ FIX
users.removeIf(User::isInactive);
// Or use iterator
Iterator<User> it = users.iterator();
while (it.hasNext()) {
    if (it.next().isInactive()) {
        it.remove();
    }
}
```

### 21. Mutating Unmodifiable Collection
```java
// ❌ BUG: Returns mutable internal collection
public List<String> getTags() {
    return tags; // Caller can modify internal state
}

// ✅ FIX
public List<String> getTags() {
    return Collections.unmodifiableList(tags);
    // Or: return List.copyOf(tags);
}
```

### 22. HashMap Key Mutation
```java
// ❌ BUG: Mutating key after insertion
User user = new User("john");
map.put(user, data);
user.setName("jane"); // Hash code changed, can't find entry!

// ✅ FIX: Use immutable keys or don't mutate
```

---

## API/REST Bugs

### 23. Missing Validation
```java
// ❌ BUG: No input validation
@PostMapping("/users")
public User createUser(@RequestBody UserRequest request) {
    return userService.create(request); // Accepts anything
}

// ✅ FIX
@PostMapping("/users")
public User createUser(@Valid @RequestBody UserRequest request) {
    return userService.create(request);
}

public class UserRequest {
    @NotBlank @Email
    private String email;
    
    @NotBlank @Size(min = 2, max = 100)
    private String name;
}
```

### 24. Inconsistent Response Status
```java
// ❌ BUG: Returns 200 for creation
@PostMapping("/orders")
public Order createOrder(@RequestBody OrderRequest request) {
    return orderService.create(request); // Returns 200, should be 201
}

// ✅ FIX
@PostMapping("/orders")
@ResponseStatus(HttpStatus.CREATED)
public Order createOrder(@RequestBody OrderRequest request) {
    return orderService.create(request);
}
```

### 25. N+1 in REST Response
```java
// ❌ BUG: Serialization triggers N+1
@GetMapping("/orders")
public List<Order> getOrders() {
    return orderRepository.findAll(); 
    // Jackson serializes items -> N queries
}

// ✅ FIX
@GetMapping("/orders")
public List<OrderDTO> getOrders() {
    return orderRepository.findAllWithItems().stream()
        .map(OrderDTO::from)
        .toList();
}
```

---

## Logic Bugs

### 26. Off-by-One Error
```java
// ❌ BUG: Skips last element
for (int i = 0; i < items.size() - 1; i++) { // Should be < size()
    process(items.get(i));
}

// ✅ FIX
for (int i = 0; i < items.size(); i++) {
    process(items.get(i));
}
```

### 27. Floating Point Comparison
```java
// ❌ BUG: Floating point comparison
if (price == 19.99) { // May fail due to precision
    applyDiscount();
}

// ✅ FIX
if (BigDecimal.valueOf(price).compareTo(new BigDecimal("19.99")) == 0) {
    applyDiscount();
}
// Or use epsilon comparison for doubles
if (Math.abs(price - 19.99) < 0.001) {
    applyDiscount();
}
```

### 28. String Comparison with ==
```java
// ❌ BUG: Compares references, not content
if (status == "ACTIVE") { // May be false even if equal
    process();
}

// ✅ FIX
if ("ACTIVE".equals(status)) { // Null-safe
    process();
}
```

### 29. Integer Cache Boundary
```java
// ❌ BUG: Works for -128 to 127, fails outside
Integer a = 200;
Integer b = 200;
if (a == b) { // false! Outside cache range
    // ...
}

// ✅ FIX
if (a.equals(b)) {
    // ...
}
```

### 30. Time Zone Bugs
```java
// ❌ BUG: Uses system default timezone
LocalDateTime now = LocalDateTime.now();
Date date = Date.from(now.atZone(ZoneId.systemDefault()).toInstant());

// ✅ FIX: Be explicit about timezone
ZonedDateTime now = ZonedDateTime.now(ZoneId.of("UTC"));
Instant instant = now.toInstant();
```

---

## Detection Patterns Summary

| Bug Type | Detection Signal |
|----------|-----------------|
| NPE Risk | `.get()` without `isPresent()`, chained dots, primitive unboxing |
| Resource Leak | `new FileInputStream`, `Files.lines()` without try-with-resources |
| Race Condition | Shared mutable state, check-then-act, compound operations |
| Transaction Bug | Missing `@Transactional`, private transactional methods |
| Validation Missing | `@RequestBody` without `@Valid` |
| Collection Mutation | Loop with `remove()`, returning internal collection |
| Logic Error | `==` for objects, float comparison, boundary conditions |
