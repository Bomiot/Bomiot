# 信号机制

## 简介

Bomiot 通过**信号（Signal）机制**实现业务逻辑的解耦与扩展。开发者可以在不修改框架核心代码的情况下，通过信号注入自定义行为。Bomiot 提供三类信号入口，对应项目根目录下的三个文件：

| 文件 | 信号类型 | 用途 |
|------|----------|------|
| `files.py` | 文件信号 | 文件上传、下载、删除等文件操作的拦截与扩展 |
| `receiver.py` | 数据信号 | 数据 API 的接管与自定义 |
| `server.py` | 服务器信号 | 服务器生命周期、监控等事件 |

---

## 信号使用方式

通过 `bomiot_signals.send()` 发送信号，框架会自动接收并执行对应逻辑。

```python
from bomiot.server.core.signal import bomiot_signals

def my_handler(sender, **kwargs):
    print("信号触发")

# 发送信号
bomiot_signals.send(sender=my_handler, msg={
    'models': 'YourModel',
    'data': { ... }
})
```

> 信号代码通常写在应用的 `urls.py` 中，刷新 Web 页面后即生效。

---

## 数据信号（receiver.py）

用于接管数据 API，实现自定义的查询、过滤、权限等逻辑。

```python
# receiver.py
from bomiot.server.core.signal import bomiot_signals

def custom_data_handler(sender, **kwargs):
    # 自定义数据处理逻辑
    pass

bomiot_signals.send(sender=custom_data_handler, msg={
    'models': 'MyModel',
    'data': {
        'filter': {'status': 'active'},
        'ordering': '-created_time'
    }
})
```

---

## 文件信号（files.py）

用于在文件上传、下载、删除等操作前后执行自定义逻辑，例如病毒扫描、格式转换、权限校验等。

```python
# files.py
from bomiot.server.core.signal import bomiot_signals

def file_upload_handler(sender, **kwargs):
    # 文件上传后的处理逻辑
    file_path = kwargs.get('file_path')
    pass

bomiot_signals.send(sender=file_upload_handler, msg={
    'action': 'upload',
    'data': {}
})
```

---

## 服务器信号（server.py）

用于服务器启动、关闭、监控等生命周期事件。

```python
# server.py
from bomiot.server.core.signal import bomiot_signals

def server_start_handler(sender, **kwargs):
    # 服务器启动时执行
    pass

bomiot_signals.send(sender=server_start_handler, msg={
    'action': 'startup',
    'data': {}
})
```

---

## 信号与定时任务

信号也可用于注册定时任务，详见「定时任务」文档：

```python
bomiot_signals.send(sender=my_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'description': '每60秒执行一次'
    }
})
```

---

## 注意事项

- 信号发送后框架会异步处理，请勿在信号处理器中执行耗时过长的阻塞操作
- 同一模型可注册多个信号处理器，按注册顺序执行
- 开发阶段修改信号代码后，刷新 Web 页面即可重新加载
