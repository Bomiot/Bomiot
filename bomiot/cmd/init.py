from os.path import join, exists
from os import makedirs, getcwd
import shutil
from pathlib import Path
from tomlkit import parse, dumps
from configparser import ConfigParser
from .create_key import auth_key_get

def create_file(folder: str):
    """
    create file
    :return:
    """
    current_path = Path(__file__).resolve()
    working_space = join(getcwd())
    file_path = join(current_path.parent, 'file')
    if folder != '':
        shutil.copy2(join(file_path, 'setup.ini'), working_space)
        setup_config = ConfigParser()
        setup_config.read(join(working_space, 'setup.ini'), encoding='utf-8')
        setup_config.set('project', 'name', folder)
        setup_config.write(open(join(working_space, 'setup.ini'), "wt"))
    if exists(join(working_space, 'pyproject.toml')) is False:
        if folder != '':
            with open(join(file_path, 'pyproject.toml'), 'r', encoding='utf-8') as pip_file:
                deploy_pip = parse(pip_file.read())
            deploy_pip['tool']['poetry']['name'] = folder
            deploy_pip['tool']['poetry']['version'] = '0.0.1'
            with open(join(working_space, 'pyproject.toml'), 'w', encoding='utf-8') as user_pip_file:
                user_pip_file.write(dumps(deploy_pip))
    auth_key_get()
    if exists(join(working_space, '.gitignore')) is False:
        shutil.copy2(join(file_path, '.gitignore'), working_space)

    if exists(join(working_space, 'LICENSE')) is False:
        shutil.copy2(join(file_path, 'LICENSE'), working_space)

    log_path = join(working_space, 'logs')
    exists(log_path) or makedirs(log_path)

    deploy_path = join(working_space, 'deploy')
    exists(deploy_path) or makedirs(deploy_path)

    working_config = ConfigParser()
    working_path = join(join(current_path.parent.parent, 'server'), 'workspace.ini')
    working_config.read(working_path, encoding='utf-8')
    working_config.set('space', 'name', working_space)
    working_config.write(open(working_path, "wt"))

    print('')
    print("  $$$$$$    $$$$$   $$$       $$$  $$   $$$$$   $$$$$$")
    print("  $$   $$  $$   $$  $$ $     $ $$  $$  $$   $$    $$")
    print("  $$$$$$$  $$   $$  $$  $   $  $$  $$  $$   $$    $$")
    print("  $$   $$  $$   $$  $$   $ $   $$  $$  $$   $$    $$")
    print("  $$$$$$    $$$$$   $$    $    $$  $$   $$$$$     $$")
    print('')