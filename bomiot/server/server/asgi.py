import os

from django.core.asgi import get_asgi_application
from bomiot.server.core.websocket import websocket_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

http_application = get_asgi_application()


async def application(scope, receive, send):
    if scope['type'] in ['http', 'https']:
        await http_application(scope, receive, send)
    elif scope['type'] in ['websocket']:
        await websocket_application(scope, receive, send)
    else:
        raise Exception('Unknown Type' + scope['type'])