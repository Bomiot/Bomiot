# Request Flow

## Complete Request Lifecycle

```
HTTP Request
  │
  ▼
Django Middleware Chain
  ├─ GZipMiddleware
  ├─ SecurityMiddleware
  ├─ SessionMiddleware
  ├─ LocaleMiddleware
  ├─ CorsMiddleware
  ├─ CommonMiddleware
  ├─ AuthenticationMiddleware
  └─ MessageMiddleware
  │
  ▼
JwtAuthorizationMiddleware
  ├─ Check ALLOWED_PATHS: '/', '/login/', '/favicon.ico'
  ├─ Check ALLOWED_PREFIXES: '/admin/', '/statics/', '/js/', ...
  ├─ Check ALLOWED_METHODS: ['OPTIONS']
  ├─ Parse token from HTTP_TOKEN header
  └─ parse_payload(token) → validate
  │
  ▼
DRF CoreAuthentication
  ├─ Skip auth for: '/', '/django/api/', '/django/core/user/permission/'
  ├─ Get token → parse_payload → get user_id + permission
  ├─ Validate user exists, is_active
  ├─ Validate permission matches token
  └─ Return (True, user)
  │
  ▼
DRF CoreThrottle
  ├─ Get IP from HTTP_X_FORWARDED_FOR or REMOTE_ADDR
  ├─ Clean expired throttle records (> 1 second)
  ├─ Count requests in ALLOCATION_SECONDS window
  └─ Reject if count >= THROTTLE_SECONDS
  │
  ▼
DRF CorePermission / NormalPermission
  └─ has_permission(request, view) → True/False
  │
  ▼
URL Routing → ViewSet
  │
  ▼
ViewSet (e.g. GoodsCreate.create)
  ├─ Get project_name from HTTP_PROJECT header
  ├─ bomiot_data_signals.send_robust(mode='create', data=data)
  │    └─ receiver_callback() dynamically imports receiver.py
  │         └─ AST finds class+method → calls GoodsClass.goods_create()
  │              └─ create_googs_process(data) validates business rules
  │                   └─ Returns msg/detail response
  ├─ Check response: msg → write to DB, detail → return error
  └─ Return Response
```

## Key Code: ViewSet Signal Dispatch

```python
with transaction.atomic():
    responses = bomiot_data_signals.send_robust(
        sender=self.__class__,
        request=self.request,
        mode='create',
        data=data
    )
    for receiver, response in responses:
        if isinstance(response, Exception):
            raise response
        if isinstance(response, dict) and response.get("msg"):
            data['department'] = self.request.auth.department
            data['creater'] = self.request.auth.username
            models.Goods.objects.create(data=data, project=project_name)
            return Response(response)
        if isinstance(response, dict) and response.get("detail"):
            return Response(response)
```

## Key Code: receiver_callback

```python
def receiver_callback(data, method):
    project_name = data.get('request').COOKIES.get('project', settings.PROJECT_NAME)
    receiver_path = join(settings.WORKING_SPACE, project_name, 'receiver.py')
    receiver_check = check_method_in_file_by_ast(receiver_path, method)
    if receiver_check[0] is True:
        # Dynamic import + AST class/method lookup + execution
        spec = importlib.util.spec_from_file_location("receiver", receiver_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        target_class = getattr(module, receiver_check[1]['class'])
        instance = target_class()
        result = getattr(instance, receiver_check[1]['method'])(data)
        return result
    else:
        # Default success message based on mode
        return msg_message_return(language, "Success Create")
```

## Response Types

| Key | Meaning | Action |
|-----|---------|--------|
| `msg` | Success | Write to DB, return success |
| `detail` | Error | Return error, no DB write |
| `login` | Auth expired | Return login required |
