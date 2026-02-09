# Audit Criteria (Mission Critical)

Conduct the review across these expanded pillars.

## 1. Architecture & Reliability
*   **System Design:** Component boundaries and responsibilities.
*   **Resiliency Patterns:**
    *   **Circuit Breakers:** Are they used for downstream dependencies?
    *   **Timeouts:** Are strict timeouts configured? (No infinite waits).
    *   **Retries:** Do retries use exponential backoff and jitter?
    *   **Bulkheading:** Does a failure in one subsystem crash the whole app?
*   **Idempotency:** Are API endpoints and message consumers idempotent? How is this enforced (idempotency keys, unique constraints)?
*   **Scaling:** Stateless vs Stateful. Distributed locking strategy.

## 2. Data Integrity (Payments Specific)
*   **Money Types:** *Strictly forbid* `float` or `double` for currency. Look for `BigDecimal` or Integer-based cents.
*   **Concurrency Control:**
    *   **Locking:** Are critical updates (balance changes, status transitions) protected by Pessimistic Locking (`SELECT FOR UPDATE`) or Optimistic Locking (`@Version`)?
    *   **Race Conditions:** Look for check-then-act patterns that aren't atomic.
*   **Transactions:** Are boundaries correct? Do external API calls happen *inside* DB transactions (bad practice)?
*   **Audit Trails:** Are critical changes logged to an immutable history/ledger?

## 3. Code Quality & Tech Debt
*   **Structure:** Code organization and module structure.
*   **DRY Violations:** *Aggressively* check for duplicated logic.
*   **Error Handling:**
    *   Are specific exceptions caught?
    *   Are errors mapped to proper HTTP 4xx/5xx codes?
    *   **Zombie Code:** Flag deprecated or unused code paths.
*   **Dependencies:** Check for outdated or risky libraries.

## 4. Observability
*   **Logging:** Is PII (Personally Identifiable Information) or PCI data (Card numbers) being logged? **Flag this immediately.**
*   **Context:** Do logs include `traceId`, `orderId`, `userId`?
*   **Metrics:** Are business metrics (payment_success, payment_failed) emitted?

## 5. Test Review
*   **Coverage:** Unit, Integration, E2E.
*   **Failure Modes:** Do tests simulate timeouts, DB failures, downstream 500s?
*   **Edge Cases:** Negative amounts, zero amounts, concurrent requests, duplicate webhooks.
*   **Quality:** Assertions must be meaningful.

## 6. Performance
*   **Database:** N+1 queries, missing indexes, efficient pagination.
*   **Connection Management:** Connection pool sizing, potential leaks.
*   **Caching:** Is cache invalidation handled correctly? (Stale data risk).