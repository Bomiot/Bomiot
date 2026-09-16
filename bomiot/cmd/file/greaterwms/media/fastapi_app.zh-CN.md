# FastAPI 后端

## 简介

Bomiot 支持 **FastAPI** 构建高并发后端。

---

## 创建项目

```shell
bomiot project <project_name>
```

## 项目结构

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

---

## 使用 Django ORM

由于 Bomiot 在所有后端间共享 Django ORM，可在 FastAPI 中直接导入 Django 模型：

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

> 💡 实时信号推送详见 [服务器监控](server)。

---

## 请求头

Bomiot 为每个请求注入自定义请求头：

请求头 | Description / 说明 |
| `token` | JWT 认证令牌
| `language` | 当前语言（`en-US`
| `project` | 当前项目名

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

FastAPI 原生支持 `async/await`，非常适合 I/O 密集型操作：

```python
import asyncio

@app.get("/slow/")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"result": "done"}
```

---

## 性能

FastAPI 是三个后端中最快的。使用 [Locust](performance) 进行压测：

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

---

## 参考资料

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI GitHub](https://github.com/fastapi/fastapi)

---

更多高级用法，请参考官方文档或社区资源。
