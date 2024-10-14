import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from django.conf import settings
from . import views

def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('register/', views.registers, name='register'),
    path('checktoken/', views.check_token, name='check_token'),
    path(r'^', include('bomiot.server.core.urls')),
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

print(1, os.environ.get('RUN_MAIN'))