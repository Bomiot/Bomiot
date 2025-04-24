import json
import mimetypes
import os
from django.conf import settings
from django.http import StreamingHttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from bomiot.server.core.jwt_auth import create_token, parse_payload
from bomiot.server.core.models import Permission
from bomiot.server.core.message import login_message_return, detail_message_return, others_message_return
from .pkgcheck import url_ignore
from os.path import join, isdir, exists
from os import listdir
import importlib.util
from pathlib import Path
from django.urls import get_resolver, URLPattern, URLResolver
import pkg_resources

User = get_user_model()

def logins(request):
    data = json.loads(request.body.decode().replace("'", '"'))
    user_check = User.objects.filter(username=data.get('username'), is_delete=False)
    if user_check.exists() is False:
        return JsonResponse(detail_message_return(request.META.get('HTTP_LANGUAGE', ''), "User not exists"))
    else:
        user = authenticate(username=data.get('username'), password=data.get('password'))
        context = {}
        if user:
            if user.is_active is True:
                login(request, user)
                user_info = {
                    "id": user.id,
                    "username": user.username,
                    "admin": user.is_superuser,
                    "permission": user.permission
                }
                token = create_token(user_info)
                context['token'] = token
                context['msg'] = others_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Success Login')
                return JsonResponse(context)
            else:
                return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User is not active'))
        else:
            return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User or Password error'))


@login_required
def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'msg': others_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Welcome Back Again')})
    else:
        return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User Not Log In'))


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

def get_all_url(resolver=None, pre='/'):
    if resolver is None:
        resolver = get_resolver()
    for r in resolver.url_patterns:
        if isinstance(r, URLPattern):
            if '<pk>' in str(r.pattern):
                continue
            yield pre + str(r.pattern).replace('^', '').replace('$', ''), r.name
        if isinstance(r, URLResolver):
            yield from get_all_url(r, pre + str(r.pattern))


def permission_check(data):
    api_list = url_ignore()
    if str(data[0]) not in api_list and str(data[1]) != 'None':
        try:
            Permission.objects.get_or_create(api=str(data[0]), name=str(data[1]))
        except:
            pass
        user_data = User.objects.filter(is_superuser=True)
        for i in user_data:
            i.permission[str(data[1])] = str(data[0])
            i.save()
        return data


def init_permission():
    try:
        user_data = User.objects.filter(is_superuser=True)
        for i in user_data:
            user_folder = join(settings.MEDIA_ROOT, i.username)
            exists(user_folder) or os.makedirs(user_folder)
            i.permission = {}
            i.save()
        api_list = list(map(lambda data: permission_check(data), get_all_url()))
    except:
        pass
