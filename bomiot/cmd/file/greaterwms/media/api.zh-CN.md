# API 开发

## 简介

Bomiot 基于 Django REST Framework 提供 RESTful API，支持通过模型、序列化器和视图快速构建接口。同时可通过信号机制对现有 API 进行接管和扩展。

---

## 创建 API

### 1. 定义模型

在应用的 `models.py` 中定义数据模型，推荐继承 `CoreModel` 基类：

```python
from bomiot.server.core.model import CoreModel

class Goods(CoreModel):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)
```

`CoreModel` 已包含 `id`、`created_time`、`updated_time`、`is_delete` 等通用字段。

### 2. 创建序列化器

在 `serializers.py` 中定义序列化器：

```python
from rest_framework import serializers
from .models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
```

### 3. 创建视图

在 `views.py` 中使用 `ModelViewSet`：

```python
from rest_framework.viewsets import ModelViewSet
from .models import Goods
from .serializers import GoodsSerializer

class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.filter(is_delete=False)
    serializer_class = GoodsSerializer
```

### 4. 注册路由

在 `urls.py` 中注册：

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

## API 自动发现

Bomiot 会自动扫描 `greaterwms/` 下各应用的 `urls.py` 并挂载到对应前缀。例如应用名 `myapp` 的路由会自动挂载到 `/myapp/` 下。

---

## 认证与权限

所有 API 默认需要 JWT 认证。请求头需携带：

```
token: <jwt_token>
```

通过 `bomiot.initadmin` 创建的管理员拥有全部权限，普通用户可在「权限」页面分配接口权限。

---

## 分页

列表接口默认支持分页，请求参数：

| 参数 | 说明 |
|------|------|
| `page` | 页码（从 1 开始） |
| `max_page` | 每页条数 |

响应结构：

```json
{
  "results": [...],
  "count": 100
}
```

---

## 通过信号接管 API

使用 `receiver.py` 中的数据信号，可以在不修改视图代码的情况下自定义查询逻辑：

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

## 前端调用

前端通过 `boot/axios.js` 封装的方法调用：

```js
import { get, post } from 'boot/axios'

const list = await get({ url: 'myapp/goods/', params: { page: 1, max_page: 20 } })
const item = await post({ url: 'myapp/goods/', body: { name: 'A', code: 'A001' } })
```
