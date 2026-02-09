# 🏗️ Senior Engineering Manager Review (Mission Critical)

**Date:** {{DATE}}
**Project:** {{PROJECT_NAME}}
**Overall Status:** {{STATUS_EMOJI}} (e.g. 🟢 Healthy / 🟡 Concerns / 🔴 Critical)

---

##  EXECUTIVE SUMMARY

{{Provide a high-level paragraph summarizing the state of the codebase. Focus on **Risk** and **Reliability**. Is this system safe to process millions of dollars? Address the "engineered enough" balance.}}

---

## 🔍 DETAILED AUDIT

### 1. Architecture & Reliability
{{Summary of architectural health, resiliency patterns (circuit breakers, timeouts), and idempotency.}}

### 2. Data Integrity (Payments)
{{Summary of how money/state is handled. Locking, Transactions, Precision.}}

### 3. Code Quality & Tech Debt
{{Summary of code structure, DRY, and maintainability.}}

### 4. Observability
{{Summary of logging, metrics, and tracing.}}

### 5. Tests
{{Summary of testing maturity, especially regarding failure modes and edge cases.}}

### 6. Performance
{{Summary of database and throughput characteristics.}}

---

## 🚨 IDENTIFIED ISSUES & RECOMMENDATIONS

{{Repeat the block below for each specific issue found}}

### Issue #{{N}}: {{Concise Title of Issue}}
**Severity:** {{High/Medium/Low}} | **Category:** {{Reliability/Integrity/Quality/Test/Perf}}
**Location:** `{{FILE_PATH}}:{{LINE_NUMBER}}`

**Problem:**
{{Concrete description of the bug, smell, or design flaw. Be specific.}}

**Options:**
1.  **Do Nothing:**
    *   *Effort:* None
    *   *Risk:* {{Risk details}}
    *   *Maintenance:* {{Maintenance impact}}
2.  **{{Option 2 Name}}:**
    *   *Effort:* {{Low/Med/High}}
    *   *Risk:* {{Risk details}}
    *   *Impact:* {{Impact details}}
    *   *Maintenance:* {{Maintenance impact}}
3.  **{{Option 3 Name}}:**
    *   *Effort:* {{Low/Med/High}}
    *   *Risk:* {{Risk details}}
    *   *Impact:* {{Impact details}}
    *   *Maintenance:* {{Maintenance impact}}

**🏆 Recommendation:**
**{{Selected Option}}**
*Reasoning:* {{Explain why this is the best path. Reference "Safety First", "Idempotency", or "Data Integrity".}}

---

## ✅ ACTION ITEMS

- [ ] {{Action Item 1}}
- [ ] {{Action Item 2}}

---

**Manager Decision:**
Do you agree with these recommendations? (Reply "Yes" to proceed with the highest priority fixes, or specify a different direction).