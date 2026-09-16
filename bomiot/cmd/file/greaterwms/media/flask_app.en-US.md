# Flask Backend

## Introduction

Bomiot supports **Flask** for lightweight backends. Flask apps run alongside Django and FastAPI apps in the same process.

---

## Create a Project

```shell
bomiot project <project_name>
```

## Project Structure

```
my-project/                    # Project directory
├── flask_app/                 # Flask app
│   └── main.py                # Main file
...
```

Then you can write your Flask application within `main.py`.

---

## Basic Example

```python
from flask import Flask

app = Flask(__name__)

@app.route("/test/", methods=["GET"])
def test():
    return {"message": "Hello from Flask"}
```

The endpoint is accessible at `http://127.0.0.1:8000/flask_app/test/`.

---

## Using Django ORM

Django's ORM is universal — import models directly in Flask:

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
from flask import Flask, request

@app.route("/test/", methods=["GET"])
def test():
    token = request.headers.get("token", "")
    language = request.headers.get("language", "en-US")
    return {"token": token, "language": language}
```

---

## WebSocket Support

For WebSocket in Flask, use `flask-socketio` or switch to [FastAPI](fastapi_app) which has native WebSocket support.

---

## When to Use Flask

| Scenario
|------|------|
| High concurrency
| Enterprise features
| Lightweight APIs
| Real-time push

---

## References

- [Flask Official Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask GitHub](https://github.com/pallets/flask)

---

For more advanced usage, refer to the official documentation or community resources.
