# Task Scheduler

## Location

`bomiot/server/core/scheduler.py`

## Overview

Uses **APScheduler** with `DjangoJobStore` for persistent scheduled tasks.

## Architecture

```python
scheduler = BackgroundScheduler(timezone=TIMEZONE, executors={
    'default': ThreadPoolExecutor(20)
})
scheduler.add_jobstore(DjangoJobStore(), 'default')

class SchedulerManager(Thread):
    def __init__(self, scheduler):
        self.scheduler = scheduler
        JobList.objects.filter().delete()  # Clear on startup
        self.scheduler.start()

    def run(self):
        self.sync_jobs(force=True)
        while not self._stop_event:
            self.sync_jobs()
            time.sleep(60)  # Check every 60 seconds
```

## JobList Model

```python
class JobList(CoreModel):
    job_id = models.CharField(max_length=255)       # Unique job ID
    module_name = models.CharField(max_length=255)   # e.g. 'greaterwms.task'
    func_name = models.CharField(max_length=255)     # e.g. 'example_job'
    trigger = models.CharField(max_length=255)       # 'cron' | 'interval' | 'date'
    description = models.TextField()
    configuration = models.TextField()              # JSON config for trigger args
    type = models.BooleanField(default=True)         # Enabled/disabled
```

## Trigger Types

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', ...],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', ...],
    'date': ['run_date', 'timezone']
}
```

## Job Execution

```python
def _update_job(self, job, force=False):
    config = json.loads(job.configuration)
    trigger_type = job.trigger  # 'cron', 'interval', or 'date'
    trigger_args = {arg: config.get(arg) for arg in ARGS_MAP[trigger_type]
                    if config.get(arg) is not None}

    module = importlib.import_module(job.module_name)
    job_func = getattr(module, job.func_name)

    self.scheduler.add_job(
        func=job_func,
        trigger=trigger_type,
        id=job.job_id,
        replace_existing=True,
        kwargs={'sender': job_func, **trigger_args}
    )
```

## Task Example

`greaterwms/task.py`:

```python
import os

def example_job(**kwargs):
    """Scheduled example job"""
    from datetime import datetime
    print(os.environ.get('AUTHED', 'false'))
    print(f"Scheduled task test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

## Job Lifecycle

```
1. Job created in JobList (type=True to enable)
2. SchedulerManager.sync_jobs() runs every 60s
3. Checks active jobs vs scheduled jobs
4. Removes jobs no longer in JobList
5. Adds new jobs from JobList
6. Deletes old executions (> 7 days)
```

## Configuration

Enabled via `setup.ini`:

```ini
[system_control]
scheduler = True
```

## Execution Cleanup

```python
def delete_old_job_executions(self, max_age=7):
    cutoff = datetime.now() - timedelta(days=max_age)
    old_executions = DjangoJobExecution.objects.filter(run_time__lt=cutoff)
    if old_executions.count() > 0:
        old_executions.delete()
```
