# Review Checklist Templates

## Template Selection Logic

Select checklists based on files changed:

| Changed Files | Apply Checklists |
|--------------|------------------|
| `*Controller.java` | API, Security, Validation |
| `*Service.java` | Business Logic, Transaction |
| `*Repository.java` | Database, Query Performance |
| `*Entity.java` | Data Model, Migration |
| `*Config*.java` | Configuration, Security |
| `*Test*.java` | Test Quality |
| `application*.yml` | Configuration |
| `pom.xml` / `build.gradle` | Dependencies |
| `*DTO.java` / `*Request.java` | API Contract |
| `*Exception.java` | Error Handling |

---

## API/Controller Changes

### When you modify or add a Controller:

```markdown
## API Checklist

### Endpoint Design
- [ ] RESTful conventions followed (GET for read, POST for create, etc.)
- [ ] Consistent URL naming (`/api/v1/resources/{id}`)
- [ ] Proper HTTP status codes (201 for create, 204 for delete, etc.)
- [ ] Pagination implemented for list endpoints

### Input Validation
- [ ] `@Valid` annotation on request body
- [ ] All fields have appropriate validation annotations
- [ ] Custom validators for complex rules
- [ ] Error messages are user-friendly

### Security
- [ ] `@PreAuthorize` or `@Secured` annotation present
- [ ] No sensitive data in URL parameters
- [ ] IDOR protection (ownership verification)
- [ ] Rate limiting considered for sensitive endpoints

### Documentation
- [ ] OpenAPI/Swagger annotations (`@Operation`, `@ApiResponse`)
- [ ] Request/response examples documented
- [ ] Error responses documented

### Testing
- [ ] Unit tests with MockMvc
- [ ] Happy path tested
- [ ] Validation error cases tested
- [ ] Authorization tested
- [ ] Integration test for complete flow
```

---

## Service/Business Logic Changes

### When you modify or add a Service:

```markdown
## Business Logic Checklist

### Transaction Management
- [ ] `@Transactional` on methods that modify data
- [ ] Transaction boundaries are appropriate
- [ ] Rollback rules defined for exceptions
- [ ] No long-running operations inside transactions

### Error Handling
- [ ] Business exceptions are meaningful
- [ ] Exceptions include relevant context
- [ ] Errors are logged appropriately
- [ ] Partial failures handled gracefully

### Concurrency
- [ ] Thread-safety considered for shared state
- [ ] No race conditions in check-then-act patterns
- [ ] Optimistic locking for concurrent updates

### Dependencies
- [ ] Constructor injection used
- [ ] Circular dependencies avoided
- [ ] Single Responsibility maintained

### Testing
- [ ] Unit tests with mocked dependencies
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Business rules verified
```

---

## Repository/Database Changes

### When you modify queries or add repository methods:

```markdown
## Database Checklist

### Query Performance
- [ ] No N+1 query patterns
- [ ] JOIN FETCH or EntityGraph for eager loading
- [ ] Indexes exist for WHERE clause columns
- [ ] EXPLAIN ANALYZE run for complex queries
- [ ] Pagination for large result sets

### Data Integrity
- [ ] Constraints defined at database level
- [ ] Unique constraints where needed
- [ ] Foreign key relationships correct
- [ ] Cascading rules appropriate

### Migration
- [ ] Flyway/Liquibase migration created
- [ ] Migration is backward compatible
- [ ] Rollback script provided
- [ ] Data migration tested with production-like data

### Testing
- [ ] Repository tests with @DataJpaTest
- [ ] Tests use realistic data volumes
- [ ] Edge cases (empty, null, large) tested
```

---

## Entity/Data Model Changes

### When you modify JPA entities:

```markdown
## Data Model Checklist

### JPA Mapping
- [ ] Fetch type is LAZY by default
- [ ] Cascade types are intentional
- [ ] Orphan removal set correctly
- [ ] Bidirectional relationships have proper mappedBy

### Validation
- [ ] Bean validation annotations on fields
- [ ] Custom validators for complex rules
- [ ] Null handling defined

### Audit
- [ ] Created/modified timestamps present
- [ ] Created/modified by user tracked
- [ ] Soft delete considered if applicable

### Migration Required
- [ ] New columns have defaults for existing data
- [ ] Column type changes are safe
- [ ] Index changes considered
- [ ] Migration script created and tested
```

---

## Security-Sensitive Changes

### When modifying authentication, authorization, or security config:

```markdown
## Security Checklist

### Authentication
- [ ] Password hashing uses BCrypt/Argon2
- [ ] Session management configured correctly
- [ ] Token expiration appropriate
- [ ] Refresh token mechanism secure

### Authorization
- [ ] Principle of least privilege applied
- [ ] All endpoints have authorization checks
- [ ] Role hierarchy correct
- [ ] Method-level security where needed

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] No sensitive data in logs
- [ ] PII handled according to policy
- [ ] Secure cookie flags set

### Configuration
- [ ] No hardcoded secrets
- [ ] Secrets in environment variables or vault
- [ ] Debug endpoints disabled in production
- [ ] CORS configured restrictively

### Review Required By
- [ ] Security team review for HIGH risk changes
- [ ] Penetration test for new auth flows
```

---

## Configuration Changes

### When modifying application.yml or config classes:

```markdown
## Configuration Checklist

### Environment Safety
- [ ] No secrets in config files
- [ ] Profile-specific settings correct
- [ ] Production defaults are secure
- [ ] Feature flags documented

### Backward Compatibility
- [ ] New properties have defaults
- [ ] Removed properties handled gracefully
- [ ] Environment variable names documented

### Performance Settings
- [ ] Connection pool sizes appropriate
- [ ] Timeout values reasonable
- [ ] Cache settings configured
- [ ] Thread pool sizes reviewed
```

---

## Dependency Changes

### When modifying pom.xml or build.gradle:

```markdown
## Dependency Checklist

### Security
- [ ] No known vulnerabilities (run dependency-check)
- [ ] Dependencies from trusted sources
- [ ] Version is stable (not SNAPSHOT in prod)

### Compatibility
- [ ] Compatible with Java version
- [ ] Compatible with Spring Boot version
- [ ] No conflicting transitive dependencies

### Licensing
- [ ] License compatible with project
- [ ] No GPL in proprietary project (if applicable)

### Maintenance
- [ ] Dependency is actively maintained
- [ ] Not deprecated or abandoned
- [ ] Update path exists for security patches
```

---

## Test Changes

### When modifying or adding tests:

```markdown
## Test Quality Checklist

### Coverage
- [ ] New code paths are tested
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Integration points tested

### Quality
- [ ] Tests are independent (no order dependency)
- [ ] Tests are deterministic (no flaky tests)
- [ ] Test names describe behavior
- [ ] Assertions are meaningful

### Maintenance
- [ ] No hardcoded test data that can break
- [ ] Test utilities/builders used
- [ ] Mocks are minimal and focused
- [ ] Tests run fast (<100ms for unit tests)
```

---

## Critical Path Changes

### When modifying payment, auth, or other critical flows:

```markdown
## Critical Path Checklist

### Risk Assessment
- [ ] Risk score calculated
- [ ] Rollback plan documented
- [ ] Feature flag for gradual rollout
- [ ] Monitoring alerts configured

### Testing
- [ ] End-to-end test for complete flow
- [ ] Failure scenarios tested
- [ ] Performance test under load
- [ ] Chaos engineering considered

### Review
- [ ] Senior developer review required
- [ ] Security team review for auth changes
- [ ] QA sign-off obtained
- [ ] Product owner aware of changes

### Deployment
- [ ] Canary deployment planned
- [ ] Metrics baseline established
- [ ] On-call team notified
- [ ] Rollback tested
```

---

## Generated Checklist Example

For a PR that modifies `OrderController.java`, `OrderService.java`, and adds `V2024_01_15__add_discount.sql`:

```markdown
# PR Self-Review Checklist

## Because you modified OrderController.java:
- [ ] `@Valid` on request body parameters
- [ ] Authorization check (`@PreAuthorize`) present
- [ ] Proper HTTP status codes returned
- [ ] OpenAPI documentation updated
- [ ] MockMvc test added/updated

## Because you modified OrderService.java:
- [ ] `@Transactional` annotation appropriate
- [ ] Business exceptions meaningful
- [ ] Edge cases handled (null, empty, limits)
- [ ] Unit test with mocked dependencies

## Because you added a database migration:
- [ ] Migration tested on copy of production data
- [ ] Rollback script available
- [ ] Index impact analyzed
- [ ] Backward compatible (can deploy before app update)

## General
- [ ] No hardcoded values
- [ ] Logging added for debugging
- [ ] No security warnings from static analysis
- [ ] PR description explains the "why"
```
