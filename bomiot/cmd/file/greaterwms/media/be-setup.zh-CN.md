# 项目配置 (setup.ini)

`setup.ini` 位于工作空间根目录，由 `bomiot init` 从框架模板 `bomiot/cmd/file/setup.ini` 拷贝生成。`bomiot/server/server/settings.py` 在启动时通过 `ConfigParser` 读取它，所有运行时配置（数据库、限流、JWT、文件上传、邮件等）都集中在此文件。本文按段说明每个 section 的字段、读取方式、回退默认值与对应的运行行为。

## 配置文件全貌

模板内容如下（节选自 `bomiot/cmd/file/setup.ini`）：

```ini
[project]
name = bomiot

[database]
# engine，Accept (sqlite、mysql、oracle、postgresql)
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port

[templates]
name = templates/dist/spa/index.html

[locale]
time_zone = 'UTC'

[throttle]
allocation_seconds = 1
throttle_seconds = 10

[request]
limit = 2

[jwt]
user_jwt_time = 1000000

[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf

[mail]
email_host = email_host
email_port = 465
email_host_user = email_host_user
email_host_password = email_host_password
default_from_email = default_from_email
email_from = email_from
email_use_ssl = True
```

> greaterwms 工程应将 `[project] name` 改为 `greaterwms`，其余字段按实际环境调整。

## settings.py 的读取入口

`bomiot/server/server/settings.py` 顶部：

```python
from configparser import ConfigParser

WORKING_SPACE = os.path.join(os.getcwd())
sys.path.insert(0, WORKING_SPACE)

CONFIG = ConfigParser()
setup_ini_path = join(WORKING_SPACE, 'setup.ini')
CONFIG.read(setup_ini_path, encoding='utf-8')
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')
```

后续每个 section 的读取都使用 `CONFIG.get` / `CONFIG.getint` / `CONFIG.getboolean`，并提供 `fallback=` 兜底默认值，即使 `setup.ini` 缺失或某段未声明，框架也能以默认值启动。

## 各 section 详解

### [project]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `name` | str | `bomiot` | 工程名，赋给 `PROJECT_NAME`，决定模板路径、媒体目录、语言包目录、动态 app 注册前缀 |

读取：

```python
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')
```

`PROJECT_NAME` 在多处被使用：`TEMPLATES_PATH = join(WORKING_SPACE, PROJECT_NAME)` 决定 Django 模板根；`STATIC_ROOT` / `MEDIA_ROOT` 在 `PROJECT_NAME != 'bomiot'` 时指向 `WORKING_SPACE/PROJECT_NAME/`；`load_apps_from_project()` 仅扫描 `WORKING_SPACE/PROJECT_NAME/` 下的子目录注册为 `PROJECT_NAME.app`。

### [database]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `engine` | str | `sqlite` | 数据库引擎，可选 `sqlite` / `mysql` / `postgresql` / `oracle` |
| `name` | str | — | 库名 / sqlite 文件路径 |
| `user` | str | — | 用户名 |
| `password` | str | — | 密码 |
| `host` | str | — | 主机 |
| `port` | str | — | 端口 |

读取分支：

```python
db_engine = CONFIG.get('database', 'engine', fallback='sqlite')
if db_engine == 'sqlite':
    DB_DIR = join(WORKING_SPACE, 'dbs')
    exists(DB_DIR) or os.makedirs(DB_DIR)
    DB_PATH = join(DB_DIR, 'db.sqlite3')
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                              'NAME': DB_PATH,
                              'CONN_MAX_AGE': 60,
                              'OPTIONS': {'timeout': 60}}}
elif db_engine == 'mysql':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql',
                              'NAME': CONFIG['database']['name'], ...,
                              'OPTIONS': {'charset': 'utf8mb4'}}}
else:
    # 走 DATABASE_MAP[engine] 通用分支
```

引擎字符串通过 `DATABASE_MAP` 映射到 Django 后端：`postgresql` → `django.db.backends.postgresql_psycopg2`，`oracle` → `django.db.backends.oracle`。sqlite 模式自动在 `WORKING_SPACE/dbs/` 下创建 `db.sqlite3`。

### [templates]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `name` | str | `templates/dist/spa/index.html` | 前端 SPA 入口 HTML 相对路径 |

模板字段当前未在 `settings.py` 中作为变量读取，而是由 `bomiot/server/server/views.py` 中的 `IndexTemplateView.get_template_names()` 直接拼接：`join(settings.WORKING_SPACE, settings.PROJECT_NAME, 'templates/dist/spa/index.html')`。

### [locale]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `time_zone` | str | `'UTC'` | 时区字符串 |

读取：

```python
TIME_ZONE = CONFIG.getint('local', 'time_zone', fallback='UTC')
```

注意 section 名为 `local`（非 `locale`），且使用 `getint`；当 `setup.ini` 写成 `time_zone = 'UTC'` 时，`getint` 会因解析失败而走 `fallback`，最终 `TIME_ZONE` 取字符串 `'UTC'`。该值同时被 `bomiot/server/core/scheduler.py` 用于 `BackgroundScheduler(timezone=...)`。

### [throttle]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `allocation_seconds` | int | `1` | 同 IP 两次请求最小间隔秒数 |
| `throttle_seconds` | int | `10` | 间隔窗口内最大请求数 |

读取：

```python
ALLOCATION_SECONDS = CONFIG.getint('throttle', 'allocation_seconds', fallback=1)
THROTTLE_SECONDS = CONFIG.getint('throttle', 'throttle_seconds', fallback=10)
```

由 `bomiot/server/core/throttle.py` 的 `CoreThrottle.allow_request` 使用：每次请求往 `ThrottleModel` 表写入一条记录，清理 1 秒之前的旧记录后判断——若距上一次请求 < `ALLOCATION_SECONDS` 且累计请求数 ≥ `THROTTLE_SECONDS`，则拒绝。

### [request]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `limit` | int | `2` | 登录失败最大重试次数 |

读取：

```python
REQUEST_LIMIT = CONFIG.getint('request', 'limit', fallback=2)
```

由 `bomiot/server/server/views.py` 的 `logins()` 使用：当用户名存在但密码错误时，`user_data.request_limit` 自增；超过 `REQUEST_LIMIT` 后将 `is_active` 置 `False` 并重置计数。

### [jwt]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `user_jwt_time` | int | `1000000` | JWT 有效期（秒） |

读取：

```python
USER_JWT_TIME = CONFIG.getint('jwt', 'user_jwt_time', fallback=1000000)
JWT_SALT = 'ds()udsjo@jlsdosjf)wjd_#(#)$'
```

由 `bomiot/server/core/jwt_auth.py` 使用：

```python
payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=settings.USER_JWT_TIME)
token = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
```

### [file]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `file_size` | int | `102400000` | 上传文件最大字节数 |
| `file_extension` | str | 见模板 | 允许的扩展名列表 |

读取：

```python
FILE_SIZE = CONFIG.getint('file', 'file_size', fallback=102400000)
FILE_EXTENSION = CONFIG.get('file', 'file_extension',
                              fallback='py,png,jpg,...,pdf').replace(" ", "").split(',')
```

### [mail]

| 字段 | 类型 | 默认值 | 用途 |
|------|------|--------|------|
| `email_host` | str | `''` | SMTP 主机 |
| `email_port` | int | `465` | SMTP 端口 |
| `email_host_user` | str | `''` | 用户名 |
| `email_host_password` | str | `''` | 密码 |
| `default_from_email` | str | `''` | 默认发件人 |
| `email_from` | str | `''` | 发件人别名 |
| `email_use_ssl` | bool | `True` | 是否启用 SSL |

读取：

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.get('mail', 'email_host', fallback='')
EMAIL_PORT = CONFIG.getint('mail', 'email_port', fallback=465)
EMAIL_HOST_USER = CONFIG.get('mail', 'email_host_user', fallback='')
EMAIL_HOST_PASSWORD = CONFIG.get('mail', 'email_host_password', fallback='')
DEFAULT_FROM_EMAIL = CONFIG.get('mail', 'default_from_email', fallback='')
EMAIL_FROM = CONFIG.get('mail', 'email_from', fallback='')
EMAIL_USE_SSL = CONFIG.getboolean('mail', 'email_use_ssl', fallback=True)
```

## 不在 setup.ini 中、但常被误认在此的项

以下两项在源码中并非由 `setup.ini` 控制：

- **DEBUG**：`settings.py` 中硬编码 `DEBUG = True`，未读取 `[debug]` 段。生产部署应改为从环境变量读取或直接编辑 `settings.py`。
- **observer / scheduler / server_monitor**：在 `bomiot/server/core/apps.py` 的 `CoreConfig.ready()` 中由文件锁保证单次启动，当 `os.environ.get('WORKERS', 0) > 0` 时统一拉起 `start_monitoring()`、`sm.start()`、`ob.start()`，未通过 `setup.ini` 的 `[system_control]` 段控制开关。如需独立关闭，可改 `apps.py` 或调整 `WORKERS` 环境变量。

## 关键全局变量一览

| 变量 | 来源 | 作用 |
|------|------|------|
| `WORKING_SPACE` | `os.getcwd()` | 工作空间根，所有相对路径基准 |
| `PROJECT_NAME` | `[project] name` | 工程名前缀 |
| `BASE_DB_TABLE` | 硬编码 `'bomiot'` | 所有模型 `db_table` 前缀（如 `bomiot_goods`） |
| `BASE_DIR` | `bomiot/server/` | 框架自身目录 |
| `LANGUAGE_DIR` | `WORKING_SPACE/PROJECT_NAME/language` | i18n toml 目录 |
| `STATIC_ROOT` / `MEDIA_ROOT` | `WORKING_SPACE/PROJECT_NAME/...` | 静态/媒体根 |
| `KEY` | `WORKING_SPACE/auth_key.py` | 可选的额外密钥（用于 JWT 之外的加密） |

修改 `setup.ini` 后需重启 Django 进程生效；动态 app 发现、URL 包含等也都在 `settings.py` 加载时一次性完成。
