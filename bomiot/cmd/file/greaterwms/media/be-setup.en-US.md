# Project Configuration (setup.ini)

## Location

`setup.ini` at workspace root (next to the project directory).

## Full Configuration

```ini
[project]
name = greaterwms

[debug]
debug = True

[database]
# engine: sqlite | mysql | postgresql | oracle
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
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,...

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

## Section Reference

| Section | Key | Setting | Fallback |
|---------|-----|---------|----------|
| project | name | `PROJECT_NAME` | `bomiot` |
| database | engine | Database engine | `sqlite` |
| database | name/user/password/host/port | DB connection | — |
| locale | time_zone | `TIME_ZONE` | `UTC` |
| throttle | allocation_seconds | `ALLOCATION_SECONDS` | `1` |
| throttle | throttle_seconds | `THROTTLE_SECONDS` | `10` |
| request | limit | `REQUEST_LIMIT` | `2` |
| jwt | user_jwt_time | `USER_JWT_TIME` | `1000000` |
| file | file_size | `FILE_SIZE` | `102400000` |
| file | file_extension | `FILE_EXTENSION` | (long list) |
| system_control | observer/scheduler/server_monitor | Background services | `True` |

## How settings.py Reads It

```python
CONFIG = ConfigParser()
setup_ini_path = join(WORKING_SPACE, 'setup.ini')
CONFIG.read(setup_ini_path, encoding='utf-8')
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')
```

## Database Selection

```python
db_engine = CONFIG.get('database', 'engine', fallback='sqlite')
if db_engine == 'sqlite':
    # SQLite: file-based, auto-created in dbs/
elif db_engine == 'mysql':
    # MySQL: uses DATABASE_MAP for engine mapping
else:
    # PostgreSQL / Oracle
```

## bomiotconf.ini

Each project/plugin has a `bomiotconf.ini`:

```ini
[mode]
name = project    # or 'plugins' for plugins
```

This tells the framework whether the directory is a project or a plugin, controlling dynamic app discovery and URL inclusion.
