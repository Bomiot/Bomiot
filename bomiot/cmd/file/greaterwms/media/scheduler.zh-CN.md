# 定时任务

## 支持的触发类型

Bomiot 支持三种触发器：`cron`、`interval` 和 `date`。

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}
```

| 触发器 | 说明 | 示例 |
| --- | --- | --- |
| `cron` | 按 Cron 表达式定时触发 | 每天 02:00 执行备份 |
| `interval` | 按固定间隔触发 | 每 5 分钟检查一次 |
| `date` | 在指定时间触发一次 | 2026-12-31 23:59 执行 |

---

## 定义任务函数

在工作空间的 `task.py` 中定义任务函数：

```python
def example_job(**kwargs):
    """示例定时任务"""
    from datetime import datetime
    print(f"这是一个定时任务测试 ----------- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # 在此编写您的业务逻辑
```

---

## 注册任务

在应用的 `apps.py` 的 `ready()` 方法中，通过创建 `JobList` 记录来注册任务：

```python
from django.apps import AppConfig
from bomiot.server.core.models import JobList
import json


class ExampleConfig(AppConfig):
    name = 'example'

    def ready(self):
        try:
            JobList.objects.get_or_create(
                job_id='example_job',
                defaults={
                    'module_name': 'greaterwms.task',
                    'func_name': 'example_job',
                    'trigger': 'interval',
                    'configuration': json.dumps({'minutes': 1}),
                    'description': '示例定时任务 - 每 1 分钟执行一次',
                    'type': True,
                }
            )
        except Exception:
            pass
```

### JobList 字段说明

| 字段 | 说明 |
| --- | --- |
| `job_id` | 任务的唯一标识 |
| `module_name` | 任务函数所在模块的导入路径（如 `greaterwms.task`） |
| `func_name` | `task.py` 中任务函数的名称 |
| `trigger` | 触发类型：`cron`、`interval` 或 `date` |
| `configuration` | 触发参数的 JSON 字符串（如 `{"minutes": 1}`） |
| `description` | 任务的可读描述 |
| `type` | 任务是否启用（`True` / `False`） |

---

## 触发配置示例

### interval（间隔）

```python
JobList.objects.get_or_create(
    job_id='interval_job',
    defaults={
        'module_name': 'greaterwms.task',
        'func_name': 'interval_job',
        'trigger': 'interval',
        'configuration': json.dumps({'seconds': 60, 'end_date': '2099-05-30'}),
        'description': '每 60 秒执行一次，2099-05-30 结束',
        'type': True,
    }
)
```

### cron（定时）

```python
JobList.objects.get_or_create(
    job_id='cron_job',
    defaults={
        'module_name': 'greaterwms.task',
        'func_name': 'cron_job',
        'trigger': 'cron',
        'configuration': json.dumps({'hour': 2, 'minute': 0}),
        'description': '每天 02:00 执行',
        'type': True,
    }
)
```

### date（日期）

```python
JobList.objects.get_or_create(
    job_id='date_job',
    defaults={
        'module_name': 'greaterwms.task',
        'func_name': 'date_job',
        'trigger': 'date',
        'configuration': json.dumps({'run_date': '2026-12-31 23:59:00'}),
        'description': '在 2026-12-31 23:59:00 执行一次',
        'type': True,
    }
)
```

---

## 启用调度

确保 `setup.ini` 中 `[system_control]` 的 `scheduler = True`，服务启动后调度器自动运行。

```ini
[system_control]
scheduler = True
```

`SchedulerManager` 每 60 秒扫描一次 `JobList`，加载 `type=True` 的任务，动态导入 `task.py` 中的函数，并注册到 APScheduler。

---

## 取消任务

如需禁用任务，将对应 `JobList` 记录的 `type` 设为 `False`，`SchedulerManager` 会在下一次扫描时将其从调度器中移除。

如需永久删除任务，删除 `JobList` 记录并移除 `apps.py` 中的 `get_or_create` 代码。

---

## 注意事项

- 任务持久化存储在数据库中，服务重启后自动恢复。
- SQLite 对过于频繁的定时任务可能会锁库。
- PostgreSQL 对高并发的支持更好。
- 不要在 `__init__.py` 中注册任务，请使用应用的 `ready()` 方法。
