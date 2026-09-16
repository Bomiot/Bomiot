# Signal Dispatch

## Location

`bomiot/server/core/signal.py`

## Two Signals

```python
from django.dispatch import Signal

bomiot_signals = Signal()         # For file/system events
bomiot_data_signals = Signal()    # For business data operations
```

## How It Works

### 1. ViewSet Sends Signal

In `handler.py` / `function/goods.py`, the ViewSet sends a signal:

```python
responses = bomiot_data_signals.send_robust(
    sender=self.__class__,
    request=self.request,
    mode='create',     # 'get' | 'create' | 'update' | 'delete'
    data=data
)
```

`send_robust` catches exceptions per receiver — the ViewSet checks for them.

### 2. Pagination Also Sends Signal

`DataCorePageNumberPagination.get_paginated_response()`:

```python
responses = bomiot_data_signals.send_robust(
    sender=self.__class__,
    request=self.request,
    mode='get',
    query_params=origin,
    data=data_list
)
```

### 3. Signal Receiver: receiver_callback()

In `utils.py`:

```python
def receiver_callback(data, method):
    project_name = data.get('request').COOKIES.get('project', settings.PROJECT_NAME)
    receiver_path = join(settings.WORKING_SPACE, project_name, 'receiver.py')
    receiver_check = check_method_in_file_by_ast(receiver_path, method)
```

### 4. AST-Based Method Discovery

`check_method_in_file_by_ast()` parses `receiver.py` using Python's `ast` module:

```python
tree = ast.parse(f.read(), filename=file_path)
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name == method_name:
                    return True, {"class": node.name, "method": method_name}
```

### 5. Dynamic Execution

```python
spec = importlib.util.spec_from_file_location("receiver", receiver_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
target_class = getattr(module, class_name)
instance = target_class()
result = getattr(instance, method_name)(data)
```

### 6. Fallback

If the method doesn't exist in `receiver.py`, default success messages are returned:

```python
if mode == 'create':
    return msg_message_return(language, "Success Create")
elif mode == 'update':
    return msg_message_return(language, "Success Update")
elif mode == 'delete':
    return msg_message_return(language, "Success Delete")
```

## Response Handling in ViewSet

```python
for receiver, response in responses:
    if isinstance(response, Exception):
        raise response  # triggers transaction rollback
    if isinstance(response, dict) and response.get("msg"):
        # Success → write to DB
        models.Goods.objects.create(data=data, project=project_name)
        return Response(response)
    if isinstance(response, dict) and response.get("detail"):
        # Business error → return without saving
        return Response(response)
    if isinstance(response, dict) and response.get("login"):
        # Auth expired
        return Response(response)
```

## Flow Diagram

```
ViewSet.create()
  └─ send_robust(mode='create', data)
       └─ receiver_callback(data, 'goods_create')
            └─ AST parse receiver.py → find GoodsClass.goods_create
                 └─ GoodsClass.goods_create(data)
                      └─ create_googs_process(data)
                           └─ validate → return msg/detail
  └─ Check response → write DB or return error
```
