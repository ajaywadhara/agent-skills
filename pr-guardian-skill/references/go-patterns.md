# Go Patterns Reference

## Nil Safety

### Nil Pointer Dereference
```go
// ❌ BUG: Panic if user is nil
func getCity(user *User) string {
    return user.Address.City
}

// ✅ FIX
func getCity(user *User) string {
    if user == nil || user.Address == nil {
        return ""
    }
    return user.Address.City
}
```

### Nil Interface vs Nil Pointer
```go
// ❌ BUG: Interface with nil concrete value is not nil
func returnsError() error {
    var customErr *CustomError = nil
    return customErr  // Type is *CustomError, not nil interface
}

// ✅ FIX
func returnsError() error {
    return nil  // Return nil interface directly
}
```

---

## Error Handling

### Ignoring Errors
```go
// ❌ BUG: Error not handled
result, _ := someFunction()

// ✅ FIX
result, err := someFunction()
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

### Not Wrapping Errors
```go
// ❌ LOSES CONTEXT
if err != nil {
    return err
}

// ✅ PRESERVES CONTEXT
if err != nil {
    return fmt.Errorf("failed to process user %s: %w", userID, err)
}
```

### Panic for Errors
```go
// ❌ BAD: Panic for recoverable errors
if user == nil {
    panic("user is nil")
}

// ✅ GOOD: Return error
if user == nil {
    return errors.New("user is nil")
}
```

---

## Concurrency

### Goroutine Leak
```go
// ❌ BUG: Goroutine never terminates
go func() {
    for {
        select {
        case msg := <-ch:
            process(msg)
        }
    }
}()

// ✅ FIX: Context for cancellation
go func(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        case msg := <-ch:
            process(msg)
        }
    }
}(ctx)
```

### Race Condition
```go
// ❌ BUG: Data race
var counter int
go func() { counter++ }()
counter++

// ✅ FIX
var counter int
var mu sync.Mutex
go func() {
    mu.Lock()
    counter++
    mu.Unlock()
}()
mu.Lock()
counter++
mu.Unlock()
```

### Channel Blocking
```go
// ❌ BUG: Deadlock if no receiver
ch := make(chan int)
ch <- value  // Blocks forever

// ✅ FIX: Buffered or select
ch := make(chan int, 1)
ch <- value

// Or with select
select {
case ch <- value:
default:
    // Handle full channel
}
```

### WaitGroup Misuse
```go
// ❌ BUG: WaitGroup not incremented
var wg sync.WaitGroup
go func() {
    doWork()
    wg.Done()
}()
wg.Wait()  // Returns immediately

// ✅ FIX
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    doWork()
}()
wg.Wait()
```

---

## Resource Management

### defer in Loop
```go
// ❌ BUG: Resources not closed until function returns
for _, file := range files {
    f, _ := os.Open(file)
    defer f.Close()  // Accumulates until function ends
}

// ✅ FIX: Separate function
for _, file := range files {
    processFile(file)
}

func processFile(name string) error {
    f, err := os.Open(name)
    if err != nil {
        return err
    }
    defer f.Close()
    // process...
}
```

### HTTP Response Body
```go
// ❌ BUG: Body not closed
resp, _ := http.Get(url)
data, _ := io.ReadAll(resp.Body)

// ✅ FIX
resp, err := http.Get(url)
if err != nil {
    return err
}
defer resp.Body.Close()
data, err := io.ReadAll(resp.Body)
```

---

## Slice and Map

### Slice Append Sharing
```go
// ❌ BUG: Appending may modify original
func appendItem(items []int, item int) []int {
    return append(items, item)  // May modify original
}

// ✅ FIX: Copy if needed
func appendItem(items []int, item int) []int {
    newItems := make([]int, len(items)+1)
    copy(newItems, items)
    newItems[len(items)] = item
    return newItems
}
```

### Map Concurrency
```go
// ❌ BUG: Concurrent map access
var m = make(map[string]int)
go func() { m["key"] = 1 }()
go func() { _ = m["key"] }()  // Race condition

// ✅ FIX: sync.RWMutex or sync.Map
var m = make(map[string]int)
var mu sync.RWMutex

go func() {
    mu.Lock()
    m["key"] = 1
    mu.Unlock()
}()
go func() {
    mu.RLock()
    _ = m["key"]
    mu.RUnlock()
}()
```

### Nil Map
```go
// ❌ BUG: Write to nil map
var m map[string]int
m["key"] = 1  // Panic

// ✅ FIX: Initialize
m := make(map[string]int)
m["key"] = 1
```

---

## Security

### SQL Injection
```go
// ❌ VULNERABLE
query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)

// ✅ SECURE
query := "SELECT * FROM users WHERE id = ?"
row := db.QueryRow(query, userID)
```

### Command Injection
```go
// ❌ VULNERABLE
exec.Command("ping", userInput).Run()

// ✅ SECURE: Validate input
if !regexp.MustCompile(`^[a-zA-Z0-9.-]+$`).MatchString(userInput) {
    return errors.New("invalid hostname")
}
exec.Command("ping", "-c", "1", userInput).Run()
```

### Path Traversal
```go
// ❌ VULNERABLE
filepath.Join("/data", userInput)

// ✅ SECURE
base := "/data"
path := filepath.Join(base, userInput)
if !strings.HasPrefix(path, base) {
    return errors.New("path traversal attempt")
}
```

### Hardcoded Secrets
```go
// ❌ VULNERABLE
const APIKey = "sk-live-abc123"

// ✅ SECURE
apiKey := os.Getenv("API_KEY")
```

---

## Context Usage

### Missing Context Propagation
```go
// ❌ BAD: Context not propagated
func fetchData(id string) ([]byte, error) {
    resp, err := http.Get(url + id)
    // No way to cancel
}

// ✅ GOOD
func fetchData(ctx context.Context, id string) ([]byte, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET", url+id, nil)
    resp, err := http.DefaultClient.Do(req)
    // Request can be cancelled
}
```

### Storing Values Without Key Type
```go
// ❌ BUG: Collision risk
ctx = context.WithValue(ctx, "userID", id)

// ✅ FIX: Use typed key
type ctxKey string
const userIDKey ctxKey = "userID"
ctx = context.WithValue(ctx, userIDKey, id)
```

---

## Performance

### String Concatenation
```go
// ❌ SLOW: Creates new string each time
var result string
for _, s := range items {
    result += s
}

// ✅ FAST: strings.Builder
var sb strings.Builder
for _, s := range items {
    sb.WriteString(s)
}
result := sb.String()
```

### Unnecessary Conversions
```go
// ❌ SLOW: []byte conversion each call
func processJSON(data string) {
    json.Unmarshal([]byte(data), &result)
}

// ✅ FAST: Accept []byte directly
func processJSON(data []byte) {
    json.Unmarshal(data, &result)
}
```

---

## Interface Pollution

### Interface for Single Implementation
```go
// ❌ OVER-ENGINEERED
type UserSaver interface {
    Save(user *User) error
}

type userService struct{}

func (s *userService) Save(user *User) error { ... }

// ✅ SIMPLER: Define interface when needed
type userService struct{}

func (s *userService) Save(user *User) error { ... }
// Add interface only when mocking or multiple implementations needed
```