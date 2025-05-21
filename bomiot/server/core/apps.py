from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Core application configuration for the bomiot server.
    """
    name = 'bomiot.server.core'

    def ready(self):
        """
        init signal
        """
        from bomiot.server.core import signal