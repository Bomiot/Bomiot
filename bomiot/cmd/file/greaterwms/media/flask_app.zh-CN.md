# Flask 后端

## 简介

Bomiot 支持 **Flask** 构建轻量级后端。

---

## 创建项目

```shell
bomiot project <project_name>
```

## 项目结构

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

---

## 使用 Django ORM

Django ORM 通用——可在 Flask 中直接导入模型：

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
from flask import Flask, request

@app.route("/test/", methods=["GET"])
def test():
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## WebSocket 支持

Flask 中使用 WebSocket 需安装 `flask-socketio`，或切换至原生支持 WebSocket 的 [FastAPI](fastapi_app)。

---

## 何时使用 Flask

场景 | Recommendation / 推荐 |
| 高并发
| 企业级功能
| 轻量 API
| 实时推送

---

## 参考资料

- [Flask 官方文档](https://flask.palletsprojects.com/zh-cn/stable/)
- [Flask Official Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask GitHub](https://github.com/pallets/flask)

---

更多高级用法，请参考官方文档或社区资源。
