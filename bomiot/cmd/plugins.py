from os.path import join, exists
from os import makedirs, getcwd
import sys
import shutil
from pathlib import Path
from .create import create_file

def plugins(folder):
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

            shutil.copy2(join(file_path, 'plugins_config.ini'), plugins_path)

            create_file(str(sys.argv[2]))

            print('Initialized plugins workspace %s' % sys.argv[2])
