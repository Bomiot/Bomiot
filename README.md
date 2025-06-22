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

[![YouTube](https://img.shields.io/youtube/channel/subscribers/UCPW1wciGMIEh7CYOdLnsloA?color=red&label=YouTube&logo=youtube&style=for-the-badge)](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)

[English](README.md) | [中文](README.zh-CN.md)

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
- [📚 开发指南](#-开发指南)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)
- [🔗 相关链接](#-相关链接)

---

## 🌟 项目简介

Bomiot 是一个革命性的分布式文档管理框架和全栈开发平台，专为解决现代开发中的痛点而设计。我们相信，优秀的开源项目不仅要有强大的技术栈，更要注重开发者的使用体验和团队协作效率。

### 🎯 设计理念

- **开发者友好**: 从 0 到 1 的无缝体验，无需复杂配置
- **团队协作**: 高效的开发团队交互机制
- **模块化设计**: 插件化架构，功能可扩展
- **企业级**: 生产环境就绪，支持大规模部署

---

## ✨ 核心特性

### 🔧 开发工具
- ✅ **项目脚手架**: 一键创建项目和应用
- ✅ **插件系统**: 丰富的插件生态
- ✅ **实时文件监控**: 开发效率提升
- ✅ **热重载**: 代码修改即时生效

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

### 4. 启动服务

```bash
# 启动开发服务器
bomiot run

# 或指定端口
bomiot run --port 8080
```

---

## 📦 安装指南

### 系统要求

- **Python**: 3.9 或更高版本
- **Node.js**: 18.19.1 或更高版本
- **操作系统**: Windows, macOS, Linux

### 详细安装步骤

#### 1. 安装 Python 依赖

```bash
# 克隆项目
git clone https://github.com/Bomiot/Bomiot.git
cd Bomiot

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2. 安装前端依赖

```bash
# 进入前端目录
cd bomiot/templates

# 安装依赖
yarn install

# 或使用 npm
npm install
```

#### 3. 初始化数据库

```bash
# 创建数据库迁移
bomiot makemigrations

# 执行迁移
bomiot migrate

# 创建管理员账户
bomiot initadmin
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
# 初始化工作空间
bomiot init [folder]

# 创建新项目
bomiot project <project_name>

# 创建新应用
bomiot new <app_name>

# 创建插件
bomiot plugins <plugin_name>
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
bomiot initpwd [folder]
```

#### 服务管理

```bash
# 启动服务器
bomiot run [选项]

# 部署项目
bomiot deploy [folder]
```

#### 系统管理

```bash
# 初始化认证密钥
bomiot keys

# 从市场安装项目
bomiot market <project_name>
```

### 🚀 服务器启动选项

```bash
bomiot run [选项]

选项:
  --host HOST          服务器主机地址 (默认: 127.0.0.1)
  --port PORT          服务器端口 (默认: 8000)
  --workers WORKERS    工作进程数 (默认: 2)
  --log-level LEVEL    日志级别 (critical/error/warning/info/debug/trace)
  --ssl-keyfile FILE   SSL 密钥文件
  --ssl-certfile FILE  SSL 证书文件
  --proxy-headers      启用代理头
  --http HTTP          HTTP 实现 (auto/h11/httptools)
  --loop LOOP          异步循环 (auto/asyncio/uvloop)
```

### 📝 使用示例

```bash
# 基本启动
bomiot run

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
Bomiot/
├── bomiot/                    # 核心包
│   ├── cmd/                   # 命令行工具
│   │   ├── __init__.py       # 主命令入口
│   │   ├── project.py        # 项目管理
│   │   ├── plugins.py        # 插件管理
│   │   ├── deploy.py         # 部署工具
│   │   └── ...
│   ├── server/               # 服务器端
│   │   ├── core/            # 核心模块
│   │   ├── server/          # 服务器配置
│   │   ├── media/           # 媒体文件
│   │   └── templates/       # 前端模板
│   └── ...
├── dbs/                      # 数据库文件
├── logs/                     # 日志文件
├── deploy/                   # 部署配置
├── requirements.txt          # Python 依赖
├── pyproject.toml           # 项目配置
└── README.md               # 项目文档
```

---

## 🔧 配置说明

### 环境配置

Bomiot 使用配置文件来管理不同环境的设置：

```ini
# setup.ini
[project]
name = my-project

[database]
engine = sqlite
name = db.sqlite3

[local]
time_zone = UTC

[jwt]
user_jwt_time = 1000000

[throttle]
allocation_seconds = 1
throttle_seconds = 10

[request]
limit = 2

[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

### 数据库配置

支持多种数据库：

- **SQLite** (默认)
- **MySQL**
- **PostgreSQL**
- **Oracle**

---

## 🌐 部署指南

### 开发环境

```bash
# 启动开发服务器
bomiot run --host 0.0.0.0 --port 8000
```

### 生产环境

#### 使用 Gunicorn

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn bomiot.server.server.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
```

#### 使用 Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN bomiot init
RUN bomiot migrate

EXPOSE 8000
CMD ["bomiot", "run", "--host", "0.0.0.0", "--port", "8000"]
```

#### 使用 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📚 开发指南

### 创建自定义应用

```bash
# 1. 创建应用
bomiot new my-custom-app

# 2. 编辑应用代码
cd my-project/my-custom-app

# 3. 注册应用
# 在 bomiotconf.ini 中设置 mode = plugins
```

### 创建定时任务

```python
from bomiot.server.core.signal import bomiot_job_signals

@receiver(bomiot_job_signals)
def my_scheduled_task(sender, **kwargs):
    # 你的任务逻辑
    print("执行定时任务")
    
# 发送任务信号
bomiot_job_signals.send(sender=my_scheduled_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'description': '每分钟执行一次'
    }
})
```

### API 开发

```python
from rest_framework import viewsets
from bomiot.server.core.client import CoreModelViewSet

class MyModelViewSet(CoreModelViewSet):
    """
    自定义 API 视图集
    """
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    filter_class = MyModelFilter
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

### 开发环境设置

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
- [YouTube 频道](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)

### 📖 文档
- [项目 Wiki](https://github.com/Bomiot/Bomiot/wiki)
- [API 文档](https://github.com/Bomiot/Bomiot/wiki/API-Documentation)

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