# Flask Backend

## Introduction

**Flask** is a lightweight Python web framework with a deliberately small core: it imposes no project structure and bundles no database or form components, leaving those choices to the developer. It is easy to get started with, yet scales up to complex applications through its rich extension ecosystem.

Bomiot supports writing backend endpoints with Flask — a good fit for lightweight, flexible APIs.

### Key Features

- **Micro core**: only routing, request handling, and template rendering are built in; everything else is opt-in
- **No enforced project layout**: single-file apps and multi-package projects are equally valid
- **Decorator routing**: define an endpoint in one line with `@app.route()`
- **Built-in dev server and debugger**: auto-reload on code changes, with an interactive in-browser debugger
- **Extension ecosystem**: mature extensions for ORM, forms, authentication, and more (Flask-SQLAlchemy, Flask-Login, …)

---

## Using It in Bomiot

### Create a Project

```shell
bomiot project <project_name>
```

### Project Structure

```
my-project/                    # project directory
├── flask_app/                 # Flask app
│   └── main.py                # entry file
...
```

Write your Flask app in `main.py` from here.

---

## Basic Example

```python
from flask import Flask

app = Flask(__name__)

@app.route("/test/", methods=["GET"])
def test():
    return {"message": "Hello from Flask"}
```

The endpoint is served at `http://127.0.0.1:8000/flask_app/test/`.

### Routing and Requests

```python
from flask import request

@app.route("/goods/<int:goods_id>", methods=["GET", "POST"])
def goods(goods_id):
    if request.method == "POST":
        payload = request.get_json()
        return {"id": goods_id, "received": payload}
    return {"id": goods_id}
```

- Path parameters are declared as `<type:name>`; converters like `int`, `float`, and `path` are supported
- `methods` restricts the allowed HTTP methods
- Parse request bodies with `request.get_json()`; returning a dict automatically produces a JSON response

---

## Using the Django ORM

The ORM layer is shared — import the models defined in your project directly inside Flask endpoints:

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

## Request Headers

Bomiot injects `token`, `language`, and `project` headers into every request:

```python
from flask import request

@app.route("/test/", methods=["GET"])
def test():
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## WebSocket Support

WebSocket in Flask requires `flask-socketio`, or switch to FastAPI, which supports WebSocket natively.

---

## When to Use Flask

| Scenario | Recommendation |
|---|---|
| Lightweight APIs, prototypes | ✅ Flask is an ideal choice |
| Highly customized tech stack | ✅ The micro core stays out of your way |
| Complex enterprise business logic | Prefer the default Django backend for its fuller feature set |
| High-concurrency I/O-bound endpoints | Prefer FastAPI for native async performance |
| Real-time push (WebSocket) | Prefer FastAPI or add flask-socketio |

---

## Notes

- Flask's built-in development server is for debugging only. In Bomiot, endpoints are served by `bomiot run` — do not call `app.run()` yourself.
- Returning a dict or list is automatically serialized to JSON; use `make_response()` or a `Response` object when you need custom headers.
- Endpoints are mounted under the project prefix (e.g. `/flask_app/`); define routes with the relative part only.
