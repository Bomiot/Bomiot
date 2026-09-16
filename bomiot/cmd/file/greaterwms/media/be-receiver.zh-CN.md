# Receiver 与 Process

`receiver.py` 是项目级别的业务接入点，负责接收 bomiot 信号分发并调用 `process/` 下的具体业务函数。框架通过 AST 动态定位方法，业务逻辑全部在项目代码中实现。

## 1. Receiver 类与分发方法

`greaterwms/receiver.py` 定义多个业务类，每个类的方法名与 `mode` + sender 类名拼接而成（如 `goods_create`）一一对应：

```python
from bomiot.server.core.message import msg_message_return, detail_message_return, login_message_return
from bomiot.server.core.models import Example
from bomiot.server.core.utils import queryset_to_dict, dynamic_import_and_call
from django.core.cache import cache
from greaterwms.process.goods import create_googs_process, update_googs_process, delete_googs_process
from greaterwms.process.bin import get_bin_process, create_bin_process, update_bin_process, delete_bin_process
from greaterwms.process.supplier import create_supplier_process, update_supplier_process, delete_supplier_process
from greaterwms.process.customer import create_customer_process, update_customer_process, delete_customer_process
from greaterwms.process.asn.status_1 import asn_status_1_process
from greaterwms.process.asn.update import asn_update_process
from greaterwms.process.asn.delete import asn_delete_process
from greaterwms.process.dn.status_1 import dn_status_1_process
from greaterwms.process.dn.update import dn_update_process
from greaterwms.process.dn.delete import dn_delete_process
from greaterwms.process.asn.shelving import stock_shelving

class GoodsClass(object):
    def goods_create(self, data):
        context = create_googs_process(data)
        return context

    def goods_update(self, data):
        context = update_googs_process(data)
        return context

    def goods_delete(self, data):
        context = delete_googs_process(data)
        return context


class BinClass(object):
    def bin_get(self, data):
        context = get_bin_process(data)
        return context

    def bin_create(self, data):
        context = create_bin_process(data)
        return context

    def bin_update(self, data):
        context = update_bin_process(data)
        return context

    def bin_delete(self, data):
        context = delete_bin_process(data)
        return context


class SupplierClass(object):
    def supplier_create(self, data): ...
    def supplier_update(self, data): ...
    def supplier_delete(self, data): ...


class CustomerClass(object):
    def customer_create(self, data): ...
    def customer_update(self, data): ...
    def customer_delete(self, data): ...


class ASNClass(object):
    def asn_create(self, data):
        context = asn_status_1_process(data)
        return context

    def asn_update(self, data):
        context = asn_update_process(data)
        return context

    def asn_delete(self, data):
        context = asn_delete_process(data)
        return context


class ASNDetailClass(object):
    def asn_detail_update(self, data):
        process = data.get('data').get('process', None)
        if process == 'shelving':
            context = stock_shelving(data)
            return context


class DNClass(object):
    def dn_create(self, data):
        context = dn_status_1_process(data)
        return context

    def dn_update(self, data):
        context = dn_update_process(data)
        return context

    def dn_delete(self, data):
        context = dn_delete_process(data)
        return context
```

方法命名规则：`{model}_{action}`，与 `bomiot/server/core/utils.receiver_callback` 中根据 `mode` 拼接出的方法名匹配。`ASNDetailClass.asn_detail_update` 还会判断 `data['data']['process'] == 'shelving'` 来决定是否触发上架流程。

## 2. Process 函数

`greaterwms/process/` 目录组织业务校验与库存操作：

```
process/
├── goods.py
├── bin.py
├── supplier.py
├── customer.py
├── asn/
│   ├── status_1.py    # 创建 ASN
│   ├── update.py
│   ├── delete.py
│   └── shelving.py    # 上架
└── dn/
    ├── status_1.py
    ├── update.py
    └── delete.py
```

### 2.1 Goods Process（`greaterwms/process/goods.py`）

```python
from bomiot.server.core.message import msg_message_return, detail_message_return, login_message_return, others_message_return
from bomiot.server.core.models import Goods
from bomiot.server.core.utils import all_fields_empty
from django.contrib.auth import get_user_model

User = get_user_model()


def create_googs_process(data):
    """
    Process for creating goods.
    """
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    user_info = User.objects.filter(id=data.get('request').auth.id).first()
    goods_check = Goods.objects.filter(data__code=data.get('data').get('code'),
                                       data__department=user_info.department,
                                       is_delete=False).first()
    if goods_check is not None:
        return detail_message_return(language, "Goods already exists")
    return msg_message_return(language, "Success Create")


def update_googs_process(data):
    """
    Process for updating goods.
    """
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    user_info = User.objects.filter(id=data.get('request').auth.id).first()
    update_field_check = all_fields_empty(data.get('updated_fields'))
    if update_field_check is False:
        goods_check = Goods.objects.filter(data__code=data.get('data').get('code'),
                                           data__department=user_info.department,
                                           is_delete=False).exclude(id=data.get('data').get('id')).first()
        if goods_check is not None:
            return detail_message_return(language, "Goods already exists")
    return msg_message_return(language, "Success Update")


def delete_googs_process(data):
    """
    Process for updating goods.
    """
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    user_info = User.objects.filter(id=data.get('request').auth.id).first()
    goods_check = Goods.objects.filter(id=data.get('data').get('id'),
                                       data__department=user_info.department,
                                       is_delete=False).first()
    if goods_check is None:
        return detail_message_return(language, "Goods does not exists")
    return msg_message_return(language, "Success Delete")
```

校验逻辑：创建时根据 `code + department` 去重；更新时结合 `updated_fields` 判断是否有冲突；删除时检查记录是否存在。返回 `msg_message_return` 表示放行，`detail_message_return` 表示拦截。

### 2.2 ASN Status 1（`greaterwms/process/asn/status_1.py`）

ASN 创建流程会生成 ASNDetail 记录并更新 Stock 库存：

```python
from bomiot.server.core.message import msg_message_return, detail_message_return
from bomiot.server.core.models import Customer
from bomiot.server.core.utils import merge_and_filter_items, all_fields_empty
from django.contrib.auth import get_user_model
from bomiot.server.core.models import ASNDetail
from bomiot.server.core.models import Stock

User = get_user_model()


def asn_status_1_process(data):
    """
    Process for asn status 1.
    """
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    data.get('data')['status'] = 1
    data.get('data')['detail'] = merge_and_filter_items(data.get('data')['detail'])
    for i in data.get('data')['detail']:
        asn_detail = {
            'asn_id': data.get('data').get('asn_id'),
            'goods_code': i.get('selected').get('label'),
            'goods_name': i.get('selected').get('name'),
            'asn_qty': float(i.get('qty')),
            'shelving_qty': 0,
            'department': data.get('request').auth.department,
            'status': 1,
        }
        ASNDetail.objects.create(data=asn_detail, project=data.get('request').META.get('HTTP_PROJECT', 'bomiot'))

        stock_exist = Stock.objects.filter(data__goods_code=i.get('selected').get('label'),
                                           data__department=data.get('request').auth.department,
                                           project=data.get('request').META.get('HTTP_PROJECT', 'bomiot'))
        if stock_exist.exists():
            stock_list = stock_exist.first()
            stock_data_list = stock_list.data
            stock_data_list['total_qty'] = float(stock_data_list.get('total_qty', 0)) + float(i.get('qty'))
            stock_data_list['asn_qty'] = float(stock_data_list.get('asn_qty', 0)) + float(i.get('qty'))
            stock_list.data = stock_data_list
            stock_list.save()
        else:
            stock_detail = {
                'goods_code': i.get('selected').get('label'),
                'goods_name': i.get('selected').get('name'),
                'total_qty': float(i.get('qty')),
                'on_hand_qty': 0,
                'can_use_qty': 0,
                'hold_qty': 0,
                'inspection_qty': 0,
                'damage_qty': 0,
                'allocated_qty': 0,
                'asn_qty': float(i.get('qty')),
                'dn_qty': 0,
                'department': data.get('request').auth.department,
            }
            Stock.objects.create(data=stock_detail, project=data.get('request').META.get('HTTP_PROJECT', 'bomiot'))
    data.get('data').pop('detail', None)
    return msg_message_return(language, "Success Create")
```

要点：
- `merge_and_filter_items` 合并 detail 中重复商品行。
- 已存在 Stock 时累加 `total_qty` 和 `asn_qty`；不存在则创建初始库存（`on_hand_qty=0`，待上架后再转移）。
- `Stock` 和 `ASNDetail` 都使用 `DataCoreModel`，操作时必须带上 `project` 与 `data__department` 进行隔离。

### 2.3 ASN Shelving（`greaterwms/process/asn/shelving.py`）

上架流程将商品移入库位，并按库位属性更新对应库存字段：

```python
from bomiot.server.core.message import msg_message_return, detail_message_return
from bomiot.server.core.models import Customer
from bomiot.server.core.utils import merge_and_filter_items, all_fields_empty
from django.contrib.auth import get_user_model
from bomiot.server.core.models import ASN, ASNDetail, Bin, Stock, StockBin

User = get_user_model()

property_list = ['Normal', 'Hold', 'Damage', 'Inspection']


def stock_shelving(data):
    """
    Process for asn detail shelving to bin.
    """
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    project = data.get('request').META.get('HTTP_PROJECT', 'bomiot')
    shelving_to_bin = data.get('data').get('selected').get('label')
    asn_id = data.get('data').get('asn_id')
    goods_code = data.get('data').get('goods_code')
    qty = float(data.get('data').get('qty', 0))
    bin_property = Bin.objects.filter(data__name=shelving_to_bin, project=project, is_delete=False).first().data.get('property', 'Normal')
    asn_status_change_data = ASN.objects.filter(data__asn_id=asn_id, project=project, is_delete=False).first()
    asn_status_change_data.data['status'] = 2
    stock_list = Stock.objects.filter(data__goods_code=goods_code, project=project, is_delete=False).first()
    stock_list.data['asn_qty'] = stock_list.data.get('asn_qty', 0) - qty
    stock_list.data['on_hand_qty'] = stock_list.data.get('on_hand_qty', 0) + qty
    if bin_property == 'Normal':
        stock_list.data['can_use_qty'] = stock_list.data.get('can_use_qty', 0) + qty
    if bin_property == 'Hold':
        stock_list.data['hold_qty'] = stock_list.data.get('hold_qty', 0) + qty
    if bin_property == 'Damage':
        stock_list.data['damage_qty'] = stock_list.data.get('damage_qty', 0) + qty
    if bin_property == 'Inspection':
        stock_list.data['inspection_qty'] = stock_list.data.get('inspection_qty', 0) + qty
    stock_bin_data = {
        'bin_name': shelving_to_bin,
        'goods_code': goods_code,
        'goods_name': data.get('data').get('goods_name'),
        'on_hand_qty': qty,
        'allocated_qty': 0,
        'department': data.get('request').auth.department,
    }
    StockBin.objects.create(data=stock_bin_data, project=project)
    stock_list.save()
    asn_status_change_data.save()
    data.get('data')['shelving_qty'] = data.get('data')['shelving_qty'] + qty
    data.get('data').pop('process', None)
    data.get('data').pop('selected', None)
    data.get('data').pop('qty', None)
    return msg_message_return(language, "Success Update")
```

业务要点：
- `Bin.property` 决定上架后的数量去向：`Normal → can_use_qty`、`Hold → hold_qty`、`Damage → damage_qty`、`Inspection → inspection_qty`。
- `Stock.asn_qty` 同步扣减，`Stock.on_hand_qty` 同步增加，确保入库与在途数量平衡。
- 新建 `StockBin` 记录具体库位库存，ASN 主单 `status` 推进到 `2`。

## 3. Process 数据结构与返回约定

`data` 入参统一结构：

| 字段 | 说明 |
|------|------|
| `request` | DRF Request 对象，可读取 `auth`、`META`、`COOKIES` |
| `mode` | `'get'` / `'create'` / `'update'` / `'delete'` |
| `data` | 业务数据，即 ViewSet 中的 `self.request.data` |
| `updated_fields` | 仅 update：`{field: (old, new)}` 变更对比 |
| `query_params` | 仅 get：原始查询参数 dict |

返回值：
- `msg_message_return(language, "Success ...")`：返回 `{"msg": "..."}`，ViewSet 据此提交事务。
- `detail_message_return(language, "...")`：返回 `{"detail": "..."}`，ViewSet 直接返回 4xx。
- `login_message_return(language, "...")`：返回 `{"login": "..."}`，强制重新登录。
- `get` 模式可返回 `[(key, value), ...]`，被合并入分页响应。

## 4. 与框架信号链路

```
GoodsCreate.create
   └── bomiot_data_signals.send_robust(mode='create', data=...)
         └── receiver_callback(data, 'goods_create')
               └── check_method_in_file_by_ast → GoodsClass
                     └── GoodsClass().goods_create(data)
                           └── create_googs_process(data)
                                 └── 校验通过 → {"msg": "Success Create"}
                                     → ViewSet 执行 Goods.objects.create(...)
```

任何 process 抛出异常会被 `send_robust` 捕获，ViewSet 在事务内 `raise` 后回滚，确保 Stock、ASNDetail、StockBin 同步一致性。
