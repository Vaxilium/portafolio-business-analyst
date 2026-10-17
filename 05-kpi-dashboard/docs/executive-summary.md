# Executive Summary — NovaBank Transfer KPIs

> **Fictitious data, for demonstration purposes only.**

![KPI Dashboard](../charts/dashboard.png)

## Context

NovaBank's retail **Instant Transfers** feature has been live for six months.
This one-page summary condenses the analysis of **50,000 transfers** (3,000
customers, 5,000 accounts, 180 days) into the KPIs that matter to the business.
The underlying data and queries are in
[Project 3](../03-sql-transactions-analysis/).

## Headline KPIs

| KPI | Value | Read |
|-----|------:|------|
| Total transfers | 50,000 | Stable ~8,500/month |
| Total transferred value | 23,949,557 | — |
| Average ticket | 478.99 | Instant tickets ~4x smaller than batch |
| Instant share | 55.2% | Adoption is strong |
| Instant settlement | ~5 s (100% < 10 s) | **Meets the speed objective** |
| Completion rate | 87.2% | ~1 in 8 does not complete |
| Flagged as suspicious | 2.0% (491,949) | Part of it settled (control gap) |
| Customers active ≤ 30 days | 74.7% | 19% have never transacted |

## What the charts say

- **Volume is stable** across the period; instant and batch are split roughly
  50/50 (chart 1).
- **Mobile App dominates** the channel mix (~52% of value) and drives most
  flagged activity; **Open API / Partner** has the lowest completion rate
  (chart 3).
- **Instant is faster but smaller**: ~5 s settlement at ~200 average versus
  ~823 for batch — an adoption that pressures fee revenue (chart 4).
- **Fraud screening flags 2%** of transfers; a meaningful portion of flagged
  value still settled, indicating room to tighten real-time holds (chart 5).
- **19% of customers never transacted** and ~6% are at risk — an activation and
  retention opportunity (chart 6).

## Recommendations

1. **Fix exception handling** so timed-out transfers reach a clear terminal
   state (2,434 pending today). See [Project 4](../04-process-improvement/).
2. **Tighten fraud holds** to stop flagged value from settling.
3. **Activate the 571 never-active customers** and re-engage the at-risk group.
4. **Promote instant transfers** while monitoring ticket size and fee impact.
5. **Investigate the Open API / Partner** channel's lower completion rate.

## Bottom line

The feature delivered on its core promise (fast, reliable happy-path transfers).
The next value unlock is in the **edge cases**: exception handling, fraud
holds and customer activation — where the biggest cost and risk reductions sit.

> All names, figures and events are fictitious and for portfolio demonstration purposes only.
