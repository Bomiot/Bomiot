from os.path import join, exists
from os import makedirs, getcwd
import sys
import shutil
from pathlib import Path
from .create import create_file


def project(folder):
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
            makedirs(project_path)
            current_path = Path(__file__).resolve()
            file_path = join(current_path.parent, 'file')

            shutil.copy2(join(file_path, 'project_config.ini'), project_path)

            create_file(str(sys.argv[2]))

            print('Initialized project workspace %s' % sys.argv[2])
