import os
from os import getcwd

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from django.conf import settings
from . import views
import pkgutil
from .pkgcheck import pkg_check
import importlib


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('register/', views.registers, name='register'),
    path('checktoken/', views.check_token, name='check_token'),
    path('', include('bomiot.server.core.urls')),
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

for module in pkgutil.iter_modules():
    try:
        settings_name = 'bomiotconf'
        exists = pkg_check(module.name, settings_name)
        if exists:
            module_import = importlib.import_module(f'{module.name}.{settings_name}')
            app_mode = getattr(module_import, 'mode_return')
            if app_mode == 'plugins':
                has_urls = exists = pkg_check(module.name, 'urls')
                if has_urls:
                    urlpatterns += [
                        path(f'{module.name}/', include(f'{module.name}.urls')),
                    ]
        else:
            continue
    except:
        continue
    finally:
        pass

current_plugins = [p for p in os.listdir(getcwd()) if os.path.isdir(p)]

for plugin in current_plugins:
    try:
        settings_name = 'bomiotconf'
        exists = pkg_check(plugin, settings_name)
        if exists:
            module_import = importlib.import_module(f'{plugin}.{settings_name}')
            app_mode = getattr(module_import, 'mode_return')
            if app_mode == 'plugins':
                has_urls = exists = pkg_check(plugin, 'urls')
                if has_urls:
                    urlpatterns += [
                        path(f'{plugin}/', include(f'{plugin}.urls')),
                    ]
        else:
            continue
    except:
        continue
    finally:
        pass

print(1, os.environ.get('RUN_MAIN'))