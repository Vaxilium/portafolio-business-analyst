-- 07_failure_reasons.sql
-- Purpose: Identify the most common reasons transfers do not complete.
-- Answers: Where should operations focus to reduce failures?
-- Output: one row per status/reason combination ordered by frequency.

SELECT
    status,
    failure_reason,
    COUNT(*)                                                        AS transactions
FROM transactions
WHERE failure_reason IS NOT NULL
GROUP BY status, failure_reason
ORDER BY transactions DESC;
