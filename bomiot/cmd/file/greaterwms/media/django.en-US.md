# Django Backend

## Introduction

Bomiot uses **Django** as its backend framework. Django is a high-level Python web framework known for "rapid development and clean, pragmatic design." It ships with an ORM, admin interface, authentication, security, and more out of the box, and is widely used in projects that need fast delivery without compromise.

### Key Features

- **Batteries included**: ORM, template engine, form handling, user authentication, admin panel, i18n, and security protections all built in
- **MTV architecture**: Model (data) — Template (presentation) — View (logic), cleanly separated
- **Powerful ORM**: define data models as Python classes, automatically mapped to database tables, with support for SQLite / MySQL / PostgreSQL / Oracle
- **Automatic admin**: a complete data-management interface generated from your models with zero code
- **Security**: built-in defenses against SQL injection, XSS, CSRF, clickjacking, and other common attacks
- **Scalable**: a proven path from prototype to products serving millions of requests

---

## Using It in Bomiot

### Create a Project

```shell
bomiot project <project_name>
```

### Create an App

```shell
bomiot app <app_name>
```

### Database Migrations

```shell
# Generate migration files
bomiot makemigrations

# Apply migrations
bomiot migrate

# Load initial data
bomiot loaddata <source>

# Export data
bomiot dumpdata [appname]
```

---

## Project Structure

```
your-project/                 # project directory
├── <app_name>/               # Django app
│   ├── migrations/           # database migrations
│   ├── __init__.py
│   ├── admin.py              # admin registration
│   ├── apps.py               # app configuration
│   ├── models.py             # data models
│   ├── serializers.py        # serializers
│   ├── urls.py               # URL routing
│   └── views.py              # API views
├── language/                 # i18n files
├── media/                    # static files
├── bomiotconf.ini            # project identity
├── receiver.py               # data takeover
├── server.py                 # server monitoring
└── files.py                  # file monitoring
setup.ini                     # global configuration
```

---

## Defining Models

Bomiot provides a `CoreModel` base class with common fields (`id`, `created_time`, `updated_time`, `is_delete`).

```python
from bomiot.server.core.models import CoreModel

class Goods(CoreModel):
    # All business data is stored in a single JSONField, keeping front and back ends consistent
    data = models.JSONField(default=dict)
```

> 💡 The `data` JSONField lets the front end send arbitrary JSON, stored directly by the backend without field-by-field mapping. See Data Structure.

If you prefer traditional field-by-field modeling, the full power of Django models (field types, indexes, constraints, relationships) is equally available.

---

## URL Routing

Define routes in `urls.py`. The `name` attribute is used for permission control:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('goods/', views.goods, name="Goods"),
]
```

- Endpoints with a `name` are protected by the Bomiot permission system.
- Endpoints without a `name` are public (no permission check).

See Permission Control.

---

## API Views

Each view function receives a `data` dict containing the request, query parameters, and payload.

```python
from bomiot.server.core.message import msg_message_return

def goods(request, data):
    # data contains: request, query_params, data (POST body)
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success")
```

---

## Data Takeover

To customize business logic, take over the API in `receiver.py` instead of modifying views.

See Data Takeover.

---

## Signal System

The Bomiot signal system (`bomiot_signals`, `bomiot_data_signals`) enables real-time communication between components:

```python
from bomiot.server.core.signal import bomiot_signals

# Send a signal
bomiot_signals.send(sender=my_func, msg={'key': 'value'})
```

- **Hot reload**: signal handlers take effect immediately, no server restart needed.
- **Real-time**: file changes, data updates, and server metrics are all broadcast via signals.

---

## Multi-Database Support

SQLite (default), MySQL, PostgreSQL, and Oracle are supported. Configure in `setup.ini`:

```ini
[database]
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port
```

See SQLite, MySQL, PostgreSQL, Oracle.
