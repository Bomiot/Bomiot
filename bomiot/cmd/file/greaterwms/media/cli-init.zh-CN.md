# bomiot init

## 概述

`bomiot init` 命令（内部 `create_file()` 函数）用于初始化 bomiot 项目的基础文件和目录。它会生成 `pyproject.toml`、复制 `greaterwms/` 项目骨架、配置 `setup.ini`、创建 `logs/` 和 `dbs/` 目录等。

> 此函数也被 `project`、`app`、`api`、`deploy` 命令内部调用。

## 用法

```bash
bomiot init [folder]
```

- `folder`：项目名称（可选，用于 `pyproject.toml` 的 name 字段，不传则默认 `bomiot`）

**cmd.py 中的注册与分发：**

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

## 源码分析

`bomiot/cmd/init.py`：

```python
def create_file(folder: str = ''):
    working_space = getcwd()
    file_path = join(Path(__file__).resolve().parent, 'file')

    # 1. 创建 pyproject.toml
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

    # 2. 复制基础文件
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

    # 3. 复制 greaterwms/ 目录
    greaterwms_source = join(file_path, 'greaterwms')
    greaterwms_dest = join(working_space, 'greaterwms')
    if exists(greaterwms_source) and not exists(greaterwms_dest):
        shutil.copytree(greaterwms_source, greaterwms_dest)

    # 4. 复制 task.py 到 greaterwms/
    task_source = join(file_path, 'task.py')
    task_dest = join(working_space, 'greaterwms', 'task.py')
    if exists(task_source) and not exists(task_dest):
        shutil.copy2(task_source, task_dest)

    # 5. 复制 bomiot_test/ 目录
    bomiot_test_source = join(file_path, 'bomiot_test')
    bomiot_test_dest = join(working_space, 'bomiot_test')
    if exists(bomiot_test_source) and not exists(bomiot_test_dest):
        shutil.copytree(bomiot_test_source, bomiot_test_dest)

    # 6. 处理 setup.ini
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

    # 7. 创建目录
    for dir_name in ['logs', 'dbs']:
        dir_path = join(working_space, dir_name)
        if not exists(dir_path):
            makedirs(dir_path, exist_ok=True)

    welcome()
    return True
```

### 执行流程

1. **生成 `pyproject.toml`**：从模板读取，设置 `tool.poetry.name`（有 folder 用 folder，否则 `bomiot`）、`version = '0.0.1'`
2. **复制基础文件**：`.gitignore`、`LICENSE`、`launcher.py`、`discovered_apps.py`、logo 图标（icns/png/ico）、`splash.png`、`sqlite3.def/dll`、`README.md`
3. **复制 `greaterwms/` 目录**：bomiot 内置的 greaterwms 项目骨架
4. **复制 `task.py`** 到 `greaterwms/task.py`
5. **复制 `bomiot_test/` 目录**
6. **处理 `setup.ini`**：
   - 不存在则从模板复制
   - 存在则确保 `[project] name = greaterwms`
7. **创建目录**：`logs/`、`dbs/`
8. **调用 `welcome()`**：打印欢迎信息

### 生成的文件清单

```
<working_space>/
├── pyproject.toml          # Poetry 配置
├── .gitignore
├── LICENSE
├── launcher.py             # 启动器
├── discovered_apps.py      # app 发现脚本
├── logo.icns / logo.png / logo.ico
├── splash.png
├── sqlite3.def / sqlite3.dll
├── README.md
├── setup.ini               # [project] name = greaterwms
├── greaterwms/             # 项目骨架
│   └── task.py
├── bomiot_test/            # 测试目录
├── logs/
└── dbs/
```

## 示例

```bash
# 在当前目录初始化，pyproject.toml name 默认为 bomiot
bomiot init

# 指定项目名
bomiot init mywms
```

## 注意事项

1. **不生成 auth_key.py**：旧版会生成 JWT auth_key.py，当前版本已移除
2. **setup.ini 项目名固定为 `greaterwms`**：无论传入什么 folder
3. **pyproject.toml 名称**：有 folder 用 folder，无 folder 用 `bomiot`
4. **使用 colorama**：输出带颜色（蓝色提示信息）
5. **调用 `welcome()`**：替代旧版的 ASCII art banner
