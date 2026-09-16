# 请求处理链路

一次 HTTP 请求从进入 Django 到返回响应，依次经过中间件链、JWT 中间件、DRF 三大组件（认证 / 限流 / 权限）、URL 路由、ViewSet、信号派发、receiver、process 函数，最后回写数据库。本文按顺序梳理整条链路并附源码片段。

## 1. Django 中间件链

`bomiot/server/server/settings.py` 中 `MIDDLEWARE` 列表：

```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',   # 已注释
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 已注释
]
```

请求依次穿过：GZip 压缩 → 安全头 → 会话 → 本地化 → CORS（`CORS_ORIGIN_ALLOW_ALL = True` 允许全域名）→ 通用处理 → 认证（注入 `request.user`）→ 消息框架。CSRF 与 Clickjacking 默认关闭以方便 API 调用。

## 2. JWT 中间件：JwtAuthorizationMiddleware

位于 `bomiot/server/core/middlewares.py`，对每个进入业务路由的请求做一次粗粒度的 Token 校验。

```python
class JwtAuthorizationMiddleware(MiddlewareMixin):
    ALLOWED_PATHS = ['/', '/login/', '/favicon.ico']
    ALLOWED_PREFIXES = ['/admin/', '/statics/', '/js/', '/css/', '/assets/']
    ALLOWED_METHODS = ['OPTIONS']

    def process_request(self, request):
        if self._is_allowed_path(request) or request.method in self.ALLOWED_METHODS:
            return
        token = request.META.get('HTTP_TOKEN', '')
        if token:
            result = parse_payload(token).get('status')
            if result is True:
                return
            raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''),
                                                     'Please Login Again'))
        raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''),
                                                 'Please Login First'))
```

要点：

- 白名单路径（首页 / 登录 / favicon）与白名单前缀（admin / 静态资源）跳过校验；`OPTIONS` 预检请求直接放行。
- Token 从 `HTTP_TOKEN` 请求头取（即前端发 `Token: xxx`）。
- `parse_payload()` 位于 `bomiot/server/core/jwt_auth.py`，用 `jwt.decode(token, JWT_SALT, algorithms='HS256', options={'verify_exp': True})` 验签并检查过期，返回 `{'status': bool, 'data': payload, 'error': ...}`。

## 3. DRF 认证：CoreAuthentication

`REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ['bomiot.server.core.auth.CoreAuthentication']`。源码：

```python
class CoreAuthentication:
    def authenticate(self, request):
        if request.path in ['/', '/django/api/docs/', '/django/api/debug/',
                            '/django/api/', '/django/core/user/permission/']:
            return False, None
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            self._raise_api_exception(request, 'Please Login First')
        result = parse_payload(token)
        if result.get('status') is False:
            self._raise_api_exception(request, 'Please Login Again')
        user_id = result.get('data', {}).get('id')
        user_permissions = result.get('data', {}).get('permission', {})
        user = User.objects.filter(id=user_id, is_delete=False).first()
        if not user:
            self._raise_api_exception(request, "User not exists")
        if not user.is_active:
            self._raise_api_exception(request, 'User is not active')
        if sorted(user.permission.items()) != sorted(user_permissions.items()):
            self._raise_api_exception(request, 'Please Login Again')
        return True, user
```

校验顺序：取 Token → 解析 payload → 查 `User` 表（带 `is_delete=False`）→ 检查 `is_active` → 比对库中 `user.permission` 与 Token 中的 `permission` 字典是否一致（不一致即视为 Token 已失效，需重新登录）。校验通过后 `request.user` / `request.auth` 均为该 `User` 实例。

## 4. DRF 限流：CoreThrottle

`DEFAULT_THROTTLE_CLASSES = ['bomiot.server.core.throttle.CoreThrottle']`。基于 `ThrottleModel` 表的 IP 维度计数限流：

```python
class CoreThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        now_time = timezone.now()
        cur_time = now_time - timezone.timedelta(seconds=1)
        # 清理 1 秒前的旧记录
        ThrottleModel.objects.filter(method=request.method.lower(),
                                     created_time__lte=cur_time).delete()
        throttle_allocation_list = ThrottleModel.objects.filter(
            ip=ip, method=request.method.lower()).order_by('id')
        throttle_count = throttle_allocation_list.count()
        if throttle_count == 0:
            ThrottleModel.objects.create(ip=ip, method=request.method.lower())
            return True
        throttle_last_created_time = throttle_allocation_list.first().created_time
        ThrottleModel.objects.create(ip=ip, method=request.method.lower())
        allocation_seconds_balance = (now_time - throttle_last_created_time).seconds
        if allocation_seconds_balance >= settings.ALLOCATION_SECONDS:
            return True
        else:
            return throttle_count < settings.THROTTLE_SECONDS
```

阈值来自 `setup.ini`：`ALLOCATION_SECONDS`（默认 1s）控制最小间隔，`THROTTLE_SECONDS`（默认 10）控制窗口内最大次数。被拒绝时 `wait()` 返回剩余等待秒数。

## 5. DRF 权限：CorePermission

`DEFAULT_PERMISSION_CLASSES = ['bomiot.server.core.permission.CorePermission']`：

```python
class CorePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            # return contains_value(request.auth.permission, request.path)
            return True
        return False
```

当前实现等价于「已登录即放行」，具体的 `permission` 字典比对已注释；`NormalPermission` 则无条件放行，用于 `ExampleList` / `PermissionList` 等公开 ViewSet。

## 6. URL 路由 → ViewSet

`bomiot/server/server/urls.py` 根路由把 `core/` 前缀交给 `bomiot/server/core/urls.py`：

```python
urlpatterns = [
    path('', views.IndexTemplateView.as_view()),
    path('login/', views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('checktoken/', views.check_token, name='check_token'),
    path('md/<str:mddocs>', views.mdurl, name='markdown'),
    path('core/', include('bomiot.server.core.urls')),
]
```

`core/urls.py` 再把业务路径映射到 `bomiot/server/function/` 下的 ViewSet：

```python
path(r'goods/', goods.GoodsList.as_view({"get": "list"}), name="Get Goods List"),
path(r'goods/create/', goods.GoodsCreate.as_view({"post": "create"}), name="Create Goods"),
path(r'goods/update/', goods.GoodsUpdate.as_view({"post": "update"}), name="Update Goods"),
path(r'goods/delete/', goods.GoodsDelete.as_view({"post": "delete"}), name="Delete Goods")
```

## 7. ViewSet 发送信号

以 `GoodsCreate.create()` 为例：

```python
def create(self, request, *args, **kwargs):
    data = self.request.data
    project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        project_name = settings.PROJECT_NAME
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
                models.Goods.objects.create(data=data, project=project_name)
                return Response(response)
            if isinstance(response, dict) and response.get("detail"):
                return Response(response)
            if isinstance(response, dict) and response.get("login"):
                return Response(response)
    return Response(data, status=status.HTTP_201_CREATED)
```

`mode` 字段取值：`create` / `update` / `delete` / `get`，由 ViewSet 决定。`send_robust` 保证即使某个 receiver 抛异常也不会中断链路，异常会以 `(receiver, exception)` 元组形式返回，ViewSet 显式 `raise` 把它转成 500。

## 8. 信号回调：receiver_callback

`bomiot/server/core/signal.py` 只声明两个 `Signal` 实例：

```python
bomiot_signals = Signal()
bomiot_data_signals = Signal()
```

`bomiot_data_signals` 的接收者是 `bomiot/server/core/utils.py` 中的 `receiver_callback`（通过 Django `@receiver` 装饰器在 `apps.py ready` 时连入）。函数体核心：

```python
def receiver_callback(data, method) -> dict:
    project_name = data.get('request').COOKIES.get('project', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        receiver_path = join(settings.WORKING_SPACE, settings.PROJECT_NAME, 'receiver.py')
    else:
        receiver_path = join(settings.WORKING_SPACE, project_name, 'receiver.py')
    receiver_check = check_method_in_file_by_ast(receiver_path, method)
    if receiver_check[0] is True:
        spec = importlib.util.spec_from_file_location("receiver", receiver_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if 'class' in receiver_check[1]:
            target_class = getattr(module, receiver_check[1]['class'])
            instance = target_class()
            result = getattr(instance, receiver_check[1]['method'])(data)
            return result
    else:
        # 默认应答：未在 receiver.py 中实现的方法走通用成功消息
        mode = data.get('mode')
        if mode == 'get':    return [('results', data.get('data'))]
        if mode == 'create': return msg_message_return(language, "Success Create")
        if mode == 'update': return msg_message_return(language, "Success Update")
        if mode == 'delete': return msg_message_return(language, "Success Delete")
```

关键点：

- 通过 `request.COOKIES['project']` 决定加载哪个工程的 `receiver.py`，支持同进程多工程。
- `check_method_in_file_by_ast()` 用 `ast.parse` 静态扫描 `receiver.py`，定位 `method_name` 所属的类与方法名，避免直接 `import` 触发副作用。
- 找到后用 `importlib.util.spec_from_file_location` 动态加载并实例化类、调用方法。

## 9. receiver.py 派发到 process 函数

`greaterwms/receiver.py` 中按业务域定义多个类，每个方法对应一个 `mode`：

```python
class GoodsClass(object):
    def goods_create(self, data):
        return create_googs_process(data)
    def goods_update(self, data):
        return update_googs_process(data)
    def goods_delete(self, data):
        return delete_googs_process(data)
```

方法名规则：`<resource>_<mode>`，与 `bomiot_data_signals.send_robust(mode=...)` 中的 `mode` 拼接而成。

## 10. process 函数做业务校验

`greaterwms/process/goods.py`：

```python
def create_googs_process(data):
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    user_info = User.objects.filter(id=data.get('request').auth.id).first()
    goods_check = Goods.objects.filter(data__code=data.get('data').get('code'),
                                       data__department=user_info.department,
                                       is_delete=False).first()
    if goods_check is not None:
        return detail_message_return(language, "Goods already exists")
    return msg_message_return(language, "Success Create")
```

`data` 字典包含 `request`、`mode`、`data`（业务 payload），对于 update 还会带 `updated_fields`。返回值约定：

- `{'msg': ...}`：业务校验通过，ViewSet 据此落库并返回。
- `{'detail': ...}`：业务失败，ViewSet 直接返回 400/通用错误。
- `{'login': ...}`：需要重新登录。

## 11. ViewSet 落库并返回

回到 `GoodsCreate.create()`，拿到 `{'msg': 'Success Create'}` 后：

```python
if isinstance(response, dict) and response.get("msg"):
    data['department'] = self.request.auth.department if self.request.auth else 0
    data['creater'] = self.request.auth.username
    models.Goods.objects.create(data=data, project=project_name)
    return Response(response)
```

- 给 `data` 字典追加 `department` / `creater`（写入 JSON 字段）。
- 用 `models.Goods.objects.create(data=data, project=project_name)` 创建记录，`project` 字段实现工程隔离。
- 整段被 `transaction.atomic()` 包裹，任何 receiver 抛出的异常都会触发 `set_rollback(True)`，对应 400 / 500 响应。

更新与删除流程对称：`GoodsUpdate.update()` 先 `queryset_to_dict` 取旧值、`compare_dicts` 算出 `updated_fields` 一并发给信号；`GoodsDelete.delete()` 拿到 `msg` 后执行 `db_data.update(is_delete=True, updated_time=timezone.now())` 完成软删除。列表查询则在 `DataCorePageNumberPagination.get_paginated_response()` 中以 `mode='get'` 发信号，让 `receiver` 有机会追加额外的列表字段。
