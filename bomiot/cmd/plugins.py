from os.path import join, exists
from os import makedirs, getcwd
import sys
import shutil
from pathlib import Path
from .create import create_file
from configparser import ConfigParser


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
            makedirs(plugins_path)
            current_path = Path(__file__).resolve()
            file_path = join(current_path.parent, 'file')

            shutil.copy2(join(file_path, 'config.ini'), plugins_path)
            shutil.copy2(join(file_path, 'bomiotconf.py'), plugins_path)

            config = ConfigParser()
            config.read(join(plugins_path, 'config.ini'), encoding='utf-8')
            config.set('mode', 'name', 'plugins')
            with open(join(plugins_path, 'config.ini'), 'w') as config_file:
                config.write(config_file)

            create_file('')

            print('Initialized plugins workspace %s' % sys.argv[2])
