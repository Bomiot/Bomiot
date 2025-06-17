from os.path import join, exists
from os import makedirs, getcwd
import os
import sys
import shutil
from pathlib import Path
from .init import create_file
import importlib.metadata
from configparser import ConfigParser
from .copyfile import copy_files


def project(folder: str):
    """
    project workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your project name')
    else:
        project_path = join(getcwd(), sys.argv[2])
        if exists(project_path):
            print('Project directory already exists')
        else:
            if sys.argv[2] in [dist.metadata['Name'] for dist in importlib.metadata.distributions()]:
                print('Project directory already exists')
            else:
                makedirs(project_path)
                static_path = join(project_path, 'static')
                exists(static_path) or os.makedirs(static_path)
                current_path = Path(__file__).resolve()
                file_path = join(current_path.parent, 'file')

                shutil.copy2(join(file_path, '__version__.py'), project_path)

                with open(join(project_path, '__init__.py'), "w") as f:
                    f.write("def version():\n")
                    f.write(f"    from {sys.argv[2]} import __version__\n")
                    f.write("    return __version__.version()\n")
                f.close()

                shutil.copy2(join(file_path, 'bomiotconf.ini'), project_path)
                shutil.copy2(join(file_path, 'websocket.py'), project_path)
                shutil.copy2(join(file_path, 'receiver.py'), project_path)
                shutil.copy2(join(file_path, 'files.py'), project_path)
                shutil.copy2(join(file_path, 'server.py'), project_path)

                create_file(str(sys.argv[2]))

                setup_config = ConfigParser()
                setup_config.read(join(join(getcwd()), 'setup.ini'), encoding='utf-8')
                setup_config.set('project', 'name', folder)
                setup_config.write(open(join(join(getcwd()), 'setup.ini'), "wt"))

                copy_files(join(join(current_path.parent.parent, 'server'), 'media'), join(project_path, 'media'))
                copy_files(join(join(current_path.parent.parent, 'server'), 'language'), join(project_path, 'language'))
                copy_files(join(current_path.parent.parent, 'templates'), join(project_path, 'templates'))
                
                print(f'Initialized project workspace {sys.argv[2]}')