# Receiver & Process

## Receiver

Location: `greaterwms/receiver.py`

The receiver defines business classes whose methods are called by the signal dispatch system.

### Structure

```python
from greaterwms.process.goods import create_googs_process, update_googs_process, delete_googs_process
from greaterwms.process.asn.status_1 import asn_status_1_process
from greaterwms.process.asn.update import asn_update_process
from greaterwms.process.asn.shelving import stock_shelving

class GoodsClass(object):
    def goods_create(self, data):
        return create_googs_process(data)

    def goods_update(self, data):
        return update_googs_process(data)

    def goods_delete(self, data):
        return delete_googs_process(data)

class ASNClass(object):
    def asn_create(self, data):
        return asn_status_1_process(data)

    def asn_update(self, data):
        return asn_update_process(data)

    def asn_delete(self, data):
        return asn_delete_process(data)

class ASNDetailClass(object):
    def asn_detail_update(self, data):
        process = data.get('data').get('process', None)
        if process == 'shelving':
            return stock_shelving(data)
```

### Method Naming Convention

The method name must match the `func_name` in the API route mapping (`api.py`):

```
api: /core/goods/create/ → func_name: goods_create
receiver.py: GoodsClass.goods_create()
```

## Process Functions

Location: `greaterwms/process/`

### Simple CRUD Example: goods.py

```python
def create_googs_process(data):
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    user_info = User.objects.filter(id=data.get('request').auth.id).first()
    goods_check = Goods.objects.filter(
        data__code=data.get('data').get('code'),
        data__department=user_info.department,
        is_delete=False
    ).first()
    if goods_check is not None:
        return detail_message_return(language, "Goods already exists")
    return msg_message_return(language, "Success Create")
```

### Complex Flow Example: ASN Create (status_1.py)

```python
def asn_status_1_process(data):
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    data.get('data')['status'] = 1
    data.get('data')['detail'] = merge_and_filter_items(data.get('data')['detail'])

    for i in data.get('data')['detail']:
        # Create ASN detail records
        ASNDetail.objects.create(data=asn_detail, project=project_name)

        # Update or create Stock
        stock_exist = Stock.objects.filter(data__goods_code=..., project=...)
        if stock_exist.exists():
            stock_list.data['total_qty'] += qty
            stock_list.data['asn_qty'] += qty
            stock_list.save()
        else:
            Stock.objects.create(data=stock_detail, project=project_name)

    data.get('data').pop('detail', None)
    return msg_message_return(language, "Success Create")
```

### Shelving Example (asn/shelving.py)

```python
def stock_shelving(data):
    # Move goods to bin
    # Update Stock: asn_qty -= qty, on_hand_qty += qty
    # Based on bin property: can_use_qty / hold_qty / damage_qty / inspection_qty
    # Create StockBin record
    # Update ASN status to 2
    return msg_message_return(language, "Success Update")
```

## Data Structure

The `data` dict passed to process functions:

```python
{
    'request': <HttpRequest>,    # Has .auth, .META, .COOKIES
    'mode': 'create',            # 'get'|'create'|'update'|'delete'
    'data': {                    # The actual business data
        'code': 'SKU001',
        'name': 'Product A',
        ...
    },
    'updated_fields': {...}      # For update mode only
}
```

## Return Values

```python
# Success
return msg_message_return(language, "Success Create")

# Business error
return detail_message_return(language, "Goods already exists")

# Auth error
return login_message_return(language, "Please Login Again")
```
