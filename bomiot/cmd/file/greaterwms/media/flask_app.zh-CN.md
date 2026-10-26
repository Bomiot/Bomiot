# Flask 后端

## 简介

**Flask** 是一个轻量级的 Python Web 框架，核心简单克制：不强制项目结构、不捆绑数据库和表单等组件，把选择权留给开发者。上手门槛低，同时可以通过丰富的扩展逐步构建出复杂应用。

Bomiot 支持用 Flask 编写后端接口，适合轻量、灵活的 API 场景。

### 核心特性

- **微框架内核**：只包含路由、请求处理、模板渲染等基础能力，其余按需扩展
- **不强制项目结构**：单文件应用和多包工程都合法，自由度完全在开发者手里
- **装饰器路由**：`@app.route()` 一行定义接口，直观易读
- **内置开发服务器与调试器**：改代码自动重载，错误页可直接交互调试
- **扩展生态**：ORM、表单、认证等都有成熟扩展（Flask-SQLAlchemy、Flask-Login 等）

---

## 在 Bomiot 中使用

### 创建项目

```shell
bomiot project <project_name>
```

### 项目结构

```
my-project/                    # 项目目录
├── flask_app/                 # Flask 应用
│   └── main.py                # 入口文件
...
```

之后即可在 `main.py` 中编写 Flask 应用。

---

## 基础示例

```python
from flask import Flask

app = Flask(__name__)

@app.route("/test/", methods=["GET"])
def test():
    return {"message": "Hello from Flask"}
```

接口访问地址为 `http://127.0.0.1:8000/flask_app/test/`。

### 路由与请求

```python
from flask import request

@app.route("/goods/<int:goods_id>", methods=["GET", "POST"])
def goods(goods_id):
    if request.method == "POST":
        payload = request.get_json()
        return {"id": goods_id, "received": payload}
    return {"id": goods_id}
```

- 路径参数用 `<类型:名称>` 声明，支持 `int`、`float`、`path` 等转换器
- `methods` 限定允许的 HTTP 方法
- 请求体用 `request.get_json()` 解析，返回 dict 自动转为 JSON 响应

---

## 使用 Django ORM

ORM 层是通用的——Flask 接口中可直接导入项目内定义的模型：

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/goods/", methods=["GET"])
def get_goods():
    from my_app.models import Goods
    goods = list(Goods.objects.filter(is_delete=False).values())
    return jsonify(goods)
```

---

## 请求头

Bomiot 为每个请求注入 `token`、`language`、`project` 请求头：

```python
from flask import request

@app.route("/test/", methods=["GET"])
def test():
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## WebSocket 支持

Flask 中使用 WebSocket 需安装 `flask-socketio`，或切换至原生支持 WebSocket的 FastAPI。

---

## 适用场景

| 场景 | 建议 |
|---|---|
| 轻量 API、原型验证 | ✅ Flask 是理想选择 |
| 需要高度自定义技术栈 | ✅ 微框架不挡路，组件自由组合 |
| 企业级复杂业务 | 建议使用默认的 Django 后端，开箱能力更全 |
| 高并发 IO 密集接口 | 建议使用 FastAPI，原生异步性能更好 |
| 实时推送（WebSocket） | 建议使用 FastAPI 或加装 flask-socketio |

---

## 注意事项

- Flask 自带的开发服务器仅供调试，Bomiot 中接口由 `bomiot run` 统一承载，无需自己调用 `app.run()`。
- 返回 dict / list 会被自动序列化为 JSON；需要自定义响应头时用 `make_response()` 或返回 `Response` 对象。
- 接口路径统一挂在项目前缀下（如 `/flask_app/`），定义路由时写相对部分即可。
