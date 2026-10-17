-- 04_instant_vs_batch_adoption.sql
-- Purpose: Compare instant vs batched transfers on completed payments.
-- Answers: Is the new instant rail being adopted, and does it change ticket size?
-- Output: one row per transfer type with value and average settlement time.

SELECT
    transfer_type,
    COUNT(*)                                                        AS transactions,
    ROUND(SUM(amount), 2)                                           AS total_value,
    ROUND(AVG(amount), 2)                                           AS avg_value,
    ROUND(AVG(settlement_seconds), 0)                               AS avg_settlement_seconds
FROM transactions
WHERE status = 'Completed'
GROUP BY transfer_type
ORDER BY transactions DESC;
