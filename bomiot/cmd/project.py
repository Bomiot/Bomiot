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
                current_path = Path(__file__).resolve()
                file_path = join(current_path.parent, 'file')

                shutil.copy2(join(file_path, '__version__.py'), project_path)

                with open(join(project_path, '__init__.py'), "w") as f:
                    f.write("def version():\n")
                    f.write(f"    from {sys.argv[2]} import __version__\n")
                    f.write("    return __version__.version()\n")
                f.close()

                shutil.copy2(join(file_path, 'bomiotconf.ini'), project_path)
                shutil.copy2(join(file_path, 'receiver.py'), project_path)
                shutil.copy2(join(file_path, 'example.py'), project_path)
                shutil.copy2(join(file_path, 'api.py'), project_path)

                create_file(str(sys.argv[2]))

                setup_ini_path = join(getcwd(), 'setup.ini')
                if not exists(setup_ini_path):
                    shutil.copy2(join(file_path, 'setup.ini'), setup_ini_path)
                setup_config = ConfigParser()
                setup_config.read(setup_ini_path, encoding='utf-8')
                project_name = setup_config.get('project', 'name', fallback='bomiot')
                if project_name.lower() == 'bomiot':
                    setup_config.set('project', 'name', folder)
                with open(setup_ini_path, "wt", encoding='utf-8') as f:
                    setup_config.write(f)

                copy_files(join(join(current_path.parent.parent, 'server'), 'media'), join(project_path, 'media'))
                copy_files(join(join(current_path.parent.parent, 'server'), 'language'), join(project_path, 'language'))
                copy_files(join(current_path.parent.parent, 'templates'), join(project_path, 'templates'))
                
                print(f'Initialized project workspace {sys.argv[2]}')