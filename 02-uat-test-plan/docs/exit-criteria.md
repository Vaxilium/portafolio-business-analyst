# UAT Exit Criteria & Sign-off Decision
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

## 1. Purpose

This document defines the criteria that must be met for the Instant Transfers
feature to be accepted and released, and records the exit decision for the
current cycle.

## 2. Exit criteria

| ID | Criterion | Threshold | Met? |
|----|-----------|-----------|:----:|
| EC-01 | Test execution completed | 100% of planned test cases executed (or formally deferred) | Yes |
| EC-02 | Critical defects | 0 open | **No** (DEF-003 open) |
| EC-03 | Major defects | 0 open | **No** (DEF-001, DEF-002 open) |
| EC-04 | Pass rate on Must-have scope | ≥ 95% | **No** (72.2%) |
| EC-05 | No blocking defect on core success scenarios | 0 blockers | **No** (TC-012 blocked) |
| EC-06 | All requirements traced and verified | 100% traceability | Yes |
| EC-07 | Sign-off by Product Owner | Approved | Pending |

## 3. Defect thresholds by severity

| Severity | Allowed open at exit |
|----------|----------------------|
| Critical | 0 |
| Major | 0 |
| Minor | ≤ 2 (with agreed workaround and fix date) |
| Trivial | ≤ 3 (may be deferred to backlog) |

## 4. Exit decision

| Item | Value |
|------|-------|
| Decision | **Conditional fail — not released** |
| Reason | 1 Critical and 2 Major defects remain open; pass rate below the Must-have threshold. |
| Next step | Cycle 2 retest after fixes to DEF-001, DEF-002 and DEF-003, plus retest of DEF-004 and DEF-005. |
| Deferrable | DEF-006 (Trivial) may be deferred to backlog with Product Owner agreement. |

## 5. Retest scope (Cycle 2)

- **Mandatory retest:** TC-007 (DEF-001), TC-010 (DEF-002), TC-012 (DEF-003).
- **Optional/minor retest:** TC-013 (DEF-004), TC-016 (DEF-005).
- **Regression subset:** TC-001, TC-005, TC-006, TC-014 (core transfer and rails).

## 6. Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| UAT Lead | _<fictional name>_ | Recommends retest | 2026-10-24 |
| Product Owner — Retail Payments | _<fictional name>_ | Not signed off | 2026-10-24 |
| Head of Fraud & Risk | _<fictional name>_ | Blocked pending DEF-003 | 2026-10-24 |

> This document is fictional and used for portfolio demonstration purposes only.
