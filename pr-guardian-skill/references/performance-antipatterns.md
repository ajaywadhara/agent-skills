# Performance Antipatterns Reference

## Database Performance Issues

### N+1 Query Problem

#### Detection Pattern
```java
// ❌ SLOW: N+1 queries
public List<OrderDTO> getOrdersWithCustomers() {
    List<Order> orders = orderRepository.findAll();  // 1 query
    return orders.stream()
        .map(order -> new OrderDTO(
            order.getId(),
            order.getCustomer().getName()  // N queries!
        ))
        .toList();
}
```

#### Performance Impact
- 100 orders = 101 queries
- 1000 orders = 1001 queries
- Response time: O(n) database roundtrips

#### Fix Patterns
```java
// ✅ FIX 1: JOIN FETCH
@Query("SELECT o FROM Order o JOIN FETCH o.customer")
List<Order> findAllWithCustomer();

// ✅ FIX 2: EntityGraph
@EntityGraph(attributePaths = {"customer", "items"})
List<Order> findAll();

// ✅ FIX 3: Batch fetching (hibernate property)
@BatchSize(size = 25)
@OneToMany(mappedBy = "order")
private List<OrderItem> items;

// application.yml
spring.jpa.properties.hibernate.default_batch_fetch_size: 25
```

---

### Missing Indexes
```java
// ❌ SLOW: Full table scan
@Query("SELECT u FROM User u WHERE u.email = :email")
Optional<User> findByEmail(String email);
// If no index on email column, scans entire table

// ✅ FIX: Add index
@Table(name = "users", indexes = {
    @Index(name = "idx_user_email", columnList = "email"),
    @Index(name = "idx_user_status_created", columnList = "status, created_at")
})
@Entity
public class User { }

// Or via migration
CREATE INDEX idx_user_email ON users(email);
```

---

### Missing Pagination
```java
// ❌ SLOW: Loads entire table into memory
public List<User> getAllUsers() {
    return userRepository.findAll();  // 1M users = OOM
}

// ✅ FIX: Use pagination
public Page<User> getUsers(int page, int size) {
    return userRepository.findAll(PageRequest.of(page, size));
}

// For streaming large datasets
@Query("SELECT u FROM User u")
Stream<User> streamAllUsers();

// Use with try-with-resources
try (Stream<User> users = userRepository.streamAllUsers()) {
    users.forEach(this::process);
}
```

---

### Eager Loading Everything
```java
// ❌ SLOW: Loads entire object graph
@Entity
public class Order {
    @OneToMany(fetch = FetchType.EAGER)  // Always loads
    private List<OrderItem> items;
    
    @ManyToOne(fetch = FetchType.EAGER)  // Always loads
    private Customer customer;
    
    @OneToMany(fetch = FetchType.EAGER)  // Always loads
    private List<Payment> payments;
}

// ✅ FIX: Default to LAZY, fetch when needed
@Entity
public class Order {
    @OneToMany(fetch = FetchType.LAZY)
    private List<OrderItem> items;
    
    @ManyToOne(fetch = FetchType.LAZY)
    private Customer customer;
}

// Fetch explicitly when needed
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
Order findByIdWithItems(Long id);
```

---

## Memory Issues

### Unbounded Collection Growth
```java
// ❌ MEMORY LEAK: Unbounded cache
private static final Map<String, Object> cache = new HashMap<>();

public Object getCached(String key) {
    return cache.computeIfAbsent(key, this::loadExpensive);
    // Never evicts - grows forever!
}

// ✅ FIX: Use bounded cache
private final Cache<String, Object> cache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(10))
    .build();

// Or use LRU
private final Map<String, Object> cache = Collections.synchronizedMap(
    new LinkedHashMap<>(100, 0.75f, true) {
        @Override
        protected boolean removeEldestEntry(Map.Entry eldest) {
            return size() > 100;
        }
    }
);
```

---

### Loading Large Files Into Memory
```java
// ❌ SLOW + OOM: Loads entire file
public List<String> processFile(Path path) {
    return Files.readAllLines(path);  // 1GB file = 1GB+ in memory
}

// ✅ FIX: Stream processing
public void processFile(Path path) {
    try (Stream<String> lines = Files.lines(path)) {
        lines.forEach(this::processLine);
    }
}

// For very large files, use BufferedReader
try (BufferedReader reader = Files.newBufferedReader(path)) {
    String line;
    while ((line = reader.readLine()) != null) {
        processLine(line);
    }
}
```

---

### String Concatenation in Loop
```java
// ❌ SLOW: Creates O(n²) intermediate strings
public String buildReport(List<Item> items) {
    String result = "";
    for (Item item : items) {
        result += item.toString() + "\n";  // New String each iteration
    }
    return result;
}

// ✅ FIX: Use StringBuilder
public String buildReport(List<Item> items) {
    StringBuilder sb = new StringBuilder(items.size() * 50);
    for (Item item : items) {
        sb.append(item).append("\n");
    }
    return sb.toString();
}

// Or use Collectors
public String buildReport(List<Item> items) {
    return items.stream()
        .map(Item::toString)
        .collect(Collectors.joining("\n"));
}
```

---

### Boxing/Unboxing in Hot Path
```java
// ❌ SLOW: Creates wrapper objects
public long sumValues(List<Long> values) {
    long sum = 0;
    for (Long value : values) {  // Unboxing each iteration
        sum += value;
    }
    return sum;
}

// ✅ FIX: Use primitive streams
public long sumValues(List<Long> values) {
    return values.stream()
        .mapToLong(Long::longValue)
        .sum();
}

// Or use primitive arrays for hot paths
public long sumValues(long[] values) {
    long sum = 0;
    for (long value : values) {
        sum += value;
    }
    return sum;
}
```

---

## CPU/Computation Issues

### Regex Compilation in Loop
```java
// ❌ SLOW: Compiles regex every iteration
public List<String> filterValid(List<String> inputs) {
    return inputs.stream()
        .filter(s -> s.matches("^[A-Z]{2}\\d{6}$"))  // Compiles each time!
        .toList();
}

// ✅ FIX: Compile once
private static final Pattern VALID_PATTERN = Pattern.compile("^[A-Z]{2}\\d{6}$");

public List<String> filterValid(List<String> inputs) {
    return inputs.stream()
        .filter(s -> VALID_PATTERN.matcher(s).matches())
        .toList();
}
```

---

### Inefficient Collection Operations
```java
// ❌ SLOW: O(n) lookup in list
List<User> users = getUsers();
for (Order order : orders) {
    User user = users.stream()
        .filter(u -> u.getId().equals(order.getUserId()))
        .findFirst()
        .orElse(null);  // O(n) for each order!
}

// ✅ FIX: Use Map for O(1) lookup
Map<Long, User> userMap = users.stream()
    .collect(Collectors.toMap(User::getId, Function.identity()));

for (Order order : orders) {
    User user = userMap.get(order.getUserId());  // O(1)
}
```

---

### Blocking in Async Context
```java
// ❌ SLOW: Blocks event loop in reactive
public Mono<Data> getData() {
    return Mono.fromCallable(() -> {
        Thread.sleep(1000);  // Blocks!
        return repository.findAll();  // Blocking JPA call
    });
}

// ✅ FIX: Use proper async/reactive
public Mono<Data> getData() {
    return Mono.fromCallable(() -> repository.findAll())
        .subscribeOn(Schedulers.boundedElastic());  // Runs on blocking pool
}

// Better: Use reactive repository
public Flux<Data> getData() {
    return reactiveRepository.findAll();
}
```

---

### Synchronous External Calls
```java
// ❌ SLOW: Sequential external calls
public AggregatedData getData(Long id) {
    User user = userService.getUser(id);         // 100ms
    List<Order> orders = orderService.getOrders(id);  // 150ms
    PaymentInfo payment = paymentService.getInfo(id); // 200ms
    // Total: 450ms (sequential)
    
    return new AggregatedData(user, orders, payment);
}

// ✅ FIX: Parallel calls
public AggregatedData getData(Long id) {
    CompletableFuture<User> userFuture = 
        CompletableFuture.supplyAsync(() -> userService.getUser(id));
    CompletableFuture<List<Order>> ordersFuture = 
        CompletableFuture.supplyAsync(() -> orderService.getOrders(id));
    CompletableFuture<PaymentInfo> paymentFuture = 
        CompletableFuture.supplyAsync(() -> paymentService.getInfo(id));
    
    CompletableFuture.allOf(userFuture, ordersFuture, paymentFuture).join();
    // Total: ~200ms (parallel, bounded by slowest)
    
    return new AggregatedData(
        userFuture.join(), 
        ordersFuture.join(), 
        paymentFuture.join()
    );
}
```

---

## Network/I/O Issues

### Missing Connection Pooling
```java
// ❌ SLOW: New connection each request
public String callApi(String url) {
    RestTemplate restTemplate = new RestTemplate();  // No pooling!
    return restTemplate.getForObject(url, String.class);
}

// ✅ FIX: Reuse with connection pool
@Bean
public RestTemplate restTemplate() {
    HttpComponentsClientHttpRequestFactory factory = 
        new HttpComponentsClientHttpRequestFactory();
    
    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
    cm.setMaxTotal(100);
    cm.setDefaultMaxPerRoute(20);
    
    CloseableHttpClient httpClient = HttpClients.custom()
        .setConnectionManager(cm)
        .build();
    
    factory.setHttpClient(httpClient);
    return new RestTemplate(factory);
}
```

---

### Missing Timeouts
```java
// ❌ DANGEROUS: No timeout, can hang forever
RestTemplate restTemplate = new RestTemplate();
String result = restTemplate.getForObject(url, String.class);

// ✅ FIX: Configure timeouts
@Bean
public RestTemplate restTemplate() {
    HttpComponentsClientHttpRequestFactory factory = 
        new HttpComponentsClientHttpRequestFactory();
    factory.setConnectTimeout(Duration.ofSeconds(5));
    factory.setReadTimeout(Duration.ofSeconds(30));
    return new RestTemplate(factory);
}
```

---

### Chatty API Design
```java
// ❌ SLOW: Multiple roundtrips
public OrderDetailsDTO getOrderDetails(Long orderId) {
    Order order = orderClient.getOrder(orderId);           // Call 1
    Customer customer = customerClient.getCustomer(order.getCustomerId()); // Call 2
    List<Product> products = order.getItems().stream()
        .map(item -> productClient.getProduct(item.getProductId()))  // N calls!
        .toList();
    return new OrderDetailsDTO(order, customer, products);
}

// ✅ FIX: Batch API or composite endpoint
// Option 1: Batch call
List<Product> products = productClient.getProducts(productIds);  // 1 call

// Option 2: Create aggregate endpoint
OrderDetailsDTO details = orderClient.getOrderWithDetails(orderId);  // 1 call
```

---

## Caching Issues

### No Caching for Expensive Operations
```java
// ❌ SLOW: Recomputes every time
public ExchangeRate getExchangeRate(String currency) {
    return externalApi.fetchRate(currency);  // 500ms each call
}

// ✅ FIX: Add caching
@Cacheable(value = "exchangeRates", key = "#currency")
public ExchangeRate getExchangeRate(String currency) {
    return externalApi.fetchRate(currency);
}

// Cache configuration
@Bean
public CacheManager cacheManager() {
    CaffeineCacheManager cacheManager = new CaffeineCacheManager();
    cacheManager.setCaffeine(Caffeine.newBuilder()
        .expireAfterWrite(Duration.ofMinutes(5))
        .maximumSize(1000));
    return cacheManager;
}
```

---

### Cache Stampede
```java
// ❌ PROBLEM: Multiple threads recompute on expiry
@Cacheable("data")
public Data getData(String key) {
    return expensiveComputation(key);  // All threads compute simultaneously
}

// ✅ FIX: Use refresh-ahead or locking
@Bean
public CacheManager cacheManager() {
    return new CaffeineCacheManager() {
        @Override
        protected Cache<Object, Object> createNativeCaffeineCache(String name) {
            return Caffeine.newBuilder()
                .expireAfterWrite(Duration.ofMinutes(10))
                .refreshAfterWrite(Duration.ofMinutes(8))  // Refresh before expiry
                .build(key -> loadData(key));
        }
    };
}
```

---

## Performance Checklist

### Database
- [ ] No N+1 queries (use JOIN FETCH, EntityGraph, or batch fetching)
- [ ] Appropriate indexes on query columns
- [ ] Pagination for large result sets
- [ ] LAZY loading by default
- [ ] Connection pool configured

### Memory
- [ ] Bounded caches with eviction
- [ ] Streaming for large files
- [ ] StringBuilder for string building
- [ ] Primitive types in hot paths

### CPU
- [ ] Regex patterns pre-compiled
- [ ] Maps for lookups instead of list iteration
- [ ] Parallel processing for independent tasks

### Network
- [ ] Connection pooling enabled
- [ ] Timeouts configured
- [ ] Batch APIs instead of chatty calls
- [ ] Caching for expensive/frequent calls

### Monitoring
- [ ] Response time metrics
- [ ] Database query logging
- [ ] Cache hit/miss ratios
- [ ] Memory usage tracking
