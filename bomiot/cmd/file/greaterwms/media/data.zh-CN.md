# 数据监控

## 介绍

Bomiot 的自带 API 通过 `bomiot_data_signals` 信号把前后端的数据交互（查询、创建、更新、删除）实时送到项目侧接管：

- `api.py` 声明 URL 与接管函数名的映射
- `receiver.py` 实现对应的接管方法，方法的返回值直接决定数据是否落库、前端收到什么反馈

不接管时接口也能工作：查询走默认过滤返回，写操作原样返回提交数据（不落库）。

---

## 工作流程

### 写操作（创建 / 更新 / 删除）

1. 前端请求命中内置 API（如 `/core/asn/create/`），视图先开启数据库事务
2. 视图发送 `bomiot_data_signals` 信号，携带 `request`、`mode`（`create` / `update` / `delete`）、`data`，更新操作额外携带 `updated_fields`
3. 框架信号接收器从请求头 `HTTP_PROJECT` 读取项目名（缺省或值为 `bomiot` 时使用主工程名），动态加载**该项目**的 `api.py`，按 URL 查出 `func_name`
4. 框架用 AST 解析**主工程** `greaterwms/receiver.py`，动态加载并调用与 `func_name` 同名的方法
5. 方法返回一个字典，框架按返回键决定行为：

| 返回 | 数据行为 | 前端表现 |
|---|---|---|
| `{"msg": ...}` | **落库**（创建注入创建人与部门、更新剔除保护字段、删除转软删除） | 提示成功 |
| `{"detail": ...}` | 不落库 | 提示失败原因 |
| `{"login": ...}` | 不落库 | 触发重新登录 |
| 未接管 / 方法不存在 | 不落库，原样返回提交数据 | 无提示 |

> 整个写操作在事务中执行，接管方法抛异常会回滚并返回 400。

### 查询（GET）

1. 视图按 `project` + `is_delete` + 部门条件过滤数据，分页前把每行的 `data` JSONField **自动展平**为顶层字段
2. 分页响应组装时发送信号（`mode='get'`），携带 `query_params`（解析后的查询参数）与 `data`（当前页数据）
3. 接管方法返回**元组列表**：
   - `('results', 数据)`：替换本页结果（不返回该项则保持原结果）
   - 其他 `('键', 值)`：作为额外字段附加到响应中

> 查询一般无需接管，只有需要在前端拿到加工后的数据时才接管。

---

## 文件位置

两个文件的作用域不同，这是机制设计上的关键点：

```shell
workspace/                    # 工作区
├── setup.ini
├── greaterwms/               # 主工程
│   └── receiver.py           # 数据接管（全局唯一，所有项目共用）
└── <your_project>/           # 各子项目
    └── api.py                # API 路由表（按 HTTP_PROJECT 请求头切换）
```

- `api.py` 按项目隔离：请求头 `HTTP_PROJECT` 决定加载哪个项目的 `api.py`
- `receiver.py` 全局只有一份：所有项目的写操作信号都汇聚到 `greaterwms/receiver.py`

---

## `api.py` — API 路由表

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

| 字段 | 说明 |
| --- | --- |
| `method` | HTTP 方法（`GET` / `POST`） |
| `api` | URL 路径 |
| `func_name` | `receiver.py` 中的接管方法名 |
| `name` | 权限显示名称 |

URL 未出现在表中时，信号查不到 `func_name`，该请求不会被接管。

---

## `receiver.py` — 数据接管

方法名与 `api.py` 的 `func_name` 一一对应，按类组织：

```python
from bomiot.server.core.message import msg_message_return, detail_message_return

class ExampleClass(object):

    def example_get(self, data):
        print(data.get('query_params').get('params'))   # 查询参数
        return [('results', data.get('data'))]          # 保持默认结果

    def example_create(self, data):
        print(data.get('data'))                         # 提交的数据
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Create")

    def example_update(self, data):
        print(data.get('updated_fields'))               # {字段: (旧值, 新值)}
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Update")

    def example_delete(self, data):
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Delete")
```

三个返回构造函数：`msg_message_return`（落库 + 成功）、`detail_message_return`（不落库 + 失败反馈）、`login_message_return`（不落库 + 重新登录）。

---

## `data` 参数结构

| 键 | 说明 | 场景 |
| --- | --- | --- |
| `request` | 请求对象（取语言/项目：`request.META` 的 `HTTP_LANGUAGE`、`HTTP_PROJECT`） | 全部 |
| `mode` | `get` / `create` / `update` / `delete` | 全部 |
| `data` | 写操作：请求体；查询：当前页已展平数据 | 全部 |
| `query_params` | 解析后的查询参数字典 | get |
| `updated_fields` | 变更字段的新旧值 `{字段: (旧值, 新值)}` | update |

---

## 项目隔离

继承 `DataCoreModel` 的模型自带 `project` 字段：

- **写入**：落库时自动写入 `HTTP_PROJECT` 的值（创建还会注入 `creater` 与 `department`）
- **查询**：默认只返回当前项目、`is_delete=False` 且满足部门条件的数据

每个项目只能看到并操作自己的数据。

---

## 注意事项

- **热更新**：`receiver.py` 每次请求动态加载，改动即时生效，无需重启；`api.py` 走模块导入缓存，改动后需重启服务
- **保持 receiver.py 精简**：接管方法只做分发，业务逻辑放到独立模块（如 `process/` 目录）中调用，避免文件臃肿
- **软删除**：删除操作实际是 `is_delete=True`，数据仍在库中
- 更新落库前框架自动剔除 `id`、`is_delete`、`created_time`、`updated_time`，防止这些字段被前端篡改
