import os
from django.urls import path
from . import views
from bomiot.server.core.scheduler import sm
from bomiot.server.core.observer import ob
from bomiot.server.core.server_monitor import start_monitoring


urlpatterns = [
    path(r'user/', views.UserList.as_view({"get": "list"}), name="Get User List"),
    path(r'user/permission/', views.PermissionList.as_view({"get": "list"})),
    path(r'user/create/', views.UserCreate.as_view({"post": "create"}), name="Create One User"),
    path(r'user/changepwd/', views.UserChangePWD.as_view({"post": "create"}), name="Change Password"),
    path(r'user/team/', views.UserSetTeam.as_view({"post": "create"}), name="Set Team For User"),
    path(r'user/department/', views.UserSetDepartment.as_view({"post": "create"}), name="Set Department For User"),
    path(r'user/lock/', views.UserLock.as_view({"post": "create"}), name="Lock & Unlock User"),
    path(r'user/delete/', views.UserDelete.as_view({"post": "create"}), name="Delete One User"),
    path(r'user/upload/', views.UserUpload.as_view({"post": "create"})),
    path(r'user/files/', views.UserFiles.as_view({"get": "list"})),
    path(r'user/files/share/', views.FileShare.as_view({"post": "create"})),
    path(r'user/files/delete/', views.DeleteFile.as_view({"post": "create"}))
]

urlpatterns += [
    path(r'team/', views.TeamList.as_view({"get": "list"}), name="Get Team List"),
    path(r'team/create/', views.TeamCreate.as_view({"post": "create"}), name="Create One Team"),
    path(r'team/setpermission/', views.TeamPermission.as_view({"post": "create"}), name="Set Permission For Team"),
    path(r'team/change/', views.TeamChange.as_view({"post": "create"}), name="Change Team"),
    path(r'team/delete/', views.TeamDelete.as_view({"post": "create"}), name="Delete Team")
]

urlpatterns += [
    path(r'department/', views.DepartmentList.as_view({"get": "list"}), name="Get Department List"),
    path(r'department/create/', views.DepartmentCreate.as_view({"post": "create"}), name="Create Department"),
    path(r'department/change/', views.DepartmentChange.as_view({"post": "create"}), name="Change Department"),
    path(r'department/delete/', views.DepartmentDelete.as_view({"post": "create"}), name="Delete Department")
]

urlpatterns += [
    path(r'pypi/', views.PyPiList.as_view({"get": "list"})),
    path(r'pypi/charts/', views.PyPiCharts.as_view({"get": "list"})),
]

urlpatterns += [
    path(r'pid/', views.PIDList.as_view({"get": "list"})),
    path(r'cpu/', views.CPUList.as_view({"get": "list"})),
    path(r'memory/', views.MemoryList.as_view({"get": "list"})),
    path(r'disk/', views.DiskList.as_view({"get": "list"})),
    path(r'network/', views.NetworkList.as_view({"get": "list"})),
    path(r'server/echarts/', views.ServerCharts.as_view({"get": "list"})),
    path(r'server/pidcharts/', views.PIDCharts.as_view({"get": "list"})),
]

# Start Scheduler
if os.environ.get('RUN_MAIN') == 'true':
    start_monitoring()
    sm.start()
    ob.start()