# 定时任务

## 支持的定时任务

```python
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date','timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}
```

---

## 定时任务编写

```python
from bomiot.server.core.signal import bomiot_signals

def my_scheduled_task(sender, **kwargs):
    print("执行定时任务")

bomiot_signals.send(sender=my_scheduled_task, msg={
    'models': 'JobList',
    'data': {
        'trigger': 'interval',
        'seconds': 60,
        'end_date': '2099-05-30',
        'description': '每60秒执行一次，2099年5月30日结束'
    }
})
```
    
`注意:`

- 不要写在`__init__.py`, `admin.py`, `apps.py`里面，因为需要Django完全加载完成，才会生效
- 任意位置给bomiot发送信号，一般是写在`urls.py`里面，刷新web端页面即生效

---

## 取消定时任务

- 直接注释，或者删除掉编写的定时任务代码，**Bomiot** 会在程序启动的时候，自动加入到任务队列中

---

## 自定义

- 如果需要不重启程序的情况下，控制 **Bomiot** 的定时任务
- 仅需要控制models中的JobList即可
- **Bomiot** 会每60秒扫描一次定时任务列表

`注意:`

- Sqlite对过于频繁的定时任务，会锁数据库
- PostgreSQL对高并发的支持更好