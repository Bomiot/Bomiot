<div align="center"><img src="https://gitee.com/Bomiot/Bomiot/raw/main/bomiot/server/media/img/logo.png" alt="Bomiot logo" width="180" height="auto" />

# 🚀 Bomiot

**AI 写代码，Bomiot 打包交付**

*二进制 · 跨平台 · 增量更新 · 源码保护*

[English](README.en.md) | [中文](README_zh-CN.md)

[![PyPI Downloads](https://img.shields.io/pypi/dm/bomiot?label=PyPI&color=green)](https://pepy.tech/projects/bomiot)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/vue-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![GitHub Stars](https://img.shields.io/github/stars/bomiot/bomiot?style=social)](https://github.com/bomiot/bomiot)
[![Home](https://img.shields.io/badge/Home-Online-brightgreen)](https://www.bomiot.com)
[![QQGroup](https://img.shields.io/badge/QQ群-1095956582-9cf?logo=tencent-qq&logoColor=000&logoWidth=15)](https://jq.qq.com/?_wv=1027&k=49HB5ymm)

</div>

---

## 🌟 关于 Bomiot

> **Bomiot 不是什么「革命性的黑科技框架」**——它把 Python 应用**无环境交付 + 持续更新 + 代码保护**这个真实需求，做成了一条完整的开箱即用链路：**让开发者把写好的应用——不带环境、不带源码、还能持续更新地——交到非技术用户手里。**

AI 把写代码压缩到了分钟级，交付却停在原地。Bomiot 补的就是这一截：`init` 初始化 → `run` 跑起来 → `build` 打成应用 → `publish` 发布更新，一条链走完。终端用户体验对标手机 App：双击即用、后台静默更新、失败自动回退。

| 痛点 | Bomiot 解决方案 |
| :--- | :--- |
| 🐢 交付难、环境耦合 | ✅ 编译为绿色版二进制，无需 Python 环境，双击即用 |
| 🔄 用户不更新 | ✅ 增量自动更新，差分下载，失败回退，零感知 |
| 🧩 前后端反复联调 | ✅ 统一交互契约，四个固定接口，前后端并行开发 |
| 🗂️ 一人维护多套系统 | ✅ 多项目隔离，请求头标识项目，数据互不越权 |
| 🛡️ 源码裸奔 | ✅ 编译为原生二进制，有效提高代码保护 |

坦诚边界：代码保护是提高门槛而非绝对安全；产物体积比原生应用大；只适合「需要把项目交到别人手上」的场景。

---

## ✨ 核心特性

| 特性 | 说明 |
| :--- | :--- |
| 📦 无环境交付 | `bomiot build` 一键编译为绿色版程序，拷贝即运行 |
| 🔄 增量自动更新 | 文件级哈希清单比对，只下载变化部分；大文件分块、断点续传；失败自动回退，用户零感知 |
| 🌍 跨平台 | Windows / macOS / Linux × x64 / arm64 全覆盖，构建时自动识别平台与架构 |
| 🦀 Rust ASGI 网关 | 原生支持 WebSocket，性能稳定，代码保护 |
| 🧩 多框架 | Django（默认）/ FastAPI / Flask，共享同一套 ORM 与数据层 |
| 📐 交互契约 | `bomiot api` 生成完整 CRUD 接口，业务逻辑写在 `receiver.py`，改动即时生效 |
| 🗂️ 多项目 | 一个工作空间多套项目，前端一键切换，后端按 `project` 请求头隔离数据 |
| 🔑 权限体系 | `urls.py` 的 `name` 声明权限，JWT 认证，部门隔离，软删除 |
| ⏰ 定时任务 | `task.py` 写函数 + `JobList` 注册，支持 cron / interval / date |
| 📁 文件监控 | 监听 `media` 目录，自动登记入库，`files.py` 可接管 |
| 📊 系统监控 | 周期采集 CPU / 内存 / 磁盘 / 网络 / 进程，`server.py` 可接管 |

---

## 🌍 跨平台支持

一份代码，处处运行。`bomiot build` 自动识别当前操作系统与 CPU 架构，无需任何参数；需要哪个平台的包，就在哪个平台上执行一次构建。

| 平台 | 架构 | 说明 |
| :--- | :--- | :--- |
| Windows | x64 | Windows 7 及以上，桌面交付最常见的目标 |
| macOS | x64 / arm64（Apple Silicon） | 自动识别 Intel 与 M 系列芯片 |
| Linux | x64 / arm64 | Ubuntu 22.04+ / glibc 2.35+，覆盖服务器与嵌入式 |

- 🖥️ **全场景设备**：办公 PC、云服务器、工控机、树莓派、边缘网关，打好一个包拷到哪台都能跑
- 🔒 **数据本地**：数据存储在各节点本机，适合内网、断网与有数据主权要求的环境
- 🔁 **更新按平台隔离**：`manifest--{app}-{os}-{arch}.json` 一平台一清单，Windows 客户端永远拉不到 macOS 的包

---

## 🚀 快速开始（5 分钟）

环境要求：Python 3.11+，Windows / macOS / Linux。

```bash
pip install bomiot        # 1. 安装
mkdir myapp && cd myapp
bomiot init               # 2. 初始化项目骨架（幂等，可重复执行）
bomiot migrate            # 3. 建表
bomiot initadmin          # 4. 创建管理员（命令会打印初始密码）
bomiot run                # 5. 启动
bomiot build              # 6. 打包：产物在 build/，双击即可运行
```

浏览器访问 `http://127.0.0.1:8000`，用管理员账号登录。

> 构建前建议先替换 `logo.ico / logo.icns / logo.png` 与 `splash.png` 为自己的素材。需要其他平台的包时，在对应平台的机器或 CI 上执行 `bomiot build` 即可。

---

## 🛠️ 命令行速查

| 命令 | 说明 |
| :--- | :--- |
| `bomiot init` | 初始化工作空间 |
| `bomiot project <name>` | 创建业务项目 |
| `bomiot app <name>` | 创建业务应用（基础骨架） |
| `bomiot api <name>` | 创建 API 应用（完整 CRUD 接口模板） |
| `bomiot makemigrations` / `migrate` | 生成 / 执行数据库迁移 |
| `bomiot loaddata` / `dumpdata` | 导入 / 导出数据 |
| `bomiot initadmin` / `initpwd` | 创建管理员 / 重置密码 |
| `bomiot run [-b host] [-p port] [-w workers]` | 启动服务（默认 `0.0.0.0:8000`，Windows 建议单 worker） |
| `bomiot build` | 本地构建当前平台应用包 |
| `bomiot publish --os=<os> --code=<口令>` | 发布增量更新（`--os` 取值 `windows`/`macos`/`linux`） |

---

## 🔧 配置（setup.ini）

工作空间根目录的 `setup.ini`，启动时加载，**改完需重启**：

| 配置段 | 关键项 | 说明 |
| :--- | :--- | :--- |
| `[database]` | `engine` | `sqlite`（默认，零配置）/ `mysql` / `postgresql` / `oracle` |
| `[debug]` | `debug` | 生产环境必须设为 `False` |
| `[file]` | `file_size` / `file_extension` | 上传大小上限（默认约 100MB）与允许的扩展名 |
| `[jwt]` | `user_jwt_time` | 登录令牌有效期（秒） |
| `[throttle]` / `[request]` | - | API 限流（按 IP + 请求方法） |
| `[mail]` | - | SMTP 邮件配置 |
| `[system_control]` | `observer` / `scheduler` / `server_monitor` | 文件监控 / 定时任务 / 系统监控三个后台服务开关，默认全开 |

---

## 📦 构建、发布与自动更新

`bomiot init` 生成的 `launcher.py` 是项目中枢，`app_name` / `version` / `base_url`（更新服务器地址）三个变量缺一不可，构建、发布、客户端更新都读它。需要追加打包内容时，在项目根目录建 `builder.toml` 配置。

```bash
bomiot build                                 # 本地构建 → build/ 目录
bomiot publish --os=windows --code=example   # 发布到更新服务器
```

### 版本控制：每个文件都有指纹

- 每次构建生成清单文件 `manifest--{app_name}-{os}-{arch}.json`，记录**每个产物文件的哈希值**——清单就是这一版的「指纹全集」
- 版本与平台严格对应：`{app_name}-{version}-{os}` 一个目录，`windows` / `macos` / `linux` 与 `x64` / `arm64` 各自的清单互不影响，Windows 客户端只会拉 Windows 的包
- 同一版本同一平台重复发布，服务器比对后直接跳过，不会重复上传
- `--code` 发布口令由服务器校验，防止他人拿到项目标识后冒充你上传被篡改的更新

### 自动更新：客户端启动时发生了什么

1. **比对版本**：客户端启动时读取本地清单，向 `base_url` 请求远端版本摘要——一致则直接启动，零开销
2. **拉取清单**：不一致则获取远端完整清单（每个文件的哈希）
3. **增量下载**：逐个文件对比哈希，**只下载新增和有变化的文件**，没动的文件一个字节都不传
4. **断点续传**：大文件按块下载，中途断网后从断点继续，不用从头再来
5. **静默替换**：下载完成后生成更新脚本，应用退出，由脚本完成文件替换并自动重启——用户全程无感知
6. **失败回退**：下载中断或校验失败，放弃本次更新，按本地版本正常启动，下次启动自动重试

用户的业务数据目录（数据库、日志、缓存等）不在更新范围内，版本再怎么换，数据都不受影响。

---

## 🌐 部署与分发

Bomiot 提供两种部署方式，**全部免费使用**：

| 对比项 | `bomiot run`（服务器部署） | `bomiot build` + `publish`（节点化分发） |
| :--- | :--- | :--- |
| 运行环境 | 需安装 Python 及依赖 | 绿色版，双击即用 |
| 增量更新 | 自行处理 | 内置静默更新 |
| 代码保护 | 源码明文 | 编译为二进制 |
| 设备绑定 | 无 | 单设备唯一绑定 |

### 传统服务器部署

```bash
bomiot run --host 0.0.0.0 --port 8000
```

外网部署请配置 HTTPS（`--ssl-keyfile` + `--ssl-certfile`），多 worker 请在 Linux / macOS 环境下运行。

### 节点化分发

`bomiot build` 生成的绿色版运行文件可直接部署到本地物理设备（PC、工控机、树莓派等）或云服务器实例。首次运行时程序自动生成本机标识文件 `auth_key.py`，携带它访问官网换取 `sponsor.py` 即完成设备绑定——所有校验均在**本地完成**，仅对当前设备有效，换机需重新绑定。

> **隐私承诺**：验证不联网、不上传任何节点信息或业务数据，代码与数据始终留在本地。

---

## ⚠️ 安全说明

生产部署： `[debug]` 设为 `False`；外网必须 HTTPS（`--ssl-keyfile` + `--ssl-certfile`）；定期备份数据库（`bomiot dumpdata`）与 `setup.ini`。建议修改自动更新 URL 与更新文件存放地址，防止他人向更新服务器上传文件。

---

## 🤝 参与建设

官方网站：https://www.bomiot.com

## 📄 开源协议

**Apache License 2.0**，详见 LICENSE 文件。

---

**⭐ 如果 Bomiot 对您有帮助，请点个 Star！**

**开箱即用，持续更新。** 这是我们能给你的承诺。

Made with ❤️ by Bomiot Team
