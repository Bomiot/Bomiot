import inspect
import time
from threading import Thread
import json
import importlib
from django.dispatch import receiver
from bomiot.server.core.signal import bomiot_job_signals
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from bomiot.server.core.models import JobList


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


# map the args
args_map = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date',
             'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}


@receiver(bomiot_job_signals)
def sm_send_success_signal_handler(sender, **kwargs):
    model_data = kwargs.get('msg', '').get('models', '')
    if model_data == 'JobList':
        job_id = f"{inspect.getmodule(sender).__name__}-{sender.__name__}"
        data = kwargs.get('msg', '').get('data', '')
        if JobList.objects.filter(job_id=job_id).exists():
            job_detail = JobList.objects.get(job_id=job_id)
            job_detail.trigger = data.get('trigger')
            job_detail.description = data.get('description', '')
            job_detail.configuration = json.dumps(data)
            job_detail.save()
        else:
            JobList.objects.create(job_id=job_id,
                                   module_name=inspect.getmodule(sender).__name__,
                                   func_name=sender.__name__,
                                   trigger=data.get('trigger'),
                                   description=data.get('description', ''),
                                   configuration=json.dumps(data)
                                   )


class SchedulerManager(Thread):
    """
    Scheduler of Job
    """

    def __init__(self, scheduler):
        """
        init manager
        :param scheduler:
        """
        super(SchedulerManager, self).__init__()
        self.scheduler = scheduler
        register_events(self.scheduler)
        self.setDaemon(True)
        self.scheduler.start()

    def existed_jobs(self):
        """
        get existed jobs stored in db
        :return:
        """
        jobs = DjangoJob.objects.all()
        return jobs

    def realtime_jobs(self):
        """
        get real-time jobs from db
        :return:
        """
        jobs = JobList.objects.filter(type=True)
        return jobs

    def realtime_job_id(self):
        """
        get real-time jobs
        :return:
        """
        jobs = self.realtime_jobs()
        for job in jobs:
            yield job.job_id

    def sync_jobs(self, force=False):
        """
        sync jobs
        :return:
        """
        jobs = self.realtime_jobs()
        for job in jobs:
            # add new jobs or modify existed jobs
            self._add_or_modify_new_jobs(job, force)
            # remove deleted jobs
            self._remove_deprecated_jobs(job, force)


    def _remove_deprecated_jobs(self, job, force=False):
        """
        remove jobs
        :return:
        """
        if not job.type and not force:
            return
        # check extra jobs which does not belong to task
        try:
            existed_jobs = self.existed_jobs()
            existed_job_ids = list(map(lambda obj: obj.id, existed_jobs))
            realtime_job_ids = list(self.realtime_job_id())
            deprecated_job_ids = [
                job_id for job_id in existed_job_ids if not job_id in realtime_job_ids]
            if deprecated_job_ids:
                # remove deprecated jobs
                for job_id in deprecated_job_ids:
                    self.scheduler.remove_job(job_id)
        except:
            pass

    def _add_or_modify_new_jobs(self, job, force=False):
        """
        add new jobs or modify existed jobs
        :return:
        """
        if not job.type and not force:
            return

        # get job id
        job_id = job.job_id
        # add job_id to array
        configuration = json.loads(job.configuration)
        trigger = job.trigger
        configuration = {arg: configuration.get(arg) for arg in args_map.get(trigger) if
                         configuration.get(arg)}
        try:
            job_func = importlib.import_module(f'{job.module_name}')
            job_function = getattr(job_func, job.func_name)
            # if job doesn't exist, add it. otherwise replace it
            self.scheduler.add_job(job_function, job.trigger, id=job_id, replace_existing=True, **configuration)
        except:
            JobList.objects.filter(job_id=job.job_id).delete()

    def run(self):
        """
        heart beat detect
        :return:
        """
        self.sync_jobs(force=True)
        while True:
            self.sync_jobs()
            time.sleep(3)


# init scheduler manager
sm = SchedulerManager(scheduler)
