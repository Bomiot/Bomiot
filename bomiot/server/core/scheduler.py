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
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from bomiot.server.core.models import JobList

# map the args
ARGS_MAP = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}

TIMEZONE = settings.TIME_ZONE if hasattr(settings, 'TIME_ZONE') else 'UTC'
executors = {
    'default': ThreadPoolExecutor(20),
}

scheduler = BackgroundScheduler(timezone=TIMEZONE, executors=executors)
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler_lock = Lock()

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
        JobList.objects.filter().delete()
        self.scheduler.start()
    
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
            self.scheduler.add_job(
                func=job_func,
                trigger=trigger_type,
                id=job.job_id,
                replace_existing=True,
                kwargs={'sender': job_func, **trigger_args}
            )
        except Exception as e:
            job.type = False
            job.save()

    def run(self):
        try:
            self.sync_jobs(force=True)
            # print("Scheduler manager started")
            while not self._stop_event:
                self.sync_jobs()
                time.sleep(60)                
        except Exception as e:
            print(f"Scheduler manager crashed: {str(e)}")
            
    def stop(self):
        self._stop_event = True
        self.scheduler.shutdown()
        print("Scheduler manager stopped")


# init scheduler manager
sm = SchedulerManager(scheduler)
