# 权限控制

## 介绍

- **Bomiot** 的权限控制是用 Django 来实现的，所以目前不支持 FastAPI 和 Flask（理论上可扩展）。

---

## 编写权限

- 权限定义在 `urls.py` 的 `name` 参数中。
- **Bomiot** 会根据这个 `name` 来匹配用户团队中的权限。
- 权限发生变化时，每个用户的权限也会自动变化。

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'example/', views.example, name="Example"),  # 通过 name 定义权限
]
```

---

## 翻译权限

- **Bomiot** 会自动翻译权限名称，从而实现多语言支持。
- 编写过 `name` 后，只需在 `language` 文件夹下编辑翻译内容即可。
- 如果没有编辑 language 文件，则直接返回定义的 `name` 值。

```toml
[permission]
"Example" = "例子"
...
```

---

## 无权限接口编写

- **Bomiot** 会自动查找权限，如果不写这个 `name`，就视为无权限接口，将不会被数据库保存。

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'example/', views.example),  # 不写 name 表示无权限要求
]
```

---

## 前端使用

- 部分用户想要前端进行页面控制和判断，可以修改 template 页面。
- 前端使用的是 Pinia。
- 用户也可以自行使用 React 和 Angular 进行判断。
- 用户登录后，会给到前端一个 JWT token，解析后就可以得到用户的权限。

```js
<script setup>
...
import { useTokenStore } from 'stores/token'
...

const tokenStore = useTokenStore()

// 使用 tokenStore.userPermissionGet 检查用户是否有权限，返回布尔值
tokenStore.userPermissionGet('Example')

// 使用 tokenStore.tokenDataGet 获取用户全部信息，自行判断
tokenStore.tokenDataGet
...
```

---

## 注意事项

- **Bomiot** 的权限系统走的是 DRF 的 permission 框架。
- 如果要编写无权限接口，注意导入的 permission 类。

```python
# 有权限判断
from bomiot.server.core.permission import CorePermission

# 无权限判断
from bomiot.server.core.permission import NormalPermission
```

---

## 自定义

- **Bomiot** 主体权限功能不可以修改。
- 不过你可以修改 `Permission` 这个模型来达到自定义功能。
- 只要数据进入 `Permission` 数据库，就可以实现权限控制，所以 FastAPI 和 Flask 理论上也可以支持权限控制。
