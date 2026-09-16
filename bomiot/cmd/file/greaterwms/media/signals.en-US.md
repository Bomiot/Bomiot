# Signals

## Introduction

Bomiot uses a **Signal** mechanism to decouple and extend business logic. Developers can inject custom behavior without modifying the framework core. Bomiot provides three signal entry points, corresponding to three files in the project root:

| File | Signal Type | Purpose |
|------|-------------|---------|
| `files.py` | File signals | Intercept & extend file upload/download/delete operations |
| `receiver.py` | Data signals | Take over & customize data APIs |
| `server.py` | Server signals | Server lifecycle, monitoring events |

---

## How to Use Signals

Send a signal via `bomiot_signals.send()`; the framework receives and executes the corresponding logic.

```python
from bomiot.server.core.signal import bomiot_signals

def my_handler(sender, **kwargs):
    print("signal fired")

# Send signal
bomiot_signals.send(sender=my_handler, msg={
    'models': 'YourModel',
    'data': { ... }
})
```

> Signal code is usually written in an app's `urls.py`; refreshing the web page reloads it.

---

## Data Signals (receiver.py)

Take over data APIs for custom query, filtering, permission logic, etc.

```python
# receiver.py
from bomiot.server.core.signal import bomiot_signals

def custom_data_handler(sender, **kwargs):
    # Custom data processing
    pass

bomiot_signals.send(sender=custom_data_handler, msg={
    'models': 'MyModel',
    'data': {
        'filter': {'status': 'active'},
        'ordering': '-created_time'
    }
})
```

---

## File Signals (files.py)

Run custom logic before/after file upload, download, delete — e.g. virus scan, format conversion, permission checks.

```python
# files.py
from bomiot.server.core.signal import bomiot_signals

def file_upload_handler(sender, **kwargs):
    file_path = kwargs.get('file_path')
    pass

bomiot_signals.send(sender=file_upload_handler, msg={
    'action': 'upload',
    'data': {}
})
```

---

## Server Signals (server.py)

Handle server lifecycle events like startup, shutdown, monitoring.

```python
# server.py
from bomiot.server.core.signal import bomiot_signals

def server_start_handler(sender, **kwargs):
    # Run on server startup
    pass

bomiot_signals.send(sender=server_start_handler, msg={
    'action': 'startup',
    'data': {}
})
```

---

## Signals & Scheduled Tasks

Signals can also register scheduled tasks (see the Scheduler doc):

```python
bomiot_signals.send(sender=my_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'description': 'Run every 60 seconds'
    }
})
```

---

## Notes

- Signals are processed asynchronously; avoid long blocking operations in handlers
- Multiple handlers can be registered for the same model, executed in registration order
- During development, refresh the web page to reload signal code
