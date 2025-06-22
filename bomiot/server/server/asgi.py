import os
from os.path import join, isdir
from os import listdir
from django.core.asgi import get_asgi_application
from asgivalid import valid_asgi, verify_info
from pathlib import Path
import sys
import importlib
import importlib.util
import importlib.metadata
from .pkgcheck import pkg_check, cwd_check, ignore_pkg, ignore_cwd
from configparser import ConfigParser
from django.core.cache import cache


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

ins = {
    'ins1': ['e', 'x', 'p', 'i', 'r', 'e'],
}

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
        if cache.has_key("asgi_valid") is False:
            cache.set("asgi_valid", valid_asgi(WORKING_SPACE))
        valid_data = cache.get("asgi_valid")
        if valid_data != '':
            valid = verify_info(valid_data)
            if not valid[0] and not valid[1]:
                async def asgi_send(event):
                    if event["type"] == "http.response.start":
                        headers = list(event.get("headers", []))
                        headers.append([b'expire', b'%s' % valid[2].encode('utf-8')])
                        event["headers"] = headers
                    await send(event)
                await http_application(scope, receive, asgi_send)
    elif scope['type'] in ['websocket']:
        if cache.has_key("asgi_valid") is False:
            cache.set("asgi_valid", valid_asgi(WORKING_SPACE))
        valid_data = cache.get("asgi_valid")
        if valid_data != '':
            valid = verify_info(valid_data)
            if not valid[0] and not valid[1]:
                await ws.websocket_application(scope, receive, send)
    else:
        raise Exception('Unknown Type' + scope['type'])