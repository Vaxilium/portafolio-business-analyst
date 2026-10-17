-- 01_kpis_overview.sql
-- Purpose: Headline KPIs for the whole transfer book.
-- Answers: How much do customers transfer, and how large is each payment?
-- Output: one row with totals and the instant-transfer share.

SELECT
    COUNT(*)                                                        AS total_transactions,
    ROUND(SUM(amount), 2)                                           AS total_value,
    ROUND(AVG(amount), 2)                                           AS avg_transaction_value,
    ROUND(SUM(fee), 2)                                              AS total_fees,
    ROUND(100.0 * SUM(CASE WHEN transfer_type = 'Instant' THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                            AS instant_share_pct
FROM transactions;
