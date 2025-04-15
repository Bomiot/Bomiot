from os.path import join, exists
from os import makedirs, getcwd, rename
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import sys
import os


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
        supervisor_path = join(deploy_path, 'supervisor')
        exists(supervisor_path) or os.makedirs(supervisor_path)

        if exists(join(supervisor_path, str(sys.argv[2]) + '.ini')) is False:
            shutil.copy2(join(file_path, 'supervisor.conf'), supervisor_path)
            if exists(join(supervisor_path, str(sys.argv[2]) + '.conf')):
                os.remove(join(supervisor_path, str(sys.argv[2]) + '.conf'))
            rename(join(supervisor_path, 'supervisor.conf'), join(supervisor_path, str(sys.argv[2]) + '.conf'))
        supervisor_config = ConfigParser()
        supervisor_config.read(join(supervisor_path, str(sys.argv[2]) + '.conf'))
        if str(sys.argv[2]) != 'bomiot':
            supervisor_config.add_section(f'program:{sys.argv[2]}')
            supervisor_config.set(f'program:{sys.argv[2]}', 'user', 'root')
            supervisor_config.set(f'program:{sys.argv[2]}', 'command', 'daphne -b 0.0.0.0 -p 8008 bomiot.server.server.asgi:application')
            supervisor_config.set(f'program:{sys.argv[2]}', 'autostart', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'autorestart', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'startsecs', '0')
            supervisor_config.set(f'program:{sys.argv[2]}', 'stopwaitsecs', '0')
            supervisor_config.set(f'program:{sys.argv[2]}', 'redirect_stderr', 'true')
        supervisor_config.set(f'program:{sys.argv[2]}', 'directory', f'{getcwd()}')
        supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                   f'{join(join(getcwd(), "logs"), "bomiot_supervisor_access.log")}')
        supervisor_config.set(f'program:{sys.argv[2]}', 'stderr_logfile',
                   f'{join(join(getcwd(), "logs"), "bomiot_supervisor_err.log")}')
        supervisor_config.remove_section('program:bomiot')
        supervisor_config.write(open(join(supervisor_path, str(sys.argv[2]) + '.conf'), "wt"))


        print(f'Deploy project {str(sys.argv[2])} workspace success')
