import importlib.metadata
import importlib.util

from os import listdir
from os.path import join, isdir, exists, isfile
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from django.conf import settings
from . import views
from .pkgcheck import pkg_check, cwd_check, ignore_pkg, ignore_cwd
from configparser import ConfigParser
from pathlib import Path
from django.urls import resolve, Resolver404


def url_exists(url_data):
    try:
        resolve(url_data)
        return True
    except Resolver404:
        return False


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='dist/spa/index.html')),
    path('login/', views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('checktoken/', views.check_token, name='check_token'),
    path('md/<str:mddocs>', views.mdurl, name='markdown'),
    path('core/', include('bomiot.server.core.urls')),
]


urlpatterns += [
    path('favicon.ico', views.favicon, name='favicon'),
    re_path('^css/.*$', views.statics, name='css'),
    re_path('^js/.*$', views.statics, name='js'),
    re_path('^assets/.*$', views.statics, name='assets'),
    re_path('^statics/.*$', views.statics, name='statics'),
    re_path('^fonts/.*$', views.statics, name='fonts'),
    re_path('^icons/.*$', views.statics, name='icons'),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]


all_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
res_pkg_list = list(set([name.lower() for name in all_packages]).difference(set(ignore_pkg())))
pkg_squared = list(map(lambda data: pkg_check(data), res_pkg_list))
filtered_pkg_squared = list(filter(lambda x: x is not None, pkg_squared))

current_path = list(set([p for p in listdir(settings.WORKING_SPACE) if isdir(p)]).difference(set(ignore_cwd())))
cur_squared = list(map(lambda data: cwd_check(data), current_path))
filtered_current_path = list(filter(lambda y: y is not None, cur_squared))


if len(filtered_pkg_squared) > 0:
    for module in filtered_pkg_squared:
        module_path = importlib.util.find_spec(module).origin
        list_module_path = Path(module_path).resolve().parent
        pkg_config_check = ConfigParser()
        pkg_config_check.read(join(list_module_path, 'bomiotconf.ini'), encoding='utf-8')
        app_mode = pkg_config_check.get('mode', 'name', fallback='plugins')
        if app_mode == 'plugins':
            try:
                if isfile(join(list_module_path, 'urls.py')):
                    if url_exists(f'/{module}/') is True:
                        urlpatterns += [
                            path(f'{module}/', include(f'{module}.urls.py'))
                        ]
            except:
                continue

if len(filtered_current_path) > 0:
    for module_name in filtered_current_path:
        app_mode_config = ConfigParser()
        app_mode_config.read(join(join(settings.WORKING_SPACE, module_name), 'bomiotconf.ini'), encoding='utf-8')
        app_mode = app_mode_config.get('mode', 'name')
        if app_mode == 'plugins':
            try:
                if isfile(join(join(settings.WORKING_SPACE, module_name), 'urls.py')):
                    if url_exists(f'/{module_name}/') is True:
                        urlpatterns += [
                            path(f'{module_name}/', include(f'{module_name}.urls'))
                        ]
            except:
                continue
        elif app_mode == 'project':
            if module_name == settings.PROJECT_NAME:
                project_path = join(settings.WORKING_SPACE, settings.PROJECT_NAME)
                for url in listdir(project_path):
                    try:
                        if url_exists(f'/{settings.PROJECT_NAME}/{url}/') is False:
                            urlpatterns += [
                                path(f'{settings.PROJECT_NAME}/{url}/', include(f'{settings.PROJECT_NAME}.{url}.urls')),
                            ]
                    except:
                        pass