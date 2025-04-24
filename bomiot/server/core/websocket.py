import datetime, os, urllib, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from bomiot.server.core.models import Message
from bomiot.server.core.field import md5_id
from bomiot.server.core.signal import bomiot_signals
from django.dispatch import receiver


@receiver(bomiot_signals, sender=Message)
def message_send_success_signal_handler(sender, **kwargs):
    message_data = Message.objects.filter(
        md5_id = kwargs['msg'].get('data', '').md5_id
    ).first()

    ## Write down your edit message data here

    message_data.can_send = True
    message_data.save()


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
            send_message = await Message.objects.acreate(sender=sender,
                                                         receiver=receiver,
                                                         detail=str(event['text']),
                                                         md5_id=md5_id()
                                                         )
            detail = await Message.objects.aget(sender=sender,
                                                receiver=receiver,
                                                md5_id=send_message.md5_id
                                               )
            if detail.can_send is True:
                text = {
                    "sender": sender,
                    "receiver": receiver,
                    "detail": detail.detail,
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
            else:
                await Message.objects.adelete(sender=sender,
                                              receiver=receiver,
                                              md5_id=send_message.md5_id
                                              )
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