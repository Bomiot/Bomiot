import os
from os.path import join, isdir
from os import listdir
from django.core.asgi import get_asgi_application
from pathlib import Path
import sys
import importlib
import importlib.util
import pkg_resources
from .pkgcheck import pkg_check, ignore_pkg, ignore_cwd
from configparser import ConfigParser


BASE_DIR = Path(__file__).resolve().parent.parent

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

CONFIG = ConfigParser()
WORKING_SPACE_CONFIG = ConfigParser()
WORKING_SPACE_CONFIG.read(join(BASE_DIR, 'workspace.ini'), encoding='utf-8')
WORKING_SPACE = WORKING_SPACE_CONFIG.get('space', 'name', fallback='Create your working space first')
CONFIG.read(join(WORKING_SPACE, 'setup.ini'), encoding='utf-8')
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')


res_pkg_list = list(set([pkg.key for pkg in pkg_resources.working_set]).difference(set(ignore_pkg())))
pkg_squared = list(map(lambda data: pkg_check(data), res_pkg_list))
filtered_pkg_squared = list(filter(lambda x: x is not None, pkg_squared))

current_path = list(set([p for p in listdir(WORKING_SPACE) if isdir(p)]).difference(set(ignore_cwd())))
filtered_current_path = list(filter(lambda y: y is not None, current_path))

ws = importlib.import_module(f'bomiot.server.core.websocket')

if len(filtered_pkg_squared) > 0:
    for module in filtered_pkg_squared:
        module_path = importlib.util.find_spec(PROJECT_NAME).origin
        list_module_path = Path(module_path).resolve().parent
        module_import = importlib.import_module(f'{module}.bomiotconf')
        app_mode = module_import.mode_return()
        if app_mode == 'project':
            if module == PROJECT_NAME and module != 'bomiot':
                ws = importlib.import_module(f'{PROJECT_NAME}.websocket')

if len(filtered_current_path) > 0:
    for module_name in filtered_current_path:
        exists_module = pkg_check(module_name)
        if exists_module is not None:
            module_import = importlib.import_module(f'{module_name}.bomiotconf')
            app_mode = module_import.mode_return()
            if app_mode == 'project':
                if module_name == PROJECT_NAME and module_name != 'bomiot':
                    ws = importlib.import_module(f'{PROJECT_NAME}.websocket')



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')
os.environ.setdefault('RUN_MAIN', 'true')

http_application = get_asgi_application()


async def application(scope, receive, send):
    if scope['type'] in ['http', 'https']:
        await http_application(scope, receive, send)
    elif scope['type'] in ['websocket']:
        await ws.websocket_application(scope, receive, send)
    else:
        raise Exception('Unknown Type' + scope['type'])