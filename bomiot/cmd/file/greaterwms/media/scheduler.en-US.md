# Scheduled Tasks

## Supported Trigger Types

Bomiot supports three types of triggers: `cron`, `interval`, and `date`.

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}
```

| Trigger | Description | Example |
| --- | --- | --- |
| `cron` | Run on a Cron schedule | Execute backup every day at 02:00 |
| `interval` | Run at a fixed interval | Check every 5 minutes |
| `date` | Run once at a specified time | Execute at 2026-12-31 23:59 |

---

## Define the Task Function

Define your task function in the workspace `task.py`:

```python
def example_job(**kwargs):
    """Example scheduled task"""
    from datetime import datetime
    print(f"This is a scheduled task test ----------- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Your business logic here
```

---

## Register the Task

Register the task in your app's `apps.py` `ready()` method by creating a `JobList` record:

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
                    'description': 'Example scheduled task - Executed once every 1 minute',
                    'type': True,
                }
            )
        except Exception:
            pass
```

### JobList Fields

| Field | Description |
| --- | --- |
| `job_id` | Unique identifier for the task |
| `module_name` | Import path of the module containing the task function (e.g. `greaterwms.task`) |
| `func_name` | Name of the task function in `task.py` |
| `trigger` | Trigger type: `cron`, `interval`, or `date` |
| `configuration` | JSON string of trigger parameters (e.g. `{"minutes": 1}`) |
| `description` | Human-readable description of the task |
| `type` | Whether the task is enabled (`True` / `False`) |

---

## Trigger Configuration Examples

### interval

```python
JobList.objects.get_or_create(
    job_id='interval_job',
    defaults={
        'module_name': 'greaterwms.task',
        'func_name': 'interval_job',
        'trigger': 'interval',
        'configuration': json.dumps({'seconds': 60, 'end_date': '2099-05-30'}),
        'description': 'Run every 60 seconds, ending on 2099-05-30',
        'type': True,
    }
)
```

### cron

```python
JobList.objects.get_or_create(
    job_id='cron_job',
    defaults={
        'module_name': 'greaterwms.task',
        'func_name': 'cron_job',
        'trigger': 'cron',
        'configuration': json.dumps({'hour': 2, 'minute': 0}),
        'description': 'Run every day at 02:00',
        'type': True,
    }
)
```

### date

```python
JobList.objects.get_or_create(
    job_id='date_job',
    defaults={
        'module_name': 'greaterwms.task',
        'func_name': 'date_job',
        'trigger': 'date',
        'configuration': json.dumps({'run_date': '2026-12-31 23:59:00'}),
        'description': 'Run once at 2026-12-31 23:59:00',
        'type': True,
    }
)
```

---

## Enable the Scheduler

Make sure `scheduler = True` under `[system_control]` in `setup.ini`. The scheduler starts automatically when the service launches.

```ini
[system_control]
scheduler = True
```

The `SchedulerManager` scans the `JobList` every 60 seconds, loads tasks where `type=True`, dynamically imports the function from `task.py`, and registers it with APScheduler.

---

## Cancelling a Task

To disable a task, set `type=False` on the corresponding `JobList` record. The `SchedulerManager` will remove it from the scheduler on the next scan.

To permanently delete a task, remove the `JobList` record and the `get_or_create` code from `apps.py`.

---

## Notes

- Tasks are persisted in the database and automatically restored after a restart.
- SQLite may lock the database for overly frequent scheduled tasks.
- PostgreSQL offers better support for high concurrency.
- Do not put task registration in `__init__.py`; use the app's `ready()` method instead.
