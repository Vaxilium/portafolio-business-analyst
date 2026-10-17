# Requirements Traceability Matrix (RTM)
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

This matrix links **business objectives → functional requirements → user
stories → acceptance criteria → UAT test cases**. The UAT test case IDs
(`TC-xxx`) are implemented in [Project 2 — UAT Test Plan](../../02-uat-test-plan/).

## 1. Objective → Requirement

| Objective | Functional requirements |
|-----------|-------------------------|
| OBJ-01 Deliver real-time transfers | FR-03, FR-06 |
| OBJ-02 Reduce support contacts | FR-07, FR-08 |
| OBJ-03 Improve customer satisfaction | FR-01, FR-02, FR-10 |
| OBJ-04 Keep fraud losses under control | FR-05 |
| OBJ-05 Drive adoption | FR-04, FR-11 |

## 2. Requirement → User Story → Acceptance Criteria → Test Case

| Req. ID | Requirement (short) | User story | Acceptance criteria (scenario) | UAT test cases | Priority |
|---------|---------------------|-----------|--------------------------------|----------------|----------|
| FR-01 | Initiate an instant transfer | US-01 | Successful transfer to a saved beneficiary | TC-001, TC-002 | Must |
| FR-02 | Validate beneficiary details | US-01 | Insufficient available balance | TC-002 | Must |
| FR-03 | Support on-us and off-us transfers | US-03, US-04 | On-us settles in seconds · Off-us accepted by rail | TC-005, TC-006 | Must |
| FR-04 | Enforce limits and balance | US-05 | Enforce limits (outline) · Personal lower limit | TC-008, TC-009, TC-010 | Must |
| FR-05 | Real-time fraud screening | US-06 | Low-risk passes · High-risk held | TC-011, TC-012 | Must |
| FR-06 | Settle within 10 seconds | US-03, US-04 | On-us settles in seconds · Rail timeout | TC-005, TC-007 | Must |
| FR-07 | Receive notifications | US-07 | Successful · Failed notification | TC-013 | Must |
| FR-08 | Transfer history and receipts | US-09 | Filter history · Download receipt | TC-016 | Should |
| FR-09 | Handle failed/returned transfers | US-08 | Rejected by rail · Returned after settlement | TC-014, TC-015 | Must |
| FR-10 | Manage beneficiaries | US-02 | Add new beneficiary with re-authentication | TC-003, TC-004 | Should |
| FR-11 | Customer-configurable lower limit | US-05 | Customer configures a lower personal limit | TC-010 | Could |
| FR-12 | Operations back-office | US-10 | Search pending · Manually resolve | TC-017, TC-018 | Should |

## 3. Test case index (used by Project 2)

| Test case | Title | User story | Requirement |
|-----------|-------|-----------|-------------|
| TC-001 | Complete transfer to a saved beneficiary | US-01 | FR-01 |
| TC-002 | Reject transfer with insufficient balance | US-01 | FR-01, FR-02 |
| TC-003 | Add a new beneficiary with re-authentication | US-02 | FR-01, FR-10 |
| TC-004 | Block beneficiary failing sanctions screening | US-02 | FR-10, BR-RULE-04, BR-RULE-10 |
| TC-005 | On-us transfer settles in under 10 seconds | US-03 | FR-03, FR-06 |
| TC-006 | Off-us transfer accepted by the rail | US-04 | FR-03 |
| TC-007 | Off-us transfer rail timeout becomes Pending | US-04 | FR-06, BR-RULE-06 |
| TC-008 | Reject amount below the minimum | US-05 | FR-04, BR-RULE-01 |
| TC-009 | Reject amount above available balance | US-05 | FR-04, BR-RULE-03 |
| TC-010 | Enforce and configure daily limits | US-05 | FR-04, FR-11, BR-RULE-02 |
| TC-011 | Low-risk transfer passes fraud screening | US-06 | FR-05 |
| TC-012 | High-risk transfer held for review | US-06 | FR-05, BR-RULE-05 |
| TC-013 | Customer receives outcome notification | US-07 | FR-07 |
| TC-014 | Rail rejection releases funds | US-08 | FR-09 |
| TC-015 | Returned transfer credited within 1 business day | US-08 | FR-09, BR-RULE-07 |
| TC-016 | Filter history and download a receipt | US-09 | FR-08 |
| TC-017 | Operations search pending transfers | US-10 | FR-12 |
| TC-018 | Operations manually resolve a pending transfer | US-10 | FR-12, BR-RULE-06 |

## 4. Coverage summary

| Coverage dimension | Result |
|--------------------|--------|
| Functional requirements covered by ≥ 1 user story | 12 / 12 (100%) |
| User stories with acceptance criteria | 10 / 10 (100%) |
| User stories traced to UAT test cases | 10 / 10 (100%) |
| Must-have requirements covered | 9 / 9 (100%) |

> This traceability matrix is fictional and used for portfolio demonstration purposes only.
