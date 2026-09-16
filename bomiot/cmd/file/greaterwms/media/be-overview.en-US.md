# Backend Architecture Overview

## Framework Structure

bomiot is a pip-installed Django framework. GreaterWMS is the project built on top of it.

```
bomiot (pip package)
├── server/
│   ├── settings.py        # Dynamic Django settings
│   ├── urls.py            # Root URL router
│   ├── views.py           # Login, index, md serving, permission init
│   ├── core/              # Core framework
│   │   ├── models.py      # Base models (CoreModel, DataCoreModel)
│   │   ├── handler.py     # Example ViewSets (signal dispatch pattern)
│   │   ├── views.py       # User/Team/Department/File ViewSets
│   │   ├── urls.py        # Core + business URL patterns
│   │   ├── middlewares.py # JWT auth middleware
│   │   ├── auth.py        # DRF authentication class
│   │   ├── jwt_auth.py    # JWT create/parse
│   │   ├── permission.py  # Permission classes
│   │   ├── page.py        # Pagination with signal dispatch
│   │   ├── throttle.py    # IP-based rate limiting
│   │   ├── scheduler.py   # APScheduler job manager
│   │   ├── observer.py    # File system watcher
│   │   ├── signal.py      # Django signals
│   │   ├── utils.py       # receiver_callback, dynamic import
│   │   └── serializers.py # DRF serializers
│   └── function/          # Business ViewSets
│       ├── goods.py, bin.py, stock.py, ...
```

```
greaterwms (project workspace)
├── setup.ini              # Project configuration
├── bomiotconf.ini         # [mode] name = project
├── api.py                 # API route → function mapping
├── receiver.py            # Business process classes (signal receivers)
├── task.py                # Scheduled task example
├── process/               # Business logic functions
│   ├── goods.py, bin.py, supplier.py, ...
│   └── asn/, dn/          # Sub-modules for complex flows
├── auth/                  # Auth views
├── language/              # i18n .toml files
└── templates/             # Frontend (Vue/Quasar)
```

## Key Design Patterns

### 1. Signal-Based Dispatch

ViewSets don't contain business logic. They send Django signals:

```python
responses = bomiot_data_signals.send_robust(
    sender=self.__class__,
    request=self.request,
    mode='create',
    data=data
)
```

The signal is received by `receiver_callback()` which dynamically imports the project's `receiver.py` and calls the matching method.

### 2. Dynamic App Discovery

`settings.py` auto-scans:
- Installed pip packages (with `bomiotconf.ini` mode=plugins)
- Workspace directories (with `bomiotconf.ini` mode=plugins)
- Project subdirectories (with `apps.py`)

### 3. JSON Data Field

All business models use `data = JSONField()`:

```python
class Goods(DataCoreModel):
    data = models.JSONField()
```

Flexible schema — no migrations needed for new fields. Query via `data__field` syntax.

### 4. Project Isolation

`DataCoreModel` has a `project` field. All queries filter by it:

```python
project_name = self.request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)
```

### 5. Soft Delete

`is_delete` field. Queries always filter `is_delete=False`. Delete sets `is_delete=True`.
