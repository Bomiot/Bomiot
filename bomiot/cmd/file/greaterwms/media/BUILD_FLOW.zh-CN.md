# Bomiot 从开发到交付完整流程

## 概述

通过 GitHub Actions + Nuitka，Bomiot 项目 push 到 GitHub 后自动构建 Windows / macOS / Linux 三个平台的绿色版（无需安装 Python 环境即可运行），实现从开发到交付的全自动化。

---

## 完整流程

```
1. 注册 GitHub 账号
  ↓
2. 新建一个仓库
  ↓
3. pip install bomiot
  ↓
4. 创建虚拟环境，pip freeze > requirements.txt
  ↓
5. bomiot init 初始化项目
  ↓
6. 修改业务代码
  ↓
7. bomiot deploy 生成 greaterwms.yaml（GitHub Actions 工作流）
  ↓
8. 上传 GitHub
  ↓
9. GitHub Actions 自动构建三平台绿色版
  ↓
10. 下载 Artifact → 跨平台无环境可交付产品
```

---

## 1. 注册 GitHub 账号

- 访问 [github.com](https://github.com) 注册账号
- 已有账号跳过此步

---

## 2. 新建一个仓库

- 点击 **New repository**
- 填写仓库名称
- 选择 Public 或 Private
- 点击 **Create repository**

---

## 3. 安装 Bomiot

```bash
pip install bomiot
```

---

## 4. 生成 requirements.txt

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 安装 bomiot 及其他依赖
pip install bomiot

# 生成依赖清单
pip freeze > requirements.txt
```

> GitHub Actions 会读取此文件在 CI 环境中安装相同依赖。

---

## 5. bomiot init 初始化项目

```bash
bomiot init
```

在当前目录生成以下文件。

`launcher.py` 中可设置软件名称和版本号：

```python
app_name = "GreaterWMS"
version = "3.0.0"
port = 8008
```

- `app_name` — 软件名称
- `version` — 版本号
- `port` — 默认端口

| 文件 / 目录 | 说明 |
| --- | --- |
| `launcher.py` | 启动入口 |
| `setup.ini` | 全局配置 |
| `splash.png` | 启动页图片（应用启动时显示的过渡画面，替换为自己的图片即可） |
| `apps.json` | 已发现应用列表（运行时生成） |
| `discovered_apps.py` | 应用扫描脚本 |
| `logo.ico` | Windows 应用图标（.ico 格式） |
| `logo.icns` | macOS 应用图标（.icns 格式） |
| `logo.png` | Linux 应用图标（.png 格式） |

> 三个图标文件分别对应三个平台的可执行文件图标，在 Nuitka 构建时通过 `windows-icon-from-ico`、`macos-app-icon`、`linux-icon` 配置项自动注入。替换为自己的图标文件即可。
| `.gitignore` | Git 忽略规则 |
| `LICENSE` | 开源协议 |
| `README.md` | 项目说明 |
| `pyproject.toml` | 项目配置 |
| `sqlite3.def` / `sqlite3.dll` | SQLite 数据库 |
| `greaterwms/` | 工作空间目录 |
| `greaterwms/server.py` | 系统监控接管（模板） |
| `greaterwms/receiver.py` | 业务数据接管（模板） |
| `greaterwms/files.py` | 文件监控接管（模板） |
| `greaterwms/task.py` | 定时任务函数（模板） |
| `bomiot_test/` | 测试模块 |
| `logs/` | 日志目录 |
| `dbs/` | 数据库目录 |

---

## 6. 自己修改完

根据需求修改项目文件，改完即可上传。

---

## 7. 上传 GitHub

将 `greaterwms.yaml` 放到 `.github/workflows/` 目录下：

```
.github/
  └── workflows/
      └── greaterwms.yaml
```

然后提交并推送：

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

push 到 `main` 分支后自动触发构建。

---

## 8. GitHub Actions 自动构建

`greaterwms.yaml` 关键配置：

| 配置项 | 值 | 说明 |
| --- | --- | --- |
| `APP_NAME` | `GreaterWMS` | 应用名称 |
| `BASE_VERSION` | `3.0.0` | 版本号 |
| `matrix.os` | `windows-latest, macos-latest, ubuntu-22.04` | 三平台并行构建 |
| `python-version` | `3.11` | Python 版本 |
| `mode` | `standalone` | 绿色版独立目录 |
| `script-name` | `launcher.py` | 入口脚本 |
| `nuitka-version` | `4.1.3` | Nuitka 版本 |
| `lto` | `yes` | 链接时优化 |
| `windows-console-mode` | `disable` | 隐藏控制台 |
| `enable-plugins` | `tk-inter` | Tkinter 插件 |

### 构建流程

```
Checkout 仓库 → Setup Python 3.11 → pip install -r requirements.txt
  ↓
discovered_apps.py 扫描 greaterwms/ 下的 apps.py → 生成 apps.json
  ↓
Nuitka standalone 构建（三平台并行）
  ↓
上传 Artifact
```

### 三平台产物

| 平台 | 图标 | 产物 |
| --- | --- | --- |
| Windows | `logo.ico` | `build/*.dist/` + `build/*.exe` |
| macOS | `logo.icns` | `build/*.app/` |
| Linux | `logo.png` | `build/*.dist/` + `build/*.bin` |

### 数据文件（不编译，直接复制）

| 文件 | 说明 |
| --- | --- |
| `setup.ini` | 全局配置 |
| `splash.png` | 启动页 |
| `apps.json` | 应用列表 |
| `greaterwms/server.py` | 系统监控接管 |
| `greaterwms/receiver.py` | 业务数据接管 |
| `greaterwms/files.py` | 文件监控接管 |
| `greaterwms/task.py` | 定时任务 |

---

## 9. 下载产物

1. 进入 GitHub 仓库 → **Actions** 标签
2. 选择最新构建记录
3. 在 **Artifacts** 区域下载

产物名称：

```
GreaterWMS-3.0.0-Windows
GreaterWMS-3.0.0-macOS
GreaterWMS-3.0.0-Linux
```

解压后直接运行，无需安装 Python 或任何依赖。
