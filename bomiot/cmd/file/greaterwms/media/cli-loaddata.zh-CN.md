# bomiot loaddata

将数据文件（fixtures）中的内容导入数据库，用于恢复备份、导入初始化数据或在环境之间搬运数据。

```bash
bomiot loaddata <fixture> [fixture ...]
```

## 概述

`bomiot loaddata` 读取 JSON 格式的数据文件，将其中的记录写入数据库对应的数据表。数据文件通常由 `bomiot dumpdata` 导出，也可以手工编写——一个数据文件即是一份可重复导入的"种子数据"。

命令必须在**项目根目录**下执行。

## 基本用法

| 命令 | 说明 |
|---|---|
| `bomiot loaddata myapp.json` | 导入指定数据文件 |
| `bomiot loaddata app1.json app2.json` | 一次导入多个数据文件 |
| `bomiot loaddata seeds` | 省略扩展名，按 fixtures 查找规则搜索同名数据文件 |

## 数据文件的查找位置

传入不带路径的文件名时，按以下顺序查找：

| 位置 | 说明 |
|---|---|
| 各应用的 `fixtures/` 目录 | 随应用分发的初始化数据，按文件名查找 |
| 当前目录及指定路径 | 传入相对/绝对路径时直接读取 |

> 项目初始化数据建议放在对应应用的 `fixtures/` 目录下，文件名与应用相关（如 `myapp.json`），团队成员拉取代码后执行 `bomiot loaddata myapp` 即可完成初始化。

## 常用选项

| 选项 | 说明 |
|---|---|
| `--app myapp` | 只导入文件中属于 `myapp` 应用的数据 |
| `--ignorenonexistent` | 忽略文件中已不存在的模型或字段，跳过而不是报错 |
| `--format json` | 指定数据文件格式，默认为 `json`（一般从扩展名自动识别） |
| `--exclude APP` | 导入时排除指定应用的数据（可多次使用） |

## 典型场景

### 恢复某个应用的备份

```bash
bomiot loaddata myapp_backup.json
```

### 新项目初始化种子数据

```bash
bomiot loaddata seeds.json
```

### 多环境数据迁移

```bash
# 源环境
bomiot dumpdata myapp --indent 2 --output myapp.json

# 目标环境（先确保表结构一致）
bomiot migrate
bomiot loaddata myapp.json
```

### 文件里有已删除的旧字段

```bash
bomiot loaddata old_backup.json --ignorenonexistent
```

## 导入行为说明

- 记录以**主键**为准：主键已存在则更新该记录，不存在则插入新记录
- 使用 `--natural-primary` 导出的文件不含主键，导入时全部由数据库生成新主键（相当于纯插入）
- 导入在同一个事务中完成，出错时回滚，不会留下半截数据

## 注意事项

- 导入前请确认目标库已执行 `bomiot migrate`，表结构与数据文件匹配，否则可能导入失败
- 数据文件中用户密码等字段为哈希值，导入后可直接登录使用；切勿手工修改为明文
- 重复导入同一文件是安全的（按主键覆盖更新），但不含主键的文件重复导入会产生重复数据
- 大文件导入耗时较长，导入期间避免同时写入相同数据表
