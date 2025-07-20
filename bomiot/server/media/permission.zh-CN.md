# 权限控制

## 介绍

- **Bomiot** 的权限控制是用django来控制的，所以现在暂时不支持FastAPI和Flask

---

## 编写权限

- 权限是写在urls.py的name里
- **Bomiot** 会根据这个name来匹配用户team中的权限
- 权限发生变化，每个用户也会自己变化权限

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'example/', views.example, name="Example"),
]
```

---

## 翻译权限

- **Bomiot** 会自动翻译权限名称，从而做到多语言支持
- 编写过name后，只需要在language文件夹下，编辑翻译内容即可
- 如果没有编辑language文件，则直接返回你定义的这个name名称

```toml
# zh-CN.toml
[permission]
"Example"="例子"
...
```

---

## 无权限接口编写

- **Bomiot** 会自动查找权限，如果不写这个name，就视为无权限接口，将不会被数据库保存

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'example/', views.example),
]
```

---

## 前端使用

- 部分用户想要前端进行页面控制和判断，就可以修改template页面
- 前端使用的是pinia
- 用户也可以自行使用自己的React和Angular，进行判断
- 用户登入后，会给到前端一个jwt的token，解析后，就可以得到用户的权限

```js
<script setup>
...
import { useTokenStore } from 'stores/token'
...

const tokenStore = useTokenStore()

... # 可以通过tokenStore.userPermissionGet来获取用户是否有权限，返回的是布尔值
    tokenStore.userPermissionGet('Example')
...

... # 可以通过tokenStore.tokenDataGet获取用户的全部信息，再自行判断
    tokenStore.tokenDataGet
...

```

---

## 注意事项

- **Bomiot** 的权限系统走的是Drf的permission
- 如果要编写无权限接口，注意导入的permission类

```python
# 有权限判断
from bomiot.server.core.permission import CorePermission

# 无权限判断
from bomiot.server.core.permission import NormalPermission

```

---

## 自定义

- **Bomiot** 主体权限功能不可以修改
- 不过你可以修改Permission这个Models来达到自定义功能
- 只要数据进入Permission数据库，就可以实现权限控制，所以FastAPI和Flask，理论上也是可以支持权限控制
