# JWT Authentication

## Location

- `bomiot/server/core/jwt_auth.py` — JWT create/parse
- `bomiot/server/core/auth.py` — DRF authentication class
- `bomiot/server/core/middlewares.py` — JWT middleware

## create_token

```python
def create_token(payload):
    headers = {"type": "JWT", "alg": "HS256"}
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=settings.USER_JWT_TIME)
    token = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    return token
```

- Algorithm: HS256
- Expiry: `USER_JWT_TIME` from setup.ini (default 1000000 seconds)
- Salt: `JWT_SALT` from settings (default `settings.SECRET_KEY`)

## parse_payload

```python
def parse_payload(token):
    result = {"status": False, "data": None, "error": None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, algorithms="HS256",
                                       options={"verify_exp": True})
        result["status"] = True
        result['data'] = verified_payload
    except jwt.ExpiredSignatureError:
        result['detail'] = 'Token Expired'
    except jwt.DecodeError:
        result['detail'] = 'Token Authentication Failed'
    except jwt.InvalidTokenError:
        result['detail'] = 'Illegal Token'
    return result
```

## Login Flow (server/views.py)

```python
def logins(request):
    data = json.loads(request.body.decode())
    user_check = User.objects.filter(username=data.get('username'), is_delete=False)
    if user_check.exists() is False:
        return JsonResponse(login_message_return(lang, "User not exists"))

    user = authenticate(username=data.get('username'), password=data.get('password'))
    if user:
        if user.is_active:
            login(request, user)
            user_info = {
                "id": user.id,
                "username": user.username,
                "admin": user.is_superuser,
                "permission": user.permission
            }
            token = create_token(user_info)
            return JsonResponse({'token': token, 'msg': 'Success Login'})
    else:
        # Increment request_limit, lock after REQUEST_LIMIT attempts
        user_data.request_limit += 1
        if user_data.request_limit >= settings.REQUEST_LIMIT:
            user_data.is_active = False
```

## CoreAuthentication (DRF)

```python
class CoreAuthentication:
    def authenticate(self, request):
        # Skip auth for public paths
        if request.path in ['/', '/django/api/', '/django/core/user/permission/']:
            return False, None

        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            raise APIException(login_message_return(lang, 'Please Login First'))

        result = parse_payload(token)
        if result.get('status') is False:
            raise APIException(login_message_return(lang, 'Please Login Again'))

        user_id = result.get('data', {}).get('id')
        user = User.objects.filter(id=user_id, is_delete=False).first()
        if not user:
            raise APIException(login_message_return(lang, "User not exists"))
        if not user.is_active:
            raise APIException(login_message_return(lang, 'User is not active'))

        # Verify permission matches token
        if sorted(user.permission.items()) != sorted(user_permissions.items()):
            raise APIException(login_message_return(lang, 'Please Login Again'))

        return True, user
```

## JwtAuthorizationMiddleware

```python
class JwtAuthorizationMiddleware(MiddlewareMixin):
    ALLOWED_PATHS = ['/', '/login/', '/favicon.ico']
    ALLOWED_PREFIXES = ['/admin/', '/statics/', '/js/', '/css/', '/assets/']
    ALLOWED_METHODS = ['OPTIONS']

    def process_request(self, request):
        if self._is_allowed_path(request) or request.method in self.ALLOWED_METHODS:
            return  # Skip auth

        token = request.META.get('HTTP_TOKEN', '')
        if token:
            result = parse_payload(token).get('status')
            if result is True:
                return  # Valid token
            else:
                raise APIException(login_message_return(lang, 'Please Login Again'))
        else:
            raise APIException(login_message_return(lang, 'Please Login First'))
```

## Auth Layers

```
1. JwtAuthorizationMiddleware  — token presence + basic validation
2. CoreAuthentication           — user validation + permission check
3. CorePermission               — path-based permission (currently allows all)
```
