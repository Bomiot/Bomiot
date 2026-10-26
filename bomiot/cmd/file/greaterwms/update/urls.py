from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.update_check),
    path('manifest/', views.manifest),
    path('download/<path:file_path>', views.download),
    path('publish/', views.app_info),
    path('upload/', views.upload),
]
