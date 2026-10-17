# User Stories & Acceptance Criteria (Gherkin)
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

Each user story follows the format:
*As a `<role>`, I want `<capability>`, so that `<benefit>`.*
Acceptance criteria are written in Gherkin (Given / When / Then) so they can be
reused directly as the basis for UAT test cases in Project 2.

| ID | Story | Priority | Linked requirements | UAT test cases |
|----|-------|----------|---------------------|----------------|
| US-01 | Initiate an instant transfer | Must | FR-01, FR-02 | TC-001, TC-002 |
| US-02 | Transfer to a new beneficiary | Must | FR-01, FR-10, BR-RULE-09 | TC-003, TC-004 |
| US-03 | On-us instant transfer | Must | FR-03, FR-06 | TC-005 |
| US-04 | Off-us instant transfer | Must | FR-03, FR-06 | TC-006, TC-007 |
| US-05 | Enforce limits and balance | Must | FR-04, BR-RULE-01, BR-RULE-02, BR-RULE-03 | TC-008, TC-009, TC-010 |
| US-06 | Real-time fraud screening | Must | FR-05, BR-RULE-05 | TC-011, TC-012 |
| US-07 | Receive transfer notifications | Must | FR-07 | TC-013 |
| US-08 | Handle failed/returned transfers | Must | FR-09, BR-RULE-07 | TC-014, TC-015 |
| US-09 | View transfer history and receipts | Should | FR-08 | TC-016 |
| US-10 | Operations resolve stuck transfers | Should | FR-12, BR-RULE-06 | TC-017, TC-018 |

---

## US-01 — Initiate an instant transfer

**As a** retail customer, **I want** to send money instantly to a beneficiary,
**so that** the money arrives within seconds instead of hours.

**Priority:** Must · **Linked:** FR-01, FR-02

```gherkin
Feature: Initiate an instant transfer

  Scenario: Successful transfer to a saved beneficiary
    Given I am an authenticated customer with a funded eligible account
    And the beneficiary "Maria Lopez" is saved and active
    When I submit an instant transfer of 250.00 to "Maria Lopez"
    Then the transfer is accepted for processing
    And the amount is debited from my available balance
    And I see a confirmation with a unique transfer reference

  Scenario: Insufficient available balance
    Given I am an authenticated customer with an available balance of 100.00
    When I submit an instant transfer of 150.00
    Then the transfer is rejected
    And I see the message "Insufficient available balance"
    And no amount is debited from my account
```

---

## US-02 — Transfer to a new beneficiary

**As a** retail customer, **I want** to add and pay a new beneficiary in one
flow, **so that** I can pay someone without leaving the transfer journey.

**Priority:** Must · **Linked:** FR-01, FR-10, BR-RULE-09

```gherkin
Feature: New beneficiary

  Scenario: Add a new beneficiary with re-authentication
    Given I am an authenticated customer
    When I add a new beneficiary with valid account details
    Then I am asked to re-authenticate
    And after successful re-authentication the beneficiary is saved
    And the beneficiary is available for future transfers

  Scenario: Beneficiary flagged by sanctions screening
    Given I add a beneficiary that matches a sanctions list entry
    When the screening completes
    Then the beneficiary is blocked
    And I see the message "We cannot process transfers to this beneficiary"
    And the event is reported to Compliance
```

---

## US-03 — On-us instant transfer

**As a** retail customer, **I want** transfers to another NovaBank customer to
settle instantly, **so that** funds are available immediately.

**Priority:** Must · **Linked:** FR-03, FR-06

```gherkin
Feature: On-us transfer

  Scenario: On-us transfer settles in seconds
    Given both the sender and beneficiary hold NovaBank accounts
    When I submit a valid instant transfer
    Then the transfer settles in under 10 seconds
    And the beneficiary's balance increases by the transferred amount
    And the transfer status is "Completed"
```

---

## US-04 — Off-us instant transfer

**As a** retail customer, **I want** to send money to an account at another
bank instantly, **so that** I can pay anyone, not only NovaBank customers.

**Priority:** Must · **Linked:** FR-03, FR-06

```gherkin
Feature: Off-us transfer

  Scenario: Off-us transfer accepted by the rail
    Given the beneficiary account is held at another participating bank
    When I submit a valid instant transfer
    Then the system submits the transfer to the real-time rail
    And on rail acknowledgement the transfer status is "Completed"

  Scenario: Rail timeout
    Given the beneficiary account is held at another bank
    When the real-time rail does not acknowledge within 30 seconds
    Then the transfer status is "Pending"
    And the transfer is queued for reconciliation by Payments Operations
    And I am notified that the transfer is pending
```

---

## US-05 — Enforce limits and available balance

**As a** bank, **I want** transfers to respect limits and balance, **so that**
customers cannot overspend or exceed scheme rules.

**Priority:** Must · **Linked:** FR-04, BR-RULE-01, BR-RULE-02, BR-RULE-03

```gherkin
Feature: Limits and balance

  Scenario Outline: Enforce limits
    Given my available balance is <balance>
    And my remaining daily limit is <daily_limit>
    When I submit a transfer of <amount>
    Then the outcome is <outcome>

    Examples:
      | balance | daily_limit | amount  | outcome |
      | 1000.00 | 5000.00     | 0.50    | rejected for being below the minimum amount |
      | 1000.00 | 5000.00     | 2000.00 | rejected for exceeding available balance |
      | 1000.00 | 5000.00     | 100.00  | accepted |
      | 1000.00 |   50.00     | 100.00  | rejected for exceeding the daily limit |

  Scenario: Customer configures a lower personal limit
    Given my bank daily limit is 20000.00
    When I set a personal daily limit of 2000.00
    Then transfers above 2000.00 within the same day are rejected
    And the new limit is confirmed to me
```

---

## US-06 — Real-time fraud screening

**As a** Fraud & Risk analyst, **I want** every transfer screened in real time,
**so that** fraudulent payments are held before settlement.

**Priority:** Must · **Linked:** FR-05, BR-RULE-05

```gherkin
Feature: Fraud screening

  Scenario: Low-risk transfer passes
    Given the fraud engine scores the transfer as low risk
    When I submit the transfer
    Then the transfer proceeds to settlement without additional checks

  Scenario: High-risk transfer is held
    Given the fraud engine scores the transfer as high risk
    When I submit the transfer
    Then the transfer status is "Held for review"
    And the funds are not debited
    And I am notified that the transfer is under review
```

---

## US-07 — Receive transfer notifications

**As a** retail customer, **I want** to be notified of the transfer outcome,
**so that** I know whether my money arrived.

**Priority:** Must · **Linked:** FR-07

```gherkin
Feature: Notifications

  Scenario: Successful transfer notification
    Given I have a registered device and email
    When my transfer settles successfully
    Then I receive a push notification and an email
    And the notification includes the amount, beneficiary and reference

  Scenario: Failed transfer notification
    Given I have a registered device and email
    When my transfer is rejected
    Then I receive a notification stating the reason
```

---

## US-08 — Handle failed and returned transfers

**As a** retail customer, **I want** returned funds credited back automatically,
**so that** I do not lose money when a transfer fails.

**Priority:** Must · **Linked:** FR-09, BR-RULE-07

```gherkin
Feature: Failed and returned transfers

  Scenario: Rejected by the rail
    Given the real-time rail rejects the transfer
    When the rejection is received
    Then the transfer status is "Rejected"
    And no funds are debited from my account
    And I am notified with the rejection reason

  Scenario: Returned after settlement
    Given a settled transfer is returned by the receiving bank
    When the return is processed
    Then the funds are credited back to my account within 1 business day
    And I am notified of the return
```

---

## US-09 — View transfer history and receipts

**As a** retail customer, **I want** to see my transfer history and download
receipts, **so that** I can track and prove my payments.

**Priority:** Should · **Linked:** FR-08

```gherkin
Feature: Transfer history

  Scenario: Filter transfer history
    Given I have completed several transfers
    When I open my transfer history and filter by status "Completed"
    Then only completed transfers are listed
    And each entry shows date, beneficiary, amount and status

  Scenario: Download a receipt
    Given a completed transfer is listed
    When I request the receipt
    Then I receive a document with the transfer reference, amount and timestamp
```

---

## US-10 — Operations resolve stuck transfers

**As a** Payments Operations analyst, **I want** to search and resolve stuck
transfers, **so that** pending transactions do not remain unresolved.

**Priority:** Should · **Linked:** FR-12, BR-RULE-06

```gherkin
Feature: Operations back-office

  Scenario: Search pending transfers
    Given I am an authenticated operations user
    When I filter transfers by status "Pending" and age greater than 5 minutes
    Then the matching transfers are listed with their references

  Scenario: Manually resolve a pending transfer
    Given a transfer has a "Pending" status
    When I confirm it was not settled at the rail
    Then I mark the transfer as "Rejected"
    And the funds are released back to the customer
```

> All scenarios are fictional and for demonstration purposes only.
