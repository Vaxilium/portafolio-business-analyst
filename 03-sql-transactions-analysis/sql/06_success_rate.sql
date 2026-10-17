-- 06_success_rate.sql
-- Purpose: Distribution of transfer statuses and overall success rate.
-- Answers: What share of transfers complete, and how much fails or is pending?
-- Output: one row per status with count and percentage of all transfers.

SELECT
    status,
    COUNT(*)                                                        AS transactions,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM transactions), 2) AS pct_of_total
FROM transactions
GROUP BY status
ORDER BY transactions DESC;
