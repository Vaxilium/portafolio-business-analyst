# Project 4 — Process Improvement: Failed & Pending Transfers (NovaBank)

> **Fictitious data, for demonstration purposes only.**
> NovaBank is an invented bank. All processes, KPIs and figures in this project
> are fictional and created solely to demonstrate Business Analysis and process
> improvement skills.

## Overview

This project analyses the **exception-handling process for failed, timed-out
and returned instant transfers** and proposes improvements. It builds directly
on the finding from [Project 3](../03-sql-transactions-analysis/docs/findings-report.md)
that **2,434 transfers were stuck in "Pending"** and on UAT defect
**DEF-001** from [Project 2](../02-uat-test-plan/docs/test-results-report.md).

The process today is manual, reactive and slow; the target process is largely
automated, proactive and measurable.

## Deliverables

| Document | Description |
|----------|-------------|
| [docs/as-is-to-be.md](docs/as-is-to-be.md) | AS-IS and TO-BE process diagrams (Mermaid). |
| [docs/root-cause-analysis.md](docs/root-cause-analysis.md) | 5 Whys and Ishikawa (fishbone) root cause analysis. |
| [docs/kpis-before-after.md](docs/kpis-before-after.md) | Baseline vs target KPIs. |
| [docs/improvement-proposal.md](docs/improvement-proposal.md) | Initiatives, effort/impact and estimated business case. |

## Problem in one line

Timed-out transfers have no reliable terminal status and no proactive
notification, so customers call support and agents resolve exceptions
manually — driving a long cycle time and unnecessary cost.

## Target outcomes

- Reduce average resolution time from **5 days to 0.5 day**.
- Auto-resolve **≥ 85%** of exceptions (from ~20%).
- Cut "where is my transfer?" contacts by **40%**.
- Estimated annual benefit **~55,000** (see business case).

> All data, figures and processes are fictitious and for demonstration purposes only.
