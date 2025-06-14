import os
from django.urls import path
from . import client, views, handler
from bomiot.server.function import goods
from bomiot.server.function import bin
from bomiot.server.function import stock
from bomiot.server.function import capital
from bomiot.server.function import supplier
from bomiot.server.function import customer
from bomiot.server.function import asn
from bomiot.server.function import dn
from bomiot.server.function import purchase
from bomiot.server.function import bar
from bomiot.server.function import fee
from bomiot.server.function import driver


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
    path(r'pid/', client.PIDList.as_view({"get": "list"})),
    path(r'cpu/', client.CPUList.as_view({"get": "list"})),
    path(r'memory/', client.MemoryList.as_view({"get": "list"})),
    path(r'disk/', client.DiskList.as_view({"get": "list"})),
    path(r'network/', client.NetworkList.as_view({"get": "list"})),
    path(r'server/echarts/', client.ServerCharts.as_view({"get": "list"})),
    path(r'server/pidcharts/', client.PIDCharts.as_view({"get": "list"})),
]

urlpatterns += [
    path(r'example/', handler.ExampleList.as_view({"get": "list"})),
    path(r'example/create/', handler.ExampleCreate.as_view({"post": "create"})),
    path(r'example/update/', handler.ExampleUpdate.as_view({"post": "create"})),
    path(r'example/delete/', handler.ExampleDelete.as_view({"post": "create"}))
]

urlpatterns += [
    path(r'goods/', goods.GoodsList.as_view({"get": "list"}), name="Get Goods List"),
    path(r'goods/create/', goods.GoodsCreate.as_view({"post": "create"}), name="Create Goods"),
    path(r'goods/update/', goods.GoodsUpdate.as_view({"post": "create"}), name="Update Goods"),
    path(r'goods/delete/', goods.GoodsDelete.as_view({"post": "create"}), name="Delete Goods")
]

urlpatterns += [
    path(r'bin/', bin.BinList.as_view({"get": "list"}), name="Get Bin List"),
    path(r'bin/create/', bin.BinCreate.as_view({"post": "create"}), name="Create Bin"),
    path(r'bin/update/', bin.BinUpdate.as_view({"post": "create"}), name="Update Bin"),
    path(r'bin/delete/', bin.BinDelete.as_view({"post": "create"}), name="Delete Bin")
]

urlpatterns += [
    path(r'stock/', stock.StockList.as_view({"get": "list"}), name="Get Stock List"),
    path(r'stock/create/', stock.StockCreate.as_view({"post": "create"}), name="Create Stock"),
    path(r'stock/update/', stock.StockUpdate.as_view({"post": "create"}), name="Update Stock"),
    path(r'stock/delete/', stock.StockDelete.as_view({"post": "create"}), name="Delete Stock")
]

urlpatterns += [
    path(r'capital/', capital.CapitalList.as_view({"get": "list"}), name="Get Capital List"),
    path(r'capital/create/', capital.CapitalCreate.as_view({"post": "create"}), name="Create Capital"),
    path(r'capital/update/', capital.CapitalUpdate.as_view({"post": "create"}), name="Update Capital"),
    path(r'capital/delete/', capital.CapitalDelete.as_view({"post": "create"}), name="Delete Capital")
]

urlpatterns += [
    path(r'supplier/', supplier.SupplierList.as_view({"get": "list"}), name="Get Supplier List"),
    path(r'supplier/create/', supplier.SupplierCreate.as_view({"post": "create"}), name="Create Supplier"),
    path(r'supplier/update/', supplier.SupplierUpdate.as_view({"post": "create"}), name="Update Supplier"),
    path(r'supplier/delete/', supplier.SupplierDelete.as_view({"post": "create"}), name="Delete Supplier")
]

urlpatterns += [
    path(r'customer/', customer.CustomerList.as_view({"get": "list"}), name="Get Customer List"),
    path(r'customer/create/', customer.CustomerCreate.as_view({"post": "create"}), name="Create Customer"),
    path(r'customer/update/', customer.CustomerUpdate.as_view({"post": "create"}), name="Update Customer"),
    path(r'customer/delete/', customer.CustomerDelete.as_view({"post": "create"}), name="Delete Customer")
]

urlpatterns += [
    path(r'asn/', asn.ASNList.as_view({"get": "list"}), name="Get ASN List"),
    path(r'asn/create/', asn.ASNCreate.as_view({"post": "create"}), name="Create ASN"),
    path(r'asn/update/', asn.ASNUpdate.as_view({"post": "create"}), name="Update ASN"),
    path(r'asn/delete/', asn.ASNDelete.as_view({"post": "create"}), name="Delete ASN")
]

urlpatterns += [
    path(r'dn/', dn.DNList.as_view({"get": "list"}), name="Get DN List"),
    path(r'dn/create/', dn.DNCreate.as_view({"post": "create"}), name="Create DN"),
    path(r'dn/update/', dn.DNUpdate.as_view({"post": "create"}), name="Update DN"),
    path(r'dn/delete/', dn.DNDelete.as_view({"post": "create"}), name="Delete DN")
]

urlpatterns += [
    path(r'purchase/', purchase.PurchaseList.as_view({"get": "list"}), name="Get Purchase List"),
    path(r'purchase/create/', purchase.PurchaseCreate.as_view({"post": "create"}), name="Create Purchase"),
    path(r'purchase/update/', purchase.PurchaseUpdate.as_view({"post": "create"}), name="Update Purchase"),
    path(r'purchase/delete/', purchase.PurchaseDelete.as_view({"post": "create"}), name="Delete Purchase")
]

urlpatterns += [
    path(r'bar/', bar.BarList.as_view({"get": "list"}), name="Get Bar List"),
    path(r'bar/create/', bar.BarCreate.as_view({"post": "create"}), name="Create Bar"),
    path(r'bar/update/', bar.BarUpdate.as_view({"post": "create"}), name="Update Bar"),
    path(r'bar/delete/', bar.BarDelete.as_view({"post": "create"}), name="Delete Bar")
]

urlpatterns += [
    path(r'fee/', fee.FeeList.as_view({"get": "list"}), name="Get Fee List"),
    path(r'fee/create/', fee.FeeCreate.as_view({"post": "create"}), name="Create Fee"),
    path(r'fee/update/', fee.FeeUpdate.as_view({"post": "create"}), name="Update Fee"),
    path(r'fee/delete/', fee.FeeDelete.as_view({"post": "create"}), name="Delete Fee")
]

urlpatterns += [
    path(r'driver/', driver.DriverList.as_view({"get": "list"}), name="Get Driver List"),
    path(r'driver/create/', driver.DriverCreate.as_view({"post": "create"}), name="Create Driver"),
    path(r'driver/update/', driver.DriverUpdate.as_view({"post": "create"}), name="Update Driver"),
    path(r'driver/delete/', driver.DriverDelete.as_view({"post": "create"}), name="Delete Driver")
]

urlpatterns += [
    path(r'api/', views.APIList.as_view({"get": "list"})),
    path(r'api/change/', views.APIChange.as_view({"post": "create"})),
]
