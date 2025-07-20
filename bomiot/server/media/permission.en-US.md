# Permission Control

## Introduction

- **Bomiot** permission control is implemented using Django, so it does not currently support FastAPI or Flask.

---

## Writing Permissions

- Permissions are defined in the name parameter of urls.py.
- **Bomiot** will match the permissions in the user's team based on this name.
- When permissions change, each user's permissions will automatically update accordingly.

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'example/', views.example, name="Example"),
]
```

---

## Translating Permissions

- **Bomiot** automatically translates permission names to support multi-language functionality.
- After defining the name, you only need to edit the translation content in the language folder.
- If the language file is not edited, it will directly return the defined name value.

```toml
# zh-CN.toml
[permission]
"Example"="Example"
...
```

---

## Writing Interfaces Without Permissions

- **Bomiot** automatically checks for permissions. If the name is not specified, the interface is considered to have no permission requirements and will not be saved in the database.

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'example/', views.example),
]
```

---

## Front-end

- Some users may want the frontend to control and judge pages; this can be done by modifying template pages.
- The frontend uses Pinia.
- Users can also use their own React or Angular frameworks for judgment.
- After a user logs in, a JWT token is provided to the frontend. After parsing, the user's permissions can be obtained.

```js
<script setup>
...
import { useTokenStore } from 'stores/token'
...

const tokenStore = useTokenStore()

... # You can use tokenStore.userPermissionGet to check if the user has permission, which returns a boolean value
    tokenStore.userPermissionGet('Example')
...

... # You can use tokenStore.tokenDataGet to get all user information and make judgments manually
    tokenStore.tokenDataGet
```

---

## Notes

- **Bomiot** permission system is based on DRF's permission framework.
- If writing interfaces without permission checks, pay attention to the imported permission class.

```python
# With permission checks
from bomiot.server.core.permission import CorePermission

# Without permission checks
from bomiot.server.core.permission import NormalPermission

```

---

## Customization

- The main permission functions of **Bomiot** cannot be modified.
- However, you can modify the Permission model to achieve custom functionality.
- As long as data is stored in the Permission database, permission control can be implemented. Therefore, in theory, FastAPI and Flask can also support permission control.
