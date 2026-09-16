# Backend Multi-Language Handling

## Overview

Bomiot's backend does not use Django's built-in `gettext`/`.po` translation system. Instead, it uses a lightweight **TOML file + HTTP header** approach. The frontend sends a `language` header with every request, and the backend reads the corresponding TOML translation file to return localized messages.

## Full Processing Flow

```
Frontend axios.js                 Backend Django
─────────────                   ────────────
config.headers.language          request.META['HTTP_LANGUAGE']
       │                                     │
       ▼                                     ▼
  LocalStorage read             settings.LANGUAGE_DIR/language.toml
  (default zh-CN)                          │
                                          ▼
                              tomlkit.parse() the TOML
                                          │
                                          ▼
                              message_data['category']['key']
                                          │
                                          ▼
                              return {'detail': '...'} or {'msg': '...'}
```

## 1. Frontend Sends language Header

`src/boot/axios.js` request interceptor:

```js
config.headers.language =
  JSON.parse(window.localStorage.getItem('language')) || 'zh-CN'
```

The frontend reads the user's selected language from LocalStorage (default `zh-CN`) and adds it to every request header. Django converts it to `HTTP_LANGUAGE` (auto-uppercase + `HTTP_` prefix).

## 2. Backend Reads language

The backend uniformly retrieves the language via:

```python
language = request.META.get('HTTP_LANGUAGE', 'en-US')
```

> Note: The default fallback is `en-US`, not `zh-CN`. If the frontend doesn't send this header, the backend uses English.

### Where It's Read

- `core/auth.py:66` — Login/auth error messages
- `core/page.py:133, 212, 373` — Paginated responses (permission label translation)
- `core/utils.py:309` — CRUD success messages in signal receiver callbacks
- `greaterwms/process/*/*.py` — Business module process functions
- `server/views.py:133` — Markdown endpoint

## 3. LANGUAGE_DIR Configuration

`server/settings.py:206`:

```python
LANGUAGE_DIR = join(WORKING_SPACE, 'greaterwms', 'language').replace('\\', '/')
if exists(join(WORKING_SPACE, 'greaterwms')):
    exists(LANGUAGE_DIR) or os.makedirs(LANGUAGE_DIR)
```

- Directory: `greaterwms/language/`
- Files: `zh-CN.toml`, `en-US.toml`
- Auto-created if the directory doesn't exist

## 4. TOML File Structure

`greaterwms/language/zh-CN.toml` is organized into 5 tables by message type:

```toml
[login]
"Please Login Again" = "请再次登入"
"User or Password error" = "用户或者密码错误"

[permission]
"Get User List" = "获取用户列表"
"Create ASN" = "创建到货通知书"

[detail]
"ASN has details with status greater than 1, cannot delete." = "ASN 有状态大于1的明细，不能删除"
"Customer already exists" = "客户已存在"

[msg]
"Success Create" = "创建成功"
"Success Update" = "修改成功"
"Success Delete" = "删除成功"

[others]
"Only support markdown file" = "仅支持 markdown 文件"
```

**Key convention**: English original text is the key, translation is the value. Code passes the English key when calling.

## 5. Five Message Functions

`core/message.py` provides 5 functions, one per TOML table:

- `permission_message_return(lang, data)` — returns `str`, table `[permission]`, used for permission labels and button names
- `detail_message_return(lang, data)` — returns `{'detail': str}`, table `[detail]`, used for business validation failure
- `msg_message_return(lang, data)` — returns `{'msg': str}`, table `[msg]`, used for CRUD success messages
- `login_message_return(lang, data)` — returns `{'login': str}`, table `[login]`, used for login/auth errors
- `others_message_return(lang, data)` — returns `str`, table `[others]`, used for miscellaneous messages

### Implementation (detail example)

```python
def detail_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        try:
            with open(message_path, 'r', encoding='utf-8') as message:
                message_data = parse(message.read())
            return {'detail': message_data['detail'][data]}
        except:
            return {'detail': data}
    else:
        return {'detail': data}
```

**Fallback mechanism**: If the TOML file doesn't exist or the key is missing, the original English text is returned directly, ensuring no crashes.

## 6. Usage in process Functions

`greaterwms/process/customer.py`:

```python
from bomiot.server.core.message import msg_message_return, detail_message_return

def customer_create(data):
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    if Customer.objects.filter(name=data['data'].get('name')).exists():
        return detail_message_return(language, "Customer already exists")
    return msg_message_return(language, "Success Create")
```

1. Get the request object from `data['request']`
2. Read the `HTTP_LANGUAGE` header
3. Validation fails → `detail_message_return(language, "English key")`
4. Success → `msg_message_return(language, "Success Create")`

## 7. Relationship with Django i18n

- **Translation files**: Bomiot uses TOML, Django native uses .po / .mo
- **Language detection**: Bomiot uses HTTP_LANGUAGE header, Django native uses Accept-Language / cookie
- **Trigger**: Bomiot calls message functions manually, Django native uses gettext() / trans template tags
- **Middleware**: Bomiot has no custom middleware, Django's LocaleMiddleware is loaded in MIDDLEWARE but not actually used

Although `settings.py` enables `USE_I18N = True` and `LocaleMiddleware`, actual translation is fully handled by the custom TOML solution; Django's native i18n is not used.

## 8. Steps to Add a New Translation

1. Add key-value pairs to the corresponding table in both `greaterwms/language/zh-CN.toml` and `en-US.toml`
2. Call the corresponding `*_message_return(language, "English key")` in business code
3. No restart needed (TOML is re-read on every request)
