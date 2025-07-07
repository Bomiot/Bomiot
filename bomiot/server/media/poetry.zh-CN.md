# Poetry 使用详解

## 为什么介绍 Poetry

- **Bomiot** 通过使用Poetry与PyPi的结合，实现了应用市场和插件模块的使用，方便用户环境搭建和团队合作

---

## 什么是 Poetry

**Poetry** 是一个现代化的 Python 项目依赖管理和打包工具。它可以帮助你：
- 管理和锁定依赖（自动生成 `pyproject.toml` 和 `poetry.lock`）
- 创建和管理虚拟环境
- 构建和发布 Python 包

Poetry 的目标是让 Python 项目的依赖、打包、分发更加简单、可靠和一致。

---

## Poetry 特点

- 支持 PEP 517/518（基于 `pyproject.toml`）
- 自动管理虚拟环境
- 精确锁定依赖版本
- 支持多种 Python 版本隔离
- 便捷的包发布流程（如 PyPI）

---

## Poetry 安装

推荐使用官方安装脚本：

```bash
# 推荐方式
curl -sSL https://install.python-poetry.org | python3 -

# 或者使用 pip（不推荐）
pip install poetry
```

安装后，确认版本：

```bash
poetry --version
```

---

## Poetry 基本用法

### 新建项目

```bash
poetry new myproject
```
- 会创建一个名为 `myproject` 的目录，包含标准的项目结构和初始的 `pyproject.toml` 文件。

### 在已有项目中初始化 Poetry

```bash
cd your_existing_project
poetry init
```
- 交互式填写项目依赖和元数据，生成 `pyproject.toml`。

### 添加依赖

```bash
poetry add requests
poetry add flask@2.1.0  # 指定版本
poetry add pytest --dev  # 添加开发依赖
```
- 自动写入 `pyproject.toml` 并安装依赖。

### 移除依赖

```bash
poetry remove requests
```
- 会从项目中移除并卸载对应包。

### 安装依赖

```bash
poetry install
```
- 根据 `pyproject.toml` 和 `poetry.lock` 安装所有依赖。

### 更新依赖

```bash
poetry update
poetry update requests
```
- 更新所有或指定依赖到最新可用版本。

### 虚拟环境管理

- Poetry 默认为每个项目自动创建虚拟环境，无需手动操作。
- 进入虚拟环境：

  ```bash
  poetry shell
  ```

- 直接在虚拟环境中执行命令：

  ```bash
  poetry run python script.py
  poetry run pytest
  ```

### 运行项目

假如 `pyproject.toml` 里配置了 `scripts`，可直接：

```bash
poetry run my-script
```

### 打包与发布

- 构建项目包：

  ```bash
  poetry build
  ```

- 发布到 PyPI：

  ```bash
  poetry publish
  # 首次需 poetry config pypi-token.pypi your_token
  ```

---

## 常用命令速查

| 命令                          | 作用说明                     |
|-------------------------------|------------------------------|
| poetry new <项目名>           | 创建新项目                   |
| poetry init                   | 已有项目初始化 Poetry        |
| poetry add <包名>             | 添加依赖                     |
| poetry add <包名> --dev       | 添加开发依赖                 |
| poetry remove <包名>          | 移除依赖                     |
| poetry install                | 安装依赖                     |
| poetry update                 | 更新依赖                     |
| poetry shell                  | 激活虚拟环境                 |
| poetry run <命令>             | 虚拟环境下运行命令           |
| poetry build                  | 构建项目包                   |
| poetry publish                | 发布到 PyPI                  |

---

## 常见问题

**Q1：如何指定 Python 版本？**  
A：在 `pyproject.toml` 的 `[tool.poetry.dependencies]` 里添加 `python = "^3.9"`，或 `poetry env use 3.9` 指定虚拟环境 Python 版本。

**Q2：如何切换/定位虚拟环境路径？**  
A：`poetry env list` 查看所有环境，`poetry env info` 查看当前虚拟环境详情。

**Q3：如何解决依赖冲突？**  
A：尝试 `poetry update`，如仍冲突，需手动调整依赖版本。

---

## 参考链接

- [Poetry 官方文档](https://python-poetry.org/docs/)
- [Poetry GitHub](https://github.com/python-poetry/poetry)
- [pyproject.toml 配置说明](https://python-poetry.org/docs/pyproject/)

---

如需更多高级用法（如多环境管理、插件扩展等），建议查阅官方文档或社区资源。