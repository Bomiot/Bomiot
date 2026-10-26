# Front-end / Back-end Interaction

## Introduction

Bomiot defines a unified interaction contract: every business API follows the same four endpoints, the same request format, and the same response structure. APIs created with `bomiot api <name>` follow this contract automatically.

How the contract enables collaboration:

- **Front-end** developers only need to remember one fixed set of endpoints and request format — they never care how the backend implements the business logic
- **Back-end** developers write no views; all business logic lives in `receiver.py` and the modules it dispatches to, while the view layer only emits signals
- Endpoint paths and request formats never change, so front and back ends can **develop in parallel** without blocking each other

---

## What `bomiot api <name>` Generates

```shell
bomiot api goods
```

A complete API app is generated under the main project:

```
greaterwms/goods/
├── models.py          # Goods model (data JSONField)
├── views.py           # 4 views (signal-emitting only, no business logic)
├── urls.py            # 4 fixed endpoints
├── serializers.py     # serializers
├── filter.py          # query filter
└── apps.py
```

The four fixed endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `goods/` | Paginated list query |
| POST | `goods/create/` | Create |
| POST | `goods/update/` | Update |
| POST | `goods/delete/` | Delete (soft delete) |

---

## Request Headers

Every request should carry these headers for identity and context:

| Header | Description |
| --- | --- |
| `token` | JWT authentication token |
| `language` | Current language, e.g. `zh-CN`, `en-US` |
| `project` | Current project identifier — decides data ownership and the `api.py` route |

---

## Query (GET)

```js
get({
  url: 'goods/',
  params: {
    params: JSON.stringify({ data__name__icontains: search.value }),
    page: requestData.pagination.page,
    max_page: requestData.pagination.rowsPerPage
  }
})
```

- `params` is a JSON-stringified set of query conditions; keys map directly to database lookup expressions (e.g. `data__name__icontains`, `order_by`)
- The backend executes the conditions as-is, automatically adding `project` (project isolation), `is_delete=False`, and department conditions
- The union of conditions is assembled by the backend — the front end does not need to care

The response structure is fixed:

```json
{
    "count": 100,
    "next": "http://.../goods/?page=2",
    "previous": null,
    "results": [
        { "id": 1, "name": "Sample", "creater": "admin", "created_time": "...", "updated_time": "..." }
    ]
}
```

> In `results`, the model's `data` JSONField is automatically flattened into top-level fields.

---

## Create / Update / Delete (POST)

All three endpoints accept the same kind of JSON body — the business data to write, submitted as-is; update and delete additionally carry an `id`:

```js
post('goods/create/', { name: 'Sample', price: 9.9 })
post('goods/update/', { id: 1, name: 'Sample', price: 19.9 })
post('goods/delete/', { id: 1 })
```

- The payload is stored whole in the model's `data` JSONField, keeping front-end and back-end fields naturally consistent — no field-by-field definitions
- On create, the backend automatically injects `creater` (current user) and `department`
- Delete is a soft delete (`is_delete=True`)

---

## Dispatch Chain: View → api.py → receiver.py

Views contain no business logic. The full chain:

1. A request hits an endpoint; the view opens a transaction and emits a `bomiot_data_signals` signal (carrying `mode` and `data`, plus `updated_fields` for updates)
2. The framework loads the project's `api.py` based on the `project` header and looks up the `func_name` for the URL
3. The framework calls the method of the same name in `greaterwms/receiver.py`
4. The method returns `msg` (persist) / `detail` (reject) / `login` (re-login), and the framework performs the corresponding action and responds

```
Fixed front-end request ──→ goods/create/ (view, no business logic)
                                 │  bomiot_data_signals
                                 ▼
                         api.py (URL → func_name)
                                 ▼
                         receiver.py (handler method)
                                 ▼
                         process/ (your business logic)
```

**The key to collaborative development**: the front end integrates against a contract that never changes, while the backend evolves freely behind `receiver.py`. The two sides only need to agree on `func_name` and data fields.

For the full takeover syntax, see Data Monitoring.

---

## Shipping a New API End to End

1. `bomiot api <name>` to generate the app
2. `bomiot makemigrations` + `bomiot migrate` to create the table
3. **Required**: register the four endpoints' `func_name` in the project's `api.py`. Without this, the signal finds no mapping — the request is never taken over and writes are never persisted:

```python
def api_return(data):
    api_list = [
        # ... existing entries ...
        {'method': 'GET',  'api': '/goods/',        'func_name': 'goods_get',    'name': 'Get Goods List'},
        {'method': 'POST', 'api': '/goods/create/', 'func_name': 'goods_create', 'name': 'Create Goods'},
        {'method': 'POST', 'api': '/goods/update/', 'func_name': 'goods_update', 'name': 'Update Goods'},
        {'method': 'POST', 'api': '/goods/delete/', 'func_name': 'goods_delete', 'name': 'Delete Goods'},
    ]
    api_dict = {api['api']: api for api in api_list}
    return api_dict.get(data, {})
```

4. Implement the matching methods in `receiver.py` (dispatching to `process/` modules)
5. The front end calls per the contract immediately — no need to wait for the backend implementation

---

## Notes

- `receiver.py` changes take effect immediately; `api.py` changes require a restart
- `order_by` in query conditions supports model fields, defaulting to `-id`
- Default page size is 30; `max_page` caps at 1000
- For the full `bomiot api <name>` command reference, see the api doc under the CLI tab
