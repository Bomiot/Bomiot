from os.path import join, exists
from os import makedirs, getcwd
import shutil
from pathlib import Path
import toml
from configparser import ConfigParser


def create_file(folder: str):
    """
    create file
    :return:
    """
    current_path = Path(__file__).resolve()
    working_space = join(getcwd())
    file_path = join(current_path.parent, 'file')
    if folder == '':
        folder = 'bomiot'
    if exists(join(working_space, 'setup.ini')) is False:
        shutil.copy2(join(file_path, 'setup.ini'), working_space)
        config = ConfigParser()
        config.read(join(working_space, 'setup.ini'), encoding='utf-8')
        config.set('project', 'name', folder)
        config.set('db_name', 'name', folder)
        with open(join(working_space, 'setup.ini'), 'w') as setup_file:
            config.write(setup_file)
    if exists(join(working_space, 'pydeploy.toml')) is False:
        with open(join(file_path, 'pyproject.toml'), 'r', encoding='utf-8') as pip_file:
            deploy_pip = toml.load(pip_file)
        del deploy_pip['tool']['poetry']['scripts']
        deploy_pip['tool']['poetry']['name'] = folder
        deploy_pip['tool']['poetry']['version'] = '0.0.1'
        with open(join(working_space, 'pydeploy.toml'), 'w', encoding='utf-8') as user_pip_file:
            toml.dump(deploy_pip, user_pip_file)

    if exists(join(working_space, '.gitignore')) is False:
        shutil.copy2(join(file_path, '.gitignore'), working_space)

    if exists(join(working_space, 'LICENSE')) is False:
        shutil.copy2(join(file_path, 'LICENSE'), working_space)

    if exists(join(working_space, 'README.md')) is False:
        shutil.copy2(join(file_path, 'README.md'), working_space)

    log_path = join(working_space, 'logs')
    exists(log_path) or makedirs(log_path)

    media_path = join(working_space, 'media')
    exists(media_path) or makedirs(media_path)

    deploy_path = join(working_space, 'deploy')
    exists(deploy_path) or makedirs(deploy_path)

    working_path = join(join(current_path.parent.parent, 'server'), 'workspace.ini')
    working_path_config = ConfigParser()
    working_path_config.read(working_path, encoding='utf-8')
    working_path_config.set('space', 'name', working_space)
    with open(working_path, 'w') as working_file:
        working_path_config.write(working_file)

    print("Welcome to bomiot")