# bomiot makemigrations

根据模型（Model）的变更，自动生成数据库迁移文件。

```bash
bomiot makemigrations [appname ...]
```

## 概述

项目中数据表的结构由模型代码定义。当模型发生变化——新增模型、增加/删除/修改字段、调整字段选项——这些变化需要以**迁移文件**的形式记录下来，之后由 `bomiot migrate` 应用到数据库。

`bomiot makemigrations` 会对比当前模型代码与已有迁移文件之间的差异，在应用的 `migrations/` 目录下生成新的迁移文件（按序号自动命名，如 `0002_xxx.py`）。

命令必须在**项目根目录**下执行。

## 基本用法

| 命令 | 说明 |
|---|---|
| `bomiot makemigrations` | 检测所有应用的模型变更，生成迁移文件 |
| `bomiot makemigrations myapp` | 只检测 `myapp` 应用的变更 |

## 常用选项

| 选项 | 说明 |
|---|---|
| `--name NAME` | 为迁移文件指定名称后缀，便于识别，如 `--name add_user_email` |
| `--empty myapp` | 生成一个空迁移文件，用于手写数据迁移 |
| `--dry-run` | 只显示将生成什么迁移，不实际写文件 |
| `--check` | 检测到有未生成迁移的模型变更时以非零码退出，适合 CI 检查 |
| `--merge` | 合并同一应用下出现分支的迁移文件 |

## 典型场景

### 新增了一个字段

```bash
# 修改 models 代码后
bomiot makemigrations myapp
# myapp/migrations/0003_add_score_field.py 生成
```

### 给迁移起个可读的名字

```bash
bomiot makemigrations myapp --name add_score_field
# 生成 0003_add_score_field.py
```

### 提交前检查有没有漏掉的迁移

```bash
bomiot makemigrations --check --dry-run
# 有未记录的变更时返回非零退出码，适合接入 CI
```

### 需要迁移数据而不只是表结构

```bash
bomiot makemigrations myapp --empty --name backfill_score
# 生成空迁移文件，在其中手写数据迁移逻辑
```

## 标准工作流

```text
修改模型代码
  ↓
bomiot makemigrations [myapp]   ← 生成迁移文件
  ↓
检查生成的迁移文件是否符合预期
  ↓
bomiot migrate                  ← 应用到数据库（见 migrate 文档）
  ↓
将迁移文件与模型代码一起提交到版本管理
```

## 注意事项

- **迁移文件必须提交到版本管理**。它是团队共享的数据库变更记录，其他成员拉取代码后执行 `bomiot migrate` 即可同步表结构
- 生成后建议**先查看迁移文件内容**再执行 migrate，确认变更符合预期
- 删除字段的迁移一旦应用，该字段的数据将被删除且无法恢复
- 字段改名时系统可能识别为"删除旧字段 + 新增字段"，导致旧数据丢失；迁移生成时会提示确认，注意甄别
- 团队协作中多人同时改动同一应用的模型可能产生迁移分支，可用 `--merge` 合并
- 迁移文件生成后若尚未提交，请勿直接修改已生成的迁移文件——如需调整，先回滚或删除该迁移再重新生成
