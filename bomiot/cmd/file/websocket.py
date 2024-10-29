import datetime, os, urllib, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


CONECTINGS = {}

async def websocket_application(scope, receive, send):
    while True:
        event = await receive()
        if event['type'] == 'websocket.connect':
            await send({'type': 'websocket.accept'})
            query_string = scope.get('query_string', b'').decode()
            qs = urllib.parse.parse_qs(query_string)
            sender = qs.get('sender', [''])[0]
            CONECTINGS[sender] = send
        elif event['type'] == 'websocket.receive':
            query_string = scope.get('query_string', b'').decode()
            qs = urllib.parse.parse_qs(query_string)
            sender = qs.get('sender', [''])[0]
            receiver = qs.get('receiver', [''])[0]
            text = {
                "sender": sender,
                "receiver": receiver,
                "detail": str(event['text']),
                "create_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "update_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            send = CONECTINGS[sender]
            if receiver in CONECTINGS:
                send = CONECTINGS[receiver]
                await send({
                    'type': 'websocket.send',
                    'text': str(text).replace('\'', '\"')
                })
        elif event['type'] == 'websocket.disconnect':
            try:
                query_string = scope.get('query_string', b'').decode()
                qs = urllib.parse.parse_qs(query_string)
                sender = qs.get('sender', [''])[0]
                CONECTINGS.pop(sender)
                break
            except:
                break
        else:
            pass