# UAT Test Results Report
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

## 1. Summary

| Field | Value |
|-------|-------|
| Document ID | NB-UAT-REP-002 |
| Version | 1.0 |
| Test cycle | Cycle 1 + retest (2026-10-20 → 2026-10-24) |
| Test cases planned | 18 |
| Executed | 18 |
| Passed | 13 |
| Failed | 4 |
| Blocked | 1 |
| Pass rate (executed) | 72.2% |
| Defects logged | 6 |
| Open defects (Cr/Major) | 3 |

## 2. Execution results

### 2.1 By status

| Status | Count | % | Test cases |
|--------|:-----:|:--:|------------|
| Passed | 13 | 72.2% | TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-008, TC-009, TC-011, TC-014, TC-015, TC-017, TC-018 |
| Failed | 4 | 22.2% | TC-007, TC-010, TC-013, TC-016 |
| Blocked | 1 | 5.6% | TC-012 |

### 2.2 By priority

| Priority | Total | Passed | Failed | Blocked |
|----------|:-----:|:------:|:------:|:-------:|
| P1 (High) | 11 | 8 | 2 | 1 |
| P2 (Medium) | 5 | 4 | 1 | 0 |
| P3 (Low) | 2 | 1 | 1 | 0 |

### 2.3 Requirement coverage

| Dimension | Result |
|-----------|--------|
| Functional requirements covered by executed tests | 12 / 12 (100%) |
| Must-have requirements verified | 9 / 12 executed; 3 have open defects |
| User stories with at least one executed test | 10 / 10 (100%) |

## 3. Defect analysis

### 3.1 By severity

| Severity | Count | Open | Defects |
|----------|:-----:|:----:|---------|
| Critical | 1 | 1 | DEF-003 |
| Major | 2 | 2 | DEF-001, DEF-002 |
| Minor | 2 | 1 | DEF-004, DEF-005 |
| Trivial | 1 | 1 | DEF-006 |

### 3.2 By status

| Status | Count |
|--------|:-----:|
| Open | 5 |
| In Progress | 1 |
| Fixed / Closed | 0 |

### 3.3 Key defects

| Defect | Severity | Impact |
|--------|----------|--------|
| DEF-003 | Critical | High-risk fraud hold scenario cannot be validated; contractual fraud control unverified. |
| DEF-002 | Major | Personal daily limit is not enforced → potential overspend and risk exposure. |
| DEF-001 | Major | Timed-out transfers are not marked Pending → manual reconciliation and poor customer experience. |
| DEF-004 | Minor | Missing push notification reduces transparency of transfer outcome. |
| DEF-005 | Minor | Receipt formatting issues affect the transfer history experience. |
| DEF-006 | Trivial | Error copy inconsistency; no functional impact. |

## 4. Observations

- Core happy-path scenarios (on-us and off-us transfers, beneficiary management, standard limits) pass reliably.
- Two functional gaps affect risk and limits enforcement (DEF-001, DEF-002): these are on the critical path for a banking payment feature and must be fixed before release.
- One critical control (high-risk fraud hold) could not be validated due to an environment limitation (DEF-003) and requires a retest.
- Notification and receipt issues are cosmetic-to-minor but visible to customers.

## 5. Conclusion

The feature is **not yet ready for release**. The happy path works, but 3 open
defects of Critical/Major severity breach the exit criteria defined for this
UAT. A retest cycle is required once DEF-001, DEF-002 and DEF-003 are resolved.

**Recommendation:** Conditional fail — proceed to **Cycle 2 retest** focused on
DEF-001, DEF-002, DEF-003 (functional) and DEF-004, DEF-005 (minor), then
re-run the affected test cases plus a regression subset.

> All names, figures and defects are fictional and for portfolio demonstration purposes only.
