<div align="center">
  <img src="bomiot/templates/dist/spa/icons/logo.png" alt="Bomiot logo" width="200" height="auto" />
  <h1>🚀 Bomiot</h1>
  <p><strong>One App you can do everything</strong></p>
  <p><em>Powerful Distributed Document Management Framework & Full-Stack Development Platform</em></p>

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

[English](README.md) | [中文](README-github.zh-CN.md)

</div>

---

## 📋 Table of Contents

- [🌟 Project Introduction](#-project-introduction)
- [✨ Core Features](#-core-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation Guide](#-installation-guide)
- [🛠️ Command Line Tools](#️-command-line-tools)
- [🏗️ Project Structure](#️-project-structure)
- [🔧 Configuration](#-configuration)
- [🌐 Deployment Guide](#-deployment-guide)
- [📚 Scheduled Tasks](#-scheduled-tasks)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🔗 Related Links](#-related-links)

---

## 🌟 Project Introduction

Bomiot is a revolutionary distributed document management framework and full-stack development platform, with core components written in Rust, designed to solve modern development pain points. We believe that excellent open-source projects should not only have powerful technology stacks but also focus on developer experience and team collaboration efficiency, making it simple and easy to learn.

### 🎯 Design Philosophy

- **Learning Curve**: Backend supports Django, FastAPI, Flask; Frontend supports React, Angular, Vue, Django built-in Templates (official provides a Vue set)
- **Developer Friendly**: Seamless experience from 0 to 1, no complex configuration required
- **Team Collaboration**: Efficient development team interaction mechanisms
- **Modular Design**: Plugin-based architecture with extensible functionality
- **Easy Deployment**: pip installation, convenient for team deployment, supports Python 3.9+
- **Signal Mechanism**: Data management through signal mechanism, more convenient custom API support
- **Enterprise Ready**: Production-ready, supports large-scale deployment

---

## ✨ Core Features

### 🔧 Development Tools
- ✅ **Project Scaffolding**: One-click project and application creation
- ✅ **Plugin System**: Rich plugin ecosystem
- ✅ **Real-time File Monitoring**: Enhanced development efficiency

### 🕐 Task Management
- ✅ **Scheduled Tasks**: Powerful scheduling system
- ✅ **Task Monitoring**: Real-time task status tracking
- ✅ **Error Handling**: Intelligent exception handling mechanism
- ✅ **Log Management**: Complete logging system

### 🔐 Access Control
- ✅ **Fine-grained Permissions**: Role-based access control
- ✅ **JWT Authentication**: Secure identity authentication
- ✅ **API Permissions**: Interface-level permission management
- ✅ **Operation Audit**: Complete operation logs

### 🌍 Internationalization
- ✅ **Multi-language Support**: Built-in internationalization framework
- ✅ **Dynamic Language Switching**: Runtime language switching
- ✅ **Localization Configuration**: Regional settings

### 📊 System Monitoring
- ✅ **Performance Monitoring**: CPU, memory, disk monitoring
- ✅ **Process Management**: Real-time system process monitoring
- ✅ **Network Monitoring**: Network traffic statistics
- ✅ **Health Checks**: System health status detection

### 📚 Application Market
- ✅ **Application Sharing**: Application market pip installation, convenient and fast
- ✅ **Component Market**: Hot-pluggable components, dynamic import

---

## 🚀 Quick Start

### 1. Install Bomiot

```bash
# Install using pip
pip install bomiot

# Or install using poetry
poetry add bomiot
```

### 2. Initialize Workspace

```bash
# Initialize Bomiot workspace
bomiot init
```

### 3. Create Project

```bash
# Create new project
bomiot project my-project

# Create new application
bomiot new my-app
```

### 4. Database

```bash
# Initialize database
bomiot migrate

# If you created a new application, you can generate new database migration files
bomiot makemigrations
```

### 5. Create Administrator

```bash
# Initialize administrator
bomiot initadmin

# Reset administrator account password
bomiot initpwd
```

### 6. Start Service

```bash
# Start development server
bomiot run

# Or specify port
bomiot run --host 0.0.0.0 --port 8080
```

---

## 📦 Installation Guide

### System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 18.19.1 or higher
- **Operating System**: Windows, macOS, Linux

### Modify Frontend

#### 1. Install Frontend Dependencies

```bash
# Enter frontend directory
cd my-project/templates

# Install dependencies
yarn install
```

#### 2. Open Development baseUrl

```bash
# Create database migration
vim my-project/templates/src/boot/axios.js

```

```bash
# axios.js code snippet modification
 ...
const baseURL = 'http://127.0.0.1:8000' // Replace with your actual API URL

const api = axios.create({
  baseURL: baseURL ##Open this
})
 ...
```


#### 3. Frontend Development Debugging

```bash
# Ensure backend is already started
bomiot run
```

```bash
# Restart frontend
cd my-project/templates

&

quasar dev
```

---

## 🛠️ Command Line Tools

Bomiot provides powerful command line tools to make development and management simple and efficient.

### 📋 Command Overview

```bash
bomiot [command] [options]
```

### 🔧 Core Commands

#### Project Management

```bash
# Help command
bomiot -h

# View version number
bomiot -v

# Initialize workspace
bomiot init

# Create new project
bomiot project <project_name>

# Create new application
bomiot new <app_name>

# Create plugin
bomiot plugins <plugin_name>
```

#### Application Market

```bash
# Application market
bomiot market <project_name>

# Plugin installation, plugins are automatically hot-imported
pip install -y <plugin_name>

or

poetry add <plugin_name>
```

#### Database Management

```bash
# Create database migration
bomiot makemigrations

# Execute database migration
bomiot migrate

# Load initial data
bomiot loaddata <source>

# Export data
bomiot dumpdata [appname]
```

#### User Management

```bash
# Create administrator account
bomiot initadmin

# Reset administrator password
bomiot initpwd
```

#### Service Management

```bash
# Start server
bomiot run [options]

# Deploy project
bomiot deploy <project_name>
```

#### System Validation

```bash
# Initialize validation Keys
bomiot keys
```

### 🚀 Server Startup Options

```bash
bomiot run [options]

Options:
  --host, -b HOST                Server host address (default: 127.0.0.1)
  --port, -p PORT                Server port (default: 8000)
  --workers -w WORKERS           Number of worker processes (default: 2)
  --log-level LEVEL              Log level (critical/error/warning/info/debug/trace)
  --ssl-keyfile FILE             SSL key file
  --ssl-certfile FILE            SSL certificate file
  --proxy-headers                Enable proxy headers
  --http HTTP                    HTTP implementation (auto/h11/httptools)
  --loop LOOP                    Async loop (auto/asyncio/uvloop)
  --limit-concurrency            Maximum concurrent requests (default: 1000)
  --backlog                      Maximum waiting connections (default: 2048)
  --timeout-keep-alive           HTTP keep-alive timeout (default: 5)
  --timeout-graceful-shutdown    Graceful shutdown timeout (default: 30)
```

### 📝 Usage Examples

```bash
# Basic startup
bomiot run

# Test api，method("GET")
"name": "django", "url": "http://127.0.0.1:8000/test/"
"name": "fastapi", "url": "http://127.0.0.1:8000/fastapi/test/"
"name": "flask", "url": "http://127.0.0.1:8000/flask/test/"

# Specify port and host
bomiot run --host 0.0.0.0 --port 8080

# Production environment configuration
bomiot run --host 0.0.0.0 --port 80 --workers 4 --log-level info

# SSL configuration
bomiot run --ssl-keyfile key.pem --ssl-certfile cert.pem
```

---

## 🏗️ Project Structure

```
my-project/                    # Project directory
├── fastapi_app/               # fastapi app
│   └── main.py                # Main file
├── flask_app/                 # flask app
│   └── main.py                # Main file
├── language/                  # Backend language files
│   ├── en-US.toml             # English translation file       
│   └── zh-CN.toml             # Chinese translation file
├── media/                     # Static files
│   ├── img/                   # Public images       
│   └── ***.md                 # Various md documents
├── static/                    # Static files
├── __version__.py             # my-project version
├── bomiotconf.ini             # Bomiot project identifier file
├── files.py                   # File signals
├── receiver.py                # Data API signals
├── server.py                  # Server signals
├── README.md                  # ReadME documentation
└── setup.ini                  # Project configuration file
dbs/                           # Database files
logs/                          # System logs
setup.ini                      # Project configuration file
...
```

---

## 🔧 Configuration

### Environment Configuration

Bomiot uses configuration files to manage different environment settings:

```ini
# setup.ini
[project]
name = my-project

[database](requires keys validation)
# Supports multiple databases (sqlite, mysql, oracle, postgresql)
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

[file](requires keys validation)
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

### Database Configuration

Supports multiple databases:

- **SQLite** (default)
- **MySQL** (requires keys validation)
- **PostgreSQL** (requires keys validation)
- **Oracle** (requires keys validation)

---

## 🌐 Deployment Guide

### Supervisor

```bash
# Generate deployment files
bomiot deploy my-project

# Point supervisord.conf to this file to complete daemon process deployment

```

## Scheduled Tasks

### Supported Scheduled Tasks

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date','timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}
```

### Writing Scheduled Tasks

```python
from bomiot.server.core.signal import bomiot_signals

def my_scheduled_task(sender, **kwargs):
    print("Execute scheduled task")
    
# Send signal to bomiot anywhere, usually written in urls.py, refresh web page to take effect
bomiot_signals.send(sender=my_scheduled_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'end_date': '2099-05-30',
        'description': 'Execute every 60 seconds, end on May 30, 2099'
    }
})
```

### One-time Execution Tasks Only

```python
from bomiot.server.core.signal import bomiot_signals

def my_once_task(sender, **kwargs):
    print("Execute one-time task")
    
# Send signal to bomiot anywhere to execute one-time task
bomiot_signals.send(sender=my_once_task, msg={
    'models': 'Function'
})
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### Ways to Contribute

1. **Report Bugs**: [Create Issue](https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md)
2. **Feature Requests**: [Submit Feature Request](https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md)
3. **Code Contributions**: Fork the project and submit Pull Request
4. **Documentation Improvements**: Help improve documentation
5. **Community Support**: Answer other users' questions

### Ways to Contribute Code

```bash
# 1. Fork the project
# 2. Clone your Fork
git clone https://github.com/your-username/Bomiot.git

# 3. Create feature branch
git checkout -b feature/amazing-feature

# 4. Commit changes
git commit -m 'Add amazing feature'

# 5. Push to branch
git push origin feature/amazing-feature

# 6. Create Pull Request
```

### Code Standards

- Follow PEP 8 Python code standards
- Add appropriate comments and docstrings
- Write unit tests
- Ensure all tests pass

---

## 📄 License

This project is licensed under the [APLv2](LICENSE) License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Related Links

### 📺 Video Tutorials
- [YouTube Channel](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)

### 🐛 Issue Reporting
- [Report Bug](https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md)
- [Feature Request](https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md)

### 💬 Community
- [GitHub Discussions](https://github.com/Bomiot/Bomiot/discussions)
- [Issues](https://github.com/Bomiot/Bomiot/issues)

---

<div align="center">

**⭐ If this project helps you, please give us a Star!**

Made with ❤️ by [Bomiot Team](https://github.com/Bomiot)

</div>