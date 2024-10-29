from django.apps import AppConfig
from django.core.signals import request_finished

class CoreConfig(AppConfig):
    name = 'bomiot.server.core'

#     def ready(self):
#         request_finished.connect(do_init_data, sender=self)
#
# def do_init_data(sender, **kwargs):
#     init_category()
#
# def init_category():
#     """
#         :return:None
#     """
