# setup.ini Configuration Guide

## Overview

`setup.ini` is the core configuration file of a bomiot project, located at the workspace root. Django reads it via `ConfigParser` at startup; all runtime settings (database, throttling, JWT, file upload, email, system control switches) come from this file.

**Loaded in:** `bomiot/server/server/settings.py`

```python
from configparser import ConfigParser
CONFIG = ConfigParser()
setup_ini_path = join(WORKING_SPACE, 'setup.ini')
CONFIG.read(setup_ini_path, encoding='utf-8')
```

---

## Configuration Sections

### [project]

| Field | Default | Description |
|-------|---------|-------------|
| `name` | `greaterwms` | Project name. `bomiot init` forces this to `greaterwms`; the framework uses it as the project directory name and template path prefix |

```ini
[project]
name = greaterwms
```

### [debug]

| Field | Default | Description |
|-------|---------|-------------|
| `debug` | `True` | Django DEBUG mode. Must be `False` in production |

**Source:** `DEBUG = CONFIG.getboolean('debug', 'debug', fallback=True)`

### [database]

| Field | Default | Description |
|-------|---------|-------------|
| `engine` | `sqlite` | Database engine: `sqlite`, `mysql`, `oracle`, `postgresql` |
| `name` | `db_name` | Database name (sqlite file name) |
| `user` | `db_user` | Database user |
| `password` | `db_pwd` | Database password |
| `host` | `db_host` | Database host |
| `port` | `db_port` | Database port |

**Source:** `db_engine = CONFIG.get('database', 'engine', fallback='sqlite')`

For sqlite, the database file is at `dbs/db.sqlite3`; other engines use standard Django database connection settings.

### [templates]

| Field | Default | Description |
|-------|---------|-------------|
| `name` | `templates/dist/spa/index.html` | Frontend SPA entry path (relative to project dir). Currently `IndexTemplateView` hardcodes this path; this field is reserved for future use |

### [locale]

| Field | Default | Description |
|-------|---------|-------------|
| `time_zone` | `UTC` | Time zone |

**Source:** `TIME_ZONE = CONFIG.getint('local', 'time_zone', fallback='UTC')`

### [throttle]

| Field | Default | Description |
|-------|---------|-------------|
| `allocation_seconds` | `1` | Throttle time window (seconds) |
| `throttle_seconds` | `10` | Wait time after throttle is triggered (seconds) |

**Source:**
```python
ALLOCATION_SECONDS = CONFIG.getint('throttle', 'allocation_seconds', fallback=1)
THROTTLE_SECONDS = CONFIG.getint('throttle', 'throttle_seconds', fallback=10)
```

### [request]

| Field | Default | Description |
|-------|---------|-------------|
| `limit` | `2` | Per-IP request rate limit |

**Source:** `REQUEST_LIMIT = CONFIG.getint('request', 'limit', fallback=2)`

### [jwt]

| Field | Default | Description |
|-------|---------|-------------|
| `user_jwt_time` | `1000000` | JWT token lifetime (seconds) |

**Source:** `USER_JWT_TIME = CONFIG.getint('jwt', 'user_jwt_time', fallback=1000000)`

### [file]

| Field | Default | Description |
|-------|---------|-------------|
| `file_size` | `102400000` | Max single file upload size (bytes), ~100MB |
| `file_extension` | `py,png,jpg,...` | Allowed file extensions, comma-separated |

**Source:**
```python
FILE_SIZE = CONFIG.getint('file', 'file_size', fallback=102400000)
FILE_EXTENSION = CONFIG.get('file', 'file_extension', fallback='py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf').replace(' ', '').split(',')
```

### [mail]

| Field | Default | Description |
|-------|---------|-------------|
| `email_host` | `email_host` | SMTP server address |
| `email_port` | `465` | SMTP port |
| `email_host_user` | `email_host_user` | Sender email account |
| `email_host_password` | `email_host_password` | Sender email password / auth code |
| `default_from_email` | `default_from_email` | Default sender |
| `email_from` | `email_from` | Sender display |
| `email_use_ssl` | `True` | Use SSL encrypted connection |

**Source:**
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

Controls whether the three background services start with bomiot. Read in `core/apps.py` `ready()`.

| Field | Default | Description |
|-------|---------|-------------|
| `observer` | `True` | File monitoring (watchdog), watches the media directory |
| `scheduler` | `True` | Scheduled task scheduler (APScheduler) |
| `server_monitor` | `True` | Server monitoring (CPU, memory, disk, etc.) |

**Source (`core/apps.py`):**
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

## Full Default Configuration

```ini
[project]
name = greaterwms

[debug]
debug = True

[database]
# engine, Accept (sqlite, mysql, oracle, postgresql)
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

## Applying Changes

After modifying `setup.ini`, you must **restart the Django service** for changes to take effect. Configuration is loaded once at startup; runtime edits are not hot-reloaded.
