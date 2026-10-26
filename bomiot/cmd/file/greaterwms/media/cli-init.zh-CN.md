# bomiot init

在当前目录初始化一个 Bomiot 项目，生成启动、构建、运行所需的全部基础文件。

```bash
bomiot init
```

## 概述

`bomiot init` 将 Bomiot 的项目骨架复制到当前目录：启动入口、全局配置、工作空间模板、平台图标等。执行完成后即可开始业务开发，配合 `bomiot run` 启动、`bomiot build` 构建。

> **幂等安全**：命令只补齐缺失的文件，已存在的文件不会被覆盖。重复执行不会破坏你已有的修改。

## 使用前提

- 已安装 bomiot：`pip install bomiot`
- 在一个**空目录或项目根目录**下执行（命令作用于当前工作目录）

## 生成的文件与目录

| 文件 / 目录 | 说明 |
|---|---|
| `launcher.py` | 启动入口。内含 `app_name`（应用名称）、`version`（版本号）、`base_url`（更新服务器地址）、`port` 等核心配置，构建与更新都读取它 |
| `setup.ini` | 全局配置（项目名称、debug 开关等）。已存在时不会覆盖，仅按需补全 `[project] name` |
| `pyproject.toml` | 项目配置（不存在时生成，自动写入项目名称与初始版本） |
| `builder.toml` | 构建扩展配置（追加打包内容，详见 build 文档） |
| `greaterwms/` | 工作空间目录（业务代码所在），内含接管模板与定时任务模板 `task.py` |
| `discovered_apps.py` | 应用扫描脚本（`bomiot run` 时自动生成应用清单） |
| `logo.ico` / `logo.icns` / `logo.png` | Windows / macOS / Linux 三平台应用图标，替换为自己的图标即可 |
| `splash.png` | 启动页图片（应用启动时的过渡画面） |
| `sqlite3.def` / `sqlite3.dll` | SQLite 支持文件 |
| `README.md` / `LICENSE` / `.gitignore` | 项目说明、开源协议、Git 忽略规则 |
| `logs/` / `dbs/` | 日志目录、数据库目录 |

## 执行流程

```text
bomiot init
  │
  ├─ 1. 在当前目录生成 pyproject.toml（如缺失）
  ├─ 2. 复制基础文件（launcher.py、setup.ini、图标、模板等，已存在则跳过）
  ├─ 3. 复制 greaterwms 工作空间目录（已存在则跳过）
  ├─ 4. 创建 logs/ 与 dbs/ 目录
  └─ 5. 输出欢迎信息，初始化完成
```

## 初始化后的标准流程

```text
bomiot init
  ↓
按需修改 launcher.py（app_name / version / port）与 setup.ini
  ↓
替换 logo 图标与 splash.png 为自己的素材
  ↓
bomiot run            ← 本地启动开发
  ↓
bomiot build          ← 本地构建（见 build 文档）
  ↓
bomiot deploy + push  ← 云端三平台构建（见 deploy 文档）
```

## 注意事项

- `launcher.py` 是项目的中枢配置，`app_name`、`version`、`base_url` 三个变量缺一不可，后续 build / publish / 客户端更新都依赖它
- 图标与启动页建议初始化后第一时间替换，避免带着默认素材进入构建
- `setup.ini` 已存在时只会补全项目名称，不会重置你的其他配置项
- 重复执行是安全的：所有"已存在"的文件与目录都会被跳过，不会覆盖你的业务代码
