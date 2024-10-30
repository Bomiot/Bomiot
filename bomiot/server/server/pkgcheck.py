import importlib.util
from pathlib import Path
from os.path import join, isfile
from configparser import ConfigParser

def pkg_check(module: str):
    """
    check installed packages
    :return:
    """
    # TODO: Implement package check
    try:
        module_path = importlib.util.find_spec(module).origin
        list_module_path = Path(module_path).resolve().parent
        config_path = join(list_module_path, 'bomiotconf.ini')
        if isfile(config_path):
            return module
        else:
            return None
    except:
        return None

def cwd_check(module: str):
    """
    check installed packages
    :return:
    """
    # TODO: Implement package check
    try:
        current_path = Path(__file__).resolve().parent.parent
        workspace_path = join(current_path, 'workspace.ini')
        workspace_config = ConfigParser()
        workspace_config.read(workspace_path, encoding='utf-8')
        working_space = workspace_config.get('space', 'name')
        config_path = join(join(working_space, module),'bomiotconf.ini')
        if isfile(config_path):
            return module
        else:
            return None
    except:
        return None


def ignore_pkg() -> list:
    return ['bomiot', 'django', 'pyjwt', 'asgiref', 'django-cors-headers', 'django-filter', 'djangorestframework', 'djangorestframework-csv', 'furl', 'orderedmultidict', 'orjson', 'pip', 'setuptools', 'six', 'sqlparse', 'toml', 'tzdata', 'watchdog', 'autocommand', 'backports.tarfile', 'importlib-metadata', 'importlib-resources', 'inflect', 'jaraco.collections', 'jaraco.context', 'jaraco.functools', 'jaraco.text', 'more-itertools', 'packaging', 'platformdirs', 'tomli', 'typeguard', 'typing-extensions', 'wheel', 'zipp']


def ignore_cwd() -> list:
    return ['.idea', '.venv', 'dbs', 'logs', 'media', '__pycache__', 'bomiot']

def none_return():
    return None