# Function Data

## Introduction

- **Bomiot**'s built-in API is a core feature, providing a brand new front-end and back-end interaction.
- All front-end and back-end data interactions for create/update/delete are transferred to `receiver.py` through signals.
- `api.py` maps URL paths to function names, and `receiver.py` implements the corresponding takeover logic.

---

## How It Works

1. The front end sends a request to a URL (e.g. `/core/example/create/`) with the `HTTP_PROJECT` header specifying the project name.
2. The view sends a `bomiot_data_signals` signal with `request`, `mode`, `data`, and `updated_fields`.
3. `data_callback` in `admin.py` reads `HTTP_PROJECT` from the request, loads the corresponding project's `api.py`, and looks up the URL to get the `func_name`.
4. `receiver_callback` imports `receiver.py` and calls the method matching `func_name`.
5. The method returns a result that determines whether the data is stored.

> The `HTTP_PROJECT` header determines which project's `api.py` and `receiver.py` are loaded. If set to `bomiot`, it is replaced with the default project name.

---

## `api.py` — API Routing

`api.py` defines the mapping between URL paths and receiver function names:

```python
def api_return(data):
    api_list = [
        {'method': 'GET', 'api': '/core/example/', 'func_name': 'example_get', 'name': 'Get Example List'},
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
| `func_name` | Function name in `receiver.py` |
| `name` | Permission display name |

---

## `receiver.py` — Data Takeover

The default template is commented out — uncomment it to enable:

```python
from bomiot.server.core.message import msg_message_return, detail_message_return, login_message_return
from bomiot.server.core.models import Example
from bomiot.server.core.utils import queryset_to_dict


class ExampleClass(object):

    def example_get(self, data):
        print(data.get('query_params').get('params'))
        example_list = Example.objects.filter()
        qs_list = queryset_to_dict(example_list)
        return [
            ('results', data.get('data')),
        ]

    def example_create(self, data):
        print(data.get('data'))
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Create")

    def example_update(self, data):
        print(data.get('data'))
        print(data.get('updated_fields'))
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Update")

    def example_delete(self, data):
        print(data.get('data'))
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Delete")
```

- Method names correspond to `func_name` in `api.py`: `example_get`, `example_create`, `example_update`, `example_delete`.

---

## `data` Parameter Structure

The `data` parameter passed to receiver methods is a dict containing the following keys:

| Key | Description | Available in |
| --- | --- | --- |
| `request` | Django request object | All |
| `mode` | Operation mode: `create`, `update`, `delete` (POST requests only) | create, update, delete |
| `data` | Request body data | create, update, delete |
| `query_params` | Query parameters (for GET) | get |
| `updated_fields` | Dict of changed fields with old/new values | update |

> The project name is not a key in `data`, but is obtained from the request header: `data.get('request').META.get('HTTP_PROJECT')`.

### Project Isolation

Models that inherit from `DataCoreModel` include a `project` field for multi-project data isolation:

```python
class DataCoreModel(models.Model):
    project = models.CharField(max_length=255, default='bomiot', verbose_name='Project Name')
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")
```

- **On create**: The `project` field is automatically set to the value of the `HTTP_PROJECT` header.
- **On query**: Results are automatically filtered by `project` matching the `HTTP_PROJECT` header, ensuring each project only sees its own data.

Get the current language from the request:

```python
language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
```

---

## `GET`

```python
def example_get(self, data):
    print(data.get('query_params').get('params'))  # Get query params
    example_list = Example.objects.filter()
    qs_list = queryset_to_dict(example_list)  # Serialize queryset
    return [
        ('results', data.get('data')),
    ]
```

- The `data` field in `CoreModel` is a `JSONField`. Raw queryset results nest business data inside `data`:

```json
[{
    "id": 1,
    "data": {
        "name": "test1",
        "type": 1
    },
    "project": "greaterwms",
    "is_delete": false,
    "created_time": "datetime",
    "updated_time": "datetime"
}]
```

- Use `queryset_to_dict` to flatten the `data` JSONField into top-level fields:

```json
[{
    "id": 1,
    "name": "test1",
    "type": 1,
    "project": "greaterwms",
    "is_delete": false,
    "created_time": "datetime",
    "updated_time": "datetime"
}]
```

- In general, you do not need to take over GET requests.
- Take over the interface only when you need to add or transform data before returning to the front end.

```python
return [
    ('results', data.get('data')),  # Default value; replace with your custom data
]
```

`Note:`

- The return value is a list of tuples in the form `[('results', data)]`.
- Use `data.get('query_params').get('params')` to get the query parameters.

---

## `Create`

```python
def example_create(self, data):
    print(data.get('data'))  # Get submitted data
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Create")
```

- The interface takes over data creation and must return an interaction result.
- If you do not take over the creation interface, the default behavior is that the back end stores whatever the front end sends.
- There are three return ports.

```python
from bomiot.server.core.message import msg_message_return, detail_message_return, login_message_return
```

`Note:`

- Only when `msg_message_return` is used will **Bomiot** store the data, and the front end will prompt success.
- When `detail_message_return` is used, the front end returns feedback that the data cannot be stored.
- When `login_message_return` is used, it triggers the front end to log in again, and the data will not be stored.

---

## `Update`

```python
def example_update(self, data):
    print(data.get('data'))  # Get submitted data
    print(data.get('updated_fields'))  # Get updated fields
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Update")
```

- The difference between updating and creating data is that **Bomiot** tells you which fields have been updated via `data.get('updated_fields')`.
- `updated_fields` is a dict: `{field_name: (old_value, new_value)}`.
- Other mechanisms are the same as creating data.

---

## `Delete`

```python
def example_delete(self, data):
    print(data.get('data'))  # Get submitted data (contains `id`)
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Delete")
```

- The mechanism is the same as creating data.

---

## Notes

- **Bomiot**'s signal mechanism supports hot update, meaning it takes effect immediately without restarting the server.
- After data takeover, point to other files for calling to avoid `receiver.py` becoming too bloated.
- The `data` field in `CoreModel` is a `JSONField`, which unifies front-end and back-end data.
