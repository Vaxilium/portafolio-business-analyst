# Business Requirements Document (BRD)
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

## 1. Document control

| Field | Value |
|-------|-------|
| Document ID | NB-BRD-001 |
| Version | 1.0 |
| Status | Approved for UAT design |
| Author | Business Analyst (Portfolio) |
| Reviewer | Product Owner — Retail Payments |
| Date | 2026-10-17 |
| Related projects | NB-UAT-002 (Test Plan), NB-SQL-003 (Data Analysis) |

### Revision history

| Version | Date | Description | Author |
|---------|------|-------------|--------|
| 0.1 | 2026-10-05 | Initial draft (scope and objectives) | BA |
| 0.2 | 2026-10-09 | Added business rules and NFRs after SME review | BA |
| 0.3 | 2026-10-14 | Added risks, assumptions and traceability links | BA |
| 1.0 | 2026-10-17 | Baseline approved for UAT design | BA |

## 2. Executive summary

NovaBank Retail offers domestic transfers that are settled in batches, with
cut-off times during business hours. Customers increasingly expect payments to
arrive in seconds, at any time. **Instant Transfers** will let customers send
money in real time, 24/7, to accounts inside NovaBank and to other banks over
the domestic real-time payment rail.

This document defines the business context, scope, functional and
non-functional requirements, business rules and risks. It is the baseline for
the UAT test plan (Project 2) and for the SQL transaction analysis (Project 3).

## 3. Business context and problem statement

**Problem:** Batched transfers create a poor customer experience — funds take
hours (or until the next business day) to arrive, transfers initiated after the
cut-off time queue overnight, and customers call support to know the status.

**Evidence (fictional):**
- 38% of surveyed customers say transfer speed is their top frustration.
- 22% of monthly support tickets are "where is my transfer?" enquiries.
- 15% of transfers initiated after cut-off are abandoned.

**Opportunity:** A real-time rail reduces inbound support contacts, increases
customer satisfaction (CSAT) and creates a differentiator versus peers.

## 4. Objectives and success metrics

| ID | Objective | Metric | Target |
|----|-----------|--------|--------|
| OBJ-01 | Deliver real-time transfers | % of eligible transfers settled < 10 seconds | ≥ 95% |
| OBJ-02 | Reduce transfer-related support contacts | "Where is my transfer?" tickets per 1,000 transfers | −40% |
| OBJ-03 | Improve customer satisfaction | CSAT for transfer journeys | ≥ 4.5 / 5 |
| OBJ-04 | Maintain fraud losses under control | Confirmed fraud loss as % of instant transfer value | ≤ 0.02% |
| OBJ-05 | Drive adoption | Monthly active customers using instant transfers | ≥ 25% of digital base in 6 months |

## 5. Scope

### 5.1 In scope

- Initiating instant transfers from mobile app and online banking.
- Transfers between NovaBank accounts (internal, on-us).
- Transfers to accounts at other banks via the domestic real-time rail (off-us).
- Beneficiary management (add, edit, delete, favourites).
- Velocity and value limits with customer-configurable sub-limits.
- Real-time fraud screening and risk-based holds.
- Transfer status tracking and push/email notifications.
- Handling of rejected, returned and timed-out transfers.
- Customer self-service transfer history and receipts.

### 5.2 Out of scope

- Corporate and bulk/batch payments.
- International and cross-border remittances.
- Scheduled and recurring transfers (covered by a separate initiative).
- Credit, overdraft and lending products.
- Changes to the underlying real-time rail (external provider).

### 5.3 Assumptions

- The domestic real-time payment rail exposes an API that supports on-us and off-us credit transfers with synchronous acknowledgements.
- The fraud engine can score a transfer in under 500 ms.
- Mobile app and online banking can be updated to expose the new journey.
- Customers have at least one eligible debit account.

### 5.4 Constraints

- Regulatory requirement to screen beneficiaries against sanctions lists.
- Limits defined by the payments scheme must be enforced.
- The feature must be available 24/7 with planned maintenance windows ≤ 2 hours/month.

### 5.5 Dependencies

- Real-time payment rail provider (external).
- Fraud and AML engine (internal, existing).
- Notification service (push/email/SMS).
- Core banking ledger for real-time posting and balance update.

## 6. Stakeholders

| ID | Stakeholder | Role | Interest |
|----|-------------|------|----------|
| STK-01 | Retail Customers | End users | Fast, reliable, transparent transfers |
| STK-02 | Product Owner — Retail Payments | Business owner | Delivery of the feature and adoption targets |
| STK-03 | Payments Operations | Operations | Handle exceptions, returns and reconciliations |
| STK-04 | Fraud & Risk | Risk control | Prevent fraud without harming legitimate customers |
| STK-05 | Compliance / AML | Regulatory | Sanctions and AML screening adherence |
| STK-06 | IT / Engineering | Delivery | Build and integrate the solution |
| STK-07 | Customer Support | Front line | Resolve customer enquiries and complaints |
| STK-08 | Finance / Treasury | Funding & settlement | Liquidity and scheme settlement |

## 7. Functional requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | The system shall allow an authenticated customer to initiate an instant transfer to a saved or new beneficiary. | Must |
| FR-02 | The system shall validate beneficiary account details (account number, bank code) in real time before confirmation. | Must |
| FR-03 | The system shall support on-us transfers (both accounts at NovaBank) and off-us transfers (beneficiary at another bank). | Must |
| FR-04 | The system shall display applicable limits and prevent transfers exceeding available balance or velocity/value limits. | Must |
| FR-05 | The system shall screen each transfer against the fraud/AML engine before execution. | Must |
| FR-06 | The system shall submit the transfer to the real-time rail and confirm settlement within 10 seconds for 95% of transfers. | Must |
| FR-07 | The system shall notify the customer of the transfer outcome (success, rejected, pending) via push and email. | Must |
| FR-08 | The system shall provide a transfer history with status, timestamp, beneficiary and amount, and downloadable receipts. | Should |
| FR-09 | The system shall handle rejected, returned and timed-out transfers with an appropriate status and customer message. | Must |
| FR-10 | The system shall allow a customer to save, edit, delete and mark beneficiaries as favourites. | Should |
| FR-11 | The system shall allow a customer to configure a lower personal daily limit than the bank default. | Could |
| FR-12 | The system shall expose an operations back-office view to search, monitor and manually resolve stuck transfers. | Should |

## 8. Non-functional requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-01 | Performance | 95th percentile end-to-end latency for a successful transfer ≤ 10 seconds. |
| NFR-02 | Performance | Fraud scoring must return a decision in ≤ 500 ms. |
| NFR-03 | Availability | Service availability ≥ 99.9% measured monthly, 24/7. |
| NFR-04 | Scalability | Support 500 transfers per second at peak without degradation. |
| NFR-05 | Security | All traffic encrypted in transit (TLS 1.2+) and data encrypted at rest. |
| NFR-06 | Security | Strong customer authentication for transfers above the scheme contactless-style threshold. |
| NFR-07 | Auditability | Every transfer state change must be logged with actor, timestamp and reason, retained ≥ 5 years. |
| NFR-08 | Usability | A first-time user shall complete a transfer in ≤ 60 seconds without assistance. |
| NFR-09 | Compliance | Sanctions and AML screening for all beneficiaries as per regulatory policy. |
| NFR-10 | Recoverability | Failed rail connections must be retried idempotently without duplicate postings. |

## 9. Business rules

| ID | Rule |
|----|------|
| BR-RULE-01 | The minimum transfer amount is 1.00 (local currency unit). |
| BR-RULE-02 | The default per-transaction limit is 5,000 and the default daily limit is 20,000 unless the customer configures lower. |
| BR-RULE-03 | A transfer cannot exceed the available balance of the debit account. |
| BR-RULE-04 | Beneficiaries must pass sanctions screening before the first transfer to them. |
| BR-RULE-05 | Transfers flagged as high risk by the fraud engine are held for manual review and are not settled immediately. |
| BR-RULE-06 | A transfer that is not acknowledged by the rail within 30 seconds is marked "Pending" and reconciled by Payments Operations. |
| BR-RULE-07 | Returned funds are credited back to the debit account within 1 business day. |
| BR-RULE-08 | The same transfer request submitted twice (idempotency key) must settle only once. |
| BR-RULE-09 | Customers must re-authenticate when adding a new beneficiary for the first time. |
| BR-RULE-10 | Transfers to a sanctioned beneficiary are always blocked and reported to Compliance. |

## 10. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| RISK-01 | Rail downtime blocks instant settlement. | Medium | High | Graceful degradation to queued transfer with clear customer messaging. |
| RISK-02 | Fraud losses exceed target due to real-time settlement. | Medium | High | Real-time scoring, velocity limits and risk-based holds. |
| RISK-03 | Duplicate postings during retries. | Low | High | Idempotency keys and reconciliation controls. |
| RISK-04 | Poor UX reduces adoption. | Medium | Medium | Usability testing and ≤ 60 s completion target. |
| RISK-05 | Regulatory screening gaps. | Low | High | Mandatory sanctions screening and audit logging. |

## 11. Glossary

| Term | Definition |
|------|------------|
| On-us | Both sender and beneficiary accounts are held at NovaBank. |
| Off-us | The beneficiary account is held at another bank, reached via the rail. |
| Real-time rail | External domestic payment scheme that settles payments in seconds. |
| Velocity limit | Cap on the number or value of transfers over a period. |
| Idempotency key | Unique token ensuring a repeated request settles only once. |
| Cut-off time | Time after which batched transfers are processed the next business day. |

## 12. Approval

| Role | Name | Decision | Date |
|------|------|----------|------|
| Product Owner — Retail Payments | _<fictional name>_ | Approved | 2026-10-17 |
| Head of Fraud & Risk | _<fictional name>_ | Approved | 2026-10-17 |
| Compliance Officer | _<fictional name>_ | Approved | 2026-10-17 |

> This BRD is fictional and created for portfolio demonstration purposes only.
