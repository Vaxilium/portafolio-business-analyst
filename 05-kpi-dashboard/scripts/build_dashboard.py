"""Build the executive KPI dashboard for the NovaBank transfer book.

Reads the SQLite database created in Project 3 and exports PNG charts with
pandas + matplotlib, plus a single combined dashboard image.

Usage:
    python scripts/build_dashboard.py

Outputs (in charts/):
    01_monthly_volume.png
    02_status_distribution.png
    03_channel_value.png
    04_instant_vs_batch.png
    05_fraud_screening.png
    06_customer_activity.png
    dashboard.png

Fictitious data, for demonstration purposes only.
"""

import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT.parent / "03-sql-transactions-analysis" / "data" / "novabank.db"
CHARTS_DIR = PROJECT_ROOT / "charts"

DISCLAIMER = "Fictitious data, for demonstration purposes only."
NAVY = "#1F4E78"
BLUE = "#2E75B6"
TEAL = "#2CA6A4"
AMBER = "#E8A33D"
RED = "#C0504D"
GREY = "#8C8C8C"
PALETTE = [NAVY, BLUE, TEAL, AMBER, RED, GREY]


def query(sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)


def _fmt(value: float, unit: str = "") -> str:
    return f"{value:,.2f}{unit}"


def draw_monthly_volume(ax: pd.DataFrame) -> None:
    df = query(
        """
        SELECT strftime('%Y-%m', created_at) AS month,
               SUM(CASE WHEN transfer_type='Instant' THEN 1 ELSE 0 END) AS instant,
               SUM(CASE WHEN transfer_type='Batch' THEN 1 ELSE 0 END) AS batch
        FROM transactions GROUP BY month ORDER BY month;
        """
    )
    x = range(len(df))
    ax.bar(x, df["instant"], label="Instant", color=TEAL)
    ax.bar(x, df["batch"], bottom=df["instant"], label="Batch", color=NAVY)
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["month"], rotation=45, ha="right")
    ax.set_title("Transfers per month by type", fontweight="bold")
    ax.set_ylabel("Transfers")
    ax.legend(loc="upper right")
    ax.margins(x=0.02)


def draw_status_distribution(ax) -> None:
    df = query("SELECT status, COUNT(*) AS n FROM transactions GROUP BY status ORDER BY n DESC")
    colors = [TEAL, AMBER, RED, BLUE, GREY]
    total = df["n"].sum()
    wedges, _ = ax.pie(
        df["n"],
        startangle=90,
        colors=colors[: len(df)],
        wedgeprops=dict(width=0.42, edgecolor="white"),
    )
    legend_labels = [f"{s} — {100 * n / total:.1f}%" for s, n in zip(df["status"], df["n"])]
    ax.legend(wedges, legend_labels, loc="upper center", bbox_to_anchor=(0.5, 0.05),
              fontsize=8, frameon=False, ncol=2)
    ax.set_title("Transfer status distribution", fontweight="bold")
    completed = df.loc[df["status"] == "Completed", "n"].sum()
    ax.text(0, 0, f"{(completed / total) * 100:.1f}%\ncompleted",
            ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY)


def draw_channel_value(ax) -> None:
    df = query(
        """
        SELECT c.channel_name AS channel,
               SUM(t.amount) AS value,
               100.0*SUM(CASE WHEN t.status='Completed' THEN 1 ELSE 0 END)/COUNT(*) AS success
        FROM transactions t JOIN channels c ON c.channel_id=t.channel_id
        GROUP BY c.channel_id ORDER BY value;
        """
    )
    bars = ax.barh(df["channel"], df["value"] / 1_000_000, color=BLUE)
    for bar, success in zip(bars, df["success"]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{success:.1f}%", va="center", fontsize=9, color=NAVY)
    ax.set_title("Transferred value by channel (success rate)", fontweight="bold")
    ax.set_xlabel("Value (millions)")
    ax.margins(x=0.15)


def draw_instant_vs_batch(ax) -> None:
    df = query(
        """
        SELECT transfer_type,
               AVG(amount) AS avg_value,
               AVG(settlement_seconds) AS avg_seconds
        FROM transactions WHERE status='Completed' GROUP BY transfer_type;
        """
    )
    ax2 = ax.twinx()
    x = range(len(df))
    ax.bar([i - 0.2 for i in x], df["avg_value"], width=0.4, color=TEAL, label="Avg ticket value")
    ax2.bar([i + 0.2 for i in x], df["avg_seconds"], width=0.4, color=AMBER, label="Avg settlement (s)")
    ax2.set_yscale("log")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["transfer_type"])
    ax.set_ylabel("Avg ticket value", color=TEAL)
    ax2.set_ylabel("Avg settlement seconds (log)", color=AMBER)
    ax.set_title("Instant vs Batch: ticket size and speed", fontweight="bold")
    lines = [plt.Rectangle((0, 0), 1, 1, color=TEAL), plt.Rectangle((0, 0), 1, 1, color=AMBER)]
    ax.legend(lines, ["Avg ticket value", "Avg settlement (s)"], loc="upper left", fontsize=8)


def draw_fraud_screening(ax) -> None:
    df = query(
        """
        SELECT is_flagged_fraud, COUNT(*) AS n, ROUND(SUM(amount),2) AS value
        FROM transactions GROUP BY is_flagged_fraud ORDER BY is_flagged_fraud DESC;
        """
    )
    labels = ["Flagged", "Clean"]
    counts = df["n"].tolist()
    bars = ax.bar(labels, counts, color=[RED, GREY])
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{count:,}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    flagged_value = df.loc[df["is_flagged_fraud"] == 1, "value"].sum()
    ax.set_title("Fraud screening flags", fontweight="bold")
    ax.set_ylabel("Transfers")
    ax.text(0.5, max(counts) * 0.6,
            f"Flagged value:\n{_fmt(flagged_value)}",
            ha="center", fontsize=10, color=RED, fontweight="bold")
    ax.margins(y=0.2)


def draw_customer_activity(ax) -> None:
    df = query(
        """
        SELECT band, COUNT(*) AS n FROM (
            SELECT CASE
                     WHEN MAX(t.created_at) IS NULL THEN 'No activity'
                     WHEN julianday('2026-10-17')-julianday(MAX(t.created_at))<=30 THEN 'Active <=30d'
                     WHEN julianday('2026-10-17')-julianday(MAX(t.created_at))<=90 THEN 'At risk 31-90d'
                     ELSE 'Dormant >90d' END AS band
            FROM customers c
            LEFT JOIN accounts a ON a.customer_id=c.customer_id
            LEFT JOIN transactions t ON t.account_id=a.account_id
            GROUP BY c.customer_id
        )
        GROUP BY band;
        """
    )
    agg = df.set_index("band")["n"].reindex(
        ["Active <=30d", "At risk 31-90d", "Dormant >90d", "No activity"]
    )
    bars = ax.bar(agg.index, agg.values, color=[TEAL, AMBER, RED, GREY])
    total = agg.sum()
    for bar, count in zip(bars, agg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{100 * count / total:.0f}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold")
    ax.set_title("Customers by activity recency", fontweight="bold")
    ax.set_ylabel("Customers")
    ax.margins(y=0.15)


CHART_FUNCS = [
    ("01_monthly_volume.png", draw_monthly_volume),
    ("02_status_distribution.png", draw_status_distribution),
    ("03_channel_value.png", draw_channel_value),
    ("04_instant_vs_batch.png", draw_instant_vs_batch),
    ("05_fraud_screening.png", draw_fraud_screening),
    ("06_customer_activity.png", draw_customer_activity),
]


def main() -> None:
    global conn
    if not DB_PATH.exists():
        raise SystemExit(
            f"Database not found at {DB_PATH}. Run 03-sql-transactions-analysis/scripts/generate_data.py first."
        )
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    kpis = query(
        """
        SELECT COUNT(*) total, SUM(amount) value, AVG(amount) avg_value,
               100.0*SUM(CASE WHEN transfer_type='Instant' THEN 1 ELSE 0 END)/COUNT(*) instant_share
        FROM transactions;
        """
    ).iloc[0]

    # Individual charts
    for filename, func in CHART_FUNCS:
        fig, ax = plt.subplots(figsize=(8, 5))
        func(ax)
        fig.text(0.99, 0.01, DISCLAIMER, ha="right", fontsize=6, color=GREY)
        fig.tight_layout()
        fig.savefig(CHARTS_DIR / filename, dpi=130, bbox_inches="tight")
        plt.close(fig)

    # Combined dashboard
    fig, axes = plt.subplots(3, 2, figsize=(16, 15))
    for ax, (_, func) in zip(axes.ravel(), CHART_FUNCS):
        func(ax)
    fig.suptitle(
        "NovaBank — Instant Transfers KPI Dashboard",
        fontsize=18, fontweight="bold", color=NAVY, y=0.995,
    )
    subtitle = (
        f"Total transfers: {kpis['total']:,.0f}   |   "
        f"Total value: {kpis['value']:,.0f}   |   "
        f"Avg ticket: {kpis['avg_value']:,.2f}   |   "
        f"Instant share: {kpis['instant_share']:.1f}%"
    )
    fig.text(0.5, 0.965, subtitle, ha="center", fontsize=12, color=BLUE)
    fig.text(0.99, 0.005, DISCLAIMER, ha="right", fontsize=7, color=GREY)
    fig.tight_layout(rect=[0, 0.01, 1, 0.95])
    fig.savefig(CHARTS_DIR / "dashboard.png", dpi=130, bbox_inches="tight")
    plt.close(fig)

    conn.close()
    print(f"Wrote {len(CHART_FUNCS)} charts + dashboard.png to {CHARTS_DIR}")
    print(f"  total transfers: {kpis['total']:,.0f}")
    print(f"  total value:     {kpis['value']:,.2f}")
    print(f"  instant share:   {kpis['instant_share']:.1f}%")


if __name__ == "__main__":
    main()
