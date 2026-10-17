-- 08_fraud_screening.sql
-- Purpose: Quantify how much value the fraud engine flags.
-- Answers: What share of transfers and value is flagged as suspicious?
-- Output: one row per flag state (0 = clean, 1 = flagged).

SELECT
    is_flagged_fraud,
    COUNT(*)                                                        AS transactions,
    ROUND(SUM(amount), 2)                                           AS total_value,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM transactions), 2) AS pct_of_transactions
FROM transactions
GROUP BY is_flagged_fraud
ORDER BY is_flagged_fraud DESC;
