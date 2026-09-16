# Django Backend

## Introduction

Bomiot uses **Django** as the enterprise-grade backend framework. Django's ORM is universal across all backends (Django, FastAPI, Flask), so models defined in Django can be reused everywhere.

---

## Create a Project

```shell
bomiot project <project_name>
```

## Create a Django App

```shell
bomiot new <app_name>
```

Then you can write your Django application within this app. You can also use the standard Django commands:

```shell
# Generate migration files
bomiot makemigrations

# Apply migrations
bomiot migrate
```

---

## Project Structure

```
your-project/                 # Project directory
├── <app_name>/               # Django app
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin registration
│   ├── apps.py               # App config
│   ├── models.py             # Data models
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # URL routing
│   └── views.py              # API views
├── language/                 # i18n files
├── media/                    # Static files
├── bomiotconf.ini            # Project identifier
├── receiver.py               # Data takeover
├── server.py                 # Server monitoring
└── files.py                  # File monitoring
setup.ini                     # Global config
```

---

## Defining Models

Bomiot provides a `CoreModel` base class with common fields (`id`, `created_time`, `updated_time`, `is_delete`).

```python
from bomiot.server.core.models import CoreModel

class Goods(CoreModel):
    # All business data is stored in a single JSONField for front-end/back-end consistency
    data = models.JSONField(default=dict)
```

> 💡 The `data` JSONField allows the front-end to send arbitrary JSON, and the back-end stores it directly without field-by-field mapping. See [Structure](structure) for details.

---

## URL Routing

Define routes in `urls.py` with a `name` for permission control:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('goods/', views.goods, name="Goods"),
]
```

- If `name` is specified, the interface is protected by Bomiot's permission system.
- If `name` is omitted, the interface is public (no permission check).

See [Permission](permission) for details.

---

## API Views

Bomiot uses Django REST Framework (DRF) style views. Each view function receives a `data` dict containing the request, query params, and payload.

```python
from bomiot.server.core.message import msg_message_return

def goods(request, data):
    # data contains: request, query_params, data (POST body)
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success")
```

---

## Data Takeover (receiver.py)

For custom business logic, take over the API in `receiver.py` instead of modifying views. Bomiot signals enable hot updates — changes take effect immediately without restarting the server.

See [Function Data](data) for details.

---

## Signal Mechanism

Bomiot's signal system (`bomiot_signals`, `bomiot_data_signals`) allows real-time communication between components:

```python
from bomiot.server.core.signal import bomiot_signals

# Send a signal
bomiot_signals.send(sender=my_func, msg={'key': 'value'})
```

- **Hot update**: Signal handlers take effect immediately without server restart.
- **Real-time**: File changes, data updates, and server metrics are broadcast via signals.

---

## Migrations

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

## Multi-database Support

Bomiot supports SQLite (default), MySQL, PostgreSQL, and Oracle. Configure in `setup.ini`:

```ini
[database]
engine = sqlite    # sqlite | mysql | postgresql | oracle
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port
```

See [SQLite](sqlite), [MySQL](mysql), [PostgreSQL](postgresql) for setup details.

---

## References

- [Django Official Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django GitHub](https://github.com/django/django)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

For more advanced usage, refer to the official documentation or community resources.
