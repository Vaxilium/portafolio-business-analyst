# Project 2 — UAT Test Plan: Instant Transfers (NovaBank)

> **Fictitious data, for demonstration purposes only.**
> NovaBank is an invented bank. All test data, testers, defects and results in
> this project are fictional and created solely to demonstrate Business
> Analysis and UAT skills.

## Overview

This project contains the **User Acceptance Testing (UAT)** plan and artefacts
for the **Instant Transfers** feature specified in
[Project 1 — Requirements](../01-requirements-bank-feature/). Test cases map
1:1 to the traceability matrix (`TC-001`..`TC-018`) so every business
requirement can be verified.

## Deliverables

| Artefact | File | Description |
|----------|------|-------------|
| UAT Test Plan | [docs/uat-test-plan.md](docs/uat-test-plan.md) | Scope, approach, roles, environment, entry/exit criteria, schedule. |
| Test Cases (source) | [data/test-cases.csv](data/test-cases.csv) | 18 test cases with steps and expected results. |
| Test Cases (Excel) | [data/test-cases.xlsx](data/test-cases.xlsx) | Spreadsheet version generated from the CSV. |
| Defect Log | [data/defect-log.csv](data/defect-log.csv) | 6 fictitious defects with severity and status. |
| Defect Log (Excel) | [data/defect-log.xlsx](data/defect-log.xlsx) | Spreadsheet version generated from the CSV. |
| Test Results Report | [docs/test-results-report.md](docs/test-results-report.md) | Execution summary, pass/fail, defect analysis. |
| Exit Criteria | [docs/exit-criteria.md](docs/exit-criteria.md) | Formal sign-off criteria and decision. |
| Build script | [scripts/build_test_artifacts.py](scripts/build_test_artifacts.py) | Generates the XLSX files from the CSV sources. |

## How to run

Regenerate the Excel workbooks from the CSV sources:

```powershell
python scripts/build_test_artifacts.py
```

## Summary of results (fictitious)

| Metric | Value |
|--------|-------|
| Test cases planned | 18 |
| Executed | 18 |
| Passed | 13 |
| Failed | 4 |
| Blocked | 1 |
| Pass rate (of executed) | 72.2% |
| Defects logged | 6 (1 Critical, 2 Major, 2 Minor, 1 Trivial) |

> See [docs/test-results-report.md](docs/test-results-report.md) for the full
> breakdown. All figures are fictional.
