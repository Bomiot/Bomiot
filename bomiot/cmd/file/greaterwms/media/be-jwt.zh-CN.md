# JWT 认证

bomiot 后端使用 HS256 算法的 JWT 进行用户身份认证，认证链路涉及 `jwt_auth.py`（令牌生成与解析）、`auth.py`（DRF 认证类）、`middlewares.py`（中间件）以及 `server/views.py`（登录入口）。

## 1. JWT 工具函数

`bomiot/server/core/jwt_auth.py`：

```python
import jwt
import datetime
from django.conf import settings

JWT_SALT = getattr(settings, "JWT_SALT", settings.SECRET_KEY)


def create_token(payload):
    """
    create JWT Token
    :param payload: JWT Token data
    :return: JWT Token
    """
    headers = {
        "type": "JWT",
        "alg": "HS256"
    }
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=settings.USER_JWT_TIME)
    token = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    return token


def parse_payload(token):
    """
    parse JWT Token
    :param token: JWT Token
    :return: include status, data, error
    """
    result = {"status": False, "data": None, "error": None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, algorithms="HS256", options={"verify_exp": True})
        result["status"] = True
        result['data'] = verified_payload
    except jwt.ExpiredSignatureError:
        result['detail'] = 'Token Expired'
    except jwt.DecodeError:
        result['detail'] = 'Token Authentication Failed'
    except jwt.InvalidTokenError:
        result['detail'] = 'Illegal Token'
    except Exception as e:
        result['detail'] = f"Unknown error: {str(e)}"
    return result
```

- `JWT_SALT` 取自 `setup.ini` 启动时生成的 `secrets.token_urlsafe(32)`（见 `settings.py`），回退到 `SECRET_KEY`。
- `exp` 由 `settings.USER_JWT_TIME` 控制，`setup.ini` 中默认 `user_jwt_time = 1000000` 秒。
- `parse_payload` 返回 `{"status": bool, "data": payload, "error": ...}`，`status=True` 表示通过。
- 失败时设置 `detail` 字段（`ExpiredSignatureError` / `DecodeError` / `InvalidTokenError`）。

## 2. DRF 认证类：CoreAuthentication

`bomiot/server/core/auth.py`：

```python
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from bomiot.server.core.message import login_message_return
from bomiot.server.core.jwt_auth import parse_payload
import typing

User = get_user_model()


class CoreAuthentication:
    """
    custom authenticate
    """

    def authenticate(self, request) -> typing.Tuple[bool, typing.Union[User, None]]:
        if request.path in ['/', '/django/api/docs/', '/django/api/debug/', '/django/api/', '/django/core/user/permission/']:
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

    def authenticate_header(self, request) -> None:
        pass

    @staticmethod
    def _raise_api_exception(request, message: str) -> None:
        language = request.META.get('HTTP_LANGUAGE', '')
        raise APIException(login_message_return(language, message))
```

认证流程：
1. **白名单跳过**：路径属于 `['/', '/django/api/docs/', '/django/api/debug/', '/django/api/', '/django/core/user/permission/']` 直接返回 `(False, None)`，不强制认证。
2. **Token 提取**：从 `HTTP_TOKEN` Header 取出 JWT；缺失则 `Please Login First`。
3. **Token 解析**：`parse_payload` 失败则 `Please Login Again`。
4. **用户存在性**：从 payload 取 `id`，查 `User` 表（排除软删除）。
5. **激活状态**：`user.is_active` 为 `False` 时拒绝。
6. **权限一致性**：将数据库中的 `user.permission` 与 token 中的 `permission` 排序后比对，不一致说明权限已变更，需重新登录换发 token。
7. 成功返回 `(True, user)`，`request.auth` 即被设置为该 `user` 实例，后续 ViewSet 可直接访问 `request.auth.department`、`request.auth.permission` 等。

## 3. 中间件：JwtAuthorizationMiddleware

`bomiot/server/core/middlewares.py`：

```python
from bomiot.server.core.jwt_auth import parse_payload
from bomiot.server.core.message import login_message_return
from rest_framework.exceptions import APIException
from django.utils.deprecation import MiddlewareMixin


class JwtAuthorizationMiddleware(MiddlewareMixin):
    ALLOWED_PATHS = [
        '/',
        '/login/',
        '/favicon.ico',
    ]
    ALLOWED_PREFIXES = [
        '/admin/',
        '/statics/',
        '/js/',
        '/css/',
        '/assets/',
    ]
    ALLOWED_METHODS = ['OPTIONS']

    def process_request(self, request):
        if self._is_allowed_path(request) or request.method in self.ALLOWED_METHODS:
            return

        token = request.META.get('HTTP_TOKEN', '')
        if token:
            result = parse_payload(token).get('status')
            if result is True:
                return
            else:
                raise APIException(
                    login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login Again')
                )
        else:
            raise APIException(
                login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login First')
            )

    def _is_allowed_path(self, request):
        if request.path_info in self.ALLOWED_PATHS:
            return True
        for prefix in self.ALLOWED_PREFIXES:
            if request.path_info.startswith(prefix):
                return True
        return False
```

- **白名单**：`ALLOWED_PATHS` 完整路径放行（`/`、`/login/`、`/favicon.ico`）；`ALLOWED_PREFIXES` 前缀放行（`/admin/`、静态资源等）。
- **OPTIONS 预检**：CORS 预检请求直接放行。
- 中间件只校验 token 有效性，不加载用户对象。后续 DRF `CoreAuthentication` 再做用户/权限校验，形成双层防护。

## 4. 登录流程：logins

`bomiot/server/server/views.py` 的 `logins` 函数负责签发 token：

```python
def logins(request):
    data = json.loads(request.body.decode().replace("'", '"'))
    user_check = User.objects.filter(username=data.get('username'), is_delete=False)
    if user_check.exists() is False:
        return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), "User not exists"))
    else:
        user = authenticate(username=data.get('username'), password=data.get('password'))
        context = {}
        if user:
            if user.is_active is True:
                login(request, user)
                user_info = {
                    "id": user.id,
                    "username": user.username,
                    "admin": user.is_superuser,
                    "permission": user.permission
                }
                token = create_token(user_info)
                context['token'] = token
                context['msg'] = others_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Success Login')
                return JsonResponse(context)
            else:
                return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User is not active'))
        else:
            user_data = user_check.first()
            if user_data.request_limit < settings.REQUEST_LIMIT:
                user_data.request_limit += 1
                user_data.save()
                return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User or Password error'))
            else:
                user_data.is_active = False
                user_data.request_limit = 0
                user_data.save()
                return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User is not active'))
```

登录链路：
1. **用户存在**：`User.objects.filter(username=...)`，软删除的不参与。
2. **密码校验**：Django 原生 `authenticate` 校验用户名密码。
3. **激活检查**：`user.is_active` 为 `True` 才允许登录。
4. **签发 token**：调用 `login(request, user)` 写入 session，构造 `user_info = {id, username, admin, permission}`，再 `create_token(user_info)` 返回。
5. **登录失败计数**：密码错误时 `request_limit += 1`；达到 `settings.REQUEST_LIMIT`（`setup.ini` 中默认 `limit = 2`）则锁定用户（`is_active = False`）并清零计数。

## 5. 登出与校验入口

`bomiot/server/server/views.py` 同时提供：

```python
@login_required
async def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'msg': others_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Welcome Back Again')})
    else:
        return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User Not Log In'))


async def check_token(request):
    token = request.META.get('HTTP_TOKEN')
    context = parse_payload(token)
    return JsonResponse(context)
```

- `logouts`：清除服务端 session，前端 token 自然失效（前端需主动丢弃）。
- `check_token`：调用 `parse_payload` 返回 `{status, data, detail}`，前端可借此判断 token 是否过期。

## 6. 链路总览

```
Client (HTTP_TOKEN: <jwt>)
   ├── JwtAuthorizationMiddleware.process_request
   │     └── 白名单放行 / parse_payload.status
   └── DRF ViewSet
         └── CoreAuthentication.authenticate
               ├── parse_payload(token) → user_id, permission
               ├── User.objects.filter(id=user_id, is_active=True)
               └── permission 一致性校验
                     └── 通过 → request.auth = user
```

任何一层失败都会通过 `login_message_return(language, ...)` 包装 `APIException`，统一返回 `{"login": "..."}` 形态供前端识别并跳转登录。
