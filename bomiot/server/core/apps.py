from django.apps import AppConfig
from .signal import bomiot_signals


class CoreConfig(AppConfig):
    name = 'bomiot.server.core'
