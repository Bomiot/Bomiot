# 动态路由注册

## 核心概念

bomiot 框架的动态路由注册机制：**你只需要创建一个 bomiot app（一个含 `apps.py` 的目录，可选放 `bomiotconf.ini`），框架启动时会自动把它纳入 `INSTALLED_APPS` 并把它的 `urls.py` 挂到 `urlpatterns` 里——无需手动改任何注册代码。**

三种 bomiot app 来源：

| 类型 | 位置 | 标识文件 | 路由前缀 |
|------|------|----------|----------|
| pip 包插件 | site-packages 中的发行包 | `bomiotconf.ini` `[mode] name = plugins` + `apps.py` | `/<package_name>/` |
| 工作空间插件 | WORKING_SPACE 下的子目录 | `bomiotconf.ini` `[mode] name = plugins` + `apps.py` | `/<module_name>/` |
| 主工程子 app | `<WORKING_SPACE>/<PROJECT_NAME>/` 下的子目录 | `apps.py`（无需 bomiotconf.ini） | `/<app_name>/` |

## 1. 什么是 bomiot app

一个 bomiot app 就是一个标准 Django app，最小结构：

```
my_plugin/
├── apps.py          # Django AppConfig，必须存在
├── urls.py          # 路由定义，必须存在才能被包含
├── views.py         # 视图函数/ViewSet
├── models.py         # 模型（可选）
├── bomiotconf.ini   # 插件标识（pip 包/工作空间插件必须；主工程子 app 不需要）
└── __init__.py
```

`apps.py` 示例：

```python
from django.apps import AppConfig

class MyPluginConfig(AppConfig):
    name = 'my_plugin'
    label = 'my_plugin'
```

`urls.py` 示例：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.my_list),
    path('create/', views.my_create),
]
```

这个 app 放好后，框架启动时会自动执行 `path('my_plugin/', include('my_plugin.urls'))`，路由就可访问了。

## 2. 自动注册机制

### 2.1 INSTALLED_APPS 注册（settings.py）

`bomiot/server/server/settings.py` 启动时调用 `load_dynamic_apps()`：

```python
def load_dynamic_apps() -> None:
    global INSTALLED_APPS
    load_apps_from_project()      # 主工程子目录
    load_apps_from_working_space() # 工作空间插件
    load_apps_from_packages()     # pip 包插件
```

**load_apps_from_project()** — 扫描 `<WORKING_SPACE>/<PROJECT_NAME>/` 下所有子目录，有 `apps.py` 就注册：

```python
project_path = join(WORKING_SPACE, PROJECT_NAME)
for app in listdir(project_path):
    if isfile(join(project_path, app, 'apps.py')):
        INSTALLED_APPS.append(f'{PROJECT_NAME}.{app}')
```

greaterwms 工程下 `auth/` 和 `wms_process/` 含 `apps.py`，因此注册为 `greaterwms.auth`、`greaterwms.wms_process`。

**load_apps_from_working_space()** — 扫描 WORKING_SPACE 下子目录（排除 `.idea`、`.venv`、`dbs`、`logs`、`media`、`__pycache__`、`bomiot`），读 `bomiotconf.ini` 确认 `mode=plugins`：

```python
for module_name in current_path:
    config_path = join(module_dir, 'bomiotconf.ini')
    if app_mode_config.read(config_path):
        app_mode = app_mode_config.get('mode', 'name')
        if app_mode == 'plugins' and isfile(join(module_dir, 'apps.py')):
            INSTALLED_APPS.append(module_name)
```

**load_apps_from_packages()** — 扫描所有 pip 安装的发行包，同样按 `bomiotconf.ini` 的 `mode=plugins` + `apps.py` 注册。

### 2.2 URL 自动包含（urls.py）

`bomiot/server/server/urls.py` 在根 `urlpatterns` 末尾，按相同三个来源自动追加 `include`：

**pip 包插件**：

```python
for module in filtered_pkg_squared:
    spec = importlib.util.find_spec(f'{module}.urls')
    if spec and hasattr(importlib.import_module(f'{module}.urls'), 'urlpatterns'):
        urlpatterns += [path(f'{module}/', include(f'{module}.urls'))]
```

**工作空间插件**：

```python
for module_name in filtered_current_path:
    if app_mode == 'plugins':
        spec = importlib.util.find_spec(f'{module_name}.urls')
        if spec and hasattr(importlib.import_module(f'{module_name}.urls'), 'urlpatterns'):
            urlpatterns += [path(f'{module_name}/', include(f'{module_name}.urls'))]
```

**主工程子 app**：

```python
exclude_dirs = {'__pycache__', 'static', 'media', 'templates', 'language',
                'migrations', 'tests', 'test', 'docs', 'documentation'}
url_include_list = [p for p in root_path.iterdir()
                    if p.is_dir() and p.name not in exclude_dirs]
for url in url_include_list:
    include_path = f'{module_name}.{app_name}.urls'
    spec = importlib.util.find_spec(include_path)
    if spec and hasattr(importlib.import_module(include_path), 'urlpatterns'):
        urlpatterns.append(path(f'{app_name}/', include(include_path)))
```

## 3. bomiot API 路由

除了 bomiot app 自动注册，框架还在 `bomiot/server/core/urls.py` 中预置了核心 API 路由，每个资源固定四元组：

```python
urlpatterns += [
    path(r'goods/', goods.GoodsList.as_view({"get": "list"})),
    path(r'goods/create/', goods.GoodsCreate.as_view({"post": "create"})),
    path(r'goods/update/', goods.GoodsUpdate.as_view({"post": "update"})),
    path(r'goods/delete/', goods.GoodsDelete.as_view({"post": "delete"})),
]
```

同样模式应用于 `bin`、`stock`、`capital`、`supplier`、`customer`、`asn`、`dn`、`purchase`、`bar`、`fee`、`driver`，共 12 个业务资源。这些路由通过 `path('core/', include('bomiot.server.core.urls'))` 统一挂载在 `/core/` 前缀下。

## 4. 根路由静态部分

```python
urlpatterns = [
    path('', views.IndexTemplateView.as_view()),
    path('login/', views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('checktoken/', views.check_token, name='check_token'),
    path('md/<str:mddocs>', views.mdurl, name='markdown'),
    path('core/', include('bomiot.server.core.urls')),
]
```

## 5. 新增 bomiot app 实操

### 方式一：主工程下新增子 app

在 `greaterwms/` 下建目录：

```
greaterwms/equipment/
├── __init__.py
├── apps.py
├── urls.py
└── views.py
```

重启 Django，框架自动注册 `greaterwms.equipment` 并挂载 `/equipment/` 路由。

## 6. 最终 URL 表

| 前缀 | 来源 | 用途 |
|------|------|------|
| `/login/` `/logout/` `/checktoken/` | 静态 | 鉴权 |
| `/md/<mddocs>` | 静态 | markdown 文档 |
| `/core/goods/*` `/core/bin/*` ... | core/urls.py | 核心 API |
| `/<app_name>/...` | 主工程子 app 自动注册 | 例如 `wms_process/test/` |
| `/<module_name>/...` | 工作空间插件自动注册 | 本地插件 |
| `/<package_name>/...` | pip 包插件自动注册 | 第三方插件 |
