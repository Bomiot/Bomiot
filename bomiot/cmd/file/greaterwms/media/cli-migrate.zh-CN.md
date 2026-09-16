# bomiot migrate 命令

## 概述

`bomiot migrate` 命令用于执行数据库迁移，将所有待应用的 Django 迁移应用到数据库中。它会设置 `DJANGO_SETTINGS_MODULE` 与 `RUN_MAIN` 环境变量，调用 `django.setup()` 完成应用注册，然后调用 Django 内置的 `call_command('migrate')` 应用全部 pending 迁移。

该命令由 `bomiot/cmd/migrate.py` 中的 `migrate()` 函数实现，并在 `bomiot/cmd/cmd.py` 中注册为 `migrate` 子命令。

## 用法

```bash
bomiot migrate
```

- 该命令**不接受任何参数**。它会应用项目中所有 app 的全部未应用迁移。

在 `cmd.py` 中的注册方式：

```python
# migrate
parser_migrate = subparsers.add_parser('migrate', help='Migrate database')
```

派发逻辑：

```python
# migrate
elif command == 'migrate':
    from bomiot.cmd.migrate import migrate
    migrate()
```

## 源码分析

源文件：`bomiot/cmd/migrate.py`

完整源码如下：

```python
import os
import django
from django.core.management import call_command


def migrate():
    """
    Execute database migrations
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    django.setup()
    
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}") 
```

### 设置环境变量

命令先设置两个环境变量：

- `DJANGO_SETTINGS_MODULE`：指向 bomiot 服务器设置模块 `bomiot.server.server.settings`。
- `RUN_MAIN`：设为 `'true'`。在 Django 的自动重载机制中，`RUN_MAIN` 用于标识“主进程”，避免重复触发 reloader。在此手动设置可让迁移在单进程内直接执行。

```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
```

> `setdefault` 仅在变量未设置时写入，不会覆盖已有值。

### 初始化 Django

调用 `django.setup()` 加载设置、注册应用，使 ORM 与迁移系统可用：

```python
    django.setup()
```

### 执行迁移

调用 Django 内置的 `call_command('migrate')`，等价于在命令行执行 `python manage.py migrate`，会应用所有未应用的迁移：

```python
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}") 
```

迁移过程中若抛出异常，会被 `try/except` 捕获并打印 `Error during migration: <异常信息>`，避免进程崩溃。

## 实战示例

### 首次初始化数据库

在新建项目或刚拉取代码后，执行迁移以创建数据库表：

```bash
bomiot migrate
```

典型输出（节选）：

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### 与 makemigrations 配合使用

当你修改了模型（如在插件中新增 `models.py` 字段），需要先生成迁移再应用：

```bash
# 1. 生成迁移文件
bomiot makemigrations <appname>

# 2. 应用迁移
bomiot migrate
```

### 迁移失败时的输出

若数据库连接失败或迁移冲突，会打印错误而非崩溃：

```text
Error during migration: <具体异常信息>
```

常见原因包括：数据库未启动、连接配置错误、迁移文件存在依赖冲突等。请根据错误信息排查后重试。

## 执行前置条件

1. 已在工程根目录下运行，bomiot 环境已正确配置。
2. 数据库服务已启动且连接配置正确。
3. 对于新项目，建议先执行 `bomiot init` / `bomiot project` 初始化工程结构。

## 相关命令

- [bomiot makemigrations](#)：生成迁移文件（命令入口在 `cmd.py` 中，对应 `makemigrations` 子命令）
- [bomiot initadmin](./cli-initadmin.zh-CN.md)：创建管理员（需先 `migrate` 建表）
- [bomiot initpwd](./cli-initpwd.zh-CN.md)：重置 admin 密码（需先 `migrate` 建表）
- [bomiot init](./cli-init.zh-CN.md)：初始化工程基础文件
