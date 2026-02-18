# Python Patterns Reference

## Null/None Safety

### None Dereference
```python
# ❌ BUG: AttributeError if None
user.address.city

# ✅ FIX
getattr(getattr(user, 'address', None), 'city', None)
# Or with walrus operator
if (address := user.address) and (city := address.city):
    ...
```

### Returning None Instead of Empty
```python
# ❌ BUG: Forces None checks
def get_items():
    if not items:
        return None
    return items

# ✅ FIX
def get_items():
    return items or []
```

---

## Type Safety

### Mutable Default Arguments
```python
# ❌ BUG: Shared mutable default
def append_item(item, items=[]):
    items.append(item)
    return items

# ✅ FIX
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Late Binding Closures
```python
# ❌ BUG: All lambdas capture same i
functions = [lambda: i for i in range(3)]
[f() for f in functions]  # [2, 2, 2]

# ✅ FIX
functions = [lambda i=i: i for i in range(3)]
[f() for f in functions]  # [0, 1, 2]
```

---

## Resource Management

### Unclosed Files
```python
# ❌ BUG: File not closed on exception
f = open('file.txt')
data = f.read()

# ✅ FIX
with open('file.txt') as f:
    data = f.read()
```

### Database Connection Leaks
```python
# ❌ BUG: Connection not returned
conn = db.connect()
cursor = conn.cursor()
cursor.execute(query)

# ✅ FIX
with db.connect() as conn:
    with conn.cursor() as cursor:
        cursor.execute(query)
```

---

## Concurrency

### Race Conditions
```python
# ❌ BUG: Not thread-safe
counter = 0
def increment():
    global counter
    counter += 1

# ✅ FIX
import threading
counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:
        counter += 1
```

---

## Security

### SQL Injection
```python
# ❌ VULNERABLE
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ SECURE
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Command Injection
```python
# ❌ VULNERABLE
os.system(f"ping {user_input}")

# ✅ SECURE
import shlex
subprocess.run(["ping", shlex.quote(user_input)])
```

### Pickle Deserialization
```python
# ❌ VULNERABLE: Arbitrary code execution
pickle.loads(user_data)

# ✅ SECURE: Use JSON or validate source
json.loads(user_data)
```

### Hardcoded Secrets
```python
# ❌ VULNERABLE
API_KEY = "sk-live-abc123"
DB_PASSWORD = "secret123"

# ✅ SECURE
import os
API_KEY = os.environ.get("API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```

---

## Common Mistakes

### List Modification During Iteration
```python
# ❌ BUG: Skips elements
for item in items:
    if item.invalid:
        items.remove(item)

# ✅ FIX
items = [item for item in items if not item.invalid]
```

### Integer Division Gotcha (Python 2)
```python
# ❌ BUG in Python 2: Integer division
result = 5 / 2  # 2, not 2.5

# ✅ FIX
from __future__ import division
result = 5 / 2  # 2.5
```

### Comparing Floats
```python
# ❌ BUG: Floating point precision
if x == 0.1 + 0.2:  # May be False

# ✅ FIX
from math import isclose
if isclose(x, 0.3, rel_tol=1e-9):
    ...
```

### Default Argument Mutation
```python
# ❌ BUG: Default dict is shared across calls
def add_to_cache(key, value, cache={}):
    cache[key] = value
    return cache

# ✅ FIX
def add_to_cache(key, value, cache=None):
    if cache is None:
        cache = {}
    cache[key] = value
    return cache
```

---

## Async/Await

### Missing Await
```python
# ❌ BUG: Coroutine not executed
async def fetch_data():
    result = get_data()  # Missing await
    return result

# ✅ FIX
async def fetch_data():
    result = await get_data()
    return result
```

### Blocking in Async
```python
# ❌ BUG: Blocks event loop
async def process():
    time.sleep(5)  # Blocks everything

# ✅ FIX
async def process():
    await asyncio.sleep(5)
```

---

## Performance

### String Concatenation in Loops
```python
# ❌ SLOW: Creates new string each iteration
result = ""
for item in items:
    result += str(item)

# ✅ FAST
result = "".join(str(item) for item in items)
```

### Inefficient Membership Testing
```python
# ❌ SLOW: O(n)
if item in my_list:
    ...

# ✅ FAST: O(1) average
if item in my_set:
    ...
```

---

## Error Handling

### Bare Except
```python
# ❌ BUG: Catches everything including KeyboardInterrupt
try:
    process()
except:
    pass

# ✅ FIX
try:
    process()
except SpecificException as e:
    logger.error("Failed", exc_info=e)
```

### Exception Variable Scope (Python 3)
```python
# ❌ BUG: e persists after block
try:
    process()
except Exception as e:
    ...
# e is deleted here in Python 3, but code might expect it

# ✅ FIX: Don't rely on e outside except block
```

---

## Type Hints

### Missing Optional
```python
# ❌ UNCLEAR
def get_user(id: int) -> User:
    ...  # Can return None?

# ✅ CLEAR
from typing import Optional
def get_user(id: int) -> Optional[User]:
    ...
```

### Any Abuse
```python
# ❌ LOSES TYPE SAFETY
def process(data: Any) -> Any:
    ...

# ✅ PRESERVE TYPE INFO
from typing import TypeVar, Generic
T = TypeVar('T')
def process(data: T) -> T:
    ...
```