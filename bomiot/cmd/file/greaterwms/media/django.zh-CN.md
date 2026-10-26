# Django 后端

## 简介

Bomiot 使用 **Django** 作为后端框架。Django 是一个高级的 Python Web 框架，以"快速开发"和"干净、务实的设计"著称，自带 ORM、后台管理、认证、安全等一系列开箱即用的能力，被广泛用于需要快速交付且不容妥协的项目。

### 核心特性

- **电池齐全**：ORM、模板引擎、表单处理、用户认证、管理后台、国际化、安全防护全部内置，不需要东拼西凑
- **MTV 架构**：Model（数据）— Template（呈现）— View（逻辑）分层清晰，业务代码各归其位
- **强大的 ORM**：用 Python 类定义数据模型，自动映射到数据库表，支持 SQLite / MySQL / PostgreSQL / Oracle
- **自动管理后台**：基于模型零代码生成完整的数据管理界面
- **安全性**：默认防护 SQL 注入、XSS、CSRF、点击劫持等常见攻击
- **可扩展**：从原型到百万级访问量的产品，都有成熟的扩展路径

---

## 在 Bomiot 中使用

### 创建项目

```shell
bomiot project <project_name>
```

### 创建应用

```shell
bomiot app <app_name>
```

### 数据库迁移

```shell
# 生成迁移文件
bomiot makemigrations

# 执行迁移
bomiot migrate

# 加载初始数据
bomiot loaddata <source>

# 导出数据
bomiot dumpdata [appname]
```

---

## 项目结构

```
your-project/                 # 项目目录
├── <app_name>/               # Django 应用
│   ├── migrations/           # 数据库迁移
│   ├── __init__.py
│   ├── admin.py              # 后台注册
│   ├── apps.py               # 应用配置
│   ├── models.py             # 数据模型
│   ├── serializers.py        # 序列化器
│   ├── urls.py               # URL 路由
│   └── views.py              # API 视图
├── language/                 # 多语言文件
├── media/                    # 静态文件
├── bomiotconf.ini            # 项目标识
├── receiver.py               # 数据接管
├── server.py                 # 服务器监控
└── files.py                  # 文件监控
setup.ini                     # 全局配置
```

---

## 定义模型

Bomiot 提供 `CoreModel` 基类，包含通用字段（`id`、`created_time`、`updated_time`、`is_delete`）。

```python
from bomiot.server.core.models import CoreModel

class Goods(CoreModel):
    # 所有业务数据存储在单个 JSONField 中，保持前后端一致
    data = models.JSONField(default=dict)
```

> 💡 `data` JSONField 允许前端发送任意 JSON，后端直接存储，无需逐字段映射。详见 数据结构。

如果需要传统的逐字段建模，同样可以直接使用 Django 模型的全部能力（字段类型、索引、约束、关联关系等）。

---

## URL 路由

在 `urls.py` 中定义路由，`name` 用于权限控制：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('goods/', views.goods, name="Goods"),
]
```

- 指定 `name` 的接口受 Bomiot 权限系统保护。
- 省略 `name` 的接口为公开接口（无权限校验）。

详见 权限控制。

---

## API 视图

每个视图函数接收 `data` 字典，包含请求、查询参数和载荷。

```python
from bomiot.server.core.message import msg_message_return

def goods(request, data):
    # data 包含：request、query_params、data（POST body）
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success")
```

---

## 数据接管

自定义业务逻辑时，在 `receiver.py` 中接管 API 而非修改视图。

详见 数据接管。

---

## 信号机制

Bomiot 信号系统（`bomiot_signals`、`bomiot_data_signals`）支持组件间实时通信：

```python
from bomiot.server.core.signal import bomiot_signals

# 发送信号
bomiot_signals.send(sender=my_func, msg={'key': 'value'})
```

- **热更新**：信号处理器立即生效，无需重启服务器。
- **实时性**：文件变更、数据更新、服务器指标均通过信号广播。

---

## 多数据库支持

支持 SQLite（默认）、MySQL、PostgreSQL、Oracle，在 `setup.ini` 中配置：

```ini
[database]
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port
```

详见 SQLite、MySQL、PostgreSQL、Oracle。
