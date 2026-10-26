# Poetry 使用详解

## 为什么介绍 Poetry

- **Bomiot** 通过 Poetry 与 PyPI 的结合，实现了应用市场和插件模块的使用，方便用户环境搭建和团队合作。

## 什么是 Poetry

**Poetry** 是一个 Python 依赖管理与打包工具，用一份 `pyproject.toml` 统管项目的元信息、依赖与构建：

- 声明并锁定依赖（自动生成 `poetry.lock`，保证每台机器装出完全一致的版本）
- 自动创建和管理虚拟环境
- 一键构建并发布 Python 包

---

## 安装

推荐独立安装（与项目环境隔离，不污染全局 pip）：

```bash
# macOS / Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

验证安装：

```bash
poetry --version
```

不建议 `pip install poetry`：会把 Poetry 自身的依赖装进全局环境，容易和项目依赖打架。

---

## 项目初始化

```bash
# 新项目：生成标准目录结构和 pyproject.toml
poetry new myproject

# 已有项目：交互式补全 pyproject.toml
cd myproject
poetry init
```

生成的 `pyproject.toml` 核心字段：

```toml
[tool.poetry]
name = "myproject"
version = "0.1.0"
description = ""
authors = ["your name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 依赖管理

```bash
poetry add requests            # 添加运行依赖
poetry add "flask>=2.0,<3.0"   # 指定版本区间
poetry add pytest --group dev  # 添加开发依赖（仅开发环境安装）
poetry remove requests         # 移除依赖
poetry install                 # 按 lock 文件安装全部依赖
poetry install --without dev   # 只装运行依赖（部署时用）
poetry update                  # 在版本约束内升级全部依赖并刷新 lock
poetry update requests         # 只升级指定依赖
poetry show --tree             # 查看依赖树
```

版本约束写法：

| 写法 | 含义 |
|---|---|
| `^2.31` | 允许 2.x 内升级（>=2.31, <3.0） |
| `~2.31` | 只允许补丁升级（>=2.31, <2.32） |
| `2.31.*` | 通配符，等价于 ~2.31 |
| `==2.31.0` | 锁定精确版本 |
| `>=2.0,<3.0` | 区间表达式 |

## 虚拟环境

Poetry 自动为每个项目创建独立虚拟环境，常用操作：

```bash
poetry run python main.py   # 在项目环境内执行命令
poetry run pytest
poetry env info             # 查看当前环境路径与信息
poetry env list             # 列出项目的所有环境
poetry env use 3.11         # 切换环境使用的 Python 版本
poetry env remove 3.11      # 删除指定环境
```

两个实用配置：

```bash
# 在项目目录内创建 .venv（方便 IDE 识别，推荐）
poetry config virtualenvs.in-project true

# 查看/修改全局配置
poetry config --list
```

> Poetry 2.0 起，`poetry shell` 命令移到了独立插件 `poetry-plugin-shell`。日常更推荐直接用 `poetry run <命令>`，无需进入环境。

## 构建与发布

```bash
poetry build                              # 构建 sdist 与 wheel（输出到 dist/）
poetry config pypi-token.pypi <token>     # 配置 PyPI 令牌（一次性）
poetry publish                            # 发布到 PyPI
poetry publish --build                    # 构建并发布一步完成
```

## 常用命令速查

| 命令 | 作用 |
|---|---|
| `poetry new <名称>` | 创建新项目 |
| `poetry init` | 已有项目初始化 |
| `poetry add <包>` | 添加依赖 |
| `poetry add <包> --group dev` | 添加开发依赖 |
| `poetry remove <包>` | 移除依赖 |
| `poetry install` | 安装依赖（按 lock） |
| `poetry update` | 升级依赖并刷新 lock |
| `poetry lock` | 重新生成 lock 文件 |
| `poetry run <命令>` | 在项目环境内执行 |
| `poetry env use <版本>` | 切换环境 Python 版本 |
| `poetry build` / `publish` | 构建 / 发布包 |

## 注意事项

- `poetry.lock` 必须提交到版本库，它是团队与服务器环境一致性的保证。
- 拉取他人项目后第一条命令永远是 `poetry install`，它会严格按 lock 还原环境。
- 安装新依赖用 `poetry add`，不要手动编辑 `pyproject.toml` 后忘记 `poetry lock`。
