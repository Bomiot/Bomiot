from django.apps import AppConfig
from django.db import connections, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.db.models.signals import post_migrate
import os
import time
import datetime


class CoreConfig(AppConfig):
    """
    Core application configuration for the bomiot server.
    """
    name = 'bomiot.server.core'

    def ready(self):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS bomiot_ready (
                            id INTEGER PRIMARY KEY,
                            pid INTEGER,
                            created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    cursor.execute("SELECT created_time FROM bomiot_ready WHERE id = 1")
                    result = cursor.fetchone()
                    if result:
                        created_time = result[0]
                        if created_time is None:
                            cursor.execute("DELETE FROM bomiot_ready WHERE id = 1")
                            cursor.execute("INSERT INTO bomiot_ready (id, pid, created_time) VALUES (1, %s, %s)", [os.getpid(), datetime.datetime.now()])
                        else:
                            try:
                                if hasattr(created_time, 'timestamp'):
                                    time_diff = time.time() - created_time.timestamp()
                                else:
                                    time_diff = time.time() - time.mktime(created_time.timetuple())
                                
                                if time_diff > 1:
                                    cursor.execute("DELETE FROM bomiot_ready WHERE id = 1")
                                    cursor.execute("INSERT INTO bomiot_ready (id, pid, created_time) VALUES (1, %s, %s)", [os.getpid(), datetime.datetime.now()])
                            except (AttributeError, TypeError, ValueError) as e:
                                print(f"Time format error: {e}")
                                cursor.execute("DELETE FROM bomiot_ready WHERE id = 1")
                                cursor.execute("INSERT INTO bomiot_ready (id, pid, created_time) VALUES (1, %s, %s)", [os.getpid(), datetime.datetime.now()])
                    else:
                        cursor.execute("INSERT INTO bomiot_ready (id, pid, created_time) VALUES (1, %s, %s)", [os.getpid(), datetime.datetime.now()])
                    
                    from bomiot.server.core import signal
                    from bomiot.server.server.views import init_permission
                    from bomiot.server.core.scheduler import sm
                    from bomiot.server.core.observer import ob
                    from bomiot.server.core.server_monitor import start_monitoring
                    from bomiot.server.server.views import init_permission
                    post_migrate.connect(do_init_data, sender=self)
                    try:
                        from bomiot.server.core.models import API
                        if not API.objects.filter().exists():
                            init_api()
                    except Exception as e:
                        print(f"Initial API initialization failed: {e}")
                    init_permission()
                    start_monitoring()
                    sm.start()
                    ob.start()

                    print('')
                    print("  $$$$$$    $$$$$   $$$       $$$  $$   $$$$$   $$$$$$")
                    print("  $$   $$  $$   $$  $$ $     $ $$  $$  $$   $$    $$")
                    print("  $$$$$$$  $$   $$  $$  $   $  $$  $$  $$   $$    $$")
                    print("  $$   $$  $$   $$  $$   $ $   $$  $$  $$   $$    $$")
                    print("  $$$$$$    $$$$$   $$    $    $$  $$   $$$$$     $$")
                    print('')

        except Exception as e:
            print(f"App initialization error: {e}")


def do_init_data(sender, **kwargs):
    init_api()


def init_api():
    try:
        from bomiot.server.core.models import API
        if API.objects.filter().exists():
            if API.objects.filter().count() != 52:
                API.objects.all().delete()
                create_api_data()
        else:
            create_api_data()
    except Exception as e:
        print(f"Init database error: {e}")


def create_api_data():
    from bomiot.server.core.models import API
    init_data = [
        API(id=1, method='GET', api='/core/example/', func_name='example_get', name="Get Example List"),
        API(id=2, method='POST', api='/core/example/create/', func_name='example_create', name="Create Example"),
        API(id=3, method='POST', api='/core/example/update/', func_name='example_update', name="Update Example"),
        API(id=4, method='POST', api='/core/example/delete/', func_name='example_delete', name="Delete Example"),
        API(id=5, method='GET', api='/core/goods/', func_name='goods_get', name="Get Goods List"),
        API(id=6, method='POST', api='/core/goods/create/', func_name='goods_create', name="Create Goods"),
        API(id=7, method='POST', api='/core/goods/update/', func_name='goods_update', name="Update Goods"),
        API(id=8, method='POST', api='/core/goods/delete/', func_name='goods_delete', name="Delete Goods"),
        API(id=9, method='GET', api='/core/bin/', func_name='bin_get', name="Get Bin List"),
        API(id=10, method='POST', api='/core/bin/create/', func_name='bin_create', name="Create Bin"),
        API(id=11, method='POST', api='/core/bin/update/', func_name='bin_update', name="Update Bin"),
        API(id=12, method='POST', api='/core/bin/delete/', func_name='bin_delete', name="Delete Bin"),
        API(id=13, method='GET', api='/core/stock/', func_name='stock_get', name="Get Stock List"),
        API(id=14, method='POST', api='/core/stock/create/', func_name='stock_create', name="Create Stock"),
        API(id=15, method='POST', api='/core/stock/update/', func_name='stock_update', name="Update Stock"),
        API(id=16, method='POST', api='/core/stock/delete/', func_name='stock_delete', name="Delete Stock"),
        API(id=17, method='GET', api='/core/capital/', func_name='capital_get', name="Get Capital List"),
        API(id=18, method='POST', api='/core/capital/create/', func_name='capital_create', name="Create Capital"),
        API(id=19, method='POST', api='/core/capital/update/', func_name='capital_update', name="Update Capital"),
        API(id=20, method='POST', api='/core/capital/delete/', func_name='capital_delete', name="Delete Capital"),
        API(id=21, method='GET', api='/core/supplier/', func_name='supplier_get', name="Get Supplier List"),
        API(id=22, method='POST', api='/core/supplier/create/', func_name='supplier_create', name="Create Supplier"),
        API(id=23, method='POST', api='/core/supplier/update/', func_name='supplier_update', name="Update Supplier"),
        API(id=24, method='POST', api='/core/supplier/delete/', func_name='supplier_delete', name="Delete Supplier"),
        API(id=25, method='GET', api='/core/customer/', func_name='customer_get', name="Get Customer List"),
        API(id=26, method='POST', api='/core/customer/create/', func_name='customer_create', name="Create Customer"),
        API(id=27, method='POST', api='/core/customer/update/', func_name='customer_update', name="Update Customer"),
        API(id=28, method='POST', api='/core/customer/delete/', func_name='customer_delete', name="Delete Customer"),
        API(id=29, method='GET', api='/core/asn/', func_name='asn_get', name="Get ASN List"),
        API(id=30, method='POST', api='/core/asn/create/', func_name='asn_create', name="Create ASN"),
        API(id=31, method='POST', api='/core/asn/update/', func_name='asn_update', name="Update ASN"),
        API(id=32, method='POST', api='/core/asn/delete/', func_name='asn_delete', name="Delete ASN"),
        API(id=33, method='GET', api='/core/dn/', func_name='dn_get', name="Get DN List"),
        API(id=34, method='POST', api='/core/dn/create/', func_name='dn_create', name="Create DN"),
        API(id=35, method='POST', api='/core/dn/update/', func_name='dn_update', name="Update DN"),
        API(id=36, method='POST', api='/core/dn/delete/', func_name='dn_delete', name="Delete DN"),
        API(id=37, method='GET', api='/core/purchase/', func_name='purchase_get', name="Get Purchase List"),
        API(id=38, method='POST', api='/core/purchase/create/', func_name='purchase_create', name="Create Purchase"),
        API(id=39, method='POST', api='/core/purchase/update/', func_name='purchase_update', name="Update Purchase"),
        API(id=40, method='POST', api='/core/purchase/delete/', func_name='purchase_delete', name="Delete Purchase"),
        API(id=41, method='GET', api='/core/bar/', func_name='bar_get', name="Get Bar List"),
        API(id=42, method='POST', api='/core/bar/create/', func_name='bar_create', name="Create Bar"),
        API(id=43, method='POST', api='/core/bar/update/', func_name='bar_update', name="Update Bar"),
        API(id=44, method='POST', api='/core/bar/delete/', func_name='bar_delete', name="Delete Bar"),
        API(id=45, method='GET', api='/core/fee/', func_name='fee_get', name="Get Fee List"),
        API(id=46, method='POST', api='/core/fee/create/', func_name='fee_create', name="Create Fee"),
        API(id=47, method='POST', api='/core/fee/update/', func_name='fee_update', name="Update Fee"),
        API(id=48, method='POST', api='/core/fee/delete/', func_name='fee_delete', name="Delete Fee"),
        API(id=49, method='GET', api='/core/driver/', func_name='driver_get', name="Get Driver List"),
        API(id=50, method='POST', api='/core/driver/create/', func_name='driver_create', name="Create Driver"),
        API(id=51, method='POST', api='/core/driver/update/', func_name='driver_update', name="Update Driver"),
        API(id=52, method='POST', api='/core/driver/delete/', func_name='driver_delete', name="Delete Driver"),
    ]
    API.objects.bulk_create(init_data, batch_size=200)