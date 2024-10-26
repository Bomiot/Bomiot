import os
import pkg_resources
import importlib.util

from os import listdir
from os.path import join, isdir, exists
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from django.conf import settings
from . import views
from .pkgcheck import pkg_check, ignore_pkg, ignore_cwd
from configparser import ConfigParser
from pathlib import Path

def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='dist/spa/index.html')),
    path('login/', views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('register/', views.registers, name='register'),
    path('checktoken/', views.check_token, name='check_token'),
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

CONFIG = ConfigParser()
CONFIG.read(join(settings.WORKING_SPACE, 'setup.ini'), encoding='utf-8')
project_name = CONFIG.get('project', 'name', fallback='bomiot')

pkg_list = [pkg.key for pkg in pkg_resources.working_set]
res_pkg_list = list(set(pkg_list).difference(set(ignore_pkg())))
pkg_squared = list(map(lambda data: pkg_check(data), res_pkg_list))
filtered_pkg_squared = list(filter(lambda x: x is not None, pkg_squared))

current_path = [p for p in listdir(settings.WORKING_SPACE) if isdir(p)]
current_path = list(set(current_path).difference(set(ignore_cwd())))
filtered_current_path = list(filter(lambda y: y is not None, current_path))

if len(filtered_pkg_squared) > 0:
    for module in pkg_squared:
        if module is not None:
            module_path = importlib.util.find_spec(project_name).origin
            list_module_path = Path(module_path).resolve().parent
            module_import = importlib.import_module(f'{module}.bomiotconf')
            app_mode = module_import.mode_return()
            if app_mode == 'plugins':
                if exists(join(list_module_path, 'urls')):
                    urlpatterns += [
                        path(f'{module}/', include(f'{module}.urls'))
                    ]
            elif app_mode == 'project':
                if module == project_name:
                    find_urls = [u for u in listdir(list_module_path) if isdir(u)]
                    for url in find_urls:
                        if exists(join(join(settings.WORKING_SPACE, url), 'urls')):
                            urlpatterns += [
                                path(f'{project_name}/{url}/', include(f'{project_name}.{url}.urls'))
                            ]

if len(filtered_current_path) > 0:
    for module_name in filtered_current_path:
        exists_module = pkg_check(module_name)
        if exists_module is not None:
            module_import = importlib.import_module(f'{module_name}.bomiotconf')
            app_mode = module_import.mode_return()
            if app_mode == 'plugins':
                if exists(join(join(settings.WORKING_SPACE, module_name), 'urls')):
                    urlpatterns += [
                        path(f'{module_name}/', include(f'{module_name}.urls')),
                    ]
            elif app_mode == 'project':
                if module_name == project_name:
                    project_path = join(settings.WORKING_SPACE, project_name)
                    find_urls = [u for u in listdir(project_path) if isdir(u)]
                    for url in find_urls:
                        if exists(join(join(project_path, url), 'urls')):
                            urlpatterns += [
                                path(f'{project_name}/{url}/', include(f'{project_name}.{url}.urls')),
                            ]

print(1, os.environ.get('RUN_MAIN'))