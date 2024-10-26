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
from os.path import join, isdir
from os import getcwd, listdir
import importlib.util
from pathlib import Path
import pkg_resources


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
    if settings.PROJECT_NAME == 'bomiot' or settings.PROJECT_NAME == '':
        path = join(join(join(join(join(settings.BASE_DIR.parent, 'templates'), 'dist'), 'spa'), 'icons'), 'logo.png')
    else:
        check_path = False
        current_path = [p for p in listdir(settings.WORKING_SPACE) if isdir(p)]
        for module_name in current_path:
            if module_name == settings.PROJECT_NAME:
                project_path = join(settings.WORKING_SPACE, settings.PROJECT_NAME)
                path = join(join(join(join(join(project_path, 'templates'), 'dist'), 'spa'), 'icons'), 'logo.png')
                check_path = True
            else:
                continue
        if check_path is False:
            for module in [pkg.key for pkg in pkg_resources.working_set]:
                if module == settings.PROJECT_NAME:
                    project_path = importlib.util.find_spec(settings.PROJECT_NAME).origin
                    list_project_path = Path(project_path).resolve().parent
                    path = join(join(join(join(join(list_project_path, 'templates'), 'dist'), 'spa'), 'icons'), 'logo.png')
                else:
                    continue
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = 'max-age=864000000000'
    return resp


def statics(request):
    if settings.PROJECT_NAME == 'bomiot' or settings.PROJECT_NAME == '':
        path = join(join(join(settings.BASE_DIR.parent, 'templates'), 'dist'), 'spa')
        request_path = request.path_info.split('/')
        for i in request_path:
            if i == '':
                continue
            else:
                path = join(path, i)
    else:
        check_path = False
        current_path = [p for p in listdir(settings.WORKING_SPACE) if isdir(p)]
        for module_name in current_path:
            if module_name == settings.PROJECT_NAME:
                project_path = join(settings.WORKING_SPACE, settings.PROJECT_NAME)
                path = join(join(join(project_path, 'templates'), 'dist'), 'spa')
                request_path = request.path_info.split('/')
                for i in request_path:
                    if i == '':
                        continue
                    else:
                        path = join(path, i)
                check_path = True
            else:
                continue
        if check_path is False:
            for module in [pkg.key for pkg in pkg_resources.working_set]:
                if module == settings.PROJECT_NAME:
                    project_path = importlib.util.find_spec(settings.PROJECT_NAME).origin
                    list_project_path = Path(project_path).resolve().parent
                    path = join(join(join(list_project_path, 'templates'), 'dist'), 'spa')
                    request_path = request.path_info.split('/')
                    for i in request_path:
                        if i == '':
                            continue
                        else:
                            path = join(path, i)
                else:
                    continue
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = 'max-age=864000000000'
    return resp

