# 后端多语言处理流程

## 概述

Bomiot 后端不使用 Django 内置的 `gettext`/`po` 翻译体系，而是采用 **TOML 文件 + HTTP 请求头** 的轻量级方案。前端在每个请求的 Header 中带上 `language` 字段，后端根据该值读取对应的 TOML 翻译文件，返回本地化的提示消息。

## 完整处理链路

```
前端 axios.js                    后端 Django
─────────────                   ────────────
config.headers.language          request.META['HTTP_LANGUAGE']
       │                                     │
       ▼                                     ▼
  LocalStorage 读取            settings.LANGUAGE_DIR/language.toml
  (默认 zh-CN)                          │
                                        ▼
                              tomlkit.parse() 解析 TOML
                                        │
                                        ▼
                              message_data['分类']['键名']
                                        │
                                        ▼
                              返回 {'detail': '...'} 或 {'msg': '...'}
```

## 1. 前端发送 language 请求头

`src/boot/axios.js` 的请求拦截器：

```js
config.headers.language =
  JSON.parse(window.localStorage.getItem('language')) || 'zh-CN'
```

前端从 LocalStorage 读取用户选择的语言（默认 `zh-CN`），写入每个请求的 Header。Django 会将其转为 `HTTP_LANGUAGE`（自动大写 + `HTTP_` 前缀）。

## 2. 后端读取 language

后端统一通过以下方式获取语言：

```python
language = request.META.get('HTTP_LANGUAGE', 'en-US')
```

> 注意：默认兜底值是 `en-US`，而非 `zh-CN`。若前端未发送该 Header，后端会走英文。

### 读取位置汇总

- `core/auth.py:66` — 登录/认证错误消息
- `core/page.py:133, 212, 373` — 分页响应（权限标签翻译等）
- `core/utils.py:309` — signal receiver 回调中的增删改成功消息
- `greaterwms/process/*/*.py` — 各业务模块的 process 函数
- `server/views.py:133` — Markdown 接口

## 3. LANGUAGE_DIR 配置

`server/settings.py:206`：

```python
LANGUAGE_DIR = join(WORKING_SPACE, 'greaterwms', 'language').replace('\\', '/')
if exists(join(WORKING_SPACE, 'greaterwms')):
    exists(LANGUAGE_DIR) or os.makedirs(LANGUAGE_DIR)
```

- 目录：`greaterwms/language/`
- 文件：`zh-CN.toml`、`en-US.toml`
- 若目录不存在会自动创建

## 4. TOML 文件结构

`greaterwms/language/zh-CN.toml` 按消息类型分 5 个 table：

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

**键名约定**：用英文原文作为 key，翻译文本作为 value。代码中调用时传英文 key。

## 5. 五个消息函数

`core/message.py` 提供 5 个函数，分别对应 5 个 TOML table：

- `permission_message_return(lang, data)` — 返回 `str`，对应 `[permission]`，用于权限标签、按钮名称
- `detail_message_return(lang, data)` — 返回 `{'detail': str}`，对应 `[detail]`，用于业务校验失败提示
- `msg_message_return(lang, data)` — 返回 `{'msg': str}`，对应 `[msg]`，用于增删改成功提示
- `login_message_return(lang, data)` — 返回 `{'login': str}`，对应 `[login]`，用于登录/认证错误
- `others_message_return(lang, data)` — 返回 `str`，对应 `[others]`，用于其他杂项消息

### 函数实现（以 detail 为例）

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

**兜底机制**：TOML 文件不存在或 key 未找到时，直接返回传入的英文原文，保证不会崩溃。

## 6. process 函数中的使用示例

`greaterwms/process/customer.py`：

```python
from bomiot.server.core.message import msg_message_return, detail_message_return

def customer_create(data):
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    if Customer.objects.filter(name=data['data'].get('name')).exists():
        return detail_message_return(language, "Customer already exists")
    return msg_message_return(language, "Success Create")
```

1. 从 `data['request']` 取出 request 对象
2. 读取 `HTTP_LANGUAGE` Header
3. 校验失败 → `detail_message_return(language, "英文key")`
4. 成功 → `msg_message_return(language, "Success Create")`

## 7. 与 Django 国际化的关系

- **翻译文件**：Bomiot 用 TOML，Django 原生用 .po / .mo
- **语言识别**：Bomiot 用 HTTP_LANGUAGE Header，Django 原生用 Accept-Language / cookie
- **触发方式**：Bomiot 手动调用 message 函数，Django 原生用 gettext() / trans 模板标签
- **中间件**：Bomiot 无自定义中间件，Django 原生的 LocaleMiddleware 虽在 MIDDLEWARE 中加载但未实际使用

`settings.py` 中虽启用了 `USE_I18N = True` 和 `LocaleMiddleware`，但实际翻译完全由自定义 TOML 方案完成，Django 原生 i18n 未被使用。

## 8. 新增翻译消息步骤

1. 在 `greaterwms/language/zh-CN.toml` 和 `en-US.toml` 的对应 table 中添加键值对
2. 在业务代码中调用对应的 `*_message_return(language, "英文key")`
3. 无需重启即可生效（每次请求都重新读取 TOML 文件）
