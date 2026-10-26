# FastAPI 后端

## 简介

**FastAPI** 是一个现代、高性能的 Python Web 框架，基于 Python 类型提示构建。它的设计目标是：极高的运行性能（媲美 Node.js 和 Go）、极高的开发效率、更少的 bug（类型检查在开发期就能拦住大量错误）、以及自动生成的交互式 API 文档。

Bomiot 支持用 FastAPI 编写后端接口，适合高并发和实时推送场景。

### 核心特性

- **性能**：基于 Starlette 和 Pydantic，是主流 Python 框架中性能最高的一档
- **类型驱动**：用 Python 类型注解声明参数，自动完成校验、序列化和文档
- **自动文档**：开箱即得 Swagger UI 和 ReDoc 两套交互式 API 文档
- **异步原生**：`async`/`await` 一等公民，IO 密集场景吞吐量大
- **标准兼容**：完全基于 OpenAPI 和 JSON Schema 开放标准

---

## 在 Bomiot 中使用

### 创建项目

```shell
bomiot project <project_name>
```

### 项目结构

```
my-project/                    # 项目目录
├── fastapi_app/               # FastAPI 应用
│   └── main.py                # 入口文件
...
```

之后即可在 `main.py` 中编写 FastAPI 应用。

---

## 基础示例

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/test/")
async def test():
    return {"message": "Hello from FastAPI"}
```

接口访问地址为 `http://127.0.0.1:8000/fastapi_app/test/`。

### 参数声明与校验

用类型注解声明参数，FastAPI 自动校验并转换：

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
    # goods_id 自动转为 int，转换失败返回 422 错误
    return {"id": goods_id, "detail": detail}
```

- 路径参数、查询参数、请求体全部按类型自动解析
- 校验失败自动返回 422 及详细错误位置，无需手写校验逻辑

---

## 使用 Django ORM

ORM 层在所有后端间共享——FastAPI 接口中可直接导入项目内定义的模型：

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

## WebSocket 支持

Bomiot 的 Rust ASGI 网关原生支持 WebSocket，可直接在 `main.py` 中定义 WebSocket 路由：

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

> 💡 实时信号推送详见 服务器监控。

---

## 请求头

Bomiot 为每个请求注入自定义请求头：

| 请求头 | 说明 |
|---|---|
| `token` | JWT 认证令牌 |
| `language` | 当前语言（如 `en-US`） |
| `project` | 当前项目名 |

```python
from fastapi import FastAPI, Request

@app.get("/test/")
async def test(request: Request):
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## 异步任务

FastAPI 原生支持 `async`/`await`，非常适合 IO 密集型操作：

```python
import asyncio

@app.get("/slow/")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"result": "done"}
```

> 注意：纯 CPU 密集或阻塞调用（如同步的数据库驱动）应放到线程池或用 `def` 定义路由，FastAPI 会自动在线程池中运行同步函数。

---

## 性能

FastAPI 是三个后端中最快的。使用 Locust 进行压测：

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

---

## 适用场景

| 场景 | 建议 |
|---|---|
| 高并发 IO 密集接口 | ✅ FastAPI 是首选 |
| 实时推送（WebSocket） | ✅ 原生支持 |
| 需要自动 API 文档 | ✅ 开箱即得 |
| 企业级复杂业务 + 管理后台 | 建议默认的 Django 后端 |
| 极简脚本式接口 | 可考虑 Flask，心智负担更低 |
