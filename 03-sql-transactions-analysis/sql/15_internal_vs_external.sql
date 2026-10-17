-- 15_internal_vs_external.sql
-- Purpose: Compare internal (on-us) and external (off-us) transfers.
-- Answers: Where is volume concentrated and how do success rates differ?
-- Output: one row for internal and one for external transfers.

SELECT
    CASE WHEN is_internal = 1 THEN 'Internal (NovaBank)'
         ELSE 'External (other bank)' END                           AS counterparty,
    COUNT(*)                                                        AS transactions,
    ROUND(SUM(amount), 2)                                           AS total_value,
    ROUND(100.0 * SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                            AS success_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN transfer_type = 'Instant' THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                            AS instant_share_pct
FROM transactions
GROUP BY is_internal
ORDER BY total_value DESC;
