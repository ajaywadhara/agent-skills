# TypeScript/JavaScript Patterns Reference

## Null/Undefined Safety

### Nullish Access
```typescript
// ❌ BUG: TypeError if null/undefined
user.address.city

// ✅ FIX: Optional chaining
user?.address?.city

// ❌ BUG: Falsy check catches 0, '', false
if (value) { }

// ✅ FIX: Nullish check
if (value != null) { }  // Catches null and undefined only
```

### Nullish Coalescing
```typescript
// ❌ BUG: 0 and '' treated as missing
const name = user.name || 'Unknown'

// ✅ FIX
const name = user.name ?? 'Unknown'
```

---

## Type Safety (TypeScript)

### Any Type
```typescript
// ❌ LOSES TYPE SAFETY
function process(data: any) {
  return data.value  // No type checking
}

// ✅ FIX: Use generics or unknown
function process<T extends { value: string }>(data: T) {
  return data.value
}

// Or with unknown + type guard
function process(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: string }).value
  }
}
```

### Type Assertion Abuse
```typescript
// ❌ UNSAFE: Lies to compiler
const value = data as MyType

// ✅ FIX: Validate first
function isMyType(data: unknown): data is MyType {
  return typeof data === 'object' && data !== null && 'id' in data
}

if (isMyType(data)) {
  // TypeScript knows data is MyType
}
```

### Non-Null Assertion
```typescript
// ❌ UNSAFE: Can cause runtime error
const element = document.getElementById('myId')!

// ✅ FIX: Handle null case
const element = document.getElementById('myId')
if (!element) throw new Error('Element not found')
```

---

## Async/Await

### Missing Await
```typescript
// ❌ BUG: Promise not resolved
async function fetchUser() {
  const user = getUser(id)  // Missing await
  return user.name  // user is Promise, not User
}

// ✅ FIX
async function fetchUser() {
  const user = await getUser(id)
  return user.name
}
```

### Unhandled Promise Rejections
```typescript
// ❌ BUG: Silent failure
async function process() {
  const data = await fetchData()
  processData(data)  // If this throws, unhandled
}

// ✅ FIX
async function process() {
  try {
    const data = await fetchData()
    await processData(data)
  } catch (error) {
    logger.error('Processing failed', error)
    throw error
  }
}
```

### Parallel vs Sequential
```typescript
// ❌ SLOW: Sequential awaits
const user = await fetchUser()
const posts = await fetchPosts(user.id)
const comments = await fetchComments(posts[0].id)

// ✅ FAST: Parallel when independent
const [user, posts] = await Promise.all([
  fetchUser(),
  fetchPosts()
])
const comments = await fetchComments(posts[0].id)
```

---

## Array Operations

### Mutation vs Immutability
```typescript
// ❌ MUTATES ORIGINAL
items.push(newItem)
items.sort((a, b) => a - b)

// ✅ IMMUTABLE APPROACH
const newItems = [...items, newItem]
const sorted = [...items].sort((a, b) => a - b)
```

### forEach vs map/filter
```typescript
// ❌ MISUSED: forEach with side effects
const results: Result[] = []
items.forEach(item => {
  results.push(transform(item))
})

// ✅ BETTER: map for transformation
const results = items.map(item => transform(item))
```

### Index in Loops
```typescript
// ❌ BUG: i is captured by reference
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100)  // Prints 3, 3, 3
}

// ✅ FIX: Use let or closure
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100)  // 0, 1, 2
}
```

---

## Object Safety

### Prototype Pollution
```typescript
// ❌ VULNERABLE
function merge(target: any, source: any) {
  for (const key in source) {
    target[key] = source[key]  // Can pollute __proto__
  }
}

// ✅ SECURE
function merge(target: object, source: object) {
  return { ...target, ...source }
}
```

### Property Enumeration
```typescript
// ❌ UNEXPECTED: Iterates prototype chain
for (const key in obj) { }

// ✅ EXPECTED: Own properties only
for (const key of Object.keys(obj)) { }
// Or
Object.entries(obj).forEach(([key, value]) => { })
```

---

## Security

### XSS via innerHTML
```typescript
// ❌ VULNERABLE: XSS
element.innerHTML = userInput

// ✅ SECURE
element.textContent = userInput
// Or sanitize
element.innerHTML = DOMPurify.sanitize(userInput)
```

### eval and Function
```typescript
// ❌ VULNERABLE: Code injection
eval(userInput)
new Function(userInput)()

// ✅ AVOID: Never use with user input
// Use JSON.parse for data, proper parsers for code
```

### Hardcoded Secrets
```typescript
// ❌ VULNERABLE
const API_KEY = 'sk-live-abc123'
const JWT_SECRET = 'my-secret-key'

// ✅ SECURE
const API_KEY = process.env.API_KEY
const JWT_SECRET = process.env.JWT_SECRET
```

### ReDoS (Regex DoS)
```typescript
// ❌ VULNERABLE: Catastrophic backtracking
const regex = /^(a+)+$/
regex.test('aaaaaaaaaaaaaaaaaaaaaaaaaaaa!')

// ✅ SECURE: Avoid nested quantifiers, use atomic groups
const regex = /^(?>a+)$/
```

---

## React Specific

### useEffect Dependencies
```typescript
// ❌ BUG: Stale closure
useEffect(() => {
  fetchData(userId)
}, [])  // userId not in deps

// ✅ FIX
useEffect(() => {
  fetchData(userId)
}, [userId])
```

### State Mutation
```typescript
// ❌ BUG: Direct state mutation
state.items.push(newItem)
setState(state)

// ✅ FIX
setState(prev => ({
  ...prev,
  items: [...prev.items, newItem]
}))
```

### Missing Key
```typescript
// ❌ PERFORMANCE ISSUE
items.map(item => <Item data={item} />)

// ✅ FIX
items.map(item => <Item key={item.id} data={item} />)
```

---

## Performance

### Memory Leaks
```typescript
// ❌ BUG: Event listener never removed
useEffect(() => {
  window.addEventListener('resize', handleResize)
}, [])

// ✅ FIX
useEffect(() => {
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
}, [])
```

### Expensive Re-renders
```typescript
// ❌ SLOW: Creates new function each render
<Button onClick={() => handleClick(id)} />

// ✅ FAST: Memoize
const memoizedHandleClick = useCallback(() => handleClick(id), [id])
<Button onClick={memoizedHandleClick} />
```

---

## Error Handling

### Catch with Any
```typescript
// ❌ LOSES TYPE INFO
try {
  await process()
} catch (error) {
  console.log(error.message)  // Property may not exist
}

// ✅ FIX
try {
  await process()
} catch (error) {
  if (error instanceof Error) {
    console.log(error.message)
  }
}
```