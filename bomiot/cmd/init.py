from os.path import join, exists
from os import makedirs, getcwd
import subprocess

def init(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    cmd = "bomiot makemigrations"
    subprocess.run(cmd, shell=True)

    log_path = join(getcwd(), 'logs')
    exists(log_path) or makedirs(log_path)

    print('Initialized workspace %s' % folder)
