# Bomiot api performance

## What is Locust?

**Locust** is an open-source, scalable, distributed load testing tool based on Python. It's suitable for stress testing websites, APIs, and services.
Users define user behavior with Python scripts, and Locust provides a web UI for real-time monitoring and control of the load test process.

---

## Installing Locust

### Install via pip

```bash
pip install locust
```

It is recommended to use a virtual environment.

---

## Basic Concepts

- **User**: A simulated virtual user. Each User executes one or more Tasks.
- **Task**: An operation performed by the user (e.g., visiting an API or page).
- **wait_time**: The wait time between user operations.
- **locustfile**: The test script file, default name is `locustfile.py`.

---

## Writing Your First Locust Script

Suppose you want to stress test an HTTP endpoint:

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Each user waits 1~3 seconds between operations

    @task
    def index(self):
        self.client.get("/")  # Visit the homepage

    @task
    def about(self):
        self.client.get("/about")  # Visit the about page
```

**Save as** `locustfile.py`.

---

## Running Locust

In the script directory, run:

```bash
locust
```

By default, this starts the web UI (`http://localhost:8089`). Use the UI to enter the number of concurrent users, spawn rate, and other parameters to start the test.

**Common startup parameters:**

- `-f locustfile.py`: Specify the script file
- `--host http://your.target.com`: Specify the target host to test

---

## Common Command Line Parameters

| Parameter              | Description                                 |
|------------------------|---------------------------------------------|
| `-f`                   | Specify locustfile file                     |
| `--host`               | The host address to test                    |
| `-u`, `--users`        | Number of concurrent users (for headless)   |
| `-r`, `--spawn-rate`   | Number of users to start per second (headless) |
| `--headless`           | Headless (no web UI) mode                   |
| `--run-time`           | Test duration (e.g., 1m, 10s, 1h)           |
| `--csv`                | Generate CSV format test reports            |

---

## Advanced Usage

### Custom User Behavior

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
- `@task(2)` means this task has a weight of 2, executed twice as often as another task with weight 1.

---

### Task Weighting

Use the `@task(n)` decorator to set the weight. If no parameter is given, the default weight is 1.

---

### Testing with Multiple User Types

You can define multiple User classes to simulate different roles or scenarios:

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
When Locust starts, all User classes in the script will be included automatically.

---

### Custom Startup Parameters

You can enter parameters in the web UI, or specify them directly on the command line (headless mode):

```bash
locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://127.0.0.1:8000
```
- This means 100 users, 10 new users per second, running for 1 minute.

---

### Headless Mode

Suitable for server or CI/CD automation scenarios, runs without web UI, and outputs results directly.

---

### API Performance Testing Example

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

## Result Analysis & Extensions

- Web UI provides real-time data such as RPS, response time, and failure rate.
- Supports exporting CSV files for further analysis.
- Supports distributed (master-worker) mode, suitable for large-scale load testing.

---

## FAQ

1. **How to simulate user login?**  
   You can implement login logic in the `on_start` method, save the token/cookie to an instance variable, and reuse it for subsequent requests.

2. **How to stress test HTTPS?**  
   Just set the host parameter to an https address; Locust supports HTTPS natively.

3. **How to add assertions?**  
   You can check `response.status_code` or `response.text` in your task and manually collect statistics using if statements.

---

## References

- [Locust Official Documentation](https://docs.locust.io/en/stable/)
- [Locust GitHub](https://github.com/locustio/locust)

---
