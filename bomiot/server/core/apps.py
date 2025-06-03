from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    """
    Core application configuration for the bomiot server.
    """
    name = 'bomiot.server.core'

    def ready(self):
        from bomiot.server.core import signal
        post_migrate.connect(do_init_data, sender=self)


def do_init_data(sender, **kwargs):
    init_api()


def init_api():
    try:
        from bomiot.server.core.models import API
        if API.objects.filter().exists():
            if API.objects.filter().count() != 44:
                API.objects.all().delete()
                create_api_data()
        else:
            create_api_data()
    except Exception as e:
        print(f"Init database error: {e}")


def create_api_data():
    from bomiot.server.core.models import API
    init_data = [
        API(id=1, method='GET', api='/core/example/', func_name='example_get'),
        API(id=2, method='POST', api='/core/example/create/', func_name='example_create'),
        API(id=3, method='POST', api='/core/example/update/', func_name='example_update'),
        API(id=4, method='POST', api='/core/example/delete/', func_name='example_delete'),
        API(id=5, method='GET', api='/core/goods/', func_name='goods_get'),
        API(id=6, method='POST', api='/core/goods/create/', func_name='goods_create'),
        API(id=7, method='POST', api='/core/goods/update/', func_name='goods_update'),
        API(id=8, method='POST', api='/core/goods/delete/', func_name='goods_delete'),
        API(id=9, method='GET', api='/core/bin/', func_name='bin_get'),
        API(id=10, method='POST', api='/core/bin/create/', func_name='bin_create'),
        API(id=11, method='POST', api='/core/bin/update/', func_name='bin_update'),
        API(id=12, method='POST', api='/core/bin/delete/', func_name='bin_delete'),
        API(id=13, method='GET', api='/core/stock/', func_name='stock_get'),
        API(id=14, method='POST', api='/core/stock/create/', func_name='stock_create'),
        API(id=15, method='POST', api='/core/stock/update/', func_name='stock_update'),
        API(id=16, method='POST', api='/core/stock/delete/', func_name='stock_delete'),
        API(id=17, method='GET', api='/core/capital/', func_name='capital_get'),
        API(id=18, method='POST', api='/core/capital/create/', func_name='capital_create'),
        API(id=19, method='POST', api='/core/capital/update/', func_name='capital_update'),
        API(id=20, method='POST', api='/core/capital/delete/', func_name='capital_delete'),
        API(id=21, method='GET', api='/core/supplier/', func_name='supplier_get'),
        API(id=22, method='POST', api='/core/supplier/create/', func_name='supplier_create'),
        API(id=23, method='POST', api='/core/supplier/update/', func_name='supplier_update'),
        API(id=24, method='POST', api='/core/supplier/delete/', func_name='supplier_delete'),
        API(id=25, method='GET', api='/core/customer/', func_name='customer_get'),
        API(id=26, method='POST', api='/core/customer/create/', func_name='customer_create'),
        API(id=27, method='POST', api='/core/customer/update/', func_name='customer_update'),
        API(id=28, method='POST', api='/core/customer/delete/', func_name='customer_delete'),
        API(id=29, method='GET', api='/core/asn/', func_name='asn_get'),
        API(id=30, method='POST', api='/core/asn/create/', func_name='asn_create'),
        API(id=31, method='POST', api='/core/asn/update/', func_name='asn_update'),
        API(id=32, method='POST', api='/core/asn/delete/', func_name='asn_delete'),
        API(id=33, method='GET', api='/core/dn/', func_name='dn_get'),
        API(id=34, method='POST', api='/core/dn/create/', func_name='dn_create'),
        API(id=35, method='POST', api='/core/dn/update/', func_name='dn_update'),
        API(id=36, method='POST', api='/core/dn/delete/', func_name='dn_delete'),
        API(id=37, method='GET', api='/core/purchase/', func_name='purchase_get'),
        API(id=38, method='POST', api='/core/purchase/create/', func_name='purchase_create'),
        API(id=39, method='POST', api='/core/purchase/update/', func_name='purchase_update'),
        API(id=40, method='POST', api='/core/purchase/delete/', func_name='purchase_delete'),
        API(id=41, method='GET', api='/core/bar/', func_name='bar_get'),
        API(id=42, method='POST', api='/core/bar/create/', func_name='bar_create'),
        API(id=43, method='POST', api='/core/bar/update/', func_name='bar_update'),
        API(id=44, method='POST', api='/core/bar/delete/', func_name='bar_delete'),
    ]
    API.objects.bulk_create(init_data)