# setup.ini 配置详解

## 概述

`setup.ini` 是 bomiot 项目的核心配置文件，位于工作空间根目录。Django 启动时通过 `ConfigParser` 读取该文件，所有运行时配置（数据库、限流、JWT、文件上传、邮件、系统控制开关等）均来自于此。

**读取位置：** `bomiot/server/server/settings.py`

```python
from configparser import ConfigParser
CONFIG = ConfigParser()
setup_ini_path = join(WORKING_SPACE, 'setup.ini')
CONFIG.read(setup_ini_path, encoding='utf-8')
```

---

## 完整配置项

### [project]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `name` | `greaterwms` | 项目名称。`bomiot init` 时会强制设为 `greaterwms`，框架内部以此作为项目目录名和模板路径前缀 |

```ini
[project]
name = greaterwms
```

### [debug]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `debug` | `True` | Django DEBUG 模式。生产环境必须设为 `False` |

**源码：** `DEBUG = CONFIG.getboolean('debug', 'debug', fallback=True)`

### [database]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `engine` | `sqlite` | 数据库引擎，支持 `sqlite`、`mysql`、`oracle`、`postgresql` |
| `name` | `db_name` | 数据库名称（sqlite 时为文件名） |
| `user` | `db_user` | 数据库用户名 |
| `password` | `db_pwd` | 数据库密码 |
| `host` | `db_host` | 数据库主机地址 |
| `port` | `db_port` | 数据库端口 |

**源码：** `db_engine = CONFIG.get('database', 'engine', fallback='sqlite')`

sqlite 时数据库文件位于 `dbs/db.sqlite3`；其他引擎走标准 Django 数据库连接配置。

### [templates]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `name` | `templates/dist/spa/index.html` | 前端 SPA 入口路径（相对于项目目录）。当前 `IndexTemplateView` 实际硬编码了该路径，此字段为预留配置 |

### [locale]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `time_zone` | `UTC` | 时区设置 |

**源码：** `TIME_ZONE = CONFIG.getint('local', 'time_zone', fallback='UTC')`

### [throttle]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `allocation_seconds` | `1` | 限流时间窗口（秒） |
| `throttle_seconds` | `10` | 触发限流后的等待时间（秒） |

**源码：**
```python
ALLOCATION_SECONDS = CONFIG.getint('throttle', 'allocation_seconds', fallback=1)
THROTTLE_SECONDS = CONFIG.getint('throttle', 'throttle_seconds', fallback=10)
```

### [request]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `limit` | `2` | 单 IP 请求频率限制 |

**源码：** `REQUEST_LIMIT = CONFIG.getint('request', 'limit', fallback=2)`

### [jwt]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `user_jwt_time` | `1000000` | JWT Token 有效期（秒） |

**源码：** `USER_JWT_TIME = CONFIG.getint('jwt', 'user_jwt_time', fallback=1000000)`

### [file]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `file_size` | `102400000` | 单文件上传大小上限（字节），约 100MB |
| `file_extension` | `py,png,jpg,...` | 允许上传的文件扩展名列表，逗号分隔 |

**源码：**
```python
FILE_SIZE = CONFIG.getint('file', 'file_size', fallback=102400000)
FILE_EXTENSION = CONFIG.get('file', 'file_extension', fallback='py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf').replace(' ', '').split(',')
```

### [mail]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `email_host` | `email_host` | SMTP 服务器地址 |
| `email_port` | `465` | SMTP 端口 |
| `email_host_user` | `email_host_user` | 发件邮箱账号 |
| `email_host_password` | `email_host_password` | 发件邮箱密码/授权码 |
| `default_from_email` | `default_from_email` | 默认发件人 |
| `email_from` | `email_from` | 发件人显示 |
| `email_use_ssl` | `True` | 是否使用 SSL 加密连接 |

**源码：**
```python
EMAIL_HOST = CONFIG.get('mail', 'email_host', fallback='')
EMAIL_PORT = CONFIG.getint('mail', 'email_port', fallback=465)
EMAIL_HOST_USER = CONFIG.get('mail', 'email_host_user', fallback='')
EMAIL_HOST_PASSWORD = CONFIG.get('mail', 'email_host_password', fallback='')
DEFAULT_FROM_EMAIL = CONFIG.get('mail', 'default_from_email', fallback='')
EMAIL_FROM = CONFIG.get('mail', 'email_from', fallback='')
EMAIL_USE_SSL = CONFIG.getboolean('mail', 'email_use_ssl', fallback=True)
```

### [system_control]

控制 bomiot 启动时是否启用三大后台服务，在 `core/apps.py` 的 `ready()` 中读取。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `observer` | `True` | 文件监控（watchdog），监听 media 目录变化 |
| `scheduler` | `True` | 定时任务调度器（APScheduler） |
| `server_monitor` | `True` | 服务器监控（CPU、内存、磁盘等） |

**源码（`core/apps.py`）：**
```python
_scheduler_enabled = _sys_ctrl_cfg.getboolean('system_control', 'scheduler', fallback=True)
_observer_enabled = _sys_ctrl_cfg.getboolean('system_control', 'observer', fallback=True)
_server_monitor_enabled = _sys_ctrl_cfg.getboolean('system_control', 'server_monitor', fallback=True)

if _scheduler_enabled:
    scheduler_module.sm = SchedulerManager(scheduler)
    scheduler_module.sm.start()
if _server_monitor_enabled:
    start_monitoring()
if _observer_enabled:
    ob.start()
```

---

## 默认完整配置

```ini
[project]
name = greaterwms

[debug]
debug = True

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

[system_control]
observer = True
scheduler = True
server_monitor = True
```

---

## 修改后生效

修改 `setup.ini` 后需**重启 Django 服务**才能生效。配置在服务启动时一次性加载，运行中修改不会热更新。
