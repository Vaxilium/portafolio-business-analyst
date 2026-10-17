-- 03_channel_performance.sql
-- Purpose: Compare transfer activity and success across channels.
-- Answers: Which channels drive value and which have poorer completion rates?
-- Output: one row per channel ordered by transferred value.

SELECT
    c.channel_name,
    c.channel_group,
    COUNT(*)                                                        AS transactions,
    ROUND(SUM(t.amount), 2)                                         AS total_value,
    ROUND(AVG(t.amount), 2)                                         AS avg_value,
    ROUND(100.0 * SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                            AS success_rate_pct
FROM transactions t
JOIN channels c ON c.channel_id = t.channel_id
GROUP BY c.channel_id
ORDER BY total_value DESC;
