# Bomiot 应用内支付（bomiot_pay）使用文档

## 概述

`bomiot_pay` 是 Bomiot 官方提供的 Python 库，用于在第三方软件系统中集成支付宝支付。支付成功后，系统自动将 80% 金额分账到用户指定的支付宝账号，20% 留作 Bomiot 平台佣金。

- **库名**：`bomiot_pay`
- **分账比例**：接收方 80%，Bomiot 平台 20%
- **安全机制**：`sponsor_key` 仅用于本地签名，不通过网络传输

---

## 一、初始化客户端

客户端会自动从 `auth_key.py` 读取 `COMMUNITY_KEY` 和 `SPONSOR_KEY`，无需手动传入：

```python
import bomiot_pay

client = bomiot_pay.Client()
```

> 如需手动指定，也可传入参数：`bomiot_pay.Client(community_key=..., sponsor_key=...)`

---

## 二、创建支付订单

### 方法签名

```python
result = client.create_payment(
    amount,              # float  支付金额
    currency,            # str    货币类型：CNY / USD
    recipient_account,   # str    分账接收方支付宝账号
    notify_url,          # str    支付结果回调地址（公网可访问）
    return_url=None,     # str    可选，支付完成后浏览器跳转地址
)
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `amount` | float | 是 | 支付金额 |
| `currency` | str | 是 | 货币类型：`CNY` 或 `USD`（USD 按汇率 7.0 换算为 CNY） |
| `recipient_account` | str | 是 | 分账接收方支付宝账号（见下方账号类型说明） |
| `notify_url` | str | 是 | 支付结果回调地址，Bomiot 主动 POST 通知 |
| `return_url` | str | 否 | 支付完成后浏览器跳转地址 |

### 返回值 `PaymentResult`

| 属性 | 类型 | 说明 |
|---|---|---|
| `order_id` | str | Bomiot 订单号 |
| `pay_url` | str | 支付宝支付页面 URL，将用户重定向到此地址 |

### 示例

```python
result = client.create_payment(
    amount=100.0,
    currency="CNY",
    recipient_account="2088123456789012",
    notify_url="https://your-system.com/payment/callback",
)
print(result.order_id)   # 20260920123456
print(result.pay_url)    # https://openapi.alipay.com/gateway.do?...

# 将用户重定向到 pay_url 完成支付
```

### recipient_account 账号类型识别

| 格式 | 识别为 | 示例 |
|---|---|---|
| `2088` 开头的纯数字 | `userId` | `2088123456789012` |
| 含 `@` | `loginName`（邮箱） | `user@example.com` |
| 其他 | `loginName`（手机号） | `13800138000`、`+14155552671` |

> 手机号和邮箱统一按 `loginName` 处理，支付宝后端自行解析。

---

## 三、查询订单状态

### 方法签名

```python
status = client.query_order(order_id)
```

### 返回值 `OrderStatus`

| 属性 | 类型 | 说明 |
|---|---|---|
| `order_id` | str | 订单号 |
| `pay_status` | int | 支付状态码（见下表） |
| `pay_status_text` | str | 支付状态文本 |
| `settle_status` | int | 分账状态码 |
| `settle_status_text` | str | 分账状态文本 |
| `refund_status` | int | 退款状态码 |
| `refund_status_text` | str | 退款状态文本 |
| `amount` | str | 订单总金额（CNY） |
| `settle_amount` | str | 分账金额（80%） |
| `expired` | str | 授权到期时间 |
| `fail_reason` | str | 失败原因（失败时） |

### 示例

```python
status = client.query_order(order_id=result.order_id)
print(status.pay_status)        # 1 = 已支付
print(status.settle_status)     # 1 = 分账成功
print(status.expired)           # 2027-09-20 12:00:00
```

### 状态码说明

#### pay_status（支付状态）

| 值 | 文本 | 含义 |
|---|---|---|
| 0 | pending | 待支付 |
| 1 | paid | 已支付（分账成功，授权已续期） |
| 3 | cancelled | 已取消 |
| 4 | refunded | 分账失败，已全额退款（支付失败） |
| 5 | refund_failed | 退款失败，需人工介入 |

#### settle_status（分账状态）

| 值 | 文本 | 含义 |
|---|---|---|
| 0 | unsettled | 未分账 |
| 1 | settled | 分账成功 |
| 2 | settle_failed | 分账失败 |

#### refund_status（退款状态）

| 值 | 文本 | 含义 |
|---|---|---|
| 0 | none | 未退款 |
| 1 | refunded | 退款成功 |
| 2 | refund_failed | 退款失败 |

---

## 四、验证支付回调

Bomiot 在支付处理完成后，会向 `notify_url` 发送 POST 回调。使用 `verify_callback` 验证回调签名并解析内容。

### 方法签名

```python
payload = client.verify_callback(body, signature)
```

| 参数 | 类型 | 说明 |
|---|---|---|
| `body` | str | 回调请求的原始 body 字符串 |
| `signature` | str | 请求头 `X-Bomiot-Sign` 的值 |

### 返回值（dict）

| 字段 | 说明 |
|---|---|
| `status` | `success` 或 `failed` |
| `order_id` | 订单号 |
| `amount` | 订单金额 |
| `settle_amount` | 分账金额（成功时） |
| `expired` | 授权到期时间（成功时） |
| `reason` | 失败原因（失败时） |

### 示例（Django）

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
        # 更新你的订单状态、发货等
        ...
    else:
        # 支付失败（分账失败已退款）
        reason = payload.get("reason", "")
        ...

    return JsonResponse({"status": "ok"})  # 必须返回 200
```

---

## 五、完整集成示例

```python
import bomiot_pay

# 1. 初始化客户端（自动从 auth_key.py 读取密钥）
client = bomiot_pay.Client()

# 2. 创建支付订单
result = client.create_payment(
    amount=100.0,
    currency="CNY",
    recipient_account="2088123456789012",
    notify_url="https://your-system.com/payment/callback",
    return_url="https://your-system.com/payment/return",
)

# 3. 将用户重定向到支付页面
# return redirect(result.pay_url)

# 4. （可选）主动轮询支付结果
import time

def wait_for_payment(order_id, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        status = client.query_order(order_id)
        if status.pay_status in (1, 4, 5):  # 终态
            return status
        time.sleep(3)
    return None

final_status = wait_for_payment(result.order_id)
```

---

## 六、分账失败处理

如果分账失败（例如付款人与接收方为同一人）：

1. Bomiot 自动发起**全额退款**
2. 订单 `pay_status` 标记为 `4`（已退款）或 `5`（退款失败）
3. 通过 `notify_url` 通知用户支付失败
4. **不更新授权到期时间**

用户通过回调 `verify_callback` 或 `query_order` 均可获知失败状态。

---

## 七、注意事项

1. **分账产品开通**：Bomiot 的支付宝应用需已开通「分账」产品权限
2. **接收方实名**：分账接收方支付宝账户必须为实名账户
3. **付款人≠接收人**：付款人与分账接收方不能是同一支付宝账号，否则视为分账失败并退款
4. **资金安全**：分账失败必全额退款，用户资金不会滞留在平台
5. **回调地址**：`notify_url` 必须为公网可访问地址
6. **交易限额**：单笔 CNY ≤ 5000，USD ≤ 1000
