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
    file_path = join(current_path.parent, 'file')
    if folder == '':
        folder = 'bomiot'
    if exists(join(getcwd(), 'setup.ini')) is False:
        shutil.copy2(join(file_path, 'setup.ini'), join(getcwd()))
        config = ConfigParser()
        config.read(join(getcwd(), 'setup.ini'), encoding='utf-8')
        config.set('project', 'name', folder)
        config.set('db_name', 'name', folder)
        with open(join(getcwd(), 'setup.ini'), 'w') as setup_file:
            config.write(setup_file)
    if exists(join(getcwd(), 'pydeploy.toml')) is False:
        with open(join(file_path, 'pyproject.toml'), 'r', encoding='utf-8') as pip_file:
            deploy_pip = toml.load(pip_file)
        del deploy_pip['tool']['poetry']['scripts']
        deploy_pip['tool']['poetry']['name'] = folder
        deploy_pip['tool']['poetry']['version'] = '0.0.1'
        with open(join(getcwd(), 'pydeploy.toml'), 'w', encoding='utf-8') as user_pip_file:
            toml.dump(deploy_pip, user_pip_file)

    if exists(join(getcwd(), 'LICENSE')) is False:
        shutil.copy2(join(file_path, 'LICENSE'), join(getcwd()))

    if exists(join(getcwd(), 'README.md')) is False:
        shutil.copy2(join(file_path, 'README.md'), join(getcwd()))

    log_path = join(getcwd(), 'logs')
    exists(log_path) or makedirs(log_path)

    media_path = join(getcwd(), 'media')
    exists(media_path) or makedirs(media_path)

    deploy_path = join(getcwd(), 'deploy')
    exists(deploy_path) or makedirs(deploy_path)