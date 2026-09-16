# bomiot initpwd 命令

## 概述

`bomiot initpwd` 命令用于将 bomiot 默认超级管理员 `admin` 的密码重置为 `admin`。它会设置 Django 环境变量并执行 `django.setup()`，通过 `get_user_model()` 获取用户模型，查找名为 `admin` 的超级管理员，若找到则将其密码重置为 `admin`；若不存在则提示用户先创建管理员。

该命令由 `bomiot/cmd/initpwd.py` 中的 `init_password()` 函数实现，并在 `bomiot/cmd/cmd.py` 中注册为 `initpwd` 子命令。

> ⚠️ **源码存在已知 Bug**：判断管理员是否存在时使用了 `user_data.exists`（属性访问），而非 `user_data.exists()`（方法调用），导致该条件永远为真，因此即使不存在 admin 用户也会进入重置分支并触发异常。详见下文“源码中的已知问题”。

## 用法

```bash
bomiot initpwd
```

- 该命令**不接受任何参数**。

在 `cmd.py` 中的注册方式：

```python
# init password
parser_initpwd = subparsers.add_parser(
    'initpwd', help='Init admin password')
```

派发逻辑：

```python
# init admin
elif command == 'initpwd':
    from bomiot.cmd.initpwd import init_password
    init_password()
```

## 源码分析

源文件：`bomiot/cmd/initpwd.py`

完整源码如下：

```python
import django
import os


def init_password():
    """
    init superuser password
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user_data = User.objects.filter(username='admin', is_superuser=True)
    if user_data.exists:
        user_data.first().set_password('admin')
        print('Reset admin account: admin, initial password: admin, just use it temporarily '
              'and change the password for safety')
    else:
        print('Please init one admin first')
```

### 设置 Django 环境并初始化

与 `initadmin` 一致，先设置 `DJANGO_SETTINGS_MODULE` 并调用 `django.setup()`，随后动态导入 `get_user_model()`：

```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()
```

### 查询 admin 超级管理员

使用 `filter(username='admin', is_superuser=True)` 得到一个查询集 `user_data`：

```python
    user_data = User.objects.filter(username='admin', is_superuser=True)
```

### 判断并重置密码

源码意图是：若查询集非空则重置密码，否则提示先创建管理员。但实际写成了 `if user_data.exists:`：

```python
    if user_data.exists:
        user_data.first().set_password('admin')
        print('Reset admin account: admin, initial password: admin, just use it temporarily '
              'and change the password for safety')
    else:
        print('Please init one admin first')
```

### 源码中的已知问题（Bug）

Django QuerySet 的 `exists` 是一个**方法**，正确的调用形式是 `user_data.exists()`。源码写成 `user_data.exists`（不带括号）只是取得方法对象本身的引用，而方法对象在布尔上下文中**恒为真**（bound method 对象是 truthy 的）。因此：

- 无论 admin 用户是否存在，`if user_data.exists:` 永远成立，程序始终进入重置分支。
- 当 admin 用户不存在时，`user_data.first()` 返回 `None`，随后 `None.set_password('admin')` 会抛出 `AttributeError`。
- `else` 分支（提示 `Please init one admin first`）**永远不会被执行**。

**正确写法**应为：

```python
    if user_data.exists():
        user_data.first().set_password('admin')
        ...
    else:
        print('Please init one admin first')
```

## 实战示例

### admin 用户已存在时重置密码

前置：已通过 `bomiot initadmin` 创建过 admin 用户。

```bash
bomiot initpwd
```

输出：

```text
Reset admin account: admin, initial password: admin, just use it temporarily and change the password for safety
```

随后即可使用 `admin` / `admin` 登录后台。

### admin 用户不存在时（受 Bug 影响）

由于前述 Bug，当 admin 用户不存在时，命令不会输出 `Please init one admin first`，而是在 `user_data.first().set_password('admin')` 处抛出异常：

```text
AttributeError: 'NoneType' object has no attribute 'set_password'
```

因此若你尚未创建 admin 用户，请先执行：

```bash
bomiot initadmin
```

## 执行前置条件

该命令需要加载 Django 设置并访问数据库，执行前请确保：

1. 已在工程根目录下运行。
2. 已执行过 `bomiot migrate` 建表。

## 安全提示

- 重置后的密码为弱口令 `admin`，仅供临时使用，登录后请立即修改为强密码。
- 该命令不会校验调用者身份，任何能执行 `bomiot initpwd` 的人都能将 admin 密码重置为已知值，请妥善控制运行环境权限。

## 相关命令

- [bomiot initadmin](./cli-initadmin.zh-CN.md)：创建默认 admin 超级管理员
- [bomiot migrate](./cli-migrate.zh-CN.md)：执行数据库迁移（`initpwd` 前需先建表）
- [bomiot init](./cli-init.zh-CN.md)：初始化工程基础文件
