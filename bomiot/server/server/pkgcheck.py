import importlib.util

def pkg_check(module: str):
    """
    check installed packages
    :return:
    """
    # TODO: Implement package check
    try:
        settings_name = 'bomiotconf'
        exists_module = importlib.util.find_spec(f'{module}.{settings_name}')
        if exists_module is not None:
            return module
        else:
            return None
    except:
        return None


def ignore_pkg() -> list:
    return ['django', 'pyjwt', 'asgiref', 'django-cors-headers', 'django-filter', 'djangorestframework', 'djangorestframework-csv', 'furl', 'orderedmultidict', 'orjson', 'pip', 'setuptools', 'six', 'sqlparse', 'toml', 'tzdata', 'watchdog', 'autocommand', 'backports.tarfile', 'importlib-metadata', 'importlib-resources', 'inflect', 'jaraco.collections', 'jaraco.context', 'jaraco.functools', 'jaraco.text', 'more-itertools', 'packaging', 'platformdirs', 'tomli', 'typeguard', 'typing-extensions', 'wheel', 'zipp']


def ignore_cwd() -> list:
    return ['.idea', '.venv', 'dbs', 'logs', 'media', '__pycache__', 'bomiot']

def none_return():
    return None