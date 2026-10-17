-- 02_monthly_transfer_volume.sql
-- Purpose: Monthly transfer volume trend over the last 6 months.
-- Answers: Is usage growing, flat or declining? How fast is instant adoption?
-- Output: one row per month with counts, value and instant-transfer count.

SELECT
    strftime('%Y-%m', created_at)                                   AS month,
    COUNT(*)                                                        AS transactions,
    ROUND(SUM(amount), 2)                                           AS total_value,
    SUM(CASE WHEN transfer_type = 'Instant' THEN 1 ELSE 0 END)      AS instant_transactions
FROM transactions
GROUP BY month
ORDER BY month;
