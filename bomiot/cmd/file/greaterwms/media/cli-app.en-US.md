# bomiot app

## Overview

`bomiot app` creates a new sub-APP under the current project (greaterwms). It copies a standard set of files from the bomiot framework's template directory to the new app folder, then generates the corresponding `apps.py`.

## Usage

```bash
bomiot app <folder>
```

- `folder`: The name of the APP to create (required, and cannot be `bomiot`)

**Registration and dispatch in cmd.py:**

```python
# new app
parser_app = subparsers.add_parser(
    'app', help='Create APP for project')
parser_app.add_argument('folder', default='',
                         nargs='?', type=str, help='Create APP')
# ...
elif command == 'app':
    from bomiot.cmd.createapp import new_app
    new_app(args.folder)
```

## Source Code Analysis

`bomiot/cmd/createapp.py`:

```python
def new_app(folder: str):
    if len(sys.argv) < 3:
        print('Please enter your app name')
    else:
        if sys.argv[2] == 'bomiot':
            print('Invalid app name. Please enter a valid app name.')
        else:
            current_path = Path(__file__).resolve()
            project_name = 'greaterwms'
            project_path = join(getcwd(), project_name)
            project_config = ConfigParser()
            project_config.read(join(project_path, 'bomiotconf.ini'), encoding='utf-8')
            if project_config.get('mode', 'name') == 'project':
                app_path = join(project_path, sys.argv[2])
                if exists(app_path):
                    print('App directory already exists')
                else:
                    makedirs(app_path)
                    copy_files(join(current_path.parent, 'extends'), app_path)
                    apps_path = join(app_path, 'apps.py')
                    os.remove(apps_path)
                    create_project_apps_py(apps_path, project_name, sys.argv[2])
                    print(f'Create APP success {sys.argv[2]}')
            else:
                print('Invalid project mode. Please create a new project or switch to project mode.')
```

### Execution Flow

1. **Argument validation**: `folder` must not be empty and must not be `bomiot`
2. **Locate project**: hard-coded `project_name = 'greaterwms'`, reads `./greaterwms/bomiotconf.ini`
3. **Mode check**: verifies `[mode] name = project`, otherwise reports "Invalid project mode"
4. **Create directory**: creates `greaterwms/<folder>/`
5. **Copy templates**: copies standard files from `bomiot/cmd/extends/` (admin.py, apps.py, filter.py, models.py, serializers.py, tests.py, urls.py, views.py, migrations/)
6. **Generate apps.py**: removes the template's apps.py and calls `create_project_apps_py(apps_path, 'greaterwms', folder)` to generate the correct AppConfig

### extends Template Contents

```
extends/
├── __init__.py
├── admin.py
├── apps.py            (will be overwritten)
├── filter.py
├── migrations/
│   └── __init__.py
├── models.py
├── serializers.py
├── tests.py
├── urls.py
└── views.py
```

These templates reference bomiot's built-in `Example` model (`from bomiot.server.core import models`); after creation you must manually change them to your own model definitions.

## Example

```bash
# Create a sub-APP named myapp under greaterwms
bomiot app myapp
```

Output:
```
Create APP success myapp
```

Generated structure:
```
greaterwms/
└── myapp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── filter.py
    ├── migrations/
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Notes

1. **Hard-coded project name**: `project_name = 'greaterwms'`, you must run from a directory containing `greaterwms/bomiotconf.ini`
2. **bomiotconf.ini must be project mode**: otherwise prints "Invalid project mode"
3. **No code replacement**: unlike the `api` command, `app` only copies templates without auto-replacing `Example` → your class name, manual editing required
4. **Difference from api**:
   - `app`: copies `extends/` templates, no code replacement, good for quick skeleton
   - `api`: copies `newapi/` templates, auto-replaces `Example` with your APP name, ready to use
