from os.path import join, exists
from os import makedirs, getcwd, rename
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import sys
import os
import importlib.resources

def deploy(folder: str):
    """
    deploy project
    :param folder:
    :return:
    """

    if len(sys.argv) < 3:
        print('Please enter your deploy project name')
    else:
        current_path = Path(__file__).resolve()
        file_path = join(current_path.parent, 'file')
        create_file('')
        exists(join(getcwd(), 'deploy')) or makedirs(join(getcwd(), 'deploy'))
        deploy_path = join(getcwd(), 'deploy')
        supervisor_path = join(deploy_path, 'supervisor.conf')
        exists(supervisor_path) or os.makedirs(supervisor_path)

        if exists(supervisor_path) is False:
            shutil.copy2(join(file_path, 'supervisor.conf'), supervisor_path)
        supervisor_config = ConfigParser()
        supervisor_config.read(supervisor_path)
        if str(sys.argv[2]) != 'bomiot':
            supervisor_config.add_section(f'program:{sys.argv[2]}')
            supervisor_config.set(f'program:{sys.argv[2]}', 'user', 'root')
            supervisor_config.set(f'program:{sys.argv[2]}', 'command', f'python3 {join(deploy_path, "startpid.py")}')
            supervisor_config.set(f'program:{sys.argv[2]}', 'autostart', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'autorestart', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'startsecs', '0')
            supervisor_config.set(f'program:{sys.argv[2]}', 'stopwaitsecs', '0')
            supervisor_config.set(f'program:{sys.argv[2]}', 'redirect_stderr', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'stopscript_timeout', '30')
            supervisor_config.set(f'program:{sys.argv[2]}', 'directory', f'{getcwd()}')
            supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                    f'{join(getcwd(), "logs", f"{sys.argv[2]}_access.log")}')
            supervisor_config.set(f'program:{sys.argv[2]}', 'stderr_logfile',
                    f'{join(getcwd(), "logs", f"{sys.argv[2]}_error.log")}')
            
            stoppid_path = importlib.resources.files('bomiot_process').joinpath('stoppid.py')
            supervisor_config.add_section(f'eventlistener:{sys.argv[2]}_stoppid')
            supervisor_config.set('eventlistener:run_stoppid', 'command', f'python3 {stoppid_path}')
            supervisor_config.set('eventlistener:run_stoppid', 'events', 'PROCESS_STATE_STOPPED,PROCESS_STATE_EXITED,PROCESS_STATE_FATAL')
            supervisor_config.set('eventlistener:run_stoppid', 'autostart', 'true')
            supervisor_config.set('eventlistener:run_stoppid', 'autorestart', 'true')

            supervisor_config.write(open(supervisor_path, "wt"))


        print(f'Deploy project {str(sys.argv[2])} workspace success')
