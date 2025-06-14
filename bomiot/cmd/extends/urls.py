from django.urls import path, re_path
from . import views
from bomiot.server.core.signals import bomiot_job_signals

urlpatterns = [
]

# Schedule Job
args_map = {
    'cron': ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date',
             'timezone'],
    'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone'],
    'date': ['run_date', 'timezone']
}

# def example_job():
#     """
#     Example job function
#     """
#     print("This is an example job.")

# def example_schedule_job():
#     """
#     Example schedule job function
#     """
#     print("This is an example schedule job.")

# bomiot_job_signals(sender=example_job, msg={
#     "models": "Function"
# })

# bomiot_job_signals(sender=example_schedule_job, msg={
#     "models": "JobList",
#     "data": {
#         "trigger": "interval",
#         "seconds": 3
#     }
# })