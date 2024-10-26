from os.path import join, exists, isfile, isdir
from os import makedirs, getcwd, listdir
import os
import sys
import shutil
from pathlib import Path
from .init import create_file
import pkg_resources


def copy_files(src_folder, dst_folder):
    makedirs(dst_folder, exist_ok=True)
    for item in listdir(src_folder):
        source_item = join(src_folder, item)
        destination_item = join(dst_folder, item)
        if isdir(source_item):
            copy_files(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)


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
            if sys.argv[2] in [pkg.key for pkg in pkg_resources.working_set]:
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

                shutil.copy2(join(file_path, 'config.ini'), project_path)
                shutil.copy2(join(file_path, 'bomiotconf.py'), project_path)

                create_file(str(sys.argv[2]))

                copy_files(join(current_path.parent.parent, 'templates'), join(project_path, 'templates'))

                print(f'Initialized project workspace {sys.argv[2]}')