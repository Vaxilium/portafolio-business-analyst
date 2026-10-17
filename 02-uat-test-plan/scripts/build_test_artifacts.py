"""Build Excel workbooks for the UAT test plan from the CSV sources.

Usage:
    python scripts/build_test_artifacts.py

Reads:
    data/test-cases.csv
    data/defect-log.csv

Writes:
    data/test-cases.xlsx
    data/defect-log.xlsx

Fictitious data, for demonstration purposes only.
"""

from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(color="FFFFFF", bold=True)


def _autofit(worksheet, frame: pd.DataFrame) -> None:
    for idx, column in enumerate(frame.columns, start=1):
        length = max(
            [len(str(column))] + [len(str(value)) for value in frame[column].tolist()]
        )
        letter = get_column_letter(idx)
        worksheet.column_dimensions[letter].width = min(max(length + 2, 12), 60)
    worksheet.freeze_panes = "A2"
    for cell in worksheet[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="center")


def build(csv_name: str, sheet_name: str) -> Path:
    csv_path = DATA_DIR / csv_name
    xlsx_path = csv_path.with_suffix(".xlsx")
    frame = pd.read_csv(csv_path)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name=sheet_name)
        _autofit(writer.sheets[sheet_name], frame)
    return xlsx_path, frame


def main() -> None:
    test_cases, tc_frame = build("test-cases.csv", "Test Cases")
    defect_log, defect_frame = build("defect-log.csv", "Defect Log")

    status_counts = tc_frame["Status"].value_counts().to_dict()
    print(f"Wrote {test_cases.name} ({len(tc_frame)} test cases)")
    print(f"Wrote {defect_log.name} ({len(defect_frame)} defects)")
    print(f"Test case statuses: {status_counts}")


if __name__ == "__main__":
    main()
