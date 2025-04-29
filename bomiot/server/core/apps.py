from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'bomiot.server.core'

    def ready(self):
        import bomiot.server.core.signal
