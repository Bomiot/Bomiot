from os.path import join, exists
from os import makedirs, getcwd
import os
import sys
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import importlib.metadata
from .copyfile import copy_files
from .changeapps import create_plugins_apps_py


def plugins(folder: str):
    """
    plugins workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your plugins name')
    else:
        plugins_path = join(getcwd(), sys.argv[2])
        if exists(plugins_path):
            print('Plugins directory already exists')
        else:
            if sys.argv[2] in [dist.metadata['Name'] for dist in importlib.metadata.distributions()]:
                print('Plugins directory already exists')
            else:
                os.makedirs(plugins_path)
                current_path = Path(__file__).resolve()
                file_path = join(current_path.parent, 'file')

                shutil.copy2(join(file_path, '__version__.py'), plugins_path)

                with open(join(plugins_path, '__init__.py'), "w") as f:
                    f.write("def version():\n")
                    f.write(f"    from {sys.argv[2]} import __version__\n")
                    f.write("    return __version__.version()\n")
                f.close()

                shutil.copy2(join(file_path, 'bomiotconf.ini'), plugins_path)

                plugins_config = ConfigParser()
                plugins_config.read(join(plugins_path, 'bomiotconf.ini'), encoding='utf-8')
                plugins_config.set('mode', 'name', 'plugins')
                plugins_config.write(open(join(plugins_path, 'bomiotconf.ini'), 'wt'))

                create_file('')

                copy_files(join(current_path.parent, 'extends'), plugins_path)

                apps_path = join(plugins_path, 'apps.py')
                os.remove(apps_path)
                create_plugins_apps_py(apps_path, sys.argv[2])

                print(f'Initialized plugins workspace {sys.argv[2]}')
