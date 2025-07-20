import json, orjson
import mimetypes
import os
import aiofiles
from django.conf import settings
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
from configparser import ConfigParser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.cache import cache
from bomiot.server.core.jwt_auth import create_token, parse_payload
from bomiot.server.core.models import Permission
from bomiot_message import login_message_return, others_message_return
from bomiot.server.server.pkgcheck import url_ignore
from os.path import join, isdir, exists
from os import listdir
import importlib.util
from pathlib import Path
from django.urls import get_resolver, URLPattern, URLResolver

User = get_user_model()

async def test(request):
    return JsonResponse({"msg": "This is Django API"})


def logins(request):
    data = json.loads(request.body.decode().replace("'", '"'))
    user_check = User.objects.filter(username=data.get('username'), is_delete=False)
    if user_check.exists() is False:
        return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), "User not exists"))
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
            user_data = user_check.first()
            if user_data.request_limit < settings.REQUEST_LIMIT:
                user_data.request_limit += 1
                user_data.save()
                return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User or Password error'))
            else:
                user_data.is_active = False
                user_data.request_limit = 0
                user_data.save()
                return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User is not active'))


@login_required
async def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'msg': others_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Welcome Back Again')})
    else:
        return JsonResponse(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User Not Log In'))


async def check_token(request):
    token = request.META.get('HTTP_TOKEN')
    context = parse_payload(token)
    return JsonResponse(context)


async def mdurl(request, mddocs):
    language = request.META.get('HTTP_LANUAGE', '')
    if not mddocs.endswith('.md'):
        return JsonResponse({'detail': others_message_return(language, 'Only support markdown file')})
    folder_path = Path(settings.MEDIA_ROOT)
    all_files = [f.name for f in folder_path.iterdir() if f.is_file()]
    start_words = mddocs.split('.')
    md_check_list_all = []
    md_check_list_only = []
    for i in all_files:
        if i == mddocs:
            md_check_list_only.append(i)
        else:
            if i.startswith(start_words[0]) and i.endswith('.md'):
                md_check_list_all.append(i)
    if len(md_check_list_only) == 1:
        async def file_iterator():
            async with aiofiles.open(join(settings.MEDIA_ROOT, mddocs), 'rb') as f:
                while chunk := await f.read(8192):
                    yield chunk
        response = StreamingHttpResponse(file_iterator())
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    else:
        if len(md_check_list_all) == 0:
            return JsonResponse({'detail': others_message_return(language, 'Markdown file not found')})
        async def file_iterator():
            async with aiofiles.open(join(settings.MEDIA_ROOT, mddocs), 'rb') as f:
                while chunk := await f.read(8192):
                    yield chunk
        response = StreamingHttpResponse(file_iterator())
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

def favicon(request):
    path = join(settings.MEDIA_ROOT, 'img', 'logo.png')
    resp = FileResponse(open(path, 'rb'))
    resp['Cache-Control'] = 'max-age=864000000000'
    return resp

def statics(request):
    if cache.has_key("templates_path") is False:
            CONFIG = ConfigParser()
            CONFIG.read(join(settings.WORKING_SPACE, 'setup.ini'), encoding='utf-8')
            templates_path = CONFIG.get('templates', 'name', fallback='templates/dist/spa/index.html')
            cache.set("templates_path", templates_path)
    else:
        templates_path = cache.get("templates_path")
    path = join(settings.WORKING_SPACE, settings.PROJECT_NAME)
    static_path_split = templates_path.split('/')[:-1]
    for i in static_path_split:
        if i == '':
            continue
        else:
            path = join(path, i)
    request_path = request.path_info.split('/')
    for j in request_path:
        if j == '':
            continue
        else:
            path = join(path, j)
    resp = FileResponse(open(path, 'rb'))
    resp['Cache-Control'] = 'max-age=864000000000'
    return resp

async def google(request):
    return JsonResponse({})

def queryset_to_json(queryset):
    data = list(queryset.values())
    return JsonResponse(data, safe=False)

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

def permission_check(data, perm_obj_dict, api_list, user_objs):
    if str(data[0]) not in api_list and str(data[1]) != 'None':
        perm_obj, created = perm_obj_dict.get((str(data[0]), str(data[1])))
        if not perm_obj:
            perm_obj = Permission(api=str(data[0]), name=str(data[1]))
            perm_obj_dict[(str(data[0]), str(data[1]))] = perm_obj
        for user in user_objs:
            user.permission[str(data[1])] = str(data[0])
        return perm_obj

def init_permission():
    try:
        Permission.objects.all().delete()
        user_objs = list(User.objects.filter(is_superuser=True))
        media_root = settings.MEDIA_ROOT
        for user in user_objs:
            user_folder = join(media_root, user.username)
            if not exists(user_folder):
                os.makedirs(user_folder)
            user.permission = {}
        all_api_info = list(get_all_url())
        api_list = set(url_ignore())
        perm_obj_dict = {}
        perm_objs = []
        for data in all_api_info:
            if str(data[0]) not in api_list and str(data[1]) != 'None':
                perm_obj = Permission(api=str(data[0]), name=str(data[1]))
                perm_objs.append(perm_obj)
                for user in user_objs:
                    user.permission[str(data[1])] = str(data[0])
        if perm_objs:
            Permission.objects.bulk_create(perm_objs, batch_size=200)
        User.objects.bulk_update(user_objs, ['permission'], batch_size=100)
    except Exception as e:
        print(f"Error initializing permissions: {e}")