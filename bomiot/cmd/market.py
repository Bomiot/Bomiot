from os.path import join, exists, isfile, isdir
from os import makedirs, getcwd, listdir
import os
import sys
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
from .copyfile import copy_files
from bomiot.server.server.pkgcheck import pkg_check, cwd_check, ignore_pkg, ignore_cwd
import importlib.util
import subprocess


def copy_project(folder: str):
    """
    marketplace
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
            pip_command = "pip3" if sys.version_info.major == 3 else "pip"
            try:
                subprocess.run([pip_command, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FileNotFoundError:
                pip_command = "pip"
                try:
                    subprocess.run([pip_command, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except FileNotFoundError:
                    sys.exit(1)
            try:
                subprocess.run([pip_command, "install", sys.argv[2]], check=True)
                module_path = importlib.util.find_spec(sys.argv[2]).origin
                list_module_path = Path(module_path).resolve().parent
                pkg_config_check = ConfigParser()
                pkg_config_check.read(join(list_module_path, 'bomiotconf.ini'), encoding='utf-8')
                app_mode = pkg_config_check.get('mode', 'name', fallback='plugins')
                if app_mode == 'project':
                    copy_files(list_module_path, join(getcwd(), sys.argv[2]))
                    setup_config = ConfigParser()
                    setup_config.read(join(join(getcwd()), 'setup.ini'), encoding='utf-8')
                    setup_config.set('project', 'name', folder)
                    setup_config.write(open(join(join(getcwd()), 'setup.ini'), "wt"))
                else:
                    print('No project found in the current environment, please check your environment or install the project first.')
            except subprocess.CalledProcessError as e:
                print(f"No package named {sys.argv[2]} found, please check your package name or install it first.")
                sys.exit(1)
            print(f'Initialized project workspace {sys.argv[2]}')