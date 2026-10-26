# 前后端交互

## 介绍

Bomiot 定义了一套统一的前后端交互契约：所有业务 API 都遵循相同的四个接口、相同的请求格式、相同的响应结构。使用 `bomiot api <name>` 创建的 API 自动遵循这套契约。

契约带来的协同方式：

- **前端**只需要记住固定的一组接口和请求格式，不关心后端业务怎么实现
- **后端**不需要写视图，业务逻辑全部放在 `receiver.py` 及其分发的模块中，视图层只负责发信号
- 接口地址和请求格式始终不变，前后端可以**并行开发**，互不阻塞

---

## `bomiot api <name>` 生成物

```shell
bomiot api goods
```

在主工程下生成一个完整的 API 应用：

```
greaterwms/goods/
├── models.py          # Goods 模型（data JSONField）
├── views.py           # 4 个视图（只发信号，不含业务逻辑）
├── urls.py            # 4 个固定接口
├── serializers.py     # 序列化器
├── filter.py          # 查询过滤器
└── apps.py
```

四个固定接口：

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `goods/` | 分页查询列表 |
| POST | `goods/create/` | 创建 |
| POST | `goods/update/` | 更新 |
| POST | `goods/delete/` | 删除（软删除） |

---

## 请求头

每个请求都应携带以下请求头，完成身份与上下文识别：

| 请求头 | 说明 |
| --- | --- |
| `token` | JWT 认证令牌 |
| `language` | 当前语言，如 `zh-CN`、`en-US` |
| `project` | 当前项目标识，决定数据归属与 `api.py` 路由 |

---

## 查询（GET）

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

- `params` 是一组 JSON 字符串化的查询条件，键直接对应数据库查找表达式（如 `data__name__icontains`、`order_by`）
- 后端直接执行这组条件：自动附加 `project`（项目隔离）、`is_delete=False`、部门条件
- 查询条件的并集关系由后端统一组装，前端不需要关心

响应结构固定：

```json
{
    "count": 100,
    "next": "http://.../goods/?page=2",
    "previous": null,
    "results": [
        { "id": 1, "name": "示例", "creater": "admin", "created_time": "...", "updated_time": "..." }
    ]
}
```

> `results` 中模型的 `data` JSONField 已自动展平为顶层字段。

---

## 创建 / 更新 / 删除（POST）

三个接口接收同一种 JSON 请求体——要写入的业务数据原样提交，更新与删除额外携带 `id`：

```js
post('goods/create/', { name: '示例', price: 9.9 })
post('goods/update/', { id: 1, name: '示例', price: 19.9 })
post('goods/delete/', { id: 1 })
```

- 数据整体存入模型的 `data` JSONField，前后端字段天然一致，无需逐字段定义
- 创建时后端自动注入 `creater`（当前用户）与 `department`（部门）
- 删除为软删除（`is_delete=True`）

---

## 转发链：视图 → api.py → receiver.py

视图本身不处理业务，完整链路如下：

1. 请求命中接口，视图开启事务并发送 `bomiot_data_signals` 信号（携带 `mode`、`data`，更新另带 `updated_fields`）
2. 框架按请求头 `project` 加载该项目的 `api.py`，用 URL 查出 `func_name`
3. 框架调用 `greaterwms/receiver.py` 中的同名方法
4. 方法返回 `msg`（落库）/ `detail`（拒绝）/ `login`（重新登录），框架执行对应动作并响应前端

```
前端固定请求 ──→ goods/create/（视图，无业务逻辑）
                      │  bomiot_data_signals
                      ▼
              api.py（URL → func_name）
                      ▼
              receiver.py（接管方法）
                      ▼
              process/（你的业务逻辑）
```

**协同开发的关键**：前端对接的是永远不变的接口契约，后端在 `receiver.py` 之后的世界自由演进，双方只需约定好 `func_name` 与数据字段。

接管写法的完整说明见 数据监控。

---

## 落地一个新 API 的完整步骤

1. `bomiot api <name>` 生成应用
2. `bomiot makemigrations` + `bomiot migrate` 建表
3. **必须**在该项目的 `api.py` 中登记四个接口的 `func_name`，否则信号查不到映射，请求不会被接管、写操作不会落库：

```python
def api_return(data):
    api_list = [
        # ... 已有条目 ...
        {'method': 'GET',  'api': '/goods/',        'func_name': 'goods_get',    'name': 'Get Goods List'},
        {'method': 'POST', 'api': '/goods/create/', 'func_name': 'goods_create', 'name': 'Create Goods'},
        {'method': 'POST', 'api': '/goods/update/', 'func_name': 'goods_update', 'name': 'Update Goods'},
        {'method': 'POST', 'api': '/goods/delete/', 'func_name': 'goods_delete', 'name': 'Delete Goods'},
    ]
    api_dict = {api['api']: api for api in api_list}
    return api_dict.get(data, {})
```

4. 在 `receiver.py` 中实现对应方法（可分发到 `process/` 模块）
5. 前端按契约直接调用，无需等待后端实现完成

---

## 注意事项

- `receiver.py` 改动即时生效；`api.py` 改动需重启服务
- 查询条件中的 `order_by` 支持模型字段排序，缺省按 `-id`
- 每页默认 30 条，`max_page` 上限 1000
- `bomiot api <name>` 的详细命令说明见 CLI 命令标签下的 api 文档
