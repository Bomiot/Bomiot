# Django 后端

## 简介

Bomiot 使用 **Django** 作为企业级后端框架。

---

## 创建项目

```shell
bomiot project <project_name>
```

## 创建 Django 应用

```shell
bomiot new <app_name>
```

之后即可在该应用中编写 Django 代码。也可以使用标准 Django 命令：

```shell
# 生成迁移文件
bomiot makemigrations

# 执行迁移
bomiot migrate
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

> 💡 `data` JSONField 允许前端发送任意 JSON，后端直接存储，无需逐字段映射。详见 [数据结构](structure)。

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

详见 [权限控制](permission)。

---

## API 视图

Bomiot 使用 DRF 风格视图。每个视图函数接收 `data` 字典，包含请求、查询参数和载荷。

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

详见 [数据接管](data)。

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

## 数据库迁移

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

## 多数据库支持

Bomiot 支持 SQLite（默认）、MySQL、PostgreSQL、Oracle。在 `setup.ini` 中配置：

```ini
[database]
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port
```

详见 [SQLite](sqlite)、[MySQL](mysql)、[PostgreSQL](postgresql)。

---

## 参考资料

- [Django 官方文档](https://docs.djangoproject.com/zh-hans/4.2/)
- [Django GitHub](https://github.com/django/django)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

更多高级用法，请参考官方文档或社区资源。
