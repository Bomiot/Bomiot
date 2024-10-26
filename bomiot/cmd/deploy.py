from os.path import join, exists
from os import makedirs, getcwd, rename
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import sys


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
        if exists(join(deploy_path, str(sys.argv[2]) + '.ini')) is False:
            shutil.copy2(join(file_path, 'uwsgi.ini'), deploy_path)
            rename(join(deploy_path, 'uwsgi.ini'), join(deploy_path, str(sys.argv[2]) + '.ini'))
        config = ConfigParser()
        config.read(join(deploy_path, str(sys.argv[2]) + '.ini'))
        server_path = join(current_path.parent.parent, 'server')
        config.set('uwsgi', 'chdir', server_path)
        wsgi_path = join(server_path, 'server')
        config.set('uwsgi', 'wsgi-file', join(wsgi_path, 'wsgi.py'))
        config.set('uwsgi', 'logto', join(getcwd(), 'logs'))
        with open(join(deploy_path, str(sys.argv[2]) + '.ini'), 'w') as deploy_file:
            config.write(deploy_file)

        print(f'Deploy project {str(sys.argv[2])} workspace success')
