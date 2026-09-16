<div align="center">
  <img src="bomiot/templates/dist/spa/icons/logo.png" alt="Bomiot logo" width="180" height="auto" />
  <h1>🚀 Bomiot</h1>
  <p><strong>No-environment delivery tool for Python apps</strong></p>
  <p><em>Compile to binary · Cross-platform · Incremental updates · Source code protection</em></p>

  [English](README.md) | [中文](README_CN.md)

  [![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=white)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/django-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Flask](https://img.shields.io/badge/flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![Vue.js](https://img.shields.io/badge/vue-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
  [![GitHub Stars](https://img.shields.io/github/stars/bomiot/bomiot?style=social)](https://github.com/bomiot/bomiot)
  [![Website](https://img.shields.io/badge/Website-Online-brightgreen)](https://www.bomiot.com)
</div>

---

## 📑 Table of Contents

- [About Bomiot](#-about-bomiot)
- [Video Introduction](#-video-introduction)
- [Core Features Overview](#-core-features-overview)
- [Use Case Examples](#-use-case-examples)
- [Quick Start](#-quick-start-5-minute-hands-on)
- [CLI Reference](#-cli-reference)
- [Configuration Reference](#-configuration-reference-setupini)
- [Scheduled Tasks](#-scheduled-tasks)
- [File Monitoring & Upload](#-file-monitoring--upload)
- [Real-time System Monitoring](#-real-time-system-monitoring)
- [Real-time WebSocket Communication](#-real-time-websocket-communication)
- [Deployment & Distribution](#-deployment--distribution)
- [Security Notice](#-security-notice)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 About Bomiot

Bomiot is a command-line tool for Python programmers, with its core ASGI gateway rewritten in Rust. It lets you ship your Python apps to **anyone without any environment** — no Python installation, no dependency configuration, just double-click to run, boots on startup, and silently updates in the background.

> 💡 **Bomiot is not some "revolutionary magic framework"** — technically, any capable engineer can replicate it.
>
> Its real value lies in turning a **real but often-overlooked need** — **no-environment delivery + continuous updates + code protection** for Python apps — into a **complete, out-of-the-box pipeline**:
>
> **Enabling Python developers to ship their apps — without environment dependencies, without exposing source code, with continuous updates — into the hands of non-technical users, ready to use out of the box.**

For developers, a single `bomiot deploy` command packages your Django / FastAPI / Flask app into a portable executable — copy it to the target machine and double-click to run, with zero environment setup. For end users, the experience is on par with a mobile app: boot-and-use, silent automatic version updates, and automatic rollback if an update fails — all with zero awareness. Every user / every device can be an independent node; nodes collaborate directly over the local area network. Bomiot also ships with a built-in free application marketplace where developers can freely publish and share apps, with pre-installed industry templates such as ERP / WMS available for one-click installation.

| Pain Points | Bomiot Solutions |
| :--- | :--- |
| 🐢 **Hard to ship Python apps, environment coupling** | ✅ **Portable Distribution**, compiled to binary, no Python or dependencies needed, double-click to run |
| 🔄 **Releases rely on manual notification, users don't update** | ✅ **Incremental Auto-Update**, silent delta download in background, takes effect on next launch, auto rollback on failure |
| 🖥️ **Won't auto-run on boot, hard to maintain** | ✅ **Boot-and-Use**, portable programs can be configured to auto-start on boot, ready to run out of the box |
| 🏢 **Fragmented enterprise systems, data silos** | ✅ **Enterprise System Integration**, unified access for ERP/WMS/CRM/MES/OA, data flows on demand |
| 🔗 **Multi-site / multi-facility collaboration difficulties** | ✅ **Node-based Networking**, nodes connect directly via LAN, decentralized, no central server required |
| 🧩 **Separated frontend & backend, complex integration** | ✅ **Full-Stack Unification**, Python backends (Django/FastAPI/Flask) + mainstream frontends, flexible combinations |
| 📡 **No real-time channels, inefficient polling** | ✅ **Built-in WebSocket**, native ASGI implementation, real-time bidirectional communication |
| 🛡️ **Performance bottlenecks, code leakage** | ✅ **Rust-rewritten ASGI Gateway**, compiled to native binary, more stable performance and effective code protection |
| 💰 **Closed ecosystem, hard to reuse** | ✅ **Own Free Application Marketplace** with pre-built industry templates; developers freely publish and share applications |

---

## 📹 Video Introduction

Watch the video introduction of Bomiot to quickly understand the core features and usage of the platform.

▶ **[Click to Watch Video Introduction](https://youtube.com/@greaterwms3682?si=gShTwLvMtyVNqoqC)** (YouTube)

---

## ✨ Core Features Overview

### 1. Portable Distribution / No-Environment Delivery

**Bomiot's core selling point.** Compile Python apps into portable executables — copy to the target machine and double-click to run, no Python installation, no environment configuration needed.

- 📦 **Portable Packaging**: Code, runtime and resources are compiled into a portable program, no installation required, ready to use after extraction.
- ⚡ **Instant Run**: No Python install, no environment setup, no dependencies — just double-click to run.
- 🔐 **Effective Code Protection**: Python code is compiled into native binaries, significantly improving code protection.
- 🎯 **For Non-Technical Users**: Deliver to bosses, warehouse managers, sales staff — not just engineers.

### 2. Incremental Auto-Update (Silent Upgrade · Zero Awareness)

**Distribution is just the beginning — continuous iteration is the norm.** Bomiot's built-in incremental update mechanism lets distributed portable apps automatically detect, download, and apply new versions, ending the primitive practice of "messaging customers to reinstall."

- 🔍 **Automatic Version Check**: Automatically checks for new versions at startup, no manual intervention required.
- 📦 **Incremental Delta Download**: Downloads only the changed parts (not the full package), small update size and fast speed, completed in seconds.
- 🤫 **Background Silent Upgrade**: Applies the update in the background after download, takes effect on next launch, users are completely unaware.
- ↩️ **Automatic Rollback on Failure**: If an anomaly occurs during the update, automatically rolls back to the previous working version, ensuring the app is always runnable.
- 🔄 **Unified Version Management**: After developers publish a new version, all installed nodes automatically converge to the latest version, ending the ops nightmare of "100 customers on 100 different versions."

### 3. Cross-Platform Node-Based Architecture

**Develop once, run cross-platform.** Turn every Windows / macOS / Linux device into an independent server node, supporting industrial PCs and edge gateways for IoT devices.

- 🌍 **Full Platform Support**: Native support for Windows, macOS and Linux, one codebase runs everywhere.
- 🔒 **Local Data**: Data is stored on each node, complying with data sovereignty requirements, suitable for intranet / offline environments.
- 🤖 **Edge Device Support**: Compatible with industrial PCs, Raspberry Pi, edge gateways and other IoT devices to build edge computing nodes.
- 🌐 **Node-based Networking**: Multi-site, multi-facility and multi-branch nodes interconnect over LAN — decentralized, no central server required.

### 4. Rust Rewritten ASGI Gateway

Bomiot uses Rust to rewrite the core ASGI gateway, compiles it into native binaries, bringing more stable performance and code protection.

- 🦀 **Rust ASGI Gateway**: The core gateway is written in Rust, compiled to native binaries, with more stable performance.
- 🚀 **Stable Performance**: The compiled binaries have lower latency and more stable operation under high-concurrency requests.
- 🔐 **Code Protection**: Python code is converted to native binaries along with compilation, effectively improving code protection.

### 5. Enterprise System Integration (Unified Multi-System Access · End Data Silos)

**Purpose-built for connecting internal enterprise systems**. ERP, WMS, CRM, MES, OA — inconsistent interfaces don't matter. Bomiot connects everything for you.

- 🏢 **Multi-System Connectivity**: Standard APIs, direct database access, or UI-level automation — all can be unified into Bomiot nodes.
- 🔄 **Real-Time Data Flow**: Real-time fetch and push between nodes; business states sync across systems at millisecond level.
- 🧩 **Unified Permission System**: Single account for all subsystems; centralized role & API permission control.
- 📊 **Unified Monitoring Dashboard**: All node statuses, system health and core business metrics on one screen.

### 6. Built-In Free Application Marketplace · One-Click Industry Template Installation

Bomiot has a **free and open application marketplace** with pre-installed industry templates such as ERP / WMS. Developers can also freely publish and share applications.

- 🏪 **Free Application Marketplace**: Built-in official marketplace, developers can freely publish applications, users can download with one click, **completely free**.
- 🎯 **Industry Templates**: Pre-built templates including GreaterWMS (WMS), install in one click and ready to use.
- 🔓 **Open Sharing**: All marketplace content is open for download to everyone, promoting the rapid dissemination and reuse of technology.
- 🔐 **Secure Distribution**: Applications can be compiled and encrypted before publishing, protecting developers' code choices.

### 7. Multi-Language Full-Stack Framework Freedom

No restrictions on tech stack, use the tools you are most familiar with. Bomiot supports a flexible combination of Python backend + JavaScript frontend.

- **Backend Support (Python)**:
  - 🟢 **Django** (Enterprise-grade preferred)
  - 🚀 **FastAPI** (High concurrency performance)
  - ⚪ **Flask** (Lightweight and flexible)
- **Frontend Support (JavaScript/TypeScript)**:
  - 💚 **Quasar / Vue 3** (Primary support, fully integrated)
  - 🔄 Abstraction layer reserved, extendable to React and Angular.

### 8. Built-In Scheduled Task Scheduling

A built-in database-driven scheduled task system supports multiple trigger methods.

- ⏰ **Three Triggers**: Supports `cron` (scheduled), `interval` (interval), `date` (date) three trigger methods.
- 💾 **Database Persistence**: Tasks are stored in the database, automatically restored after service restart.
- 🔄 **Auto Sync**: SchedulerManager automatically synchronizes task status every 60 seconds, adding, deleting and modifying take effect immediately.
- 📝 **Task Template**: Define task functions in `task.py`, which can be called and executed by the scheduler.

### 9. File Monitoring & Upload

Real-time file monitoring system automatically manages user-uploaded files.

- 👀 **Real-Time Monitoring**: Automatically monitors the media directory, captures file creation, modification, deletion and movement operations.
- 📋 **Auto Registration**: File changes are automatically written to the database, recording file name, type, size and owner.
- 📡 **Event Notification**: File changes are broadcast in real-time through the signal mechanism, convenient for frontend or third-party subscriptions.
- ⚙️ **Flexible Configuration**: Set file size limits and allowed file types in `setup.ini`.

### 10. Real-Time WebSocket Communication

Bomiot's Rust ASGI gateway natively supports WebSocket. You can directly write WebSocket routes in the application's `main.py`. For details, see the [WebSocket Section](#-real-time-websocket-communication).

- 💬 **Minimal Development**: Directly use the standard WebSocket syntax of FastAPI/Flask, zero learning cost.
- ⚡ **Gateway Forwarding**: The Rust gateway automatically identifies WebSocket requests and efficiently forwards them to the corresponding application.
- 🔌 **Full Framework Support**: Can be used in `main.py` of Django, FastAPI or Flask applications.

### 11. Real-Time System Monitoring

Backend system monitoring, real-time collection of server running status.

- 💻 **CPU Monitoring**: Collects CPU usage, physical cores, logical cores, frequency information.
- 🧠 **Memory Monitoring**: Collects total, used, available and usage of physical memory and swap partitions.
- 💽 **Disk Monitoring**: Collects capacity, used, available and usage of each partition.
- 🌐 **Network Monitoring**: Collects bytes sent and received over the network.
- 📊 **Process Monitoring**: Collects PID, name, CPU usage and memory usage of all running processes.
- 🗄️ **Auto Cleanup**: Historical data is automatically cleaned up (upper limit of 10080 entries) to prevent database bloating.

### 12. Built-In API Rate Limiting Protection

Provides out-of-the-box API security protection for your applications to ensure system stability.

- 🛡️ **Intelligent Rate Limiting**: Fine-grained rate limiting based on IP address and HTTP request method (GET/POST, etc.).
- 🛡️ **Anti-Scraping Protection**: Effectively prevents malicious crawlers, interface scraping and denial-of-service (DoS) attacks.
- ⚙️ **Flexible Configuration**: Customize the rate limiting time window and request frequency in the `[throttle]` section of `setup.ini`.

---

## 💡 Use Case Examples

Bomiot's platform capabilities make it suitable for a variety of real-world business scenarios. Here are some typical examples:

### 🏭 Automated Enterprise System Integration
Various enterprise internal systems (WMS, ERP, MES, OA, CRM, etc.) are often difficult to integrate due to inconsistent interfaces. With Bomiot + browser automation tools (such as Playwright), you can achieve UI-level automation **without modifying any system code**:
- Real-time fetch data from one system and automatically fill it into another
- Monitor business status changes and synchronize across systems in real time
- No need for the target system to provide an API; complete data transfer directly through UI operations
- Cooperate with Scheduled Tasks + WebSocket notifications to alert exceptions immediately

### 🛒 E-Commerce Price & Inventory Monitoring
Build automated e-commerce monitoring applications to help operations teams stay on top of market dynamics:
- Periodically scrape competitor prices and promotional information, generating price change reports
- Monitor product inventory status and automatically trigger alerts when stock is low
- Support simultaneous monitoring across multiple platforms (Taobao, JD, Pinduoduo, etc.)
- Data changes are pushed to the frontend dashboard in real time via WebSocket
- After development, it can be compiled into a portable version, distributed to multiple operators for independent operation, data does not affect each other

### 📊 Data Inspection & Automated Reporting
Leverage scheduled tasks + file monitoring capabilities to build automated data processing pipelines:
- Periodically collect business data from data sources (databases, files, APIs)
- Automatically generate Excel / PDF reports and distribute them to designated personnel
- Monitor key business indicators and automatically trigger alert notifications on anomalies
- Portable distribution, deployed to various departments for independent operation, data stays local

### 🔧 General Automation Toolkit
Transform repetitive tasks into automated workflows to boost team efficiency:
- Automated form filling and submission (HR systems, finance systems, etc.)
- Automated document generation and archiving
- System health inspection and automatic restart
- One-click compilation to portable runtime files after development, easy distribution across multiple devices and personnel

### 🤖 Industrial IoT & Edge Computing
Deploy Bomiot nodes to industrial PCs and edge gateways to build decentralized IoT solutions:
- **Edge Data Collection**: Real-time collection of sensor data on on-site equipment in workshops and warehouses
- **Local Processing & Alerts**: Data processed locally at edge nodes, low-latency alert triggering
- **Multi-Node Collaboration**: Multiple edge nodes collaborate over local network without cloud servers
- **Data Sovereignty**: Sensitive production data retained on local nodes, complying with industrial security requirements
- **Remote Operations**: Remote monitoring of edge node running status via WebSocket

### 🏠 Smart Home & Edge Gateway
Use Bomiot as an edge gateway for homes or offices to centrally manage smart devices:
- **Unified Device Access**: Connect various smart devices (lights, sensors, cameras, etc.) via MQTT protocol
- **Automation Orchestration**: Define automation rules, such as "automatically turn on AC when temperature is too high"
- **Local Automation**: Offline operation, data stays local, protecting privacy
- **Portable Distribution**: Plug-and-play deployment to home servers or mini PCs

---

## 🚀 Quick Start (5-Minute Hands-On)

```bash
# 1. Install Bomiot
pip install bomiot

# 2. Initialize workspace
bomiot init

# 3. Create project, app and API
bomiot project my-project
bomiot app my-app
bomiot api my-api

# 4. Initialize database and admin
bomiot migrate
bomiot initadmin

# 5. Start service
bomiot run --host 0.0.0.0 --port 8000
```

**Done!** Open `http://127.0.0.1:8000/` to start your development journey.

---

## 🛠️ CLI Reference

| Category | Command | Description |
| :--- | :--- | :--- |
| **Project** | `bomiot init` | Initialize workspace |
| | `bomiot project <name>` | Create new project |
| | `bomiot app <name>` | Create new app |
| | `bomiot api <name>` | Create new API |
| **Database** | `bomiot makemigrations` | Generate migration files |
| | `bomiot migrate` | Execute database migration |
| | `bomiot loaddata <source>` | Load initial data |
| | `bomiot dumpdata [appname]` | Export data |
| **Service** | `bomiot run [options]` | Start development server |
| | `bomiot deploy` | Deploy project (compile and package) |
| **Admin** | `bomiot initadmin` | Create admin account |
| | `bomiot initpwd` | Reset admin password |

---

## 🔧 Configuration Reference (`setup.ini`)

```ini
[project]
name = greaterwms

[database]
# engine: sqlite | mysql | postgresql | oracle
engine = sqlite
# ... other database connection information ...

[debug]
# Control production/debug mode
debug = True

[file]
# File upload configuration
file_size = 102400000    # Maximum file size (bytes), default 100MB
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf

[system_control]
# Backend service switches
observer = True        # File monitoring
scheduler = True       # Scheduled task scheduling
server_monitor = True  # System resource monitoring

# ... (other configuration items)
```

---

## ⏰ Scheduled Tasks

Bomiot has a built-in scheduled task system, defines tasks through `task.py`, and supports three trigger methods.

### Define Tasks
Define task functions in `task.py` of the workspace:

```python
def example_job(**kwargs):
    """Example task function"""
    from datetime import datetime
    print(f"Execution time: {datetime.now()}")
    # Write your business logic here
```

### Trigger Types
| Type | Description | Example |
| :--- | :--- | :--- |
| `cron` | Trigger regularly according to Cron expression | Execute backup at 02:00 every day |
| `interval` | Trigger at fixed intervals | Check once every 5 minutes |
| `date` | Trigger once at the specified time | Execute at 23:59 on 2026-12-31 |

### Enable Scheduling
Ensure `scheduler = True` in `[system_control]` of `setup.ini`. The scheduler will run automatically after the service starts.

---

## 📁 File Monitoring & Upload

Bomiot has a built-in file monitoring system that automatically tracks changes in user-uploaded files.

### Monitoring Mechanism
- **Real-Time Monitoring**: Monitors the `MEDIA_ROOT` media directory, recursively listens to all subdirectories.
- **Event Capture**: Automatically captures four operations of file **creation**, **modification**, **deletion** and **movement**.
- **User Association**: Automatically identifies the file owner according to the directory level and writes it to the `Files` data table.
- **Signal Notification**: Every file change broadcasts an event through `bomiot_signals`, and the frontend can subscribe in real-time.

### Upload Configuration
Configure upload parameters in the `[file]` section of `setup.ini`:

```ini
[file]
file_size = 102400000    # Maximum file size (default 100MB)
file_extension = png,jpg,pdf,docx,...  # Allowed file extensions
```

### Enable File Monitoring
Ensure `observer = True` in `[system_control]` of `setup.ini`. File monitoring will be automatically enabled after the service starts.

---

## 📊 Real-time System Monitoring

Bomiot has a built-in system monitoring module that collects core operating indicators of the server in the background. The data is stored in the database and broadcast in real-time through signals.

### Monitoring Indicators
| Indicator | Collection Content | Storage Model |
| :--- | :--- | :--- |
| **CPU** | Usage, physical cores, logical cores, frequency | `CPU` |
| **Memory** | Total, used, available, Swap information | `Memory` |
| **Disk** | Capacity, used, available, usage of each partition | `Disk` |
| **Network** | Bytes sent, bytes received | `Network` |
| **Process** | PID, name, CPU usage, memory usage | `Pids` |

### Collection Frequency
- Perform a complete collection every **5 minutes**
- CPU, memory, network data are automatically cleaned up (upper limit of 10080 entries ≈ 7 days)
- Disk and processes are fully refreshed each time

### Enable System Monitoring
Ensure `server_monitor = True` in `[system_control]` of `setup.ini`. The monitoring will automatically run in a background thread after the service starts.

---

## 📡 Real-time WebSocket Communication

Bomiot's Rust ASGI gateway natively supports WebSocket, no additional configuration required. Just write WebSocket routes directly in the application's `main.py`.

### Development Example
In the FastAPI application's `main.py`:

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### Core Features
- 💬 **Minimal Development**: Directly use the standard WebSocket syntax of FastAPI/Flask, zero learning cost.
- ⚡ **Gateway Forwarding**: The Rust gateway automatically identifies WebSocket requests and efficiently forwards them to the corresponding application.
- 🔄 **Bidirectional Communication**: Supports server-side active push, enabling real-time notifications, data broadcasting and other scenarios.
- 🔌 **Ready-to-Use**: No additional dependencies required, natively supported by the framework.

### Typical Use Cases
- Real-time Data Dashboard: Monitor metric changes pushed to the frontend in real time
- System Alert Notifications: Alert users immediately through WebSocket when exceptions occur
- Collaborative Editing: Multiple people collaboratively operating the same data in real time
- Chat & Messaging: Instant messages, notification broadcasting

---

## 🌐 Deployment & Distribution

Bomiot provides two deployment methods for different scenarios:

| Comparison | Traditional Server Deployment (`bomiot run`) | Node-Based Distribution (`bomiot deploy`) |
| :--- | :--- | :--- |
| **Cost** | ✅ Completely Free | 💎 Sponsor Only |
| **Runtime** | Requires Python & dependencies | Portable, double-click to run, no environment |
| **Incremental Update** | Self-managed | Built-in silent incremental update |
| **Code Protection** | Source code in plaintext | Compiled to binary, effective code protection |
| **Use Case** | Server deployment, development | Field PCs, industrial PCs, multi-device distribution |
| **Device Binding** | None | Supported (unique per device) |

### Traditional Server Deployment (Free)
You can deploy Bomiot applications to any server like a traditional Django/FastAPI project, **completely free, no restrictions**.

```bash
# Traditional server deployment
bomiot run --host 0.0.0.0 --port 8000
```

### Node-Based Distribution (Sponsor Only)
```bash
bomiot deploy  # Cross-platform compilation to portable runtime files
```
Generates portable runtime files through cross-platform compilation and packaging, **copy it to the target machine and double-click to run**. This distribution method is Sponsor Only, featuring compiled encryption and instant cross-platform deployment.

> 💡 **Note: Node-based distribution supports both on-premises physical devices and cloud server environments.** The portable runtime files generated by `bomiot deploy` can be deployed directly to physical devices on the enterprise intranet (PCs, industrial PCs, edge gateways, Raspberry Pi, on-premise data-center servers, etc.), as well as to cloud server instances. The device-bound verification mechanism is consistent across all scenarios.

**Device-Bound Verification Mechanism:**
- On first run, the program automatically generates `auth_key.py` based on the local network card information
- Visit the official website with `auth_key.py` to complete verification and exchange for `sponsor.py`
- All verifications are completed **locally**, bound to the unique device identifier, only valid for the current device
- Each device can only have one `sponsor.py`; changing hardware or cloud server instance requires re-binding.

> **Privacy Protection Commitment**: All verifications are completed **locally**, and your node information or business data will not be uploaded to any server. Your code, configuration and operational data are always retained on local nodes.

---

## ⚠️ Security Notice

### Data Ownership and Privacy
- **Local Verification**: All verification mechanisms run entirely locally, no network connection required, and no user data collected.
- **Data Sovereignty**: All business data, configuration files and operation logs are stored on local nodes, and you have absolute control over your data.
- **No Third-Party Dependencies**: Except for the operating system itself, Bomiot will not force you to install any cloud service or send telemetry data to third parties.

### About Code Protection
Compilation converts Python code to native binaries, effectively improving code protection.

- It is recommended to place core algorithms and sensitive logic on the **server-side node** rather than the client-side
- For high security requirements, it is recommended to cooperate with **code signing** and **local verification** mechanisms

### Deployment Recommendations
- For production environments, please set `debug` in `[debug]` of `setup.ini` to `False`
- External network deployment must configure HTTPS (`--ssl-keyfile` + `--ssl-certfile`)
- Regularly back up the database (`bomiot dumpdata`) and `setup.ini` configuration

---

## 🤝 Contributing

We welcome contributions of any form!

- 🔗 **Official Website**: [https://www.bomiot.com](https://www.bomiot.com)
- 🐛 **Submit Bug**: [Create Issue](https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md)
- ✨ **Feature Suggestion**: [Submit Feature Request](https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md)
- 💻 **Code Contribution**: Fork the repository -> Create a branch -> Submit a Pull Request
- 🧩 **Share Applications**: Develop industry applications based on Bomiot and publish them to the free application marketplace to share with the community

---

## 📄 License

This project is licensed under the **Apache License 2.0**, see [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ If Bomiot is helpful to you, please give the project a Star!**

Made with ❤️ by [Bomiot Team](https://github.com/Bomiot)

</div>
