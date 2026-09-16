# Signal 信号分发

bomiot 后端通过 Django Signals 实现 ViewSet 与业务逻辑的解耦。所有 CRUD 操作（含分页查询）都通过统一的 `bomiot_data_signals` 信号分发给项目的 `receiver.py` 处理。

## 1. 信号定义

信号位于 `bomiot/server/core/signal.py`：

```python
from django.dispatch import Signal

bomiot_signals = Signal()
bomiot_data_signals = Signal()
```

- `bomiot_signals`：用于框架级事件，例如文件上传时触发文件保存。
- `bomiot_data_signals`：业务数据信号，所有 ViewSet 的 CRUD 操作均通过该信号分发。

## 2. ViewSet 中发送信号

以 `bomiot/server/core/handler.py` 中的 `ExampleCreate.create` 为例（`bomiot/server/function/goods.py` 的 `GoodsCreate.create` 同样使用此模式）：

```python
from django.db import transaction
from bomiot.server.core.signal import bomiot_data_signals

def create(self, request, *args, **kwargs):
    data = self.request.data
    project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        project_name = settings.PROJECT_NAME
    try:
        with transaction.atomic():
            responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                        request=self.request,
                                                        mode='create',
                                                        data=data)
            for receiver, response in responses:
                if isinstance(response, Exception):
                    raise response
                if isinstance(response, dict) and response.get("msg"):
                    data['department'] = self.request.auth.department if self.request.auth else 0
                    data['creater'] = self.request.auth.username
                    models.Example.objects.create(data=data, project=project_name)
                    return Response(response)
                if isinstance(response, dict) and response.get("detail"):
                    return Response(response)
                if isinstance(response, dict) and response.get("login"):
                    return Response(response)
        return Response(data, status=status.HTTP_201_CREATED)
    except Exception as e:
        with transaction.atomic():
            transaction.set_rollback(True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

要点：
- `send_robust` 会捕获每个 receiver 抛出的异常，并以 `(receiver, exception)` 形式返回。
- ViewSet 遍历 responses，若任一 receiver 返回 `Exception`，立即 `raise` 触发 `transaction.atomic()` 回滚。
- 业务返回值约定三种：`{"msg": ...}` 表示成功并提交数据；`{"detail": ...}` 表示业务校验失败；`{"login": ...}` 表示需要重新登录。
- `mode` 取值：`'create'` / `'update'` / `'delete'` / `'get'`，与对应 CRUD 方法匹配。
- `update` 模式额外携带 `updated_fields`（变更字段对比结果）。

## 3. 分页查询中的信号分发

`bomiot/server/core/page.py` 的 `DataCorePageNumberPagination.get_paginated_response` 在 `mode='get'` 下分发信号：

```python
from bomiot.server.core.signal import bomiot_data_signals

def get_paginated_response(self, data):
    response_data = [
        ('count', self.page.paginator.count),
        ('next', self.get_next_link()),
        ('previous', self.get_previous_link()),
    ]
    data_list = list(map(lambda x: flatten_json(x) if isinstance(x, dict) else x, data))
    origin = self.request.query_params.dict()
    params_check = self.request.query_params.get('params', {})
    if params_check:
        params_str = params_check.replace('true', 'True').replace('false', 'False')
        params_str = params_check.replace("'", '"')
        params_dict = ast.literal_eval(params_str)
        if all_fields_empty(params_dict):
            origin['params'] = {}
        origin['params'] = params_dict
    else:
        origin['params'] = {}
    responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                request=self.request,
                                                mode='get',
                                                query_params=origin,
                                                data=data_list)
    for receiver, response in responses:
        if isinstance(response, Exception):
            raise response
        if isinstance(response, list):
            callback_data = True
            for i in response:
                if i[0] == 'results':
                    callback_data = False
                    break
            if callback_data is True:
                response_data += [('results', data_list)]
            response_data += response
        if response is None:
            response_data += [('results', data_list)]
    response_data += self.query_data_add()
    return Response(OrderedDict(response_data))
```

receiver 在 `mode='get'` 下可返回 `[(key, value), ...]` 列表，会被合并进响应体；返回 `None` 则自动追加默认 `results`。

## 4. 信号接收器：receiver_callback

`bomiot/server/core/utils.py` 的 `receiver_callback` 是 `bomiot_data_signals` 的统一接收器：

```python
def receiver_callback(data, method) -> dict:
    receiver_path = join(settings.WORKING_SPACE, 'greaterwms', 'receiver.py')
    receiver_check = check_method_in_file_by_ast(receiver_path, method)
    if receiver_check[0] is True:
        spec = importlib.util.spec_from_file_location("receiver", receiver_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if 'class' in receiver_check[1]:
            try:
                target_class = getattr(module, receiver_check[1]['class'])
                instance = target_class()
                if hasattr(instance, receiver_check[1]['method']):
                    result = getattr(instance, receiver_check[1]['method'])(data)
                    return result
            except AttributeError:
                print(f"class {type(receiver_check[1]).get('class')} can not find {receiver_path}")
        else:
            if hasattr(module, receiver_check[1]['method']):
                result = getattr(module, receiver_check[1]['method'])(data)
                return result
    else:
        mode = data.get('mode')
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        if mode == 'get':
            return [
                ('results', data.get('data')),
            ]
        elif mode == 'create':
            return msg_message_return(language, "Success Create")
        elif mode == 'update':
            return msg_message_return(language, "Success Update")
        elif mode == 'delete':
            return msg_message_return(language, "Success Delete")
```

`data` 字典结构：

| 字段 | 含义 |
|------|------|
| `request` | 当前 DRF Request |
| `mode` | `'get'` / `'create'` / `'update'` / `'delete'` |
| `data` | 业务数据载荷 |
| `updated_fields` | 仅 update 模式，变更字段对比 |
| `query_params` | 仅 get 模式，原始查询参数 |

`method` 由 `mode` 和 sender 类名拼接生成，例如 `goods_create` / `goods_update` / `goods_get` / `goods_delete`。

## 5. AST 方法查找

`check_method_in_file_by_ast()` 使用 Python `ast` 模块在 `receiver.py` 中按方法名定位所属类：

```python
def check_method_in_file_by_ast(file_path, method_name):
    try:
        detail = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
        found = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == method_name and isinstance(tree, ast.Module):
                    detail = {"class": node.name, "method": method_name}
                    found = True
                    break
            elif isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if item.name == method_name:
                            detail = {"class": node.name, "method": method_name}
                            found = True
                            break
                if found:
                    break
        return found, detail
    except FileNotFoundError:
        print(f"'{file_path}' can not find")
        return False, detail
    except SyntaxError as e:
        print(f"'{file_path}' {e}")
        return False, detail
```

返回 `(found, detail)`，`detail` 包含 `class`（类名）和 `method`（方法名）。仅做静态解析，不真正执行代码，便于在 receiver 未实现时安全降级。

## 6. 默认返回与降级

若 `receiver.py` 中未找到对应方法，`receiver_callback` 根据 `mode` 返回默认成功消息：

- `mode='get'`：`[('results', data)]`
- `mode='create'`：`msg_message_return(language, "Success Create")`
- `mode='update'`：`msg_message_return(language, "Success Update")`
- `mode='delete'`：`msg_message_return(language, "Success Delete")`

这样即便项目未实现 receiver，ViewSet 仍可正常返回成功，便于快速接入新模块。

## 7. send 与 send_robust

- `send_robust`：每个 receiver 独立异常捕获，ViewSet 通过 `isinstance(response, Exception)` 检测并触发事务回滚。
- `send`：用于 `bomiot_signals`，例如 `UserUpload.create` 中的文件保存信号：

```python
bomiot_signals.send(
    sender=sync_write_file,
    msg={'models': 'FileSave'},
    file_path=file_path,
    file_data=file_data
)
```

## 8. 整体流程

```
ViewSet.create()
   └── bomiot_data_signals.send_robust(mode='create', data=...)
         └── receiver_callback(data, 'goods_create')
               └── check_method_in_file_by_ast(receiver.py, 'goods_create')
                     └── importlib 动态加载 receiver.py
                           └── GoodsClass().goods_create(data)
                                 └── create_googs_process(data)
                                       └── 返回 {"msg": "Success Create"} 或 {"detail": "..."}
```

ViewSet 拿到返回值后：`msg` 提交事务并入库；`detail` 校验失败直接返回；`Exception` 触发回滚。
