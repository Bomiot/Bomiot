# FastAPI Backend

## Introduction

Bomiot supports **FastAPI** for high-concurrency backends. FastAPI apps run alongside Django apps in the same process, and Django's ORM is fully reusable.

---

## Create a Project

```shell
bomiot project <project_name>
```

## Project Structure

```
my-project/                    # Project directory
├── fastapi_app/               # FastAPI app
│   └── main.py                # Main file
...
```

Then you can write your FastAPI application within `main.py`.

---

## Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/test/")
async def test():
    return {"message": "Hello from FastAPI"}
```

The endpoint is accessible at `http://127.0.0.1:8000/fastapi_app/test/`.

---

## Using Django ORM

Since Bomiot shares Django's ORM across all backends, you can import Django models directly in FastAPI:

```python
from fastapi import FastAPI
from bomiot.server.core.models import CoreModel
import json

app = FastAPI()

@app.get("/goods/")
async def get_goods():
    from my_app.models import Goods
    goods = Goods.objects.filter(is_delete=False).values()
    return list(goods)
```

---

## WebSocket Support

Bomiot's Rust ASGI gateway natively supports WebSocket. Define WebSocket routes directly in `main.py`:

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
```

> 💡 See [Server](server) for real-time push via signals.

---

## Request Headers

Bomiot injects custom headers for every request:

| Header
|------|------|
| `token` | JWT authentication token
| `language` | Current language (`en-US`
| `project` | Current project name

```python
from fastapi import FastAPI, Request

@app.get("/test/")
async def test(request: Request):
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## Asynchronous Tasks

FastAPI supports `async/await` natively, making it ideal for I/O-bound operations:

```python
import asyncio

@app.get("/slow/")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"result": "done"}
```

---

## Performance

FastAPI is the fastest of the three supported backends. Use [Locust](performance) to benchmark:

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

---

## References

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI GitHub](https://github.com/fastapi/fastapi)

---

For more advanced usage, refer to the official documentation or community resources.
