# Process Diagrams — AS-IS and TO-BE
## Instant Transfers — NovaBank Retail Banking

> **Fictitious data, for demonstration purposes only.**

The diagrams below use [Mermaid](https://mermaid.js.org/) and render natively
on GitHub.

---

## 1. AS-IS process — Batched domestic transfer

Today, a customer transfer is queued and processed in batches around fixed
cut-off times, so funds can take hours or up to the next business day to
arrive. Customers often call support to check status.

```mermaid
flowchart TD
    A["Customer opens mobile app"] --> B["Selects Transfer"]
    B --> C["Enters beneficiary and amount"]
    C --> D["Confirms transfer"]
    D --> E{"Funds and limits OK?"}
    E -- "No" --> F["Show error to customer"]
    E -- "Yes" --> G{"Before daily cut-off?"}
    G -- "Yes" --> H["Transfer added to today's batch"]
    G -- "No" --> I["Transfer queued for next business day"]
    H --> J["Batch processed at cut-off"]
    I --> J
    J --> K["Funds settled hours later"]
    K --> L{"Customer unsure of status?"}
    L -- "Yes" --> M["Customer calls support"]
    L -- "No" --> N["Customer waits and checks later"]
    M --> O["Agent manually checks ledger"]
    O --> N
```

**Pain points (fictional):**
- Settlement takes hours; transfers after cut-off wait until the next business day.
- No reliable real-time status; customers call support ("where is my transfer?").
- Manual batch exceptions add operational effort.

---

## 2. TO-BE process — Instant Transfer

The target process executes the transfer in real time, with inline validation,
fraud screening and notifications, 24/7.

```mermaid
flowchart TD
    A["Customer initiates instant transfer"] --> B["Validate beneficiary details"]
    B --> C{"Sanctions screening passed?"}
    C -- "No" --> D["Block transfer and report to Compliance"]
    C -- "Yes" --> E{"Within limits and available balance?"}
    E -- "No" --> F["Reject with clear reason"]
    E -- "Yes" --> G["Fraud engine scoring"]
    G --> H{"Risk decision"}
    H -- "High risk" --> I["Hold for manual review and notify customer"]
    H -- "Low risk" --> J["Submit to real-time rail"]
    J --> K{"Acknowledged within 30 seconds?"}
    K -- "No" --> L["Set status Pending and queue for reconciliation"]
    K -- "Yes" --> M{"Rail accepted?"}
    M -- "Rejected" --> N["Set status Rejected and release funds"]
    M -- "Accepted" --> O["Settle in under 10 seconds"]
    O --> P["Notify customer and update history"]
    N --> P
    L --> Q["Operations reconciles pending transfer"]
    Q --> P
    I --> P
    D --> P
```

**Improvements over AS-IS:**
- Real-time settlement (target: < 10 s for 95% of transfers), 24/7.
- Inline validation, sanctions screening and fraud scoring before settlement.
- Proactive notifications reduce "where is my transfer?" support contacts.
- Automated reconciliation of pending transfers; only exceptions reach agents.

---

## 3. TO-BE sequence diagram — Off-us instant transfer

The sequence diagram shows the interaction between the customer, NovaBank and
the external real-time rail for an off-us transfer.

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant APP as NovaBank App
    participant VAL as Validation & Limits
    participant FRD as Fraud & AML Engine
    participant CORE as Core Banking Ledger
    participant RAIL as Real-time Payment Rail

    C->>APP: Initiate instant transfer
    APP->>VAL: Validate beneficiary, limits, balance
    VAL->>FRD: Screen beneficiary and score transfer
    alt High risk
        FRD-->>APP: Hold for review
        APP-->>C: Transfer under review
    else Low risk
        FRD-->>VAL: Low risk
        VAL->>CORE: Reserve funds on sender account
        VAL->>RAIL: Submit credit transfer
        alt Acknowledged and accepted
            RAIL-->>VAL: Accepted
            VAL->>CORE: Post settlement
            CORE-->>APP: Settlement confirmed
            APP-->>C: Completed notification
        else Timeout or rejected
            RAIL-->>VAL: No acknowledgement / rejected
            VAL->>CORE: Release reserved funds
            APP-->>C: Pending / rejected notification
        end
    end
```

> All process names and figures are fictional and for demonstration purposes only.
