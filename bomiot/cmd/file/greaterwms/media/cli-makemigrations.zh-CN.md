# bomiot makemigrations 命令

## 概述

`bomiot makemigrations` 命令用于为 bomiot 项目中的 Django 应用生成数据库迁移文件。它会设置 Django 环境变量、调用 `django.setup()` 初始化 Django，然后通过 Django 的 `call_command('makemigrations', ...)` 生成迁移脚本。

该命令支持传入可选的 `appname` 参数来为指定应用生成迁移，也支持 `--empty` 和 `--dry-run` 两个标志。当不传入 `appname` 时，命令会自动发现所有包含 models 的应用并为其生成迁移。

该命令在 `bomiot/cmd/cmd.py` 中注册为 `makemigrations` 子命令，派发逻辑位于 `cmd()` 函数的 `makemigrations` 分支。

## 用法

```bash
bomiot makemigrations [appname] [--empty] [--dry-run]
```

- `[appname]`：可选的应用名。可以是 app label（如 `core`），也可以是完整的点分路径（如 `bomiot.server.core`）。
- `--empty`：创建一个空的迁移文件。
- `--dry-run`：仅显示将要执行的操作，不实际生成迁移文件。

在 `cmd.py` 中的注册方式：

```python
# makemigrations
parser_makemigrations = subparsers.add_parser(
    'makemigrations', help='Generate migrations for database')
parser_makemigrations.add_argument('appname', nargs='?', type=str, help='App name (e.g., xx or dev.xx)')
parser_makemigrations.add_argument('--empty', action='store_true', help='Create an empty migration')
parser_makemigrations.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
```

## 源码分析

源文件：`bomiot/cmd/cmd.py`，`cmd()` 函数中的 `makemigrations` 分支。

### 设置 Django 环境

进入分支后，首先设置 `DJANGO_SETTINGS_MODULE` 与 `RUN_MAIN` 环境变量，并调用 `django.setup()` 完成 Django 应用注册表的初始化：

```python
elif command == 'makemigrations':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    import django
    django.setup()
    from django.core.management import call_command
    from django.apps import apps
```

### 读取参数

从解析结果中取出 `appname`、`empty`、`dry_run` 三个参数，并初始化传给 `call_command` 的参数列表：

```python
    appname = args.appname
    empty = args.empty
    dry_run = args.dry_run
    cmd_args = ['makemigrations']
```

### 指定 appname 时的应用发现逻辑

当传入了 `appname` 时，根据是否包含 `.` 分两种匹配方式：

**包含 `.`（完整点分路径）**：遍历所有 app config，按 `app_config.name` 精确匹配，找到后取其 `label` 加入参数；找不到则直接返回：

```python
    if appname:
        if '.' in appname:
            found_app_label = None
            for app_config in apps.get_app_configs():
                if app_config.name == appname:
                    found_app_label = app_config.label
                    break
            if found_app_label:
                cmd_args.append(found_app_label)
            else:
                return
```

**不含 `.`（app label）**：遍历所有 app config，按 `app_config.label` 精确匹配或 `app_config.name` 以 `.` + appname 结尾匹配，找到后加入其 label；找不到则直接返回：

```python
        else:
            found_app = None
            for app_config in apps.get_app_configs():
                if app_config.label == appname or app_config.name.endswith('.' + appname):
                    found_app = app_config.label
                    break
            if found_app:
                cmd_args.append(found_app)
            else:
                return
```

### 不传 appname 时的自动发现

当未传入 `appname` 时，遍历所有 app config，检查其 `models_module` 是否存在以及是否能取到 models，把所有包含 models 的应用 label 收集起来加入参数；如果没有任何应用包含 models，则直接返回：

```python
    else:
        apps_with_models = []
        for app_config in apps.get_app_configs():
            try:
                if app_config.models_module:
                    models = apps.get_app_config(app_config.label).get_models()
                    if models:
                        apps_with_models.append(app_config.label)
            except Exception:
                continue
        if apps_with_models:
            cmd_args.extend(apps_with_models)
        else:
            return
```

### 追加标志并执行

根据 `empty` 与 `dry_run` 标志追加对应的 `--empty` / `--dry-run` 参数，最后调用 `call_command` 执行迁移生成，捕获异常并打印错误信息：

```python
    if empty:
        cmd_args.append('--empty')
    if dry_run:
        cmd_args.append('--dry-run')
    try:
        call_command(*cmd_args)
    except Exception as e:
        print(f"Error creating migrations: {e}")
```

## 实战示例

### 为所有应用自动生成迁移

```bash
bomiot makemigrations
```

不传 `appname`，命令会自动发现所有包含 models 的应用并生成迁移。

### 为指定 app label 生成迁移

```bash
bomiot makemigrations core
```

按 app label 匹配，等价于匹配 `app_config.label == 'core'` 或 `app_config.name` 以 `.core` 结尾的应用。

### 为指定完整点分路径生成迁移

```bash
bomiot makemigrations bomiot.server.core
```

按 `app_config.name` 精确匹配 `bomiot.server.core`，找到后用其 label 调用 `makemigrations`。

### 创建空迁移

```bash
bomiot makemigrations core --empty
```

为 `core` 应用创建一个空的迁移文件，通常用于手写数据迁移。

### 预览迁移变更（不写入文件）

```bash
bomiot makemigrations --dry-run
```

只打印将要生成的迁移内容，不实际写入迁移文件。

## 相关命令

- [bomiot migrate](./cli-init.zh-CN.md)：执行 `bomiot migrate` 应用迁移到数据库
- [bomiot run](./cli-run.zh-CN.md)：生成迁移并应用后启动 uvicorn 服务
