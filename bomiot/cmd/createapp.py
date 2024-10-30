from os.path import join, exists
from os import makedirs, getcwd
import os
import sys
from pathlib import Path
from configparser import ConfigParser
from .copyfile import copy_files
from .changeapps import create_project_apps_py


def new_app(folder: str):
    """
    new app for project
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your app name')
    else:
        if sys.argv[2] == 'bomiot':
            print('Invalid app name. Please enter a valid app name.')
        else:
            current_path = Path(__file__).resolve()
            setup_path = join(getcwd(), 'setup.ini')
            app_config = ConfigParser()
            app_config.read(setup_path, encoding='utf-8')
            project_name = app_config.get('project', 'name')
            project_path = join(getcwd(), project_name)
            project_config = ConfigParser()
            project_config.read(join(project_path, 'bomiotconf.ini'), encoding='utf-8')
            if project_config.get('mode', 'name') == 'project':
                app_path = join(project_path, sys.argv[2])
                if exists(app_path):
                    print('App directory already exists')
                else:
                    makedirs(app_path)

                    copy_files(join(current_path.parent, 'extends'), app_path)

                    apps_path = join(app_path, 'apps.py')
                    os.remove(apps_path)
                    create_project_apps_py(apps_path, project_name, sys.argv[2])

                    print(f'Create APP success {sys.argv[2]}')
            else:
                print('Invalid project mode. Please create a new project or switch to project mode.')
