# 快速入门

本页用 5 分钟跑通 Bomiot 的最小闭环：**安装 → 初始化 → 启动 → 打包**。

## 环境准备

- Python 3.11 及以上，自带 pip
- 三个平台任选其一：Windows / macOS / Linux

## 第一步：安装

```bash
pip install bomiot
```

验证安装：

```bash
bomiot --version
```

## 第二步：初始化项目

```bash
mkdir myapp
cd myapp
bomiot init
```

`init` 在当前目录生成完整项目骨架：`launcher.py`（启动与更新配置）、`setup.ini`（全局配置）、工作空间目录、三平台图标等。已存在的文件不会被覆盖，可重复执行。

> 初始化后建议先替换 `logo.ico / logo.icns / logo.png` 与 `splash.png` 为自己的素材，避免带着默认图标进入构建。

## 第三步：初始化数据库

```bash
bomiot migrate      # 建表
bomiot initadmin    # 创建管理员账号，命令会打印初始密码
```

默认使用 SQLite，零配置。切换 MySQL / PostgreSQL / Oracle 见「数据库」标签下的对应文档。

## 第四步：启动

```bash
bomiot run
```

浏览器访问 `http://127.0.0.1:8000`，用上一步的管理员账号登录。

- 默认绑定 `0.0.0.0:8000`，可用 `--port 9000` 等参数调整
- **Windows 下建议使用单 worker 运行**（多 worker 支持不好），详见 CLI 命令 → run

## 第五步：打包交付

```bash
bomiot build        # 本地构建当前平台的应用包
```

构建产物在 `dist/` 目录，双击即可运行，用户机器无需安装 Python。

需要同时产出 Windows / macOS / Linux 三平台包时，用云端构建：

```bash
bomiot deploy       # 生成部署工作流
git push            # 推送后自动触发三平台构建
```

## 常用命令一览

| 命令 | 作用 |
|---|---|
| `bomiot init` | 初始化项目骨架 |
| `bomiot run` | 启动服务 |
| `bomiot migrate` / `makemigrations` | 执行 / 生成数据库迁移 |
| `bomiot initadmin` / `initpwd` | 创建管理员 / 重置密码 |
| `bomiot project` / `app` / `api` | 新建工程 / 子应用 / API |
| `bomiot loaddata` / `dumpdata` | 导入 / 导出数据 |
| `bomiot build` | 本地构建应用包 |
| `bomiot deploy` / `publish` | 云端三平台构建 / 发布增量更新 |

每个命令的完整说明见「CLI 命令」标签下的文档。

## 下一步

- 「基础 → setup.ini」：全局配置项说明
- 「数据库」：切换生产数据库
- 「CLI 命令 → build / deploy / publish」：完整的交付与更新链路
