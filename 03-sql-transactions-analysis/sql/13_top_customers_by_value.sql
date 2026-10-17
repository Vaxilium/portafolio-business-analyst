-- 13_top_customers_by_value.sql
-- Purpose: Rank customers by total transferred value (window function).
-- Answers: Who are the most valuable customers to retain?
-- Output: top 15 customers with their value rank.

SELECT
    a.customer_id,
    c.full_name,
    c.segment,
    COUNT(*)                                                        AS transactions,
    ROUND(SUM(t.amount), 2)                                         AS total_value,
    RANK() OVER (ORDER BY SUM(t.amount) DESC)                       AS value_rank
FROM transactions t
JOIN accounts a  ON a.account_id = t.account_id
JOIN customers c ON c.customer_id = a.customer_id
GROUP BY a.customer_id
ORDER BY total_value DESC
LIMIT 15;
