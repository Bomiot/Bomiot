from django.apps import AppConfig
from django.db import connections, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.db.models.signals import post_migrate
import os
from os.path import join, exists
from time import sleep
import threading
from configparser import ConfigParser, NoOptionError, NoSectionError

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
                if os.environ.get('RUN_MAIN', 'false') == 'true':
                    fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                    from bomiot.server.server.views import init_permission
                    import bomiot.server.core.scheduler as scheduler_module
                    from bomiot.server.core.scheduler import SchedulerManager, scheduler
                    from bomiot.server.core.observer import ob
                    from bomiot.server.core.server_monitor import start_monitoring
                    from bomiot.server.server.views import init_permission
                    from bomiot.server.core.signal import bomiot_signals, bomiot_data_signals
                    from bomiot_cmd.welcome import welcome
                    from bomiot.server.core.models import JobList
                    try:
                        JobList.objects.all().delete()
                    except Exception as e:
                        pass

                    # Load system_control switches from WORKING_SPACE/setup.ini
                    _sys_ctrl_cfg = ConfigParser()
                    _sys_ctrl_cfg_path = join(settings.WORKING_SPACE, 'setup.ini')
                    _scheduler_enabled = True
                    _observer_enabled = True
                    _server_monitor_enabled = True
                    if exists(_sys_ctrl_cfg_path):
                        _sys_ctrl_cfg.read(_sys_ctrl_cfg_path, encoding='utf-8')
                        try:
                            _scheduler_enabled = _sys_ctrl_cfg.getboolean('system_control', 'scheduler', fallback=True)
                            _observer_enabled = _sys_ctrl_cfg.getboolean('system_control', 'observer', fallback=True)
                            _server_monitor_enabled = _sys_ctrl_cfg.getboolean('system_control', 'server_monitor', fallback=True)
                        except (NoSectionError, NoOptionError, ValueError):
                            pass

                    if _scheduler_enabled:
                        if scheduler_module.sm is None:
                            scheduler_module.sm = SchedulerManager(scheduler)
                        if not scheduler_module.sm.is_alive():
                            scheduler_module.sm.start()

                    if _server_monitor_enabled:
                        start_monitoring()

                    if _observer_enabled:
                        if not ob.is_alive():
                            ob.start()

                    welcome()

            except FileExistsError:
                pass
                