-- 09_suspicious_transactions.sql
-- Purpose: List the highest-risk transfers for manual review.
-- Answers: Which specific transfers should Fraud & Risk investigate first?
-- Output: top 20 transfers with a fraud score >= 0.90.

SELECT
    t.transaction_id,
    c.segment,
    ch.channel_name,
    t.transfer_type,
    ROUND(t.amount, 2)                                              AS amount,
    t.status,
    t.fraud_score,
    t.created_at
FROM transactions t
JOIN accounts a   ON a.account_id = t.account_id
JOIN customers c  ON c.customer_id = a.customer_id
JOIN channels ch  ON ch.channel_id = t.channel_id
WHERE t.fraud_score >= 0.90
ORDER BY t.fraud_score DESC, t.amount DESC
LIMIT 20;
