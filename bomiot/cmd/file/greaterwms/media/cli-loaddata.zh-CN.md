# bomiot loaddata 命令

## 概述

`bomiot loaddata` 命令设计用于从配置文件中加载数据到 bomiot 项目。根据参数定义，`source` 是一个必填的位置参数，表示配置文件路径。

> **实现状态说明**：该命令的子命令解析器已在 `bomiot/cmd/cmd.py` 中注册，但 `cmd()` 函数中**没有**对应的 `elif command == 'loaddata'` 派发分支。这意味着当前版本中该命令处于"已声明但未实现"的状态——参数可以正常解析，但执行后不会进行任何实际操作。它属于规划中尚未完成的功能。

## 用法

```bash
bomiot loaddata <source>
```

- `<source>`：必填的配置文件路径（字符串类型）。

在 `cmd.py` 中的注册方式：

```python
# loaddata
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')
```

注意 `source` 没有设置 `nargs='?'` 也没有 `default` 值，因此它是一个必填参数，省略时 argparse 会直接报错退出。

## 源码分析

源文件：`bomiot/cmd/cmd.py`。

### 解析器注册

`loaddata` 子命令通过 `subparsers.add_parser('loaddata', ...)` 注册，help 文本为 `Load data from configs`，并声明了一个名为 `source` 的位置参数：

```python
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')
```

### 派发逻辑

在 `cmd()` 函数中，命令派发通过 `if/elif` 链完成。以下是 `cmd.py` 中 `cmd()` 函数的命令分支结构，可以清楚地看到 `loaddata` 缺少对应的分支：

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

可以看到 `if/elif` 链中依次处理了 `project`、`deploy`、`init`、`initadmin`、`initpwd`、`app`、`api`、`makemigrations`、`migrate`、`run`，但并没有 `loaddata` 分支。因此当执行 `bomiot loaddata <source>` 时，参数能被 argparse 成功解析，但 `command == 'loaddata'` 不匹配任何分支，函数直接结束，不执行任何数据加载操作。

### 预期行为（基于参数定义）

虽然当前未实现，但从参数 help 文本 `Configs path` 可以推断该命令的设计意图：

- 接收一个配置文件路径作为 `source`。
- 从该配置中读取数据并加载到项目数据库或运行时配置中。
- 与 `bomiot dumpdata` 命令互为逆操作（dump 导出，load 导入）。

## 实战示例

### 调用命令（当前版本不产生实际效果）

```bash
bomiot loaddata configs/backup.json
```

该命令能被 argparse 正确解析（`source` 会被赋值为 `configs/backup.json`），但由于 `cmd()` 函数中没有对应的派发分支，不会执行任何数据加载操作。

### 省略 source 参数时的行为

```bash
bomiot loaddata
```

由于 `source` 是必填位置参数且未设置默认值，argparse 会报错并退出：

```text
error: the following arguments are required: source
```

## 相关命令

- [bomiot dumpdata](./cli-dumpdata.zh-CN.md)：将数据导出到配置文件（同样处于已声明未实现状态）
- [bomiot migrate](./cli-init.zh-CN.md)：应用数据库迁移
- [bomiot makemigrations](./cli-makemigrations.zh-CN.md)：生成数据库迁移文件
