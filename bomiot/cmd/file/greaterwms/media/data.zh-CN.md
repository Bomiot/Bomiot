# 功能数据

## 介绍

- **Bomiot** 的自带 API 是核心功能，提供了一套全新的前后端交互。
- 前后端创建/更新/删除的数据交互会通过信号全部传输到 `receiver.py` 中。
- `api.py` 将 URL 路径映射到函数名，`receiver.py` 实现对应的接管逻辑。

---

## 工作原理

1. 前端向某个 URL 发送请求（如 `/core/example/create/`），并通过 `HTTP_PROJECT` 请求头指定项目名称。
2. 视图发送 `bomiot_data_signals` 信号，携带 `request`、`mode`、`data`、`updated_fields`。
3. `admin.py` 中的 `data_callback` 从请求中读取 `HTTP_PROJECT`，加载对应项目的 `api.py`，查找该 URL 获取 `func_name`。
4. `receiver_callback` 导入 `receiver.py` 并调用与 `func_name` 匹配的方法。
5. 方法返回结果，决定数据是否被存储。

> `HTTP_PROJECT` 请求头决定加载哪个项目的 `api.py` 和 `receiver.py`。设为 `bomiot` 时会替换为默认项目名称。

---

## `api.py` — API 路由

`api.py` 定义了 URL 路径与接收函数名的映射关系：

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

| 字段 | 说明 |
| --- | --- |
| `method` | HTTP 方法（`GET` / `POST`） |
| `api` | URL 路径 |
| `func_name` | `receiver.py` 中的函数名 |
| `name` | 权限显示名称 |

---

## `receiver.py` — 数据接管

默认模板是注释状态，取消注释即可启用：

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

- 方法名与 `api.py` 中的 `func_name` 对应：`example_get`、`example_create`、`example_update`、`example_delete`。

---

## `data` 参数结构

传递给接收方法的 `data` 参数是一个字典，包含以下键：

| 键 | 说明 | 可用场景 |
| --- | --- | --- |
| `request` | Django 请求对象 | 全部 |
| `mode` | 操作模式：`create`、`update`、`delete`（仅 POST 请求） | create、update、delete |
| `data` | 请求体数据 | create、update、delete |
| `query_params` | 查询参数（GET 请求） | get |
| `updated_fields` | 变更字段的新旧值字典 | update |

> 项目名称不是 `data` 的键，而是从请求头中获取：`data.get('request').META.get('HTTP_PROJECT')`。

### 项目隔离

继承自 `DataCoreModel` 的模型包含 `project` 字段，用于多项目数据隔离：

```python
class DataCoreModel(models.Model):
    project = models.CharField(max_length=255, default='bomiot', verbose_name='Project Name')
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")
```

- **创建时**：`project` 字段自动设置为 `HTTP_PROJECT` 请求头的值。
- **查询时**：结果自动按 `project` = `HTTP_PROJECT` 过滤，确保每个项目只能看到自己的数据。

从请求中获取当前语言：

```python
language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
```

---

## 获取（GET）

```python
def example_get(self, data):
    print(data.get('query_params').get('params'))  # 获取查询参数
    example_list = Example.objects.filter()
    qs_list = queryset_to_dict(example_list)  # 序列化 queryset
    return [
        ('results', data.get('data')),
    ]
```

- `CoreModel` 中的 `data` 字段是 `JSONField`。原始 queryset 结果将业务数据嵌套在 `data` 中：

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

- 使用 `queryset_to_dict` 将 `data` JSONField 展平为顶层字段：

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

- 一般情况下，不需要接管 GET 请求。
- 仅在需要向前端返回数据中添加或转换数据时，才进行接口接管。

```python
return [
    ('results', data.get('data')),  # 这是默认值，可替换为自定义数据
]
```

`注意:`

- 返回值是元组列表，形式为 `[('results', data)]`。
- 使用 `data.get('query_params').get('params')` 获取查询参数。

---

## 创建（Create）

```python
def example_create(self, data):
    print(data.get('data'))  # 获取提交的数据
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Create")
```

- 创建数据的接口接管，必须返回交互结果。
- 如果不接管创建数据接口，默认就是前端传什么，后端存什么。
- 一共 3 种返回端口。

```python
from bomiot.server.core.message import msg_message_return, detail_message_return, login_message_return
```

`注意:`

- 只有使用 `msg_message_return` 时，**Bomiot** 才会存储数据，并且前端提示成功。
- 使用 `detail_message_return` 时，前端返回不能存储的反馈信息。
- 使用 `login_message_return` 时，会触发前端重新登录，并且数据不会被存储。

---

## 更新（Update）

```python
def example_update(self, data):
    print(data.get('data'))  # 获取提交的数据
    print(data.get('updated_fields'))  # 获取更新的字段
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Update")
```

- 更新数据与创建数据不同的是，**Bomiot** 会通过 `data.get('updated_fields')` 告诉你更新了哪些字段。
- `updated_fields` 是一个字典：`{字段名: (旧值, 新值)}`。
- 其他机制与创建数据相同。

---

## 删除（Delete）

```python
def example_delete(self, data):
    print(data.get('data'))  # 获取提交的数据（包含 `id`）
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Delete")
```

- 机制与创建数据相同。

---

## 注意

- **Bomiot** 的信号机制是热更新，即即时生效，无需重启服务器。
- 数据接管后，指向其他文件做调用，避免 `receiver.py` 过于臃肿。
- `CoreModel` 中的 `data` 字段是 `JSONField`，统一了前后端数据。
