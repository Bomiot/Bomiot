# 定时任务

bomiot 后端基于 APScheduler 与 `django_apscheduler` 提供定时任务能力。任务定义保存在 `JobList` 表中，由后台线程 `SchedulerManager` 周期性同步到 APScheduler 实例执行。

## 1. 任务模型：JobList

`bomiot/server/core/models.py`：

```python
class JobList(CoreModel):
    job_id = models.CharField(max_length=255, verbose_name="Job ID")
    module_name = models.CharField(max_length=255, verbose_name="Module Name")
    func_name = models.CharField(max_length=255, verbose_name="Function Name")
    trigger = models.CharField(max_length=255, verbose_name="Trigger")
    description = models.TextField(default='', null=True, blank=True, verbose_name="Description")
    configuration = models.TextField(null=True, verbose_name="Configuration")
    type = models.BooleanField(default=True, verbose_name="Type")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_job'
        verbose_name = settings.BASE_DB_TABLE + ' Job'
        verbose_name_plural = verbose_name
        ordering = ['-id']
```

字段含义：
- `job_id`：APScheduler 任务 ID，全局唯一。
- `module_name`：可导入的 Python 模块路径，例如 `greaterwms.task`。
- `func_name`：模块中的函数名，例如 `example_job`。
- `trigger`：触发器类型，取值 `cron` / `interval` / `date`。
- `configuration`：JSON 字符串，键名取决于 trigger 类型。
- `type`：是否启用，`True` 才会被加载到调度器。

## 2. 调度器初始化

`bomiot/server/core/scheduler.py`：

```python
import inspect
import time
from threading import Thread, Lock
import json
import importlib

from django.conf import settings
from django.core.cache import cache
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from bomiot.server.core.models import JobList

ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}

TRIGGER_CLASSES = {
    'interval': IntervalTrigger,
    'cron': CronTrigger,
    'date': DateTrigger,
}

TIMEZONE = settings.TIME_ZONE if hasattr(settings, 'TIME_ZONE') else 'UTC'
executors = {
    'default': ThreadPoolExecutor(20),
}

scheduler = BackgroundScheduler(timezone=TIMEZONE, executors=executors)
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler_lock = Lock()
```

要点：
- 使用 `BackgroundScheduler` 后台运行，不阻塞 Django 主进程。
- `DjangoJobStore` 将任务持久化到数据库，进程重启后状态可恢复。
- `ThreadPoolExecutor(20)` 限制并发 20 个线程，避免定时任务挤占业务线程。
- `ARGS_MAP` 映射三种触发器类型支持的参数名，用于从 `JobList.configuration` 中安全提取参数。
- `TRIGGER_CLASSES` 将字符串映射到具体 Trigger 类，便于动态构造。

## 3. SchedulerManager 线程

`bomiot/server/core/scheduler.py` 的核心管理线程：

```python
class SchedulerManager(Thread):
    """
    Scheduler of Job
    """

    def __init__(self, scheduler):
        super(SchedulerManager, self).__init__()
        self.scheduler = scheduler
        self._stop_event = False
        register_events(self.scheduler)
        self.daemon = True

    def get_existing_jobs(self):
        try:
            return DjangoJob.objects.values_list('id', flat=True)
        except Exception as e:
            return []

    def get_active_jobs(self):
        try:
            return JobList.objects.filter(type=True)
        except Exception as e:
            return []

    def sync_jobs(self, force=False):
        with scheduler_lock:
            try:
                active_jobs = self.get_active_jobs()
                active_job_ids = {job.job_id for job in active_jobs}
                scheduled_job_ids = {job.id for job in self.scheduler.get_jobs()}
                for job_id in scheduled_job_ids.difference(active_job_ids):
                    try:
                        self.scheduler.remove_job(job_id)
                    except Exception as e:
                        print(f"Error removing job {job_id}: {str(e)}")
                scheduled_job_ids_res = {job.id for job in self.scheduler.get_jobs()}
                for job in active_job_ids.difference(scheduled_job_ids_res):
                    self._update_job(active_jobs.filter(job_id=job).first(), force)
                self.delete_old_job_executions()
            except Exception as e:
                print(f"Error syncing jobs: {str(e)}")

    def delete_old_job_executions(self, max_age=7):
        cutoff = datetime.now() - timedelta(days=max_age)
        old_executions = DjangoJobExecution.objects.filter(
            run_time__lt=cutoff
        )
        if old_executions.count() > 0:
            old_executions.delete()

    def _update_job(self, job, force=False):
        try:
            config = json.loads(job.configuration)
            trigger_type = job.trigger
            if trigger_type not in ARGS_MAP:
                return
            trigger_args = {
                arg: config.get(arg)
                for arg in ARGS_MAP[trigger_type]
                if config.get(arg) is not None
            }
            module = importlib.import_module(job.module_name)
            job_func = getattr(module, job.func_name)
            if not callable(job_func):
                return
            trigger_cls = TRIGGER_CLASSES[trigger_type]
            self.scheduler.add_job(
                func=job_func,
                trigger=trigger_cls(**trigger_args),
                id=job.job_id,
                replace_existing=True,
                kwargs={'sender': job_func}
            )
        except Exception as e:
            job.type = False
            job.save()

    def run(self):
        try:
            JobList.objects.filter().delete()
            self.scheduler.start()
            self.sync_jobs(force=True)
            while not self._stop_event:
                self.sync_jobs()
                time.sleep(60)
        except Exception as e:
            print(f"Scheduler manager crashed: {str(e)}")

    def stop(self):
        self._stop_event = True
        self.scheduler.shutdown()
        print("Scheduler manager stopped")


# Global scheduler manager instance (initialized lazily)
sm = None
```

## 4. 同步与执行逻辑

`SchedulerManager.run()` 启动后做的事：
1. `JobList.objects.filter().delete()`：清空 JobList（由外部逻辑重新写入任务，避免脏数据）。
2. `self.scheduler.start()`：启动 APScheduler。
3. `sync_jobs(force=True)`：首次强制全量同步。
4. 进入循环，每 60 秒 `sync_jobs()` 一次，动态发现新任务。

`sync_jobs()` 的同步策略：
- 比对 `JobList` 中启用的 `job_id` 集合与 APScheduler 中已注册的 `job.id`。
- 已注册但 `JobList` 不再启用的任务，`scheduler.remove_job(job_id)` 移除。
- `JobList` 中启用但 APScheduler 没有的任务，调用 `_update_job` 注册。
- 同步完成后调用 `delete_old_job_executions()` 清理 7 天前的执行记录。

`_update_job(job, force=False)` 的注册流程：
1. `json.loads(job.configuration)` 解析触发参数。
2. 校验 `job.trigger` 必须在 `ARGS_MAP` 中。
3. 按 `ARGS_MAP[trigger_type]` 过滤出非空参数构造 `trigger_args`。
4. `importlib.import_module(job.module_name)` 动态导入模块。
5. `getattr(module, job.func_name)` 取出函数，校验可调用。
6. `TRIGGER_CLASSES[trigger_type](**trigger_args)` 构造触发器。
7. `scheduler.add_job(func=..., trigger=..., id=job.job_id, replace_existing=True, kwargs={'sender': job_func})`。
8. 任何异常都会将 `job.type` 置为 `False` 并保存，下次循环跳过该任务，避免反复失败。

## 5. 触发器配置示例

`configuration` 字段是 JSON 字符串，按 trigger 类型键名不同：

- **interval**（间隔执行）：
  ```json
  {"minutes": 5, "seconds": 30}
  ```
  支持 `weeks/days/hours/minutes/seconds/start_date/end_date/timezone`。

- **cron**（Cron 表达式）：
  ```json
  {"day_of_week": "mon-fri", "hour": 9, "minute": 0}
  ```
  支持 `year/month/day/week/day_of_week/hour/minute/second/start_date/end_date/timezone`。

- **date**（一次性）：
  ```json
  {"run_date": "2026-12-31 23:59:59"}
  ```
  支持 `run_date/timezone`。

未在 `ARGS_MAP` 中的键会被忽略，避免触发器构造异常。

## 6. 任务函数示例

`greaterwms/task.py` 提供示例任务：

```python
import os
import requests

def example_job(**kwargs):
    """Scheduled example job"""
    from datetime import datetime
    print(os.environ.get('AUTHED', 'false'))
    print(os.environ.get('IS_LAN', 'false'))
    print(f"This is a scheduled task test ----------- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Your business logic here
```

约定：
- 任务函数必须能被 `importlib.import_module('greaterwms.task')` 找到。
- 函数签名建议使用 `**kwargs`，APScheduler 注册时通过 `kwargs={'sender': job_func}` 注入。
- 业务函数应自带异常捕获或保证快速返回，避免阻塞 20 线程的线程池。

新增任务步骤：
1. 在 `greaterwms/task.py` 或业务模块中编写函数。
2. 在 `JobList` 中插入记录（`module_name='greaterwms.task'`、`func_name='example_job'`、`trigger='interval'`、`configuration='{"seconds": 60}'`、`type=True`）。
3. 等待 `SchedulerManager` 下一次 `sync_jobs`（最长 60 秒）自动加载，或重启服务立即生效。

## 7. 启停控制：setup.ini

定时任务的启停由 `setup.ini` 控制：

```ini
[system_control]
observer = True
scheduler = True
server_monitor = True
```

只有 `[system_control] scheduler = True` 时，应用启动流程才会实例化 `SchedulerManager` 并 `start()`。设为 `False` 则完全不启动调度器，适合单机调试或前端纯静态部署场景。修改配置后需重启服务生效。

`sm` 全局实例采用懒加载（`sm = None`），由外部启动逻辑判断 `setup.ini` 配置后决定是否赋值，避免在导入阶段就启动线程。

## 8. 链路总览

```
setup.ini: [system_control] scheduler = True
   └── 应用启动 → SchedulerManager(scheduler).start()
         └── JobList.objects.filter().delete()
         └── scheduler.start() + register_events
         └── sync_jobs(force=True) 全量注册
         └── while not _stop_event:
               ├── sync_jobs() 每 60s 增量同步
               │     ├── 移除已停用任务
               │     ├── _update_job 注册新任务
               │     │     └── importlib.import_module(module_name)
               │     │     └── scheduler.add_job(func, trigger, id=job_id)
               │     └── delete_old_job_executions() 清 7 天前记录
               └── APScheduler 线程池 (20) 执行任务
                     └── greaterwms/task.example_job(**kwargs)
                           └── 业务逻辑（写日志 / 更新库存 / 拉取数据等）
```

任务执行日志由 `django_apscheduler` 写入 `DjangoJobExecution` 表，配合 `register_events(self.scheduler)` 可在 Django Admin 中查看运行历史。
