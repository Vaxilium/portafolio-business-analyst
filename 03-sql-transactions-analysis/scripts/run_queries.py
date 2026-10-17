"""Run every SQL query in sql/ against data/novabank.db and print the results.

Usage:
    python scripts/run_queries.py            # run all queries
    python scripts/run_queries.py 03 05      # run only files starting with 03 and 05

Fictitious data, for demonstration purposes only.
"""

import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "novabank.db"
SQL_DIR = PROJECT_ROOT / "sql"


def print_table(headers, rows, max_rows=None):
    rows = list(rows)
    shown = rows if max_rows is None else rows[:max_rows]
    str_rows = [[("" if v is None else str(v)) for v in r] for r in shown]
    widths = [len(h) for h in headers]
    for r in str_rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(v))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("-" * len(line))
    for r in str_rows:
        print("  ".join(v.ljust(widths[i]) for i, v in enumerate(r)))
    if max_rows is not None and len(rows) > max_rows:
        print(f"... {len(rows) - max_rows} more rows")
    print(f"({len(rows)} rows)")


def main() -> None:
    filters = sys.argv[1:]
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run scripts/generate_data.py first.")
        sys.exit(1)

    files = sorted(SQL_DIR.glob("*.sql"))
    if filters:
        files = [f for f in files if any(f.name.startswith(p) for p in filters)]

    conn = sqlite3.connect(DB_PATH)
    for sql_file in files:
        text = sql_file.read_text(encoding="utf-8")
        print("\n" + "=" * 78)
        print(f"# {sql_file.name}")
        print("=" * 78)
        cur = conn.execute(text)
        headers = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print_table(headers, rows, max_rows=25)
    conn.close()


if __name__ == "__main__":
    main()
