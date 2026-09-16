# 权限与部门隔离

bomiot 后端权限体系由 Permission 表、User/Team 模型、ViewSet 内权限检查以及数据隔离四部分组成。权限对象在系统启动时由 URL 自动生成，团队权限可批量下发给用户，部门字段则用于数据查询隔离。

## 1. 权限模型

`bomiot/server/core/models.py`：

```python
class Permission(CoreModel):
    api = models.CharField(max_length=255, verbose_name="Permission API")
    name = models.CharField(max_length=255, verbose_name="Permission Name")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_permission'
        verbose_name = settings.BASE_DB_TABLE + ' Permission'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

- `api`：URL 路径，如 `/core/goods/create/`。
- `name`：权限名称（即 URL `name` 反查名），如 `Create Goods`。
- `User.permission` 与 `Team.permission` 均为 `JSONField`，存储结构 `{name: api}`，例如 `{"Create Goods": "/core/goods/create/"}`。

## 2. init_permission 自动扫描

`bomiot/server/server/views.py`：

```python
def get_all_url(resolver=None, pre='/'):
    if resolver is None:
        resolver = get_resolver()
    for r in resolver.url_patterns:
        if isinstance(r, URLPattern):
            if '<pk>' in str(r.pattern):
                continue
            yield pre + str(r.pattern).replace('^', '').replace('$', ''), r.name
        if isinstance(r, URLResolver):
            yield from get_all_url(r, pre + str(r.pattern))


def permission_check(data, perm_obj_dict, api_list, user_objs):
    if str(data[0]) not in api_list and str(data[1]) != 'None':
        perm_obj, created = perm_obj_dict.get((str(data[0]), str(data[1])))
        if not perm_obj:
            perm_obj = Permission(api=str(data[0]), name=str(data[1]))
            perm_obj_dict[(str(data[0]), str(data[1]))] = perm_obj
        for user in user_objs:
            user.permission[str(data[1])] = str(data[0])
        return perm_obj


def init_permission():
    try:
        Permission.objects.all().delete()
        user_objs = list(User.objects.filter(is_superuser=True))
        media_root = settings.MEDIA_ROOT
        for user in user_objs:
            user_folder = join(media_root, user.username)
            if not exists(user_folder):
                os.makedirs(user_folder)
            user.permission = {}
        all_api_info = list(get_all_url())
        api_list = set(url_ignore())
        perm_obj_dict = {}
        perm_objs = []
        for data in all_api_info:
            if str(data[0]) not in api_list and str(data[1]) != 'None':
                perm_obj = Permission(api=str(data[0]), name=str(data[1]))
                perm_objs.append(perm_obj)
                for user in user_objs:
                    user.permission[str(data[1])] = str(data[0])
        if perm_objs:
            Permission.objects.bulk_create(perm_objs, batch_size=200)
        User.objects.bulk_update(user_objs, ['permission'], batch_size=100)
    except Exception as e:
        print(f"Error initializing permissions: {e}")
```

启动扫描流程：
1. `Permission.objects.all().delete()`：清空旧权限。
2. 取所有超级用户，清空其 `permission` 字段并初始化其媒体目录。
3. `get_all_url()` 递归遍历 URL 路由树，跳过含 `<pk>` 的详情路径，产出 `(api, name)` 列表。
4. 通过 `url_ignore()` 过滤系统级路径（如 `/admin/`、登录等）。
5. 为每个业务 URL 创建 `Permission` 记录并 `bulk_create`。
6. 将所有权限写入超管的 `permission` JSON。

## 3. 团队权限分发：TeamPermission

`bomiot/server/core/views.py`：

```python
class TeamPermission(viewsets.ModelViewSet):
    def get_permission_data(self, data):
        permission_data = models.Permission.objects.filter(name=data).first()
        return {
            permission_data.name: permission_data.api
        }

    def create(self, request, **kwargs):
        data = self.request.data
        team_check = models.Team.objects.filter(id=data.get('id'), is_delete=False)
        if team_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Team not exists"))
        else:
            team_data = team_check.first()
            if "Set Permission For Team" not in self.request.auth.permission:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "User does not have permission to set permission for team"))
            else:
                permission_list = data.get('permission')
                data_list = list(map(lambda data: self.get_permission_data(data), permission_list))
                permission_data = reduce(lambda x, y: {**x, **y}, data_list)
                team_data.permission = permission_data
                User.objects.filter(team=team_data.id, is_delete=False).update(
                    permission=permission_data
                )
                team_data.save()
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                            "Success change team permission"), status=200)
```

要点：
- 仅持有 `Set Permission For Team` 权限的用户可调用，超管天然放行。
- 通过 `reduce` 合并多个 `{name: api}` 字典。
- 写入 `Team.permission` 后立即 `User.objects.filter(team=...).update(permission=permission_data)`，团队下所有用户的权限同步刷新。
- `permission` 字段被写回 JWT（详见 `be-jwt.zh-CN.md`），下次请求若与库中不一致会被强制重新登录。

## 4. 用户归队：UserSetTeam

`bomiot/server/core/views.py`：

```python
class UserSetTeam(viewsets.ModelViewSet):
    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=int(data.get('id')), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if "Set Team For User" not in self.request.auth.permission:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "User does not have permission to set team for user"))
            else:
                team_data = models.Team.objects.filter(id=int(data.get('team_id')), is_delete=False).first()
                user_data.permission = team_data.permission if team_data else {}
                user_data.team = int(data.get('team_id'))
                user_data.save()
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                            "Success set team"), status=200)
```

用户被指派到团队后，`user_data.permission` 直接继承自 `team_data.permission`。该写入将使旧 token 中权限不一致，下次请求触发 `CoreAuthentication` 的权限一致性校验失败，强制重新登录换发新 token。

## 5. ViewSet 内权限检查

业务 ViewSet 通过判断 `self.request.auth.permission` 字典是否包含权限名（即 Permission.name）来决定放行，例如 `bomiot/server/core/views.py` 中创建用户：

```python
class UserCreate(viewsets.ModelViewSet):
    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(username=data.get('username'), is_delete=False)
        if user_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User exists"))
        else:
            if self.request.auth.is_superuser is True:
                User.objects.create_user(username=data.get('username'), password=data.get('username'))
                user_folder = join(settings.MEDIA_ROOT, data.get('username'))
                exists(user_folder) or os.makedirs(user_folder)
            else:
                if "Create One User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to create user"))
                else:
                    User.objects.create_user(username=data.get('username'), password=data.get('username'))
                    user_folder = join(settings.MEDIA_ROOT, data.get('username'))
                    exists(user_folder) or os.makedirs(user_folder)
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success Create User"), status=200)
```

权限检查统一范式：

```python
if self.request.auth.is_superuser is True:
    # 超管放行
    ...
else:
    if "<Permission Name>" not in self.request.auth.permission:
        raise APIException(detail_message_return(language, "User does not have permission to ..."))
    else:
        # 执行业务
        ...
```

涉及权限检查的 ViewSet 包括：`UserCreate`（`Create One User`）、`UserChangePWD`（`Change Password`）、`UserSetTeam`（`Set Team For User`）、`UserSetDepartment`（`Set Department For User`）、`UserLock`（`Lock & Unlock User`）、`UserDelete`（`Delete One User`）、`TeamCreate/Change/Delete`、`TeamPermission`（`Set Permission For Team`）、`DepartmentCreate/Change/Delete` 等。

## 6. 部门数据隔离：get_queryset

`bomiot/server/core/handler.py` 的 `ExampleList.get_queryset`（`bomiot/server/function/goods.py` 的 `GoodsList.get_queryset` 同样）：

```python
def get_queryset(self):
    project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        project_name = settings.PROJECT_NAME
    query_params = self.request.query_params.get('params', '')
    if query_params:
        query_str = query_params.replace("'", '"')
        query_str = query_str.replace("true", "True").replace("false", "False")
        query_data = orjson.loads(query_str)
        if all_fields_empty(query_data):
            query_data = {}
    else:
        query_data = {}
    if "is_delete" not in query_data:
        query_data['is_delete'] = False
    if not any(key.startswith('data__department') for key in query_data):
        query_data = {key: value for key, value in query_data.items() if not key.startswith('data__department')}
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
        or_conditions.append(Q(**{**department_condition, "is_delete": query_data['is_delete'], "project": project_name}))
    else:
        for key, value in query_data.items():
            if key != 'is_delete':
                or_conditions.append(Q(**{key: value, **department_condition, "is_delete": query_data['is_delete'], "project": project_name}))
    if or_conditions:
        query_conditions &= Q(*or_conditions, _connector=Q.OR)
    return models.Example.objects.filter(query_conditions).order_by(ordering)
```

部门隔离规则：
- `department == 0`：超管，`data__department__gte = 0`，可见全部部门数据。
- 其他 `department = N`：`data__department__gte = N`，可见自身部门及子部门（数值更大的下级部门）。
- 若客户端显式传入 `data__department` 过滤，仍以 `__gte = self.request.auth.department` 兜底，防止越权查询上级部门。

## 7. Project 隔离

所有 `DataCoreModel` 子类查询都强制带 `project=project_name`：

```python
project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
if project_name.lower() == 'bomiot':
    project_name = settings.PROJECT_NAME
```

通过 `HTTP_PROJECT` Header 区分不同业务前端，`'bomiot'` 关键字被强制重置为 `settings.PROJECT_NAME`，避免误查框架默认数据。Process 函数中 `Stock`、`ASNDetail`、`StockBin` 等也都带上 `project` 字段入库，形成完整的多项目数据隔离。

## 8. 权限数据流

```
init_permission() 启动扫描 URL
   └── Permission 表初始化 + 超管 user.permission 全量
         └── TeamPermission.create 写 Team.permission
               └── User.objects.filter(team=...).update(permission=...)
                     └── UserSetTeam 将 team.permission 继承给 user
                           └── login 时 create_token({id, username, admin, permission})
                                 └── CoreAuthentication 比对 token.permission 与 user.permission
                                       └── 一致 → request.auth = user
                                             └── ViewSet 检查 "<Name>" in request.auth.permission
                                                   └── get_queryset 按 department/project 隔离数据
```

权限一经变更（TeamPermission/UserSetTeam），旧 token 的 permission 与库中不一致，下次请求被强制重新登录换发新 token，确保权限即时生效。
