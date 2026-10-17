-- 11_active_vs_dormant.sql
-- Purpose: Segment customers by recency of last transaction (retention).
-- Answers: How many customers are active, at risk or dormant?
-- Output: activity bands with customer counts and share of the base.
-- Note: reference date is fixed at 2026-10-17 to keep results reproducible.

SELECT
    activity_band,
    COUNT(*)                                                        AS customers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers), 1)   AS pct_of_base
FROM (
    SELECT
        c.customer_id,
        CASE
            WHEN MAX(t.created_at) IS NULL THEN '4. No activity'
            WHEN julianday('2026-10-17') - julianday(MAX(t.created_at)) <= 30 THEN '1. Active (<=30d)'
            WHEN julianday('2026-10-17') - julianday(MAX(t.created_at)) <= 90 THEN '2. At risk (31-90d)'
            ELSE '3. Dormant (>90d)'
        END AS activity_band
    FROM customers c
    LEFT JOIN accounts a     ON a.customer_id = c.customer_id
    LEFT JOIN transactions t ON t.account_id = a.account_id
    GROUP BY c.customer_id
)
GROUP BY activity_band
ORDER BY activity_band;
