# bomiot dumpdata

将数据库中的应用数据导出为标准 JSON 数据文件，用于数据备份、迁移或作为初始化数据随项目分发。

```bash
bomiot dumpdata [appname ...]
```

## 概述

`bomiot dumpdata` 读取数据库内容，将指定应用（或全部应用）的表数据序列化为 JSON 格式输出。输出的数据文件可以在其他环境中通过 `bomiot loaddata` 原样导入，实现数据在环境之间的搬运。

命令必须在**项目根目录**下执行。

## 基本用法

| 命令 | 说明 |
|---|---|
| `bomiot dumpdata` | 导出所有应用的数据（输出到标准输出） |
| `bomiot dumpdata myapp` | 只导出 `myapp` 应用的数据 |
| `bomiot dumpdata myapp.mymodel` | 只导出 `myapp` 应用中某一张表的数据 |
| `bomiot dumpdata app1 app2` | 一次导出多个应用的数据 |
| `bomiot dumpdata myapp > backup.json` | 将导出结果写入文件（推荐做法） |

> 导出大量数据时务必使用重定向写入文件，直接在终端打印既慢又难以保存。

## 常用选项

| 选项 | 说明 |
|---|---|
| `--output FILE` | 输出到指定文件（等价于 `>` 重定向），支持 `.gz` / `.bz2` 等压缩格式 |
| `--indent N` | JSON 缩进空格数，让数据文件可读、可纳入版本管理，如 `--indent 2` |
| `--exclude APP` | 排除指定应用（可多次使用） |
| `--exclude APP.MODEL` | 排除指定应用中的某张表 |
| `--natural-foreign` | 外键字段使用自然键序列化，避免跨环境主键不一致问题 |
| `--natural-primary` | 不序列化主键，导入时由目标库重新生成 |
| `--pks 1,2,3` | 只导出指定主键的记录（需配合单个模型使用） |
| `--format json` | 指定序列化格式，默认为 `json` |

## 典型场景

### 备份某个应用的数据

```bash
bomiot dumpdata myapp --indent 2 --output myapp_backup.json
```

### 导出单张表并便于阅读

```bash
bomiot dumpdata myapp.mymodel --indent 2 > mymodel.json
```

### 全量备份但排除临时数据

```bash
bomiot dumpdata --exclude sessions --exclude admin.logentry --output full_backup.json
```

### 导出少量种子数据（用于初始化）

```bash
bomiot dumpdata myapp.mymodel --pks 1,2,3 --indent 2 --output seeds.json
```

## 与 bomiot loaddata 配合

导出的数据文件可直接导入到另一个环境：

```bash
# 在源环境导出
bomiot dumpdata myapp --indent 2 --output myapp.json

# 在目标环境导入
bomiot loaddata myapp.json
```

用于项目初始化数据时，一般将数据文件放在应用的 `fixtures` 目录下，`loaddata` 会自动按文件名查找。

## 注意事项

- 全量导出包含所有表，文件可能很大；生产环境建议指定应用或使用 `--exclude` 缩小范围
- 数据文件包含明文内容，涉及敏感数据时注意保管，不要提交到公开仓库
- 跨环境导入时，如果两端的表结构（迁移版本）不一致，导入可能失败，请先在目标环境执行 `bomiot migrate`
- 数据库中用户密码等字段以哈希形式导出，导入后保持可用
