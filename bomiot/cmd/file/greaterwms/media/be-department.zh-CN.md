# 部门隔离

## 概述

bomiot 后端通过 `department` 字段实现数据隔离。用户只能看到自己部门及下级部门的数据，上级部门的数据不可见。

> 注意：bomiot 框架的 `CorePermission.has_permission` 直接 `return True`，**没有权限管理功能**。数据隔离仅靠 `get_queryset` 中的 department 过滤实现。

## 1. User 模型

`bomiot/server/core/models.py`：

```python
class User(AbstractUser, CoreModel):
    department = models.IntegerField(default=0)  # 0 = 超管
```

- `department = 0`：超级管理员，可见所有部门数据
- `department = N`（N > 0）：普通用户，只能看到 `department >= N` 的数据

## 2. get_queryset 中的部门隔离

`bomiot/server/core/handler.py`（`ExampleList.get_queryset`）和 `bomiot/server/function/goods.py`（`GoodsList.get_queryset`）实现一致：

```python
def get_queryset(self):
    project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    # ... 解析查询参数 ...

    if not any(key.startswith('data__department') for key in query_data):
        query_data = {key: value for key, value in query_data.items()
                      if not key.startswith('data__department')}
        if self.request.auth.department == 0:
            department_condition = {"data__department__gte": 0}
        else:
            department_condition = {"data__department__gte": self.request.auth.department}
    else:
        department_condition = {"data__department__gte": self.request.auth.department}

    # ... 构建查询条件 ...
    or_conditions.append(Q(**{key: value, **department_condition,
                              "is_delete": query_data['is_delete'],
                              "project": project_name}))
    return models.Example.objects.filter(query_conditions).order_by(ordering)
```

### 隔离规则

| 用户 department | 查询条件 | 可见范围 |
|----------------|----------|----------|
| 0（超管） | `data__department__gte=0` | 所有部门 |
| 1 | `data__department__gte=1` | 部门 1 及下级 |
| 2 | `data__department__gte=2` | 部门 2 及下级，看不到部门 1 |

### 防越权

即使用户在查询参数中显式传入 `data__department`，仍以 `__gte=self.request.auth.department` 兜底，防止越权查询上级部门。

## 3. 部门层级设计

部门用整数表示层级，数值越大层级越低：

```
department = 0  → 超管（总公司）
department = 1  → 一级部门
department = 2  → 二级部门
department = 3  → 三级部门
...
```

- 部门 1 能看到部门 1、2、3... 的数据
- 部门 2 只能看到部门 2、3... 的数据，看不到部门 1 的

## 4. 与 Project 隔离组合

每个查询同时带 `project` 和 `department` 两个过滤条件：

```python
Q(**{key: value,
     **department_condition,           # 部门隔离
     "is_delete": query_data['is_delete'],  # 软删除
     "project": project_name})               # 项目隔离
```

三层隔离叠加：**项目隔离 + 部门隔离 + 软删除**。

## 5. 设置用户部门

`bomiot/server/core/views.py`：

```python
class UserSetDepartment(viewsets.ModelViewSet):
    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=int(data.get('id')), is_delete=False)
        if user_check.exists():
            user_data = user_check.first()
            user_data.department = int(data.get('department'))
            user_data.save()
        return Response(msg_message_return(language, "Success set department"), status=200)
```

设置后立即生效，下次查询 `get_queryset` 会用新的 `department` 值过滤。
