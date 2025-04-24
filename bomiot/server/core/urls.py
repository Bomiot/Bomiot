import os
from django.urls import path
from . import views
from bomiot.server.core.scheduler import sm
from bomiot.server.core.observer import ob


urlpatterns = [
    path(r'user/', views.UserList.as_view({"get": "list"}), name="Get User List"),
    path(r'user/permission/', views.PermissionList.as_view({"get": "list"}), name="Get Permission List"),
    path(r'user/create/', views.UserCreate.as_view({"post": "create"}), name="Create One User"),
    path(r'user/setpermission/', views.UserPermission.as_view({"post": "create"}), name="Set Permission For User"),
    path(r'user/changepwd/', views.UserChangePWD.as_view({"post": "create"}), name="Change Password"),
    path(r'user/lock/', views.UserLock.as_view({"post": "create"}), name="Lock & Unlock User"),
    path(r'user/delete/', views.UserDelete.as_view({"post": "create"}), name="Delete One User"),
    path(r'user/upload/', views.UserUpload.as_view({"post": "create"})),
    path(r'user/files/', views.UserFiles.as_view({"get": "list"})),
    path(r'user/files/share/', views.FileShare.as_view({"post": "create"})),
    path(r'user/files/delete/', views.DeleteFile.as_view({"post": "create"})),
]

# Start Scheduler
if os.environ.get('RUN_MAIN') == 'true':
    sm.start()
    ob.start()
