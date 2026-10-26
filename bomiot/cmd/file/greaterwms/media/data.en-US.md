# Data Monitoring

## Introduction

Bomiot's built-in APIs push every front-end/back-end data interaction (query, create, update, delete) to the project side in real time via the `bomiot_data_signals` signal:

- `api.py` declares the mapping from URLs to handler function names
- `receiver.py` implements the matching handler methods; the method's return value directly decides whether data is persisted and what feedback the front end receives

Endpoints work without takeover too: queries return with default filtering, and write operations echo the submitted data back (without persisting it).

---

## How It Works

### Write Operations (Create / Update / Delete)

1. The front-end request hits a built-in API (e.g. `/core/asn/create/`); the view opens a database transaction first
2. The view emits a `bomiot_data_signals` signal carrying `request`, `mode` (`create` / `update` / `delete`), and `data`; updates additionally carry `updated_fields`
3. The framework's signal receiver reads the project name from the `HTTP_PROJECT` header (falling back to the main project name when absent or set to `bomiot`), dynamically loads **that project's** `api.py`, and looks up the `func_name` for the URL
4. The framework parses **the main project's** `greaterwms/receiver.py` via AST, dynamically loads it, and calls the method named `func_name`
5. The method returns a dict; the framework acts on its key:

| Return | Data behavior | Front-end result |
|---|---|---|
| `{"msg": ...}` | **Persisted** (create injects creator and department, update strips protected fields, delete becomes soft delete) | Success message |
| `{"detail": ...}` | Not persisted | Failure reason shown |
| `{"login": ...}` | Not persisted | Triggers re-login |
| Not taken over / method missing | Not persisted; submitted data echoed back | No message |

> The whole write operation runs inside a transaction; an exception in the handler rolls back and returns 400.

### Queries (GET)

1. The view filters data by `project` + `is_delete` + department conditions, and **auto-flattens** each row's `data` JSONField into top-level fields before pagination
2. While assembling the paginated response, a signal is emitted (`mode='get'`) carrying `query_params` (the parsed query dict) and `data` (the current page)
3. The handler returns a **list of tuples**:
   - `('results', data)`: replaces the page results (omit to keep the original results)
   - Any other `('key', value)`: appended to the response as extra fields

> Queries usually need no takeover — only take over when the front end needs processed data.

---

## File Location

The two files have different scopes — a key design point of the mechanism:

```shell
workspace/                    # workspace
├── setup.ini
├── greaterwms/               # main project
│   └── receiver.py           # data takeover (single global file, shared by all projects)
└── <your_project>/           # each sub-project
    └── api.py                # API route table (switched by the HTTP_PROJECT header)
```

- `api.py` is per-project: the `HTTP_PROJECT` header decides which project's `api.py` is loaded
- `receiver.py` is global: write signals from every project converge on `greaterwms/receiver.py`

---

## `api.py` — API Route Table

```python
def api_return(data):
    api_list = [
        {'method': 'GET',  'api': '/core/example/',        'func_name': 'example_get',    'name': 'Get Example List'},
        {'method': 'POST', 'api': '/core/example/create/', 'func_name': 'example_create', 'name': 'Create Example'},
        {'method': 'POST', 'api': '/core/example/update/', 'func_name': 'example_update', 'name': 'Update Example'},
        {'method': 'POST', 'api': '/core/example/delete/', 'func_name': 'example_delete', 'name': 'Delete Example'},
    ]
    api_dict = {api['api']: api for api in api_list}
    return api_dict.get(data, {})
```

| Field | Description |
| --- | --- |
| `method` | HTTP method (`GET` / `POST`) |
| `api` | URL path |
| `func_name` | Handler method name in `receiver.py` |
| `name` | Permission display name |

URLs not present in the table resolve to no `func_name`, so the request is never taken over.

---

## `receiver.py` — Data Takeover

Method names correspond one-to-one with `func_name` in `api.py`, organized into classes:

```python
from bomiot.server.core.message import msg_message_return, detail_message_return

class ExampleClass(object):

    def example_get(self, data):
        print(data.get('query_params').get('params'))   # query parameters
        return [('results', data.get('data'))]          # keep default results

    def example_create(self, data):
        print(data.get('data'))                         # submitted data
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Create")

    def example_update(self, data):
        print(data.get('updated_fields'))               # {field: (old, new)}
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Update")

    def example_delete(self, data):
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Delete")
```

Three return constructors: `msg_message_return` (persist + success), `detail_message_return` (reject + failure feedback), `login_message_return` (reject + re-login).

---

## The `data` Parameter

| Key | Description | Scenario |
| --- | --- | --- |
| `request` | Request object (language/project via `request.META`: `HTTP_LANGUAGE`, `HTTP_PROJECT`) | all |
| `mode` | `get` / `create` / `update` / `delete` | all |
| `data` | Writes: request body; queries: current page, already flattened | all |
| `query_params` | Parsed query parameter dict | get |
| `updated_fields` | Changed fields as `{field: (old, new)}` | update |

---

## Project Isolation

Models inheriting `DataCoreModel` carry a `project` field:

- **Writes**: the `HTTP_PROJECT` value is stamped automatically on persist (create also injects `creater` and `department`)
- **Queries**: by default only rows of the current project with `is_delete=False` and matching department conditions are returned

Each project can only see and operate on its own data.

---

## Notes

- **Hot reload**: `receiver.py` is loaded dynamically per request — changes take effect immediately without restart. `api.py` goes through the module import cache, so changes require a restart
- **Keep `receiver.py` thin**: handler methods should only dispatch; put business logic in separate modules (e.g. a `process/` directory) to avoid bloat
- **Soft delete**: delete operations actually set `is_delete=True`; the data stays in the database
- Before persisting an update, the framework strips `id`, `is_delete`, `created_time`, and `updated_time` so these fields cannot be tampered with from the front end
