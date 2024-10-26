from os.path import join, exists
from os import makedirs, getcwd
import shutil
from pathlib import Path
import toml
from configparser import ConfigParser


def create_app(folder: str):
    """
    create file
    :return:
    """
    current_path = Path(__file__).resolve()
    working_space = join(getcwd())
    file_path = join(current_path.parent, 'extends')
    if folder != '':
        folder = 'bomiot'

    print("Welcome to bomiot")