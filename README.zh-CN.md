<div align="center">
  <img src="bomiot/templates/dist/spa/icons/logo.png" alt="Bomiot logo" width="200" height="auto" />
  <h1>🚀 Bomiot</h1>
  <p><strong>One App you can do everything</strong></p>
  <p><em>强大的分布式文档管理框架 & 全栈开发平台</em></p>

<!-- Badges -->
![License: APLv2](https://img.shields.io/github/license/Bomiot/Bomiot)
![Release Version (latest Version)](https://img.shields.io/github/v/release/Bomiot/Bomiot?color=orange&include_prereleases)
![i18n Support](https://img.shields.io/badge/i18n-Support-orange.svg)

![repo size](https://img.shields.io/github/repo-size/Bomiot/Bomiot)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Bomiot/Bomiot)
![Contributors](https://img.shields.io/github/contributors/Bomiot/Bomiot?color=blue)

![GitHub Org's stars](https://img.shields.io/github/stars/Bomiot?style=social)
![GitHub Follows](https://img.shields.io/github/followers/Singosgu?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Bomiot/Bomiot?style=social)
![GitHub Watch](https://img.shields.io/github/watchers/Bomiot/Bomiot?style=social)

![Python](https://img.shields.io/badge/Python-3.9+-yellowgreen)
![Django](https://img.shields.io/badge/Django-4.2+-yellowgreen)
![Quasar Cli](https://img.shields.io/badge/Quasar/cli-2.4.1+-yellowgreen)
![Vue](https://img.shields.io/badge/Vue-3.4.18+-yellowgreen)
![NodeJS](https://img.shields.io/badge/NodeJS-18.19.1+-yellowgreen)

[![BiliBili](https://img.shields.io/badge/BiliBili-4987-red)](https://space.bilibili.com/407321291/channel/seriesdetail?sid=776320)

[English](README.en.md) | [中文](README.zh-CN.md)

</div>

---

## 📋 目录

- [🌟 项目简介](#-项目简介)
- [✨ 核心特性](#-核心特性)
- [🚀 快速开始](#-快速开始)
- [📦 安装指南](#-安装指南)
- [🛠️ 命令行工具](#️-命令行工具)
- [🏗️ 项目结构](#️-项目结构)
- [🔧 配置说明](#-配置说明)
- [🌐 部署指南](#-部署指南)
- [📚 定时任务](#-定时任务)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)
- [🔗 相关链接](#-相关链接)

---

## 🌟 项目简介

Bomiot 是一个革命性的分布式文档管理框架和全栈开发平台，核心部分是用Rust编写，专为解决现代开发中的痛点而设计。我们相信，优秀的开源项目不仅要有强大的技术栈，更要注重开发者的使用体验和团队协作效率，简单易学。

### 🎯 设计理念

- **学习曲线**：后端支持Django，FastAPI，Flask，前端支持React，Angular，Vue，Django自带Templates（官方提供的是一套Vue）
- **开发者友好**: 从 0 到 1 的无缝体验，无需复杂配置
- **团队协作**: 高效的开发团队交互机制
- **模块化设计**: 插件化架构，功能可扩展
- **部署容易**：pip安装，方便团队各自部署，支持3.9以上版本的python
- **信号机制**：由信号机制管理数据，更便捷的自定义api支持
- **企业级**: 生产环境就绪，支持大规模部署

---

## ✨ 核心特性

### 🔧 开发工具
- ✅ **项目脚手架**: 一键创建项目和应用
- ✅ **插件系统**: 丰富的插件生态
- ✅ **实时文件监控**: 开发效率提升

### 🕐 任务管理
- ✅ **定时任务**: 强大的调度系统
- ✅ **任务监控**: 实时任务状态跟踪
- ✅ **错误处理**: 智能异常处理机制
- ✅ **日志管理**: 完整的日志记录系统

### 🔐 权限控制
- ✅ **细粒度权限**: 基于角色的访问控制
- ✅ **JWT 认证**: 安全的身份验证
- ✅ **API 权限**: 接口级别的权限管理
- ✅ **操作审计**: 完整的操作日志

### 🌍 国际化
- ✅ **多语言支持**: 内置国际化框架
- ✅ **动态语言切换**: 运行时语言切换
- ✅ **本地化配置**: 区域化设置

### 📊 系统监控
- ✅ **性能监控**: CPU、内存、磁盘监控
- ✅ **进程管理**: 系统进程实时监控
- ✅ **网络监控**: 网络流量统计
- ✅ **健康检查**: 系统健康状态检测

### 📚 应用市场
- ✅ **应用分享**：应用市场pip安装，方便快捷
- ✅ **组件市场**：组件热插拔，动态导入

---

## 🚀 快速开始

### 1. 安装 Bomiot

```bash
# 使用 pip 安装
pip install bomiot

# 或使用 poetry 安装
poetry add bomiot
```

### 2. 初始化工作空间

```bash
# 初始化 Bomiot 工作空间
bomiot init
```

### 3. 创建项目

```bash
# 创建新项目
bomiot project my-project

# 创建应用
bomiot new my-app
```

### 4. 数据库

```bash
# 初始化数据库
bomiot migrate

# 如果创建了新应用，可以生成新的数据库迁移文件
bomiot makemigrations
```

### 5. 新建管理员

```bash
# 初始化管理员
bomiot initadmin

# 重置管理员账号密码
bomiot initpwd
```

### 6. 启动服务

```bash
# 启动开发服务器
bomiot run

# 或指定端口
bomiot run --host 0.0.0.0 --port 8080
```

---

## 📦 安装指南

### 系统要求

- **Python**: 3.9 或更高版本
- **Node.js**: 18.19.1 或更高版本
- **操作系统**: Windows, macOS, Linux

### 修改前端

#### 1. 安装前端依赖

```bash
# 进入前端目录
cd my-project/templates

# 安装依赖
yarn install
```

#### 3. 打开开发baseUrl

```bash
# 创建数据库迁移
vim my-project/templates/src/boot/axios.js

```

```bash
# axios.js代码片段修改
 ...
const baseURL = 'http://127.0.0.1:8000' // Replace with your actual API URL

const api = axios.create({
  baseURL: baseURL ##打开这里
})
 ...
```


#### 3. 前端开发调试

```bash
# 确保后端已经启动
bomiot run
```

```bash
# 前端重新启动
ce my-project/templates

&

quasar d
```

---

## 🛠️ 命令行工具

Bomiot 提供了强大的命令行工具，让开发和管理变得简单高效。

### 📋 命令概览

```bash
bomiot [命令] [选项]
```

### 🔧 核心命令

#### 项目管理

```bash
# Help指令
bomiot -h

# 查看版本号
bomiot -v

# 初始化工作空间
bomiot init

# 创建新项目
bomiot project <project_name>

# 创建新应用
bomiot new <app_name>

# 创建插件
bomiot plugins <plugin_name>
```

#### 应用市场

```bash
# 应用市场
bomiot market <project_name>

# 插件安装，插件是自动热导入的
pip install -y <plugin_name>

or

poetry add <plugin_name>
```

#### 数据库管理

```bash
# 创建数据库迁移
bomiot makemigrations

# 执行数据库迁移
bomiot migrate

# 加载初始数据
bomiot loaddata <source>

# 导出数据
bomiot dumpdata [appname]
```

#### 用户管理

```bash
# 创建管理员账户
bomiot initadmin

# 重置管理员密码
bomiot initpwd
```

#### 服务管理

```bash
# 启动服务器
bomiot run [选项]

# 部署项目
bomiot deploy <project_name>
```

#### 系统校验

```bash
# 初始化校验Keys
bomiot keys
```

### 🚀 服务器启动选项

```bash
bomiot run [选项]

选项:
  --host, -b HOST                服务器主机地址 (默认: 127.0.0.1)
  --port, -p PORT                服务器端口 (默认: 8000)
  --workers -w WORKERS           工作进程数 (默认: 2)
  --log-level LEVEL              日志级别 (critical/error/warning/info/debug/trace)
  --ssl-keyfile FILE             SSL 密钥文件
  --ssl-certfile FILE            SSL 证书文件
  --proxy-headers                启用代理头
  --http HTTP                    HTTP 实现 (auto/h11/httptools)
  --loop LOOP                    异步循环 (auto/asyncio/uvloop)
  --limit-concurrency            最大并发请求数(默认：1000)
  --backlog                      最大等待连接数(默认：2048)
  --timeout-keep-alive           HTTP 长连接超时时间(默认: 5)
  --timeout-graceful-shutdown    优雅关闭超时时间(默认：30)
```

### 📝 使用示例

```bash
# 基本启动
bomiot run

# 测试api，method("GET")
"name": "django","url": "http://127.0.0.1:8000/test/"
"name": "fastapi", "url": "http://127.0.0.1:8000/fastapi/test/"
"name": "flask", "url": "http://127.0.0.1:8000/flask/test/"

# 指定端口和主机
bomiot run --host 0.0.0.0 --port 8080

# 生产环境配置
bomiot run --host 0.0.0.0 --port 80 --workers 4 --log-level info

# SSL 配置
bomiot run --ssl-keyfile key.pem --ssl-certfile cert.pem
```

---

## 🏗️ 项目结构

```
my-project/                    # 项目目录
├── fastapi_app/               # fastapi app
│   └── main.py                # 主文件
├── flask_app/                 # flask app
│   └── main.py                # 主文件
├── language/                  # 后端语言文件
│   ├── en-US.toml             # 英文翻译文件       
│   └── zh-CN.toml             # 中文翻译文件
├── media/                     # 静态文件
│   ├── img/                   # 公用图片       
│   └── ***.md                 # md的各种文档
├── static/                    # 静态文件
├── __version__.py             # my-project版本
├── bomiotconf.ini             # Bomiot项目标识文件
├── files.py                   # 文件信号
├── receiver.py                # 数据API信号
├── server.py                  # 服务器信号
├── README.md                  # ReadME文档
└── setup.ini                  # 项目配置文件
dbs/                           # 数据库文件
logs/                          # 系统日志
setup.ini                      # 项目配置文件
...
```

---

## 🔧 配置说明

### 环境配置

Bomiot 使用配置文件来管理不同环境的设置：

```ini
# setup.ini
[project]
name = my-project

[database](需要keys校验)
# 支持多种数据库 (sqlite、mysql、oracle、postgresql)
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port

[local]
time_zone = UTC

[jwt]
user_jwt_time = 1000000

[throttle]
allocation_seconds = 1
throttle_seconds = 10

[request]
limit = 2

[file](需要keys校验)
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

### 数据库配置

支持多种数据库：

- **SQLite** (默认)
- **MySQL**  (需要keys校验)
- **PostgreSQL** (需要keys校验)
- **Oracle** (需要keys校验)

---

## 🌐 部署指南

### Supervisor

```bash
# 生成部署文件
bomiot deploy my-project

# supervisord.conf指向这个文件，就可以完成守护进程部署

```

## 定时任务

### 支持的定时任务

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date','timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}
```

### 定时任务编写

```python
from bomiot.server.core.signal import bomiot_signals

def my_scheduled_task(sender, **kwargs):
    print("执行定时任务")
    
# 任意位置给bomiot发送信号，一般是写在urls.py里面，刷新web端页面即生效
bomiot_signals.send(sender=my_scheduled_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'end_date': '2099-05-30',
        'description': '每60秒执行一次，2099年5月30日结束'
    }
})
```

### 仅一次性执行的任务

```python
from bomiot.server.core.signal import bomiot_signals

def my_once_task(sender, **kwargs):
    print("执行一次性任务")
    
# 任意位置给bomiot发送信号，即可以执行一次性任务
bomiot_signals.send(sender=my_once_task, msg={
    'models': 'Fuction'
})
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

1. **报告 Bug**: [创建 Issue](https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md)
2. **功能请求**: [提交功能请求](https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md)
3. **代码贡献**: Fork 项目并提交 Pull Request
4. **文档改进**: 帮助完善文档
5. **社区支持**: 回答其他用户的问题

### 贡献代码

```bash
# 1. Fork 项目
# 2. 克隆你的 Fork
git clone https://github.com/your-username/Bomiot.git

# 3. 创建功能分支
git checkout -b feature/amazing-feature

# 4. 提交更改
git commit -m 'Add amazing feature'

# 5. 推送到分支
git push origin feature/amazing-feature

# 6. 创建 Pull Request
```

### 代码规范

- 遵循 PEP 8 Python 代码规范
- 添加适当的注释和文档字符串
- 编写单元测试
- 确保所有测试通过

---

## 📄 许可证

本项目采用 [APLv2](LICENSE) 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🔗 相关链接

### 📺 视频教程
- [BiliBili 频道](https://space.bilibili.com/407321291/channel/seriesdetail?sid=776320)

### 🐛 问题反馈
- [报告 Bug](https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md)
- [功能请求](https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md)

### 💬 社区
- [GitHub Discussions](https://github.com/Bomiot/Bomiot/discussions)
- [Issues](https://github.com/Bomiot/Bomiot/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给我们一个 Star！**

Made with ❤️ by [Bomiot Team](https://github.com/Bomiot)

</div>