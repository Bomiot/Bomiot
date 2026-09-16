# bomiot dumpdata 命令

## 概述

`bomiot dumpdata` 命令设计用于将 bomiot 项目的数据导出到配置文件。根据参数定义，`appname` 是一个可选的位置参数，默认值为 `core`，用于指定要导出数据的应用名。

> **实现状态说明**：该命令的子命令解析器已在 `bomiot/cmd/cmd.py` 中注册，但 `cmd()` 函数中**没有**对应的 `elif command == 'dumpdata'` 派发分支。这意味着当前版本中该命令处于"已声明但未实现"的状态——参数可以正常解析（包括使用默认值 `core`），但执行后不会进行任何实际操作。它属于规划中尚未完成的功能。

## 用法

```bash
bomiot dumpdata [appname]
```

- `[appname]`：可选的应用名，字符串类型，默认值为 `core`。省略时自动使用 `core`。

在 `cmd.py` 中的注册方式：

```python
# dumpdata
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')
```

注意 `appname` 设置了 `nargs='?'` 和 `default='core'`，因此它是可选的——省略时自动取默认值 `core`，不会报错。

## 源码分析

源文件：`bomiot/cmd/cmd.py`。

### 解析器注册

`dumpdata` 子命令通过 `subparsers.add_parser('dumpdata', ...)` 注册，help 文本为 `Dump data to configs`，并声明了一个名为 `appname` 的可选位置参数：

```python
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')
```

关键参数属性：

- `default='core'`：未传入 appname 时默认导出 `core` 应用的数据。
- `nargs='?'`：允许省略该位置参数，使参数变为可选。
- `type=str`：值的类型为字符串。

### 派发逻辑

在 `cmd()` 函数中，命令派发通过 `if/elif` 链完成。以下是 `cmd.py` 中 `cmd()` 函数的命令分支结构，可以清楚地看到 `dumpdata` 缺少对应的分支：

```python
def cmd():
    """
    run from cmd
    :return:
    """
    args = parser.parse_args()
    command = args.command
    if command == 'project':
        ...
    elif command == 'deploy':
        ...
    elif command == 'init':
        ...
    elif command == 'initadmin':
        ...
    elif command == 'initpwd':
        ...
    elif command == 'app':
        ...
    elif command == 'api':
        ...
    # marketplace
    # elif command == 'market':
    #     ...
    # # init auth keys
    # elif command == 'keys':
    #     ...
    # makemigrations
    elif command == 'makemigrations':
        ...
    # migrate
    elif command == 'migrate':
        from bomiot.cmd.migrate import migrate
        migrate()
    # run server
    elif command == 'run':
        ...
```

可以看到 `if/elif` 链中依次处理了 `project`、`deploy`、`init`、`initadmin`、`initpwd`、`app`、`api`、`makemigrations`、`migrate`、`run`，但并没有 `dumpdata` 分支。因此当执行 `bomiot dumpdata` 或 `bomiot dumpdata someapp` 时，参数能被 argparse 成功解析，但 `command == 'dumpdata'` 不匹配任何分支，函数直接结束，不执行任何数据导出操作。

### 预期行为（基于参数定义）

虽然当前未实现，但从参数 help 文本 `Appname` 和默认值 `core` 可以推断该命令的设计意图：

- 接收一个应用名 `appname`，默认为 `core`。
- 将该应用的数据导出到配置文件（dump）。
- 与 `bomiot loaddata` 命令互为逆操作（dump 导出，load 导入）。

## 实战示例

### 调用命令（当前版本不产生实际效果）

```bash
bomiot dumpdata
```

不传 `appname`，argparse 使用默认值 `core`。但由于 `cmd()` 函数中没有对应的派发分支，不会执行任何数据导出操作。

### 指定应用名调用

```bash
bomiot dumpdata goods
```

`appname` 被赋值为 `goods`，同样不会执行实际操作。

## 相关命令

- [bomiot loaddata](./cli-loaddata.zh-CN.md)：从配置文件加载数据（同样处于已声明未实现状态）
- [bomiot migrate](./cli-init.zh-CN.md)：应用数据库迁移
- [bomiot makemigrations](./cli-makemigrations.zh-CN.md)：生成数据库迁移文件
