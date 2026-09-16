# Dynamic Route Registration

## Core Concept

bomiot's dynamic route registration: **you just create a bomiot app (a directory with `apps.py`, optionally a `bomiotconf.ini`), and the framework automatically adds it to `INSTALLED_APPS` and includes its `urls.py` in `urlpatterns` — no manual registration code needed.**

Three sources of bomiot apps:

| Type | Location | Marker Files | Route Prefix |
|------|----------|-------------|--------------|
| pip package plugin | site-packages | `bomiotconf.ini` mode=plugins + `apps.py` | `/<package_name>/` |
| workspace plugin | WORKING_SPACE subdir | `bomiotconf.ini` mode=plugins + `apps.py` | `/<module_name>/` |
| project sub-app | `<WORKING_SPACE>/<PROJECT_NAME>/` subdir | `apps.py` (no bomiotconf.ini needed) | `/<app_name>/` |

## 1. What Is a bomiot App

A bomiot app is a standard Django app. Minimal structure:

```
my_plugin/
├── apps.py          # Django AppConfig, required
├── urls.py          # URL definitions, required for route inclusion
├── views.py         # View functions/ViewSets
├── models.py         # Models (optional)
├── bomiotconf.ini   # Plugin marker (required for pip/workspace; not needed for project sub-apps)
└── __init__.py
```

`apps.py`:

```python
from django.apps import AppConfig

class MyPluginConfig(AppConfig):
    name = 'my_plugin'
    label = 'my_plugin'
```

`urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.my_list),
    path('create/', views.my_create),
]
```

Once placed, the framework auto-executes `path('my_plugin/', include('my_plugin.urls'))` on startup.

## 2. Auto-Registration Mechanism

### 2.1 INSTALLED_APPS (settings.py)

`bomiot/server/server/settings.py` calls `load_dynamic_apps()` on startup:

```python
def load_dynamic_apps() -> None:
    global INSTALLED_APPS
    load_apps_from_project()      # project sub-directories
    load_apps_from_working_space() # workspace plugins
    load_apps_from_packages()     # pip package plugins
```

**load_apps_from_project()** — scans `<WORKING_SPACE>/<PROJECT_NAME>/` for `apps.py`:

```python
project_path = join(WORKING_SPACE, PROJECT_NAME)
for app in listdir(project_path):
    if isfile(join(project_path, app, 'apps.py')):
        INSTALLED_APPS.append(f'{PROJECT_NAME}.{app}')
```

In greaterwms, `auth/` and `wms_process/` have `apps.py`, so they register as `greaterwms.auth` and `greaterwms.wms_process`.

**load_apps_from_working_space()** — scans WORKING_SPACE subdirs (excluding `.idea`, `.venv`, `dbs`, `logs`, `media`, `__pycache__`, `bomiot`), reads `bomiotconf.ini` for `mode=plugins`:

```python
for module_name in current_path:
    config_path = join(module_dir, 'bomiotconf.ini')
    if app_mode_config.read(config_path):
        app_mode = app_mode_config.get('mode', 'name')
        if app_mode == 'plugins' and isfile(join(module_dir, 'apps.py')):
            INSTALLED_APPS.append(module_name)
```

**load_apps_from_packages()** — scans all pip-installed packages, same `bomiotconf.ini` mode=plugins + `apps.py` check.

### 2.2 URL Auto-Inclusion (urls.py)

`bomiot/server/server/urls.py` auto-appends `include` for each discovered app:

**pip package plugins**:

```python
for module in filtered_pkg_squared:
    spec = importlib.util.find_spec(f'{module}.urls')
    if spec and hasattr(importlib.import_module(f'{module}.urls'), 'urlpatterns'):
        urlpatterns += [path(f'{module}/', include(f'{module}.urls'))]
```

**workspace plugins**:

```python
for module_name in filtered_current_path:
    if app_mode == 'plugins':
        spec = importlib.util.find_spec(f'{module_name}.urls')
        if spec and hasattr(importlib.import_module(f'{module_name}.urls'), 'urlpatterns'):
            urlpatterns += [path(f'{module_name}/', include(f'{module_name}.urls'))]
```

**project sub-apps**:

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

## 3. bomiot API Routes

Besides bomiot app auto-registration, the framework pre-defines core API routes in `bomiot/server/core/urls.py`. Each resource follows a four-action pattern:

```python
urlpatterns += [
    path(r'goods/', goods.GoodsList.as_view({"get": "list"})),
    path(r'goods/create/', goods.GoodsCreate.as_view({"post": "create"})),
    path(r'goods/update/', goods.GoodsUpdate.as_view({"post": "update"})),
    path(r'goods/delete/', goods.GoodsDelete.as_view({"post": "delete"})),
]
```

Same pattern for: `bin`, `stock`, `capital`, `supplier`, `customer`, `asn`, `dn`, `purchase`, `bar`, `fee`, `driver` — 12 business resources total. All mounted under `/core/` prefix.

## 4. Root Static Routes

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

## 5. Adding a bomiot App — Practical Guide

### Option A: Project sub-app

Create a directory under `greaterwms/`:

```
greaterwms/equipment/
├── __init__.py
├── apps.py
├── urls.py
└── views.py
```

Restart Django — framework auto-registers `greaterwms.equipment` and mounts `/equipment/` routes.

## 6. Final URL Table

| Prefix | Source | Purpose |
|--------|--------|---------|
| `/login/` `/logout/` `/checktoken/` | static | auth |
| `/md/<mddocs>` | static | markdown docs |
| `/core/goods/*` `/core/bin/*` ... | core/urls.py | core APIs |
| `/<app_name>/...` | project sub-app auto-registered | e.g. `wms_process/test/` |
| `/<module_name>/...` | workspace plugin auto-registered | local plugins |
| `/<package_name>/...` | pip package plugin auto-registered | third-party plugins |
