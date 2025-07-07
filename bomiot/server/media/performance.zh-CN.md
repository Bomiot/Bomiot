# Bomiot api 压力测试

## 什么是 Locust?

**Locust** 是一个基于 Python 的分布式、可扩展的开源性能测试工具，适用于网站、API、服务等的负载测试。  
它以编写 Python 脚本的方式定义用户行为，通过 Web 界面实时监控和控制压力测试进程。

---

## 安装 Locust

### 使用 pip 安装

```bash
pip install locust
```

推荐在虚拟环境下安装。

---

## 基本概念

- **User**：模拟的虚拟用户，每个 User 可以执行若干个 Task。
- **Task**：用户执行的操作（如访问 API、请求页面）。
- **wait_time**：用户操作间的等待时间。
- **locustfile**：测试脚本文件，默认名为 `locustfile.py`。

---

## 编写第一个 Locust 脚本

假设我们要压测一个 HTTP 接口：

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # 每个用户操作之间等待 1~3 秒

    @task
    def index(self):
        self.client.get("/")  # 访问首页

    @task
    def about(self):
        self.client.get("/about")  # 访问 about 页面
```

**保存为** `locustfile.py`。

---

## 运行 Locust

在脚本目录下执行：

```bash
locust
```

默认会启动 Web UI（本地 `http://localhost:8089`），通过界面输入并发用户数和启动速率等参数，开始压测。

**常见启动参数：**

- `-f locustfile.py`：指定脚本文件
- `--host http://your.target.com`：指定压测目标主机

---

## 常用参数说明

| 参数                | 说明                               |
|---------------------|------------------------------------|
| `-f`                | 指定 locustfile 文件               |
| `--host`            | 测试目标的主机地址                 |
| `-u`、`--users`     | 并发用户数（headless模式用）        |
| `-r`、`--spawn-rate`| 每秒启动用户数（headless模式用）    |
| `--headless`        | 无界面模式                         |
| `--run-time`        | 压测时长（如 1m, 10s, 1h）         |
| `--csv`             | 生成 csv 格式测试报告              |

---

## 进阶用法

### 自定义用户行为

```python
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(2)
    def view_products(self):
        self.client.get("/products")

    @task(1)
    def view_cart(self):
        self.client.get("/cart")
```
- `@task(2)` 表示该任务权重为 2，执行频率为另一个权重为 1 的两倍。

---

### 任务权重设置

通过 `@task(n)` 装饰器设置权重。如果不加参数，默认权重为 1。

---

### 多用户类型测试

可定义多个 User 类，模拟不同角色或场景：

```python
from locust import HttpUser, task, between

class BuyerUser(HttpUser):
    wait_time = between(1, 2)
    @task
    def buy(self):
        self.client.get("/buy")

class SellerUser(HttpUser):
    wait_time = between(2, 4)
    @task
    def sell(self):
        self.client.post("/sell", {"item": "book"})
```
启动 Locust 时会自动包含所有定义的 User。

---

### 自定义启动参数

可在 Web UI 输入参数，也可以命令行直接指定（headless模式）：

```bash
locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://127.0.0.1:8000
```
- 表示 100 个用户，每秒新增 10 个用户，运行 1 分钟。

---

### 无界面（headless）模式

适合服务器、CI/CD 自动化场景，无需 Web UI，直接输出结果。

---

### Bomiot API 性能测试示例

```python
from locust import HttpUser, task, between

class PerformanceAPI(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post(
            "/login/",
            json={"username": "admin", "password": "admin"}
        )
        result = response.json()
        self.token = result.get("token", "")
        self.headers = {"token": f"{self.token}"} if self.token else {}

    @task(1)
    def get_django_test(self):
        self.client.get("/test/", headers=self.headers, name="Get django test")

    @task(1)
    def get_fastapi_test(self):
        self.client.get("/fastapi/test/", headers=self.headers, name="Get fastapi test")
    
    @task(1)
    def get_flask_test(self):
        self.client.get("/flask/test/", headers=self.headers, name="Get flask test")
```

---

## 结果分析与扩展

- Web UI：实时展示 RPS、响应时间、失败率等数据。
- 支持导出 CSV 文件，方便后续分析。
- 支持分布式（master-worker）模式，适合大规模压测。

---

## 常见问题

1. **如何模拟用户登录？**  
   可在 `on_start` 方法中实现登录逻辑，将 token/cookie 保存在实例变量用于后续请求。

2. **怎么压测 HTTPS？**  
   直接在 host 写 https 地址即可，Locust 支持。

3. **如何扩展断言？**  
   可通过判断 `response.status_code` 或 `response.text`，用 `if` 语句手动统计异常。

---

## 参考链接

- [Locust 官方文档（英文）](https://docs.locust.io/en/stable/)
- [Locust GitHub](https://github.com/locustio/locust)

---
