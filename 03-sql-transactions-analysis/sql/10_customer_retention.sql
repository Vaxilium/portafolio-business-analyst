-- 10_customer_retention.sql
-- Purpose: Count monthly active customers over time.
-- Answers: Is the active customer base growing or shrinking?
-- Output: one row per month with the number of distinct active customers.

SELECT
    strftime('%Y-%m', t.created_at)                                 AS month,
    COUNT(DISTINCT a.customer_id)                                   AS active_customers
FROM transactions t
JOIN accounts a ON a.account_id = t.account_id
GROUP BY month
ORDER BY month;
