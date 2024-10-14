import json
import mimetypes
import orjson
from django.conf import settings
from django.http import StreamingHttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from bomiot.server.core.jwt_auth import create_token, parse_payload


User = get_user_model()


def logins(request):
    data = json.loads(request.body.decode().replace("'", '"'))
    user = authenticate(username=data['username'], password=data['pwd'])
    context = {}
    if user:
        login(request, user)
        user_info = {
            "id": user.id,
            "username": user.username
        }
        token = create_token(user_info)
        context['token'] = token
        context['msg'] = "Success Login"
        return JsonResponse(context)
    else:
        return JsonResponse({"msg": "User Does Not Exists"})


@login_required
def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        JsonResponse({'msg': 'success'})
    else:
        return JsonResponse({'msg': 'User Not Log In'})


async def registers(request):
    data = orjson.loads(request.body)
    context = {}
    if data['username'] == '':
        context['detail'] = '100001'
        return JsonResponse(context)
    if data['pwd1'] == '':
        context['detail'] = '100002'
        return JsonResponse(context)
    if data['pwd2'] == '':
        context['detail'] = '100003'
        return JsonResponse(context)
    if data['pwd1'] != data['pwd2']:
        context['detail'] = '100004'
        return JsonResponse(context)
    user_exists = User.objects.filter(username=str(data['username'])).aiterator()
    if user_exists.exists():
        context['detail'] = '100005'
        return JsonResponse(context)
    else:
        user = User.objects.acreate_user(username=str(data['username']),
                                        password=str(data['pwd1']))
        await user.asave()
        login(request, user)
        context['detail'] = 'success'
        return JsonResponse(context)


def check_token(request):
    token = request.META.get('HTTP_TOKEN')
    context = parse_payload(token)
    return JsonResponse(context)


def favicon(request):
    path = str(settings.BASE_DIR) + '/static/icons/logo.png'
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = 'max-age=864000000000'
    return resp


def statics(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = 'max-age=864000000000'
    return resp


# def page_not_found(request, exception):
#     return render(request, '404.html', status=404)
#
#
# def permission_denied(request, exception):
#     return render(request, '403.html', status=403)
