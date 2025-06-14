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

def url_ignore():
    return ['/admin/', '/admin/login/', '/admin/logout/', '/admin/password_change/', '/admin/password_change/done/', '/admin/autocomplete/', '/admin/jsi18n/', '/admin/r/<int:content_type_id>/<path:object_id>/', '/admin/auth/group/',
            '/admin/auth/group/add/', '/admin/auth/group/<path:object_id>/history/', '/admin/auth/group/<path:object_id>/delete/', '/admin/auth/group/<path:object_id>/change/', '/admin/auth/group/<path:object_id>/', '/admin/django_apscheduler/djangojob/',
            '/admin/django_apscheduler/djangojob/add/', '/admin/django_apscheduler/djangojob/<path:object_id>/history/', '/admin/django_apscheduler/djangojob/<path:object_id>/delete/', '/admin/django_apscheduler/djangojob/<path:object_id>/change/',
            '/admin/django_apscheduler/djangojob/<path:object_id>/', '/admin/django_apscheduler/djangojobexecution/', '/admin/django_apscheduler/djangojobexecution/add/', '/admin/django_apscheduler/djangojobexecution/<path:object_id>/history/',
            '/admin/django_apscheduler/djangojobexecution/<path:object_id>/delete/', '/admin/django_apscheduler/djangojobexecution/<path:object_id>/change/', '/admin/django_apscheduler/djangojobexecution/<path:object_id>/',
            '/admin/core/user/<id>/password/', '/admin/core/user/', '/admin/core/user/add/', '/admin/core/user/<path:object_id>/history/', '/admin/core/user/<path:object_id>/delete/', '/admin/core/user/<path:object_id>/change/',
            '/admin/core/user/<path:object_id>/', '/admin/(?P<app_label>auth|django_apscheduler|core)/', '/admin/(?P<url>.*)', '/', '/login/', '/logout/', '/register/', '/checktoken/', '/favicon.ico', '/css/.*', '/md/<str:mddocs>',
            '/js/.*', '/assets/.*', '/statics/.*', '/fonts/.*', '/icons/.*', '/static/(?P<path>.*)', '/media/(?P<path>.*)', '/silk/', '/silk/stats/', '/silk/stats/requests/', '/silk/stats/queries/', '/silk/stats/memory/', '/silk/stats/requests/<int:request_id>/', '/silk/stats/queries/<int:query_id>/', '/silk/stats/memory/<int:memory_id>/'
            ]