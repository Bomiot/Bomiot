# FastAPI Backend

## Introduction

**FastAPI** is a modern, high-performance Python web framework built on Python type hints. Its design goals: very high runtime performance (on par with Node.js and Go), great developer ergonomics, fewer bugs (type checking catches many errors during development), and automatically generated interactive API documentation.

Bomiot supports writing backend endpoints with FastAPI — a good fit for high-concurrency and real-time push scenarios.

### Key Features

- **Performance**: built on Starlette and Pydantic, among the fastest mainstream Python frameworks
- **Type-driven**: declare parameters with Python type annotations; validation, serialization, and documentation come for free
- **Automatic docs**: interactive Swagger UI and ReDoc out of the box
- **Async-native**: first-class `async`/`await`, high throughput for IO-bound workloads
- **Standards-based**: fully compatible with OpenAPI and JSON Schema

---

## Using It in Bomiot

### Create a Project

```shell
bomiot project <project_name>
```

### Project Structure

```
my-project/                    # project directory
├── fastapi_app/               # FastAPI app
│   └── main.py                # entry file
...
```

Write your FastAPI app in `main.py` from here.

---

## Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/test/")
async def test():
    return {"message": "Hello from FastAPI"}
```

The endpoint is served at `http://127.0.0.1:8000/fastapi_app/test/`.

### Parameter Declaration and Validation

Declare parameters with type annotations; FastAPI validates and converts them automatically:

```python
from pydantic import BaseModel

class GoodsIn(BaseModel):
    name: str
    price: float
    stock: int = 0

@app.post("/goods/")
async def create_goods(item: GoodsIn):
    return {"received": item}

@app.get("/goods/{goods_id}")
async def get_goods(goods_id: int, detail: bool = False):
    # goods_id is converted to int automatically; invalid values return a 422 error
    return {"id": goods_id, "detail": detail}
```

- Path parameters, query parameters, and request bodies are all parsed per their declared types
- Validation failures automatically return a 422 response with detailed error locations — no hand-written validation needed

---

## Using the Django ORM

The ORM layer is shared across all backends — import the models defined in your project directly inside FastAPI endpoints:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/goods/")
async def get_goods():
    from my_app.models import Goods
    goods = Goods.objects.filter(is_delete=False).values()
    return list(goods)
```

---

## WebSocket Support

Bomiot's Rust ASGI gateway supports WebSocket natively. Define WebSocket routes directly in `main.py`:

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

> 💡 For real-time signal push, see Server Monitoring.

---

## Request Headers

Bomiot injects custom headers into every request:

| Header | Description |
|---|---|
| `token` | JWT authentication token |
| `language` | Current language (e.g. `en-US`) |
| `project` | Current project name |

```python
from fastapi import FastAPI, Request

@app.get("/test/")
async def test(request: Request):
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## Async Tasks

FastAPI natively supports `async`/`await`, ideal for IO-bound operations:

```python
import asyncio

@app.get("/slow/")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"result": "done"}
```

> Note: CPU-bound or blocking calls (such as synchronous database drivers) should go in a thread pool, or be defined with plain `def` — FastAPI runs sync functions in a thread pool automatically.

---

## Performance

FastAPI is the fastest of the three backends. Load-test with Locust:

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

---

## When to Use FastAPI

| Scenario | Recommendation |
|---|---|
| High-concurrency IO-bound endpoints | ✅ FastAPI is the top choice |
| Real-time push (WebSocket) | ✅ Native support |
| Automatic API documentation | ✅ Out of the box |
| Complex enterprise logic + admin panel | Prefer the default Django backend |
| Minimal script-style endpoints | Consider Flask for lower mental overhead |
