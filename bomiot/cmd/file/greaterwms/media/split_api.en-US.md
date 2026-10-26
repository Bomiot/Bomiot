# Bomiot In-App Payment (bomiot_pay) Documentation

## Overview

`bomiot_pay` is the official Python library provided by Bomiot for integrating Alipay payments into third-party software systems. After a successful payment, 80% of the amount is automatically split to the recipient's Alipay account, and 20% remains as the Bomiot platform commission.

- **Library name**: `bomiot_pay`
- **Split ratio**: recipient 80%, Bomiot platform 20%
- **Security**: `sponsor_key` is only used for local signing and is never transmitted over the network

---

## 1. Initialize the Client

The client automatically reads `COMMUNITY_KEY` and `SPONSOR_KEY` from `auth_key.py` — no manual parameters needed:

```python
import bomiot_pay

client = bomiot_pay.Client()
```

> To specify keys manually: `bomiot_pay.Client(community_key=..., sponsor_key=...)`

---

## 2. Create a Payment Order

### Method Signature

```python
result = client.create_payment(
    amount,              # float  Payment amount
    currency,            # str    Currency: CNY / USD
    recipient_account,   # str    Recipient Alipay account for the split
    notify_url,          # str    Callback URL for payment result (publicly accessible)
    return_url=None,     # str    Optional: browser redirect URL after payment
)
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | float | Yes | Payment amount |
| `currency` | str | Yes | Currency: `CNY` or `USD` (USD is converted to CNY at rate 7.0) |
| `recipient_account` | str | Yes | Recipient Alipay account (see account type notes below) |
| `notify_url` | str | Yes | Callback URL; Bomiot sends a POST notification here |
| `return_url` | str | No | Browser redirect URL after payment completes |

### Return Value `PaymentResult`

| Attribute | Type | Description |
|---|---|---|
| `order_id` | str | Bomiot order ID |
| `pay_url` | str | Alipay payment page URL; redirect the user here |

### Example

```python
result = client.create_payment(
    amount=100.0,
    currency="CNY",
    recipient_account="2088123456789012",
    notify_url="https://your-system.com/payment/callback",
)
print(result.order_id)   # 20260920123456
print(result.pay_url)    # https://openapi.alipay.com/gateway.do?...

# Redirect the user to pay_url to complete payment
```

### recipient_account Account Type Detection

| Format | Detected as | Example |
|---|---|---|
| Pure digits starting with `2088` | `userId` | `2088123456789012` |
| Contains `@` | `loginName` (email) | `user@example.com` |
| Other | `loginName` (mobile) | `13800138000`, `+14155552671` |

> Both mobile numbers and emails are treated as `loginName`; Alipay parses them on its end.

---

## 3. Query Order Status

### Method Signature

```python
status = client.query_order(order_id)
```

### Return Value `OrderStatus`

| Attribute | Type | Description |
|---|---|---|
| `order_id` | str | Order ID |
| `pay_status` | int | Payment status code (see table below) |
| `pay_status_text` | str | Payment status text |
| `settle_status` | int | Split settlement status code |
| `settle_status_text` | str | Split settlement status text |
| `refund_status` | int | Refund status code |
| `refund_status_text` | str | Refund status text |
| `amount` | str | Total order amount (CNY) |
| `settle_amount` | str | Split amount (80%) |
| `expired` | str | Authorization expiry time |
| `fail_reason` | str | Failure reason (on failure) |

### Example

```python
status = client.query_order(order_id=result.order_id)
print(status.pay_status)        # 1 = paid
print(status.settle_status)     # 1 = settled
print(status.expired)           # 2027-09-20 12:00:00
```

### Status Codes

#### pay_status

| Value | Text | Meaning |
|---|---|---|
| 0 | pending | Awaiting payment |
| 1 | paid | Paid (split successful, authorization extended) |
| 3 | cancelled | Cancelled |
| 4 | refunded | Split failed, fully refunded (payment failed) |
| 5 | refund_failed | Refund failed, manual intervention required |

#### settle_status

| Value | Text | Meaning |
|---|---|---|
| 0 | unsettled | Not settled |
| 1 | settled | Split successful |
| 2 | settle_failed | Split failed |

#### refund_status

| Value | Text | Meaning |
|---|---|---|
| 0 | none | No refund |
| 1 | refunded | Refund successful |
| 2 | refund_failed | Refund failed |

---

## 4. Verify Payment Callback

After payment processing completes, Bomiot sends a POST callback to `notify_url`. Use `verify_callback` to verify the signature and parse the payload.

### Method Signature

```python
payload = client.verify_callback(body, signature)
```

| Parameter | Type | Description |
|---|---|---|
| `body` | str | Raw callback request body string |
| `signature` | str | Value of the `X-Bomiot-Sign` request header |

### Return Value (dict)

| Field | Description |
|---|---|
| `status` | `success` or `failed` |
| `order_id` | Order ID |
| `amount` | Order amount |
| `settle_amount` | Split amount (on success) |
| `expired` | Authorization expiry time (on success) |
| `reason` | Failure reason (on failure) |

### Example (Django)

```python
from django.http import JsonResponse

def payment_callback(request):
    body = request.body.decode("utf-8")
    signature = request.headers.get("X-Bomiot-Sign", "")

    try:
        payload = client.verify_callback(body, signature)
    except Exception as e:
        return JsonResponse({"status": "error"}, status=403)

    if payload["status"] == "success":
        # Update your order status, deliver goods, etc.
        ...
    else:
        # Payment failed (split failed, refunded)
        reason = payload.get("reason", "")
        ...

    return JsonResponse({"status": "ok"})  # Must return 200
```

---

## 5. Complete Integration Example

```python
import bomiot_pay

# 1. Initialize the client (auto-reads keys from auth_key.py)
client = bomiot_pay.Client()

# 2. Create a payment order
result = client.create_payment(
    amount=100.0,
    currency="CNY",
    recipient_account="2088123456789012",
    notify_url="https://your-system.com/payment/callback",
    return_url="https://your-system.com/payment/return",
)

# 3. Redirect the user to the payment page
# return redirect(result.pay_url)

# 4. (Optional) Actively poll for payment result
import time

def wait_for_payment(order_id, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        status = client.query_order(order_id)
        if status.pay_status in (1, 4, 5):  # terminal states
            return status
        time.sleep(3)
    return None

final_status = wait_for_payment(result.order_id)
```

---

## 6. Split Failure Handling

If the split fails (e.g., the payer is the same person as the recipient):

1. Bomiot automatically initiates a **full refund**
2. Order `pay_status` is marked as `4` (refunded) or `5` (refund failed)
3. The user is notified of the failure via `notify_url`
4. **Authorization expiry time is NOT updated**

Users can learn about the failure status via either the callback (`verify_callback`) or `query_order`.

---

## 7. Notes

1. **Split product enabled**: Bomiot's Alipay app must have the "Royalty Settlement" product enabled
2. **Recipient real-name**: The recipient's Alipay account must be a real-name verified account
3. **Payer ≠ recipient**: The payer cannot be the same Alipay account as the split recipient, otherwise the split is treated as failed and refunded
4. **Fund safety**: A failed split always triggers a full refund; user funds never get stuck on the platform
5. **Callback URL**: `notify_url` must be a publicly accessible address
6. **Transaction limit**: Single transaction CNY ≤ 5000, USD ≤ 1000
