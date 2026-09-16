# 模型设计

bomiot 后端的所有模型集中在 `bomiot/server/core/models.py`，由抽象基类 `CoreModel` / `DataCoreModel` 派生出系统模型与业务模型两大分支。本文基于源码梳理基类设计、JSON 字段模式、表名规则、查询过滤与软删除机制。

## 1. 两个抽象基类

### CoreModel —— 系统与监控模型

```python
class CoreModel(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True,
                                       verbose_name="Updated Time")

    class Meta:
        ordering = ['-id']
        abstract = True
```

只提供软删除标记与创建/更新时间，不包含 `project` 字段。`User`、`Permission`、`ThrottleModel`、`JobList`、`Files`、`Message`、`Pids`、`CPU`、`Memory`、`Disk`、`Network`、`Department` 都继承自它，因为它们属于「系统级」数据，不需要按工程隔离。

### DataCoreModel —— 业务数据模型

```python
class DataCoreModel(models.Model):
    project = models.CharField(max_length=255, default='bomiot', verbose_name='Project Name')
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True,
                                        verbose_name="Updated Time")

    class Meta:
        ordering = ['-id']
        abstract = True
```

相比 `CoreModel` 多了 `project` 字段（默认 `'bomiot'`），用于多工程数据隔离。`Team`、`Example`、`Goods`、`Bin`、`Stock`、`StockBin`、`Capital`、`Supplier`、`Customer`、`ASN`、`ASNDetail`、`DN`、`DNDetail`、`Purchase`、`Bar`、`Fee`、`Driver` 全部继承 `DataCoreModel`。

## 2. 系统模型示例

`User` 复用 Django 的 `AbstractUser`，并扩展权限、限流、团队、部门字段：

```python
class User(AbstractUser, CoreModel):
    type = models.IntegerField(default=1, verbose_name="User Type")
    phone = models.CharField(default='', max_length=255, blank=True, verbose_name="Phone")
    permission = models.JSONField(default=dict, null=True, verbose_name="Permission")
    request_limit = models.IntegerField(default=0, verbose_name="Request Limit")
    team = models.IntegerField(default=0, blank=True, verbose_name="Team")
    department = models.IntegerField(default=0, blank=True, verbose_name="Department")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_user'
        verbose_name = settings.BASE_DB_TABLE + ' User'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

- `permission` 是 JSONField，保存 `{permission_name: api_path, ...}` 字典，登录时塞进 JWT payload，`CoreAuthentication` 还会比对库中与 Token 中的字典是否一致。
- `request_limit` 由登录失败计数使用，超过 `settings.REQUEST_LIMIT` 后置 `is_active=False`。
- `department == 0` 表示管理员，业务查询时见所有部门数据。

`ThrottleModel` / `JobList` / `Files` / `Message` / `Pids` / `CPU` / `Memory` / `Disk` / `Network` 都直接继承 `CoreModel`，配合 `bomiot/server/core/scheduler.py`、`observer.py`、`server_monitor.py` 实现限流计数、定时任务元数据、文件索引、消息推送与系统监控。

## 3. 业务模型与 JSON 字段模式

所有业务模型都使用同一种结构：

```python
class Goods(DataCoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_goods'
        verbose_name = settings.BASE_DB_TABLE + ' Goods'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

`Team` 是少数派——它显式声明了 `name` 与 `permission` 字段：

```python
class Team(DataCoreModel):
    name = models.CharField(default='', max_length=255, verbose_name="Team Name")
    permission = models.JSONField(default=dict, null=True, verbose_name="Permission")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_team'
        ...
```

`ASN` 同样是纯 `data = JSONField()`：

```python
class ASN(DataCoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_asn'
        verbose_name = settings.BASE_DB_TABLE + ' ASN'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

`ASNDetail` 也是相同结构，业务字段（`asn_id` / `goods_code` / `goods_name` / `asn_qty` / `shelving_qty` / `department` / `status`）全部塞进 `data`，由 `greaterwms/process/asn/status_1.py` 写入：

```python
asn_detail = {
    'asn_id': data.get('data').get('asn_id'),
    'goods_code': i.get('selected').get('label'),
    'goods_name': i.get('selected').get('name'),
    'asn_qty': float(i.get('qty')),
    'shelving_qty': 0,
    'department': data.get('request').auth.department,
    'status': 1,
}
ASNDetail.objects.create(data=asn_detail, project=...)
```

### JSON 模式的好处

1. **零迁移扩展**：业务方随时可以往 `data` 字典加键，无需 Django migration。
2. **跨字段查询**：Django ORM 支持 `data__<key>` 双下划线语法，例如：
   ```python
   Goods.objects.filter(data__code='SKU001', data__department=2, is_delete=False)
   ```
3. **复合查询**：`Stock.objects.filter(data__goods_code=label, data__department=dept, project='greaterwms')`。
4. **差异化更新**：`Stock` 增量更新时直接改字典再 `save()`：
   ```python
   stock_data_list['asn_qty'] = float(stock_data_list.get('asn_qty', 0)) + float(qty)
   stock_list.data = stock_data_list
   stock_list.save()
   ```

### 与 django_filters 的协作

`bomiot/server/core/filter.py` 通过 `JSONFIELD_FILTER_OVERRIDE` 让 `django_filters.FilterSet` 自动识别 JSONField 子键，支持 `exact / iexact / contains / icontains / lt / lte / gt / gte / range` 等查询：

```python
def generate_jsonfield_filter(lookup_expr, filter_class):
    return {JSONField: {'filter_class': filter_class,
                         'extra': lambda f: {'lookup_expr': lookup_expr}}}

JSONFIELD_FILTER_OVERRIDE = {
    **generate_jsonfield_filter('exact', CharFilter),
    **generate_jsonfield_filter('icontains', CharFilter),
    **generate_jsonfield_filter('gte', NumberFilter),
    **generate_jsonfield_filter('range', RangeFilter),
    ...
}

class GoodsFilter(FilterSet):
    class Meta:
        model = models.Goods
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE
```

每个业务模型都有对应的 `FilterSet`（`GoodsFilter` / `BinFilter` / `StockFilter` / `ASNFilter` / `DNFilter` 等），并在 ViewSet 的 `filter_backends = [DjangoFilterBackend, OrderingFilter]` 中启用。

## 4. 表名规则

所有 `Meta.db_table` 都以 `settings.BASE_DB_TABLE` 为前缀，而 `BASE_DB_TABLE` 在 `settings.py` 中硬编码为 `'bomiot'`：

```python
BASE_DB_TABLE = 'bomiot'
```

因此实际表名为 `bomiot_user` / `bomiot_permission` / `bomiot_goods` / `bomiot_asn_detail` / `bomiot_dn_detail` 等。改 `BASE_DB_TABLE` 即可全局换表名前缀，便于多实例共用同一数据库。

## 5. ViewSet 的查询过滤

`bomiot/server/function/goods.py` 的 `GoodsList.get_queryset()` 是业务模型查询的代表：

```python
def get_queryset(self):
    project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        project_name = settings.PROJECT_NAME
    query_params = self.request.query_params.get('params', '')
    if query_params:
        query_str = query_params.replace("'", '"').replace("true", "True").replace("false", "False")
        query_data = orjson.loads(query_str)
        if all_fields_empty(query_data):
            query_data = {}
    else:
        query_data = {}
    if "is_delete" not in query_data:
        query_data['is_delete'] = False
    if not any(key.startswith('data__department') for key in query_data):
        query_data = {k: v for k, v in query_data.items()
                      if not k.startswith('data__department')}
        if self.request.auth.department == 0:
            department_condition = {"data__department__gte": 0}
        else:
            department_condition = {"data__department__gte": self.request.auth.department}
    else:
        department_condition = {"data__department__gte": self.request.auth.department}
    ordering = query_data.pop('order_by', '-id')
    query_conditions = Q()
    or_conditions = []
    if len(query_data) == 1:
        or_conditions.append(Q(**{**department_condition,
                                   "is_delete": query_data['is_delete'],
                                   "project": project_name}))
    else:
        for key, value in query_data.items():
            if key != 'is_delete':
                or_conditions.append(Q(**{key: value, **department_condition,
                                          "is_delete": query_data['is_delete'],
                                          "project": project_name}))
    if or_conditions:
        query_conditions &= Q(*or_conditions, _connector=Q.OR)
    return models.Goods.objects.filter(query_conditions).order_by(ordering)
```

要点拆解：

1. **工程隔离**：`HTTP_PROJECT` 请求头决定 `project_name`；若传 `bomiot` 则映射为 `settings.PROJECT_NAME`，最终作为 `project=project_name` 过滤条件。
2. **前端查询参数**：`?params={'data__code':'SKU001', 'data__department__gte':2}` 形式的 JSON 字符串，先做 `True/False` 替换再 `orjson.loads`。
3. **强制软删除过滤**：若未传 `is_delete`，自动补 `is_delete=False`。
4. **部门隔离**：
   - 前端未显式传 `data__department*` 时，按用户身份注入 `data__department__gte=<user.department>`，`department == 0` 视为管理员可见全部（`gte 0`）。
   - 前端若显式传，则保留其条件但仍叠加 `gte user.department` 兜底，避免越权。
5. **多条件 OR**：多个查询字段之间用 `Q.OR` 连接，配合 `is_delete` 与 `project` 共同构成每个分支的 AND 条件，最终拼成 `(cond1 OR cond2 OR ...) AND is_delete AND project`。
6. **排序**：`order_by` 默认 `-id`，可被前端参数覆盖。

`DataCorePageNumberPagination.get_paginated_response()` 在列表返回前还会以 `mode='get'` 发一次信号，让 `receiver` 有机会追加额外的列表字段（例如统计聚合），最后输出 `{'count', 'next', 'previous', 'results'}` 结构。

## 6. 软删除与写操作

业务 ViewSet 的 `delete()` 不真正 `DELETE`，而是 `update(is_delete=True, updated_time=timezone.now())`：

```python
class GoodsDelete(ModelViewSet):
    queryset = models.Goods.objects.filter(is_delete=False)

    def delete(self, request, *args, **kwargs):
        data = self.request.data
        db_data = models.Goods.objects.filter(id=data.get('id'), is_delete=False)
        with transaction.atomic():
            responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                                        request=self.request,
                                                        mode='delete',
                                                        data=data)
            for receiver, response in responses:
                if isinstance(response, dict) and response.get("msg"):
                    db_data.update(project=project_name, is_delete=True,
                                   updated_time=timezone.now())
                    return Response(response)
```

- `queryset` 已带 `is_delete=False` 过滤，避免误删已软删的记录。
- 收到 `msg` 才真正落库；收到 `detail` 直接返回业务错误不删除。
- 整段包在 `transaction.atomic()` 中，receiver 抛异常会触发回滚。

`create` 与 `update` 同样在事务中：`create` 收到 `msg` 后执行 `models.Goods.objects.create(data=data, project=project_name)`；`update` 先 `queryset_to_dict` 取旧值、`compare_dicts` 计算 `updated_fields`，再 `db_data.update(data=data, project=project_name, updated_time=timezone.now())`。所有写操作都以信号回调的返回值为前置条件，确保业务规则先于数据库变更被校验。

## 7. 模型清单速查

| 模型 | 基类 | 特有字段 | 表名 |
|------|------|----------|------|
| `User` | `AbstractUser, CoreModel` | `type/phone/permission/request_limit/team/department` | `bomiot_user` |
| `Permission` | `CoreModel` | `api/name` | `bomiot_permission` |
| `ThrottleModel` | `CoreModel` | `ip/method` | `bomiot_throttle` |
| `JobList` | `CoreModel` | `job_id/module_name/func_name/trigger/description/configuration/type` | `bomiot_job` |
| `Files` | `CoreModel` | `name/type/size/owner/shared_to` | `bomiot_files` |
| `Message` | `CoreModel` | `sender/receiver/detail/can_send` | `bomiot_message` |
| `Pids` | `CoreModel` | `pid/name/memory/create_time/memory_usage/cpu_usage` | `bomiot_pids` |
| `CPU` | `CoreModel` | `cpu_usage/physical_cores/logical_cores/cpu_frequency/...` | `bomiot_cpu` |
| `Memory` | `CoreModel` | `total/used/free/percent/swap_*` | `bomiot_memory` |
| `Disk` | `CoreModel` | `device/mountpoint/total/used/free/percent` | `bomiot_disk` |
| `Network` | `CoreModel` | `bytes_sent/bytes_recv` | `bomiot_network` |
| `Department` | `CoreModel` | `name` | `bomiot_department` |
| `Team` | `DataCoreModel` | `name/permission` | `bomiot_team` |
| `Example` | `DataCoreModel` | `data(JSONField)` | `bomiot_example` |
| `Goods` `Bin` `Stock` `StockBin` `Capital` `Supplier` `Customer` `ASN` `ASNDetail` `DN` `DNDetail` `Purchase` `Bar` `Fee` `Driver` | `DataCoreModel` | `data(JSONField)` | `bomiot_<lower>` |

后续新增业务模型只需在 `models.py` 中按 `class Xxx(DataCoreModel): data = models.JSONField()` 套用模板，配套建 `XxxFilter` 与 `XxxSerializer`，即可享受工程隔离、部门隔离、软删除、JSON 查询、信号派发的全套能力。
