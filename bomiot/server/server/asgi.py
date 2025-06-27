from os.path import join, isdir
from os import listdir
from django.core.asgi import get_asgi_application
from pathlib import Path
import sys
import importlib
from bomiot.server.server.pkgcheck import pkg_check, cwd_check, ignore_pkg, ignore_cwd
from configparser import ConfigParser

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, BASE_DIR)

CONFIG = ConfigParser()
WORKING_SPACE_CONFIG = ConfigParser()
WORKING_SPACE_CONFIG.read(join(BASE_DIR, 'workspace.ini'), encoding='utf-8')
WORKING_SPACE = WORKING_SPACE_CONFIG.get('space', 'name', fallback='Create your working space first')
CONFIG.read(join(WORKING_SPACE, 'setup.ini'), encoding='utf-8')
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')

current_path = list(set([p for p in listdir(WORKING_SPACE) if isdir(p)]).difference(set(ignore_cwd())))
cur_squared = list(map(lambda data: cwd_check(data), current_path))
filtered_current_path = list(filter(lambda y: y is not None, cur_squared))

ws = importlib.import_module(f'bomiot.server.core.websocket')

if len(filtered_current_path) > 0:
    for module_name in filtered_current_path:
        app_mode_config = ConfigParser()
        try:
            app_mode_config.read(join(join(WORKING_SPACE, PROJECT_NAME), 'bomiotconf.ini'), encoding='utf-8')
            app_mode = app_mode_config.get('mode', 'name')
            if app_mode == 'project':
                if module_name == PROJECT_NAME:
                    ws = importlib.import_module(f'{PROJECT_NAME}.websocket')
        except:
            pass

http_application = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] in ['http', 'https']:
        await http_application(scope, receive, send)
    elif scope['type'] in ['websocket']:
        await ws.websocket_application(scope, receive, send)
    else:
        raise Exception('Unknown Type' + scope['type'])