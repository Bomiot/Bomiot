from os import getenv, getcwd
from os.path import join
import configparser


APP_DEBUG = getenv('APP_DEBUG', True)

ADMINS = [
    'admin'
]
