# Bomiot Split Payment User Agreement

**Last Updated: 2026-09-20**

Welcome to the Bomiot Split Payment service (hereinafter "the Service"). Please read this agreement carefully before using the Service. By using the Service, you acknowledge that you have read, understood, and agreed to all terms of this agreement.

---

## 1. Service Description

The Service is provided by Bomiot (hereinafter "the Platform"), enabling third-party software systems to integrate Alipay payment functionality. Upon successful payment, funds are automatically split — 80% to the user-specified Alipay account and 20% retained as the Platform commission.

---

## 2. User Responsibilities

1. **Lawful Use**: The user agrees to use the Service only for lawful commercial transactions, including but not limited to software sales, digital goods delivery, and service subscriptions.
2. **Authentic Transactions**: The user guarantees that each payment corresponds to a real product or service transaction; fabricated transaction backgrounds are prohibited.
3. **Account Authenticity**: The split recipient Alipay account provided by the user must be a real-name verified account owned by the user or used with lawful authorization.
4. **Safekeeping of auth_key**: The user shall safely store the `auth_key.py` file; losses due to leakage are borne by the user.
5. **Legal Compliance**: The user's use of the Service must comply with applicable laws and regulations of China and the user's jurisdiction.

---

## 3. Prohibited Activities

The user shall not use the Service for the following:

1. **Money Laundering**: Using the Service to transfer illicit funds to other accounts via split settlement
2. **Cash-Out**: Converting credit card limits into cash through fabricated transactions
3. **Fund Pooling**: Aggregating funds from multiple unknown sources into a single account
4. **Transaction Splitting**: Breaking large transactions into multiple small ones to evade monitoring
5. **Self-Split**: The payer and split recipient being the same Alipay account (the system will automatically block and refund)
6. **Facilitating Illegal Activities**: Providing payment channels for gambling, fraud, pyramid schemes, or other illegal activities
7. **Other Illegal Acts**: Any activity that violates applicable laws and regulations

---

## 4. Transaction Limits

To mitigate risk, the Service enforces transaction limits:

| Currency | Per-Transaction Limit |
|---|---|
| CNY (Chinese Yuan) | 5,000 |
| USD (US Dollar) | 1,000 |

The Platform reserves the right to adjust limits based on risk assessment.

---

## 5. Risk Control Measures

The Platform implements the following risk control measures:

1. **Royalty Relation Binding Verification**: Before payment creation, the recipient account is verified via the Alipay royalty relation bind API
2. **Payer Verification**: The payer and split recipient must not be the same Alipay account
3. **Split Failure Refund**: On split failure, a full refund is automatically initiated to protect user funds
4. **Transaction Records**: All transactions are fully recorded, including payer, recipient, amount, time, and status
5. **Anomaly Monitoring**: The Platform reserves the right to monitor, freeze, and investigate anomalous transactions

---

## 6. Disclaimer

1. **Alipay-Side Risk**: The Service depends on Alipay's royalty settlement API. The Platform is not liable for transaction failures caused by Alipay-side risk control, account freezes, or API changes, but will assist the user with refund processing.

2. **User Violations**: Legal liability arising from the user's violation of Section 3 (Prohibited Activities) is borne solely by the user. The Platform reserves the right to cooperate with law enforcement investigations.

3. **Force Majeure**: The Platform is not liable for service interruptions or anomalies caused by natural disasters, network failures, system maintenance, policy changes, or other force majeure events.

4. **Indirect Losses**: The Platform is not liable for indirect losses arising from the use of the Service (including but not limited to loss of profits, loss of goodwill, or data loss).

5. **Third-Party Actions**: The Platform is not liable for fund delays or failures caused by third parties such as Alipay, banks, or network operators, but will actively assist the user in communicating with the third party.

6. **Account Security**: Fund losses caused by the user's own negligence (e.g., auth_key leakage, server compromise, callback URL hijacking) are borne by the user.

---

## 7. Refund Policy

1. **Split Failure**: On split failure, the Platform automatically initiates a full refund to the payer's Alipay account.
2. **Refund Timing**: Refund arrival time depends on Alipay's processing, typically instant but no longer than 3 business days.
3. **Refund Failure**: If the refund fails (e.g., payer account abnormality), the Platform will mark it as "manual intervention required." The user can check the status via the order query API and contact the Platform for resolution.

---

## 8. Data and Privacy

1. The Platform only collects transaction data directly related to the Service (order ID, amount, recipient account, payment status, etc.).
2. The Platform will not sell or provide user transaction data to third parties, except as required by law.
3. The user's `COMMUNITY_KEY` and `SPONSOR_KEY` are used solely for identity verification and signature validation, and are not stored or transmitted in plaintext.

---

## 9. Agreement Changes

The Platform reserves the right to modify this agreement at any time. After changes are made, the updated agreement will be published on the official website. Continued use of the Service constitutes acceptance of the modified agreement. If the user does not agree with the changes, they should stop using the Service.

---

## 10. Contact

If you have any questions or need assistance, please contact:

- Website: https://www.bomiot.com
- Email: support@bomiot.com

---

**By using this Service, you acknowledge that you have read and agreed to all terms of this agreement.**
