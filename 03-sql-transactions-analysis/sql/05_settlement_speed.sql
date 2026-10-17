-- 05_settlement_speed.sql
-- Purpose: Measure instant transfer speed against the <10 second target.
-- Answers: Does instant settlement meet the 95% under 10 seconds objective?
-- Output: one row with min/avg/max settlement time and the share under 10s.

SELECT
    ROUND(AVG(settlement_seconds), 0)                               AS avg_seconds,
    MIN(settlement_seconds)                                         AS min_seconds,
    MAX(settlement_seconds)                                         AS max_seconds,
    ROUND(100.0 * SUM(CASE WHEN settlement_seconds <= 10 THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                            AS pct_under_10_seconds
FROM transactions
WHERE status = 'Completed'
  AND transfer_type = 'Instant';
