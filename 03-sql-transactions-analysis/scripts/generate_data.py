"""Generate the fictitious NovaBank SQLite database.

Creates data/novabank.db with four tables:
    customers, accounts, channels, transactions

The dataset is 100% fictitious and reproducible (fixed random seed).

Usage:
    python scripts/generate_data.py
"""

import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

SEED = 42
AS_OF = datetime(2026, 10, 17, 12, 0, 0)
HISTORY_DAYS = 180

N_CUSTOMERS = 3000
N_ACCOUNTS = 5000
N_TRANSACTIONS = 50000

CITIES = [
    "Northport", "Westbrook", "Lakeview", "Rivergate",
    "Hillcrest", "Suncity", "Baytown", "Fernwood",
]
COUNTRY = "Novaland"
BANKS = [
    "NovaBank", "Union Trust Bank", "Metro Savings",
    "Coastal Credit", "Pioneer Bank", "Sterling Financial",
]
SEGMENTS = ["Retail", "Premium", "SME"]
ACCOUNT_TYPES = ["Checking", "Savings", "Wallet"]
CURRENCY = "USD"

CHANNELS = [
    (1, "Mobile App", "Digital"),
    (2, "Online Banking", "Digital"),
    (3, "Open API / Partner", "Digital"),
    (4, "ATM", "Self-service"),
    (5, "Branch", "Assisted"),
    (6, "Contact Centre", "Assisted"),
]

STATUS_WEIGHTS = [
    ("Completed", 0.88),
    ("Pending", 0.05),
    ("Rejected", 0.04),
    ("Returned", 0.02),
    ("Held for review", 0.01),
]
FAILURE_REASONS = {
    "Rejected": [
        "Insufficient available balance",
        "Beneficiary account closed",
        "Exceeds daily limit",
        "Sanctions screening match",
    ],
    "Returned": [
        "Beneficiary account not found",
        "Receiving bank returned funds",
    ],
    "Held for review": [
        "High fraud risk score",
        "Manual review required",
    ],
    "Pending": [
        "Rail timeout",
        "Awaiting reconciliation",
    ],
}

DDL = """
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id     TEXT PRIMARY KEY,
    full_name       TEXT NOT NULL,
    segment         TEXT NOT NULL,
    city            TEXT NOT NULL,
    country         TEXT NOT NULL,
    birth_date      TEXT NOT NULL,
    onboarding_date TEXT NOT NULL,
    status          TEXT NOT NULL
);

CREATE TABLE accounts (
    account_id     TEXT PRIMARY KEY,
    customer_id    TEXT NOT NULL REFERENCES customers(customer_id),
    account_type   TEXT NOT NULL,
    currency       TEXT NOT NULL,
    balance        REAL NOT NULL,
    credit_limit   REAL NOT NULL,
    open_date      TEXT NOT NULL,
    status         TEXT NOT NULL,
    is_primary     INTEGER NOT NULL
);

CREATE TABLE channels (
    channel_id    INTEGER PRIMARY KEY,
    channel_name  TEXT NOT NULL,
    channel_group TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id       TEXT PRIMARY KEY,
    account_id           TEXT NOT NULL REFERENCES accounts(account_id),
    channel_id           INTEGER NOT NULL REFERENCES channels(channel_id),
    direction            TEXT NOT NULL,
    transfer_type        TEXT NOT NULL,
    counterparty_name    TEXT NOT NULL,
    counterparty_bank    TEXT NOT NULL,
    is_internal          INTEGER NOT NULL,
    amount               REAL NOT NULL,
    currency             TEXT NOT NULL,
    fee                  REAL NOT NULL,
    status               TEXT NOT NULL,
    failure_reason       TEXT,
    fraud_score          REAL NOT NULL,
    is_flagged_fraud     INTEGER NOT NULL,
    created_at           TEXT NOT NULL,
    settled_at           TEXT,
    settlement_seconds   INTEGER
);

CREATE INDEX idx_tx_account ON transactions(account_id);
CREATE INDEX idx_tx_created ON transactions(created_at);
CREATE INDEX idx_tx_status ON transactions(status);
CREATE INDEX idx_acc_customer ON accounts(customer_id);
"""


def weighted_choice(rng, options, weights):
    return rng.choices(options, weights=weights, k=1)[0]


def main() -> None:
    rng = random.Random(SEED)
    fake = Faker("en_US")
    Faker.seed(SEED)

    db_path = Path(__file__).resolve().parent.parent / "data" / "novabank.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(DDL)

    # --- Channels ---------------------------------------------------------
    cur.executemany(
        "INSERT INTO channels (channel_id, channel_name, channel_group) VALUES (?, ?, ?)",
        CHANNELS,
    )

    # --- Customers --------------------------------------------------------
    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        cid = f"CUST-{i:05d}"
        segment = weighted_choice(rng, SEGMENTS, [0.80, 0.15, 0.05])
        onboarding = AS_OF - timedelta(days=rng.randint(30, 3650))
        birth = AS_OF - timedelta(days=rng.randint(6570, 25550))
        status = weighted_choice(rng, ["Active", "Dormant", "Closed"], [0.90, 0.07, 0.03])
        customers.append(
            (
                cid,
                fake.name(),
                segment,
                rng.choice(CITIES),
                COUNTRY,
                birth.strftime("%Y-%m-%d"),
                onboarding.strftime("%Y-%m-%d"),
                status,
            )
        )
    cur.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", customers
    )

    # --- Accounts ---------------------------------------------------------
    accounts = []
    account_ids = []
    for i in range(1, N_ACCOUNTS + 1):
        aid = f"ACC-{i:05d}"
        customer = customers[rng.randint(0, N_CUSTOMERS - 1)]
        cid = customer[0]
        acc_type = weighted_choice(rng, ACCOUNT_TYPES, [0.60, 0.30, 0.10])
        balance = round(rng.lognormvariate(6.5, 1.1), 2)
        credit_limit = round(rng.choice([0, 0, 0, 500, 1000, 2500]), 2)
        open_date = datetime.strptime(customer[6], "%Y-%m-%d")
        open_date = open_date + timedelta(days=rng.randint(0, 30))
        accounts.append(
            (
                aid,
                cid,
                acc_type,
                CURRENCY,
                balance,
                credit_limit,
                open_date.strftime("%Y-%m-%d"),
                customer[7] if customer[7] != "Closed" else "Closed",
                1 if i <= N_CUSTOMERS else 0,
            )
        )
        account_ids.append(aid)
    cur.executemany(
        "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", accounts
    )

    # customer name lookup for counterparties
    name_by_id = {c[0]: c[1] for c in customers}

    # --- Transactions -----------------------------------------------------
    channel_weights = [0.52, 0.26, 0.05, 0.08, 0.06, 0.03]
    channel_ids = [c[0] for c in CHANNELS]
    transactions = []
    for i in range(1, N_TRANSACTIONS + 1):
        tid = f"TRN-{i:07d}"
        aid = rng.choice(account_ids)
        channel_id = weighted_choice(rng, channel_ids, channel_weights)
        transfer_type = weighted_choice(rng, ["Instant", "Batch"], [0.55, 0.45])
        direction = weighted_choice(rng, ["Debit", "Credit"], [0.72, 0.28])

        if rng.random() < 0.65:
            counterparty_bank = "NovaBank"
            counterparty_name = name_by_id[rng.choice(customers)[0]]
            is_internal = 1
        else:
            counterparty_bank = rng.choice([b for b in BANKS if b != "NovaBank"])
            counterparty_name = fake.name()
            is_internal = 0

        if transfer_type == "Instant":
            amount = round(rng.lognormvariate(4.8, 1.0), 2)
            fee = 0.0
        else:
            amount = round(rng.lognormvariate(6.1, 1.1), 2)
            fee = round(rng.choice([0.0, 0.5, 1.0, 1.5]), 2)

        status = weighted_choice(
            rng, [s for s, _ in STATUS_WEIGHTS], [w for _, w in STATUS_WEIGHTS]
        )
        failure_reason = None
        if status in FAILURE_REASONS:
            failure_reason = rng.choice(FAILURE_REASONS[status])

        if rng.random() < 0.02:
            fraud_score = round(rng.uniform(0.80, 0.99), 3)
        else:
            fraud_score = round(rng.uniform(0.0, 0.50), 3)
        is_flagged = 1 if fraud_score >= 0.80 else 0
        if is_flagged and status == "Completed" and rng.random() < 0.55:
            status = "Held for review"
            failure_reason = "High fraud risk score"

        created = AS_OF - timedelta(
            days=rng.randint(0, HISTORY_DAYS - 1),
            hours=rng.randint(0, 23),
            minutes=rng.randint(0, 59),
            seconds=rng.randint(0, 59),
        )

        settled_at = None
        settlement_seconds = None
        if status == "Completed":
            if transfer_type == "Instant":
                settlement_seconds = rng.randint(2, 9)
            else:
                settlement_seconds = rng.randint(3600, 86400)
            settled = created + timedelta(seconds=settlement_seconds)
            settled_at = settled.strftime("%Y-%m-%d %H:%M:%S")

        transactions.append(
            (
                tid,
                aid,
                channel_id,
                direction,
                transfer_type,
                counterparty_name,
                counterparty_bank,
                is_internal,
                amount,
                CURRENCY,
                fee,
                status,
                failure_reason,
                fraud_score,
                is_flagged,
                created.strftime("%Y-%m-%d %H:%M:%S"),
                settled_at,
                settlement_seconds,
            )
        )
    cur.executemany(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        transactions,
    )

    conn.commit()
    cur.execute("ANALYZE")
    conn.commit()
    conn.close()

    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"Wrote {db_path}")
    print(f"  customers={N_CUSTOMERS} accounts={N_ACCOUNTS} transactions={N_TRANSACTIONS}")
    print(f"  size={size_mb:.2f} MB")


if __name__ == "__main__":
    main()
