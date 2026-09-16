# bomiot project

## 概述

`bomiot project` 命令用于在当前目录下创建一个新的 bomiot 项目工作空间。它会创建项目目录、复制 `bomiotconf.ini` 配置、调用 `create_file()` 生成基础文件、复制 `templates/` 前端模板。

> 注意：项目名不能为 `greaterwms`（保留名），也不能与已安装的 pip 包同名。

## 用法

```bash
bomiot project <folder>
```

- `folder`：项目名称（必选）

**cmd.py 中的注册与分发：**

```python
parser_project = subparsers.add_parser(
    'project', help='Project workspace, default to GreaterWMS')
parser_project.add_argument('folder', default='',
                         nargs='?', type=str, help='project workspace folder')
# ...
if command == 'project':
    from bomiot.cmd.project import project
    project(args.folder)
```

## 源码分析

`bomiot/cmd/project.py`：

```python
def project(folder: str):
    if len(sys.argv) < 3:
        print('Please enter your project name')
        return

    project_name = sys.argv[2]

    # Check if project name is reserved
    if project_name.lower() == 'greaterwms':
        print('Project name "greaterwms" is reserved and cannot be used')
        return

    project_path = join(getcwd(), project_name)

    if exists(project_path):
        print('Project directory already exists')
        return

    # Check if project name conflicts with installed packages
    try:
        installed_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
        if project_name in installed_packages:
            print('Project directory already exists')
            return
    except Exception as e:
        logging.warning(f"Could not check installed packages: {e}")

    try:
        makedirs(project_path, exist_ok=True)
        current_path = Path(__file__).resolve()
        file_path = join(current_path.parent, 'file')

        # Write init file
        init_file_path = join(project_path, '__init__.py')
        with open(init_file_path, "w", encoding='utf-8') as f:
            pass

        # Copy essential files
        essential_files = ['bomiotconf.ini']
        for file_name in essential_files:
            src_path = join(file_path, file_name)
            dst_path = join(project_path, file_name)
            if exists(src_path):
                shutil.copy2(src_path, dst_path)
            else:
                logging.warning(f"Essential file not found: {src_path}")

        # Create additional files via create_file function
        create_file(str(project_name))

        # Copy additional directories
        copy_files(join(current_path.parent.parent, 'templates'), join(project_path, 'templates'))

        print(f'Initialized project workspace {project_name}')
    except OSError as e:
        print(f"Error creating project directory: {e}")
        return
    except Exception as e:
        print(f"Unexpected error during project initialization: {e}")
        return
```

### 执行流程

1. **参数校验**：`folder` 不能为空
2. **保留名检查**：`greaterwms` 是保留名，不能使用
3. **目录冲突检查**：目标目录不能已存在
4. **pip 包冲突检查**：项目名不能与已安装的 pip 包同名
5. **创建目录**：`makedirs(project_path, exist_ok=True)`
6. **生成 `__init__.py`**：创建空的 `__init__.py`
7. **复制 `bomiotconf.ini`**：从 `bomiot/cmd/file/` 复制
8. **调用 `create_file(project_name)`**：生成 pyproject.toml、setup.ini、greaterwms/、logs/、dbs/ 等（详见 [bomiot init](./cli-init.zh-CN.md)）
9. **复制 `templates/`**：从 bomiot 包复制前端模板到 `project/templates/`

### 生成的项目结构

```
<project_name>/
├── __init__.py
├── bomiotconf.ini
├── templates/          # 前端 Vue 模板
└── ...                 # create_file() 生成的文件
```

## 示例

```bash
# 创建一个名为 mywms 的项目
bomiot project mywms
```

输出：
```
Initialized project workspace mywms
```

## 项目创建后的必要操作

`bomiot project` 只负责创建项目骨架，但前端模板中的项目名仍为默认值 `greaterwms`，需要手动修改后重新构建。

### 1. 修改 Pinia store 中的项目名

打开 `templates/src/stores/project.js`，将 `project` 改为你的项目名：

```js
// 修改前
project: 'greaterwms'

// 修改后（假设项目名为 mywms）
project: 'mywms'
```

### 2. 重新构建前端

```bash
cd <project_name>/templates
npx quasar build
```

### 3. 启动项目

```bash
cd <project_name>
bomiot run
```

## 注意事项

1. **保留名**：`greaterwms` 不可用作项目名
2. **pip 包冲突**：项目名不能与已安装的 pip 包重名
3. **只复制 bomiotconf.ini**：不像旧版会复制 `__version__.py`、`receiver.py`、`example.py`、`api.py`
4. **setup.ini 项目名固定为 greaterwms**：由 `create_file()` 内部决定，与传入的 `folder` 无关
5. **Pinia store 项目名需手动修改**：`templates/src/stores/project.js` 中的 `project` 默认为 `'greaterwms'`，每次 `bomiot project` 后需手动改为实际项目名并执行 `quasar build`
