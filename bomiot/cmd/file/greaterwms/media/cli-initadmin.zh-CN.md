# bomiot initadmin 命令

## 概述

`bomiot initadmin` 命令用于创建 bomiot 的默认超级管理员账户。它会设置 Django 环境变量并执行 `django.setup()`，通过 `get_user_model()` 获取用户模型，检查是否已存在名为 `admin` 的超级管理员；若不存在则创建一个，账户名为 `admin`、邮箱为 `admin@bomiot.com`、初始密码为 `admin`，并设置 `is_active`、`is_superuser`、`is_staff` 均为 `True`，最后提醒用户及时修改密码。

该命令由 `bomiot/cmd/initadmin.py` 中的 `init_admin()` 函数实现，并在 `bomiot/cmd/cmd.py` 中注册为 `initadmin` 子命令。

## 用法

```bash
bomiot initadmin
```

- 该命令**不接受任何参数**。

在 `cmd.py` 中的注册方式：

```python
# init admin
parser_initadmin = subparsers.add_parser(
    'initadmin', help='Create default super user admin')
```

派发逻辑：

```python
# init admin
elif command == 'initadmin':
    from bomiot.cmd.initadmin import init_admin
    init_admin()
```

## 源码分析

源文件：`bomiot/cmd/initadmin.py`

### 设置 Django 环境并初始化

首先设置 `DJANGO_SETTINGS_MODULE` 环境变量指向 bomiot 的服务器设置模块，然后调用 `django.setup()` 完成应用注册，之后才能使用 Django ORM：

```python
import django
import os
from configparser import ConfigParser


def init_admin():
    """
    create superuser
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model
```

> 注意：`os.environ.setdefault` 仅在环境变量未设置时写入，不会覆盖已有值。

### 获取用户模型

使用 Django 内置的 `get_user_model()` 动态获取当前项目配置的用户模型（可能是自定义 User 模型）：

```python
    User = get_user_model()
```

### 检查管理员是否已存在

通过 `User.objects.get(username='admin', is_superuser=True)` 尝试获取已存在的 admin 超级管理员。若存在则提示用户可直接登录；若抛出异常（即不存在），则进入创建分支：

```python
    try:
        User.objects.get(username='admin', is_superuser=True)
        print('Admin user already exists, you can use admin to login:')
    except:
```

### 创建管理员账户

在 `except` 分支中构造账户信息，并通过 `update_or_create` 按 `email` 与 `username` 创建或更新记录，再设置密码与权限标志：

```python
        username = 'admin'
        email = f'{username}@bomiot.com'
        password = username
        admin, created = User.objects.update_or_create(email=email, username=username)
        admin.set_password(password)
        admin.is_active = True
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        print('%s admin account: %s(%s), initial password: %s, just use it temporarily '
              'and change the password for safety' % \
              ('Created' if created else 'Reset', username, email, password))
```

关键点：

- `username = 'admin'`
- `email = 'admin@bomiot.com'`（由 `f'{username}@bomiot.com'` 拼接）
- `password = 'admin'`（与用户名相同）
- `update_or_create` 会按 `email` 与 `username` 查找，存在则更新、不存在则创建，返回 `(对象, created_bool)`。
- `set_password(password)` 会对明文密码做哈希后再保存。
- `is_active`、`is_superuser`、`is_staff` 均设为 `True`，使其具备登录后台与全部权限。
- 输出信息会根据 `created` 选择 `Created` 或 `Reset`，并明确提醒“just use it temporarily and change the password for safety”（仅供临时使用，请及时修改密码）。

## 实战示例

### 首次创建管理员

```bash
bomiot initadmin
```

输出：

```text
Created admin account: admin(admin@bomiot.com), initial password: admin, just use it temporarily and change the password for safety
```

之后即可使用 `admin` / `admin` 登录 bomiot 后台。

### 管理员已存在时再次执行

```bash
bomiot initadmin
```

输出：

```text
Admin user already exists, you can use admin to login:
```

### 执行前置条件

由于该命令需要加载 Django 设置并访问数据库，执行前请确保：

1. 已在工程根目录（含 `setup.ini` 或已配置好 bomiot 环境）下运行。
2. 已执行过 `bomiot migrate` 建表，否则 `User` 表不存在会报错。

## 安全提示

- 初始密码为弱口令 `admin`，仅供首次登录使用，登录后请立即在后台或通过 [bomiot initpwd](./cli-initpwd.zh-CN.md) 之外的途径修改为强密码。
- 该账户拥有 `is_superuser=True` 与 `is_staff=True`，具备全部后台权限，请妥善保管。

## 相关命令

- [bomiot migrate](./cli-migrate.zh-CN.md)：执行数据库迁移（`initadmin` 前需先建表）
- [bomiot initpwd](./cli-initpwd.zh-CN.md)：重置 admin 密码为 `admin`
- [bomiot init](./cli-init.zh-CN.md)：初始化工程基础文件
