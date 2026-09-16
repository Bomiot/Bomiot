# API Development

## Introduction

Bomiot provides RESTful APIs based on Django REST Framework. You can quickly build endpoints with models, serializers, and views, and take over or extend existing APIs through the signal mechanism.

---

## Create an API

### 1. Define a Model

Define your model in the app's `models.py`, preferably inheriting `CoreModel`:

```python
from bomiot.server.core.model import CoreModel

class Goods(CoreModel):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)
```

`CoreModel` already includes common fields like `id`, `created_time`, `updated_time`, `is_delete`.

### 2. Create a Serializer

Define a serializer in `serializers.py`:

```python
from rest_framework import serializers
from .models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
```

### 3. Create a View

Use `ModelViewSet` in `views.py`:

```python
from rest_framework.viewsets import ModelViewSet
from .models import Goods
from .serializers import GoodsSerializer

class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.filter(is_delete=False)
    serializer_class = GoodsSerializer
```

### 4. Register Routes

Register in `urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoodsViewSet

router = DefaultRouter()
router.register('goods', GoodsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

---

## Automatic URL Discovery

Bomiot automatically scans each app's `urls.py` under `greaterwms/` and mounts it under the corresponding prefix. For example, an app named `myapp` has its routes mounted at `/myapp/`.

---

## Auth & Permissions

All APIs require JWT auth by default. Include the header:

```
token: <jwt_token>
```

Admins created via `bomiot initadmin` have full permissions; regular users can be granted endpoint permissions on the Permission page.

---

## Pagination

List endpoints support pagination by default:

| Param | Description |
|-------|-------------|
| `page` | Page number (starts at 1) |
| `max_page` | Items per page |

Response:

```json
{
  "results": [...],
  "count": 100
}
```

---

## Take Over APIs via Signals

Use data signals in `receiver.py` to customize query logic without modifying views:

```python
from bomiot.server.core.signal import bomiot_signals

def custom_filter(sender, **kwargs):
    pass

bomiot_signals.send(sender=custom_filter, msg={
    'models': 'Goods',
    'data': {
        'filter': {'quantity__gt': 0}
    }
})
```

---

## Frontend Call

Use the wrapped methods from `boot/axios.js`:

```js
import { get, post } from 'boot/axios'

const list = await get({ url: 'myapp/goods/', params: { page: 1, max_page: 20 } })
const item = await post({ url: 'myapp/goods/', body: { name: 'A', code: 'A001' } })
```
