# Scheduled Tasks


## Supported Scheduled Tasks

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date','timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}
```

---

## Writing Scheduled Tasks
```python

from bomiot.server.core.signal import bomiot_signals

def my_scheduled_task(sender, **kwargs):
    print("Executing scheduled task")

bomiot_signals.send(sender=my_scheduled_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'end_date': '2099-05-30',
        'description': 'Executes every 60 seconds, ending on May 30, 2099'
    }
})
```

`Note:`

- Do not write this code in `__init__.py`, `admin.py`, or `apps.py`, as it requires Django to be fully loaded before it can take effect.

- Send signals to **Bomiot** from any location; typically, this is done in `urls.py`. The task will become active upon refreshing the web page.

---

## Cancelling Scheduled Tasks

- To cancel a scheduled task, simply comment out or delete the task code you've written. **Bomiot** will automatically add tasks to the task queue when the program starts.

---

## Customization

- If you need to control **Bomiot**'s scheduled tasks without restarting the program, you only need to manage the JobList within your models.

- **Bomiot** scans the scheduled task list every 60 seconds.

`Note:`

- SQLite may lock the database for overly frequent scheduled tasks.
- PostgreSQL offers better support for high concurrency.