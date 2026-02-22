# Testing Coverage Checks

Patterns for detecting untested code and disabled tests that increase deployment risk.

---

## New File Without Test Detection

### Pair Matching Per Stack

#### Java/Spring Boot
```
Source:  src/main/java/com/example/UserService.java
Test:    src/test/java/com/example/UserServiceTest.java
         or src/test/java/com/example/UserServiceTests.java
         or src/test/java/com/example/UserServiceIT.java (integration)

Source:  src/main/java/com/example/UserController.java
Test:    src/test/java/com/example/UserControllerTest.java
         or src/test/java/com/example/UserControllerIT.java
```

#### Node.js
```
Source:  src/services/userService.ts
Test:    src/services/userService.test.ts
         or src/services/__tests__/userService.test.ts
         or test/services/userService.spec.ts

Source:  src/routes/users.ts
Test:    src/routes/users.test.ts
         or tests/routes/users.spec.ts
```

#### Python
```
Source:  app/services/user_service.py
Test:    tests/test_user_service.py
         or tests/services/test_user_service.py
         or app/services/test_user_service.py

Source:  app/views/users.py
Test:    tests/test_users.py
         or tests/views/test_users.py
```

### Detection Workflow

1. List all new source files in diff (added, not test files)
2. For each new source file, check if a corresponding test file exists:
   - In the same diff (new test file added)
   - In the existing codebase (test already exists)
3. Flag new source files without any test: WARNING

### Exceptions (Do Not Flag)

- Configuration files (application.yml, settings.py, config.ts)
- Migration files (SQL, Alembic revisions, Django migrations)
- Static assets (CSS, images, fonts)
- Type definition files (*.d.ts, *.pyi)
- Package manifest files (pom.xml, package.json, requirements.txt)
- Infrastructure files (Dockerfile, *.tf, k8s manifests)
- Documentation files (*.md, *.rst)

---

## Disabled / Skipped Test Detection

### Patterns Per Stack

#### Java
```java
@Disabled                           // JUnit 5
@Disabled("reason")
@Ignore                             // JUnit 4 (legacy)
@Ignore("reason")
assumeTrue(false)                   // Programmatic skip
@EnabledIf / @DisabledIf            // Conditional
@Tag("slow") + exclude config       // Tag-based exclusion
```

#### Node.js (Jest/Mocha/Vitest)
```javascript
test.skip('test name', ...)
it.skip('test name', ...)
describe.skip('suite name', ...)
xit('test name', ...)               // Mocha
xdescribe('suite name', ...)        // Mocha
test.todo('test name')              // Not implemented
```

#### Python (pytest/unittest)
```python
@pytest.mark.skip
@pytest.mark.skip(reason="...")
@pytest.mark.skipIf(condition, "...")
@unittest.skip("reason")
@unittest.skipIf(condition, "reason")
@unittest.expectedFailure
```

### Detection Regex

```regex
# Java
@Disabled|@Ignore

# JavaScript/TypeScript
\b(test|it|describe)\.skip\s*\(
\b(xit|xdescribe)\s*\(

# Python
@pytest\.mark\.skip|@unittest\.skip
```

### Severity Rules

| Scenario | Severity | Description |
|----------|----------|-------------|
| Test newly disabled in this diff | WARNING | Was passing before, why disable now? |
| Test disabled with TODO/FIXME comment | WARNING | Known issue, track it |
| Test disabled for > 30 days (if detectable) | WARNING | Likely dead test |
| Test added with skip | INFO | Placeholder, track completion |

---

## Integration Test Config Change Impact

### When Integration Test Config Changes

If these files change, integration tests may not reflect reality:

```
# Java
src/test/resources/application-test.yml
src/test/resources/application-integration.yml
testcontainers.properties

# Node.js
jest.config.js / jest.config.ts
vitest.config.ts
.env.test
test/setup.js

# Python
conftest.py
pytest.ini / setup.cfg [tool:pytest]
tox.ini
.env.test
```

### Severity
- WARNING: Test config changed without corresponding test updates
- INFO: Test config changed with matching test updates

---

## E2E Test Recommendations by Change Type

| Change Type | E2E Recommendation |
|-------------|-------------------|
| API endpoint added/modified | Run API contract tests |
| Authentication flow changed | Run full auth E2E suite |
| Database migration | Run data integrity tests |
| UI component changed | Run visual regression tests |
| Payment/billing flow | Run complete payment E2E |
| Email/notification flow | Run notification E2E |
| File upload/download | Run file handling E2E |
| Search functionality | Run search accuracy tests |
