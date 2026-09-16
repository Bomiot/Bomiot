# bomiot api

## Overview

`bomiot api` creates a new sub-APP under the current project (greaterwms). Unlike the `app` command, it **automatically replaces `Example` in the templates with your APP name**, producing a ready-to-use complete API skeleton.

## Usage

```bash
bomiot api <folder>
```

- `folder`: The name of the APP to create (required, and cannot be `bomiot`)

**Registration and dispatch in cmd.py:**

```python
# new app
parser_app = subparsers.add_parser(
    'api', help='Create Bomiot API for project')
parser_app.add_argument('folder', default='',
                         nargs='?', type=str, help='Create API')
# ...
elif command == 'api':
    from bomiot.cmd.createapi import new_api
    new_api(args.folder)
```

## Source Code Analysis

`bomiot/cmd/createapi.py`:

```python
def new_api(folder: str):
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
                    copy_files(join(current_path.parent, 'newapi'), app_path)
                    apps_path = join(app_path, 'apps.py')
                    os.remove(apps_path)
                    create_project_apps_py(apps_path, project_name, sys.argv[2])
                    # ... code replacement ...
                    print(f'Create APP success {sys.argv[2]}')
            else:
                print('Invalid project mode. Please create a new project or switch to project mode.')
```

### Execution Flow

1. **Argument validation**: `folder` must not be empty and must not be `bomiot`
2. **Locate project**: hard-coded `project_name = 'greaterwms'`
3. **Mode check**: `[mode] name = project`
4. **Copy newapi templates**: copies the complete file set from `bomiot/cmd/newapi/`
5. **Generate apps.py**: calls `create_project_apps_py(apps_path, 'greaterwms', folder)`
6. **Code replacement**: iterates over `filter.py`, `models.py`, `serializers.py`, `urls.py`, `views.py` and performs replacements

### Code Replacement Logic

```python
# filter.py
'from bomiot.server.core import models' → f'from {project_name}.{app_name} import models'

# serializers.py
'from bomiot.server.core import models' → f'from {project_name}.{app_name} import models'

# urls.py
'from bomiot.server.function import example' → f'from {project_name}.{app_name} import views'

# views.py
'from bomiot.server.core import models, serializers, filter' → f'from {project_name}.{app_name} import models, serializers, filter'

# all files
'Example' → app_name.capitalize()   # class name
'example' → app_name.lower()        # variable/path name
```

## Example

```bash
# Create an API sub-APP named order
bomiot api order
```

After generation, the import in `order/views.py` becomes:
```python
from greaterwms.order import models, serializers, filter
```

Model class name changes from `Example` to `Order`, and `example` in paths becomes `order`.

## app vs api Comparison

| Feature | `bomiot app` | `bomiot api` |
|---------|-------------|--------------|
| Template source | `extends/` | `newapi/` |
| Code replacement | none, manual edit required | auto-replaces Example/import paths |
| Use case | custom skeleton, flexible | quick ready-to-use CRUD API |

## Notes

1. **Hard-coded project name**: must run from a directory containing `greaterwms/bomiotconf.ini`
2. **bomiotconf.ini must be project mode**
3. **Replacement is global**: `Example` → `Order`, `example` → `order`; any other comments containing "example" will also be replaced
4. **Run migrations after creation**: `bomiot makemigrations order` + `bomiot migrate`
