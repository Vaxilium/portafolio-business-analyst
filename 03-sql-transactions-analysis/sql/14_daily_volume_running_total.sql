-- 14_daily_volume_running_total.sql
-- Purpose: Daily transferred value with a cumulative running total.
-- Answers: How has cumulative transferred value evolved over the period?
-- Output: one row per day with daily value and running total (window function).

SELECT
    day,
    ROUND(daily_value, 2)                                           AS daily_value,
    ROUND(SUM(daily_value) OVER (ORDER BY day), 2)                  AS running_total
FROM (
    SELECT
        strftime('%Y-%m-%d', created_at)                            AS day,
        SUM(amount)                                                 AS daily_value
    FROM transactions
    GROUP BY day
)
ORDER BY day;
