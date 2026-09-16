# bomiot init

## Overview

`bomiot init` (internal `create_file()` function) initializes the base files and directories of a bomiot project. It generates `pyproject.toml`, copies the `greaterwms/` project skeleton, configures `setup.ini`, creates `logs/` and `dbs/` directories, etc.

> This function is also called internally by the `project`, `app`, `api`, and `deploy` commands.

## Usage

```bash
bomiot init [folder]
```

- `folder`: Project name (optional, used for the `name` field in `pyproject.toml`; defaults to `bomiot` if not provided)

**Registration and dispatch in cmd.py:**

```python
parser_init = subparsers.add_parser(
    'init', help='Init bomiot')
parser_init.add_argument('folder', default='',
                         nargs='?', type=str, help='Init Workingspace')
# ...
elif command == 'init':
    from bomiot.cmd.init import create_file
    create_file(args.folder)
```

## Source Code Analysis

`bomiot/cmd/init.py`:

```python
def create_file(folder: str = ''):
    working_space = getcwd()
    file_path = join(Path(__file__).resolve().parent, 'file')

    # 1. Create pyproject.toml
    if not exists(join(working_space, 'pyproject.toml')):
        pyproject_source = join(file_path, 'pyproject.toml')
        if exists(pyproject_source):
            with open(pyproject_source, 'r', encoding='utf-8') as pip_file:
                deploy_pip = parse(pip_file.read())
            tool_section = deploy_pip.get('tool', {})
            poetry_section = tool_section.get('poetry', {})
            poetry_section['name'] = folder if folder else 'bomiot'
            poetry_section['version'] = '0.0.1'
            deploy_pip['tool'] = tool_section
            with open(join(working_space, 'pyproject.toml'), 'w', encoding='utf-8') as f:
                f.write(dumps(deploy_pip))

    # 2. Copy base files
    files_to_copy = [
        ('.gitignore', '.gitignore'),
        ('LICENSE', 'LICENSE'),
        ('launcher.py', 'launcher.py'),
        ('discovered_apps.py', 'discovered_apps.py'),
        ('logo.icns', 'logo.icns'),
        ('logo.png', 'logo.png'),
        ('logo.ico', 'logo.ico'),
        ('splash.png', 'splash.png'),
        ('sqlite3.def', 'sqlite3.def'),
        ('sqlite3.dll', 'sqlite3.dll'),
        ('README.md', 'README.md')
    ]
    for source_file, dest_file in files_to_copy:
        source_path = join(file_path, source_file)
        dest_path = join(working_space, dest_file)
        if not exists(dest_path) and exists(source_path):
            shutil.copy2(source_path, dest_path)

    # 3. Copy greaterwms/ directory
    greaterwms_source = join(file_path, 'greaterwms')
    greaterwms_dest = join(working_space, 'greaterwms')
    if exists(greaterwms_source) and not exists(greaterwms_dest):
        shutil.copytree(greaterwms_source, greaterwms_dest)

    # 4. Copy task.py to greaterwms/
    task_source = join(file_path, 'task.py')
    task_dest = join(working_space, 'greaterwms', 'task.py')
    if exists(task_source) and not exists(task_dest):
        shutil.copy2(task_source, task_dest)

    # 5. Copy bomiot_test/ directory
    bomiot_test_source = join(file_path, 'bomiot_test')
    bomiot_test_dest = join(working_space, 'bomiot_test')
    if exists(bomiot_test_source) and not exists(bomiot_test_dest):
        shutil.copytree(bomiot_test_source, bomiot_test_dest)

    # 6. Handle setup.ini
    setup_ini_dest = join(working_space, 'setup.ini')
    setup_ini_source = join(file_path, 'setup.ini')
    if not exists(setup_ini_dest):
        if exists(setup_ini_source):
            shutil.copy2(setup_ini_source, setup_ini_dest)
    else:
        config = ConfigParser()
        config.read(setup_ini_dest, encoding='utf-8')
        if config.has_section('project') and config.has_option('project', 'name'):
            if config.get('project', 'name').lower() != 'greaterwms':
                config.set('project', 'name', 'greaterwms')
                with open(setup_ini_dest, "wt", encoding='utf-8') as f:
                    config.write(f)
        else:
            if not config.has_section('project'):
                config.add_section('project')
            config.set('project', 'name', 'greaterwms')
            with open(setup_ini_dest, "wt", encoding='utf-8') as f:
                config.write(f)

    # 7. Create directories
    for dir_name in ['logs', 'dbs']:
        dir_path = join(working_space, dir_name)
        if not exists(dir_path):
            makedirs(dir_path, exist_ok=True)

    welcome()
    return True
```

### Execution Flow

1. **Generate `pyproject.toml`**: reads from template, sets `tool.poetry.name` (uses folder if provided, otherwise `bomiot`) and `version = '0.0.1'`
2. **Copy base files**: `.gitignore`, `LICENSE`, `launcher.py`, `discovered_apps.py`, logo icons (icns/png/ico), `splash.png`, `sqlite3.def/dll`, `README.md`
3. **Copy `greaterwms/` directory**: the built-in greaterwms project skeleton
4. **Copy `task.py`** to `greaterwms/task.py`
5. **Copy `bomiot_test/` directory**
6. **Handle `setup.ini`**:
   - If not present, copy from template
   - If present, ensure `[project] name = greaterwms`
7. **Create directories**: `logs/`, `dbs/`
8. **Call `welcome()`**: prints the welcome message

### Generated File List

```
<working_space>/
├── pyproject.toml          # Poetry config
├── .gitignore
├── LICENSE
├── launcher.py             # launcher
├── discovered_apps.py      # app discovery script
├── logo.icns / logo.png / logo.ico
├── splash.png
├── sqlite3.def / sqlite3.dll
├── README.md
├── setup.ini               # [project] name = greaterwms
├── greaterwms/             # project skeleton
│   └── task.py
├── bomiot_test/            # test directory
├── logs/
└── dbs/
```

## Example

```bash
# Initialize in current directory, pyproject.toml name defaults to bomiot
bomiot init

# Specify project name
bomiot init mywms
```

## Notes

1. **No auth_key.py**: the old version generated a JWT auth_key.py; the current version has removed it
2. **setup.ini project name is always `greaterwms`**: regardless of the folder passed
3. **pyproject.toml name**: uses folder if provided, otherwise `bomiot`
4. **Uses colorama**: output is colored (blue informational messages)
5. **Calls `welcome()`**: replaces the old ASCII art banner
