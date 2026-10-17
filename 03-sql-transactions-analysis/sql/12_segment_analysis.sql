-- 12_segment_analysis.sql
-- Purpose: Compare transfer behaviour across customer segments.
-- Answers: Which segment drives the most value and the largest tickets?
-- Output: one row per segment with customers, transactions and value.

SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id)                                   AS customers,
    COUNT(t.transaction_id)                                         AS transactions,
    ROUND(SUM(t.amount), 2)                                         AS total_value,
    ROUND(AVG(t.amount), 2)                                         AS avg_value
FROM customers c
JOIN accounts a     ON a.customer_id = c.customer_id
JOIN transactions t ON t.account_id = a.account_id
GROUP BY c.segment
ORDER BY total_value DESC;
