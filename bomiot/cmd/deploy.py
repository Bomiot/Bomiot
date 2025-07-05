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
        create_file('')
        exists(join(getcwd(), 'deploy')) or makedirs(join(getcwd(), 'deploy'))
        deploy_path = join(getcwd(), 'deploy')
        if str(sys.argv[2]) != 'bomiot':
            supervisor_path = join(deploy_path, f'{sys.argv[2]}.conf')
            if exists(supervisor_path) is False:
                with open(supervisor_path, "wt") as f:
                    f.write("")
                supervisor_config = ConfigParser()
                supervisor_config.read(supervisor_path)
                supervisor_config.add_section(f'program:{sys.argv[2]}')
                supervisor_config.set(f'program:{sys.argv[2]}', 'user', 'root')
                supervisor_config.set(f'program:{sys.argv[2]}', 'command', 'bomiot run -b 0.0.0.0 -p 8000 -w 4')
                supervisor_config.set(f'program:{sys.argv[2]}', 'autostart', 'true')
                supervisor_config.set(f'program:{sys.argv[2]}', 'autorestart', 'true')
                supervisor_config.set(f'program:{sys.argv[2]}', 'startretries', '3')
                supervisor_config.set(f'program:{sys.argv[2]}', 'exitcodes', '0,2')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stopsignal', 'TERM')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stopwaitsecs', '10')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stopasgroup', 'true')
                supervisor_config.set(f'program:{sys.argv[2]}', 'killasgroup', 'true')
                supervisor_config.set(f'program:{sys.argv[2]}', 'directory', f'{getcwd()}')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                        f'{join(getcwd(), "logs", f"{sys.argv[2]}_access.log")}')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stderr_logfile',
                        f'{join(getcwd(), "logs", f"{sys.argv[2]}_error.log")}')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile_maxbytes', '20MB')
                supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile_backups', '10')

                supervisor_config.write(open(supervisor_path, "wt"))


        print(f'Deploy project {str(sys.argv[2])} workspace success')
