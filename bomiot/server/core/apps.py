from django.apps import AppConfig
from django.db import connections, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.db.models.signals import post_migrate
import os
from os.path import join, exists
from time import sleep
import threading

class CoreConfig(AppConfig):
    """
    Core application configuration for the bomiot server.
    """
    name = 'bomiot.server.core'

    def ready(self):
        from django.conf import settings
        from bomiot.server.core import signal
        workers = int(os.environ.get('WORKERS', 0))
        if workers > 0:
            lockfile = f"{join(settings.WORKING_SPACE, 'bomiot_ready.lock')}"
            try:
                fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                from bomiot.server.server.views import init_permission
                from bomiot.server.core.scheduler import sm
                from bomiot.server.core.observer import ob
                from bomiot.server.core.server_monitor import start_monitoring
                from bomiot.server.server.views import init_permission
                from bomiot.server.core.signal import bomiot_signals, bomiot_data_signals
                start_monitoring()
                sm.start()
                ob.start()
                # def backgrun_init():
                #     init_permission()
                # init_thread = threading.Thread(target=backgrun_init, daemon=True)
                # init_thread.start()

                print('')
                print("  $$$$$$    $$$$$   $$$       $$$  $$   $$$$$   $$$$$$")
                print("  $$   $$  $$   $$  $$ $     $ $$  $$  $$   $$    $$")
                print("  $$$$$$$  $$   $$  $$  $   $  $$  $$  $$   $$    $$")
                print("  $$   $$  $$   $$  $$   $ $   $$  $$  $$   $$    $$")
                print("  $$$$$$    $$$$$   $$    $    $$  $$   $$$$$     $$")
                print('')

            except FileExistsError:
                pass
                