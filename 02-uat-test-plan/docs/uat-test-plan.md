# UAT Test Plan
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

## 1. Document control

| Field | Value |
|-------|-------|
| Document ID | NB-UAT-002 |
| Version | 1.0 |
| Status | Executed |
| Author | QA / UAT Lead (Portfolio) |
| Reviewed by | Product Owner — Retail Payments |
| Date | 2026-10-24 |
| Related documents | NB-BRD-001 (BRD), NB-RTM-001 (Traceability Matrix) |

## 2. Purpose

This plan defines how **User Acceptance Testing** for the Instant Transfers
feature will be conducted to confirm that the solution meets the business
requirements defined in the BRD (NB-BRD-001) and is fit for release.

## 3. Scope

### 3.1 In scope

- Initiating on-us and off-us instant transfers.
- Beneficiary management and re-authentication.
- Limits, minimum amounts and available-balance controls.
- Real-time fraud and sanctions screening behaviour.
- Notifications, transfer history and receipts.
- Handling of rejected, returned and pending (timeout) transfers.
- Operations back-office search and manual resolution.

### 3.2 Out of scope

- Scheduled/recurring transfers.
- Corporate and bulk payments.
- Cross-border remittances.
- Performance and load testing beyond the non-functional acceptance checks (covered by a separate performance test).

## 4. Test approach

- **Type:** Business-facing user acceptance testing (black-box), complemented by integration checks against the real-time rail simulator.
- **Design technique:** Scenario-based, using the Gherkin acceptance criteria from Project 1. Equivalence partitioning and boundary value analysis for amount and limit rules.
- **Coverage:** Each functional requirement (FR-01..FR-12) is covered by at least one test case; every Must-have requirement is covered.
- **Execution:** Manual execution by business users in a UAT environment with realistic (fictitious) accounts and data.
- **Defect management:** Defects are raised in the defect log, triaged daily and classified by severity.

## 5. Test environment and data

| Item | Detail |
|------|--------|
| Environment | UAT-2 (mirrors production configuration) |
| Channels | NovaBank mobile app (iOS/Android) and online banking |
| Rail | Real-time payment rail **simulator** |
| Fraud engine | UAT instance with configurable risk rules |
| Test data | 5 fictitious customers, 10 accounts, 20 beneficiaries (company prefixes `NB-UAT-`) |
| Data privacy | 100% fictitious data; no production data is used |

## 6. Roles and responsibilities

| Role | Responsibility |
|------|----------------|
| UAT Lead | Plans and coordinates execution, maintains the test case matrix, chairs defect triage. |
| Business testers | Execute test cases and record actual results. |
| BA | Clarifies requirements and expected behaviour. |
| Developers | Fix defects and provide builds for retest. |
| Product Owner | Approves exit and sign-off decisions. |

## 7. Entry criteria

- BRD and user stories approved and baselined.
- UAT build deployed to UAT-2 and smoke test passed.
- Test data prepared.
- Test cases reviewed and approved.

## 8. Exit criteria

See [exit-criteria.md](exit-criteria.md). In summary:

- 100% of test cases executed (or explicitly deferred with approval).
- 0 open defects of Critical or Major severity.
- ≥ 95% pass rate on executed Must-have scope.
- No open defect blocks the core success scenarios.

## 9. Test schedule (fictitious)

| Phase | Dates | Activity |
|-------|-------|----------|
| Preparation | 2026-10-17 → 2026-10-19 | Test cases review, data setup, environment check |
| Execution cycle 1 | 2026-10-20 → 2026-10-22 | Full test execution, defect logging |
| Retest cycle | 2026-10-23 → 2026-10-24 | Retest fixes, regression on affected areas |
| Sign-off | 2026-10-24 | Exit review and decision |

## 10. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Rail simulator instability blocks off-us tests | Coordinator prioritises on-us tests and schedules off-us on stable slots |
| Limited access to fraud-engine test settings | Pre-agree rule profiles with Fraud & Risk before execution |
| Test data collisions | Use unique company prefixes per tester |
| Compressed schedule | Focus first on Must-have requirements; defer Could-items |

## 11. Test case summary

| Test case | Title | Priority | Type |
|-----------|-------|----------|------|
| TC-001 | Complete transfer to a saved beneficiary | P1 | Functional |
| TC-002 | Reject transfer with insufficient balance | P1 | Negative |
| TC-003 | Add a new beneficiary with re-authentication | P1 | Functional |
| TC-004 | Block beneficiary failing sanctions screening | P1 | Security |
| TC-005 | On-us transfer settles in under 10 seconds | P1 | Non-functional |
| TC-006 | Off-us transfer accepted by the rail | P1 | Integration |
| TC-007 | Off-us transfer rail timeout becomes Pending | P1 | Negative |
| TC-008 | Reject amount below the minimum | P2 | Negative |
| TC-009 | Reject amount above available balance | P1 | Negative |
| TC-010 | Enforce and configure daily limits | P1 | Functional |
| TC-011 | Low-risk transfer passes fraud screening | P1 | Functional |
| TC-012 | High-risk transfer held for review | P1 | Functional |
| TC-013 | Customer receives outcome notification | P2 | Functional |
| TC-014 | Rail rejection releases funds | P1 | Negative |
| TC-015 | Returned transfer credited within 1 business day | P1 | Integration |
| TC-016 | Filter history and download a receipt | P3 | UI |
| TC-017 | Operations search pending transfers | P2 | Functional |
| TC-018 | Operations manually resolve a pending transfer | P2 | Functional |

> All content is fictional and for portfolio demonstration purposes only.
