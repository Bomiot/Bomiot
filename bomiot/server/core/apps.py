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
        from bomiot.server.core.models import API
        from bomiot.server.core import signal
        post_migrate.connect(do_init_data, sender=self)
        try:
            init_api()
        except Exception as e:
            print(f"Initial API initialization failed: {e}")
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
                from bomiot.server.core.signal import bomiot_signals
                start_monitoring()
                sm.start()
                ob.start()
                def backgrun_init():
                    init_permission()
                init_thread = threading.Thread(target=backgrun_init, daemon=True)
                init_thread.start()

                print('')
                print("  $$$$$$    $$$$$   $$$       $$$  $$   $$$$$   $$$$$$")
                print("  $$   $$  $$   $$  $$ $     $ $$  $$  $$   $$    $$")
                print("  $$$$$$$  $$   $$  $$  $   $  $$  $$  $$   $$    $$")
                print("  $$   $$  $$   $$  $$   $ $   $$  $$  $$   $$    $$")
                print("  $$$$$$    $$$$$   $$    $    $$  $$   $$$$$     $$")
                print('')

            except FileExistsError:
                pass
                
def do_init_data(sender, **kwargs):
    init_api()


def init_api():
    try:
        from bomiot.server.core.models import API
        api_check = API.objects.filter()
        if api_check.exists():
            api_check.delete()
            create_api_data()
        else:
            create_api_data()
    except Exception as e:
        print(f"Init database error: {e}")


def create_api_data():
    from django.conf import settings
    import importlib
    if settings.PROJECT_NAME == 'bomiot':
        api_path = join(settings.BASE_DIR, 'core', 'api.py')
    else:
        api_path = join(settings.WORKING_SPACE, settings.PROJECT_NAME, 'api.py')
    if not exists(api_path):
        raise FileNotFoundError(f"Can not find path: {api_path}")
    if settings.PROJECT_NAME == 'bomiot':
        module_path = 'bomiot.server.core.api'
    else:
        module_path = f'{settings.PROJECT_NAME}.api'
    try:
        api_module = importlib.import_module(module_path)
        if hasattr(api_module, 'api_return'):
            api_return_func = getattr(api_module, 'api_return')
            result = api_return_func()
        else:
            raise AttributeError(f"api.py don't find api_return function")
    except:
        pass