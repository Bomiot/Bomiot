# bomiot app

## 概述

`bomiot app` 命令用于在当前项目（greaterwms）下创建一个新的子 APP。它会从 bomiot 框架的模板目录复制一套标准文件到新项目目录，并生成对应的 `apps.py`。

## 用法

```bash
bomiot app <folder>
```

- `folder`：要创建的 APP 名称（必选，且不能为 `bomiot`）

**cmd.py 中的注册与分发：**

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

## 源码分析

`bomiot/cmd/createapp.py`：

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

### 执行流程

1. **参数校验**：`folder` 不能为空且不能为 `bomiot`
2. **定位项目**：硬编码 `project_name = 'greaterwms'`，读取 `./greaterwms/bomiotconf.ini`
3. **模式校验**：检查 `[mode] name = project`，不是 project 模式则报错
4. **创建目录**：在 `greaterwms/<folder>/` 下创建目录
5. **复制模板**：从 `bomiot/cmd/extends/` 复制一套标准文件（admin.py, apps.py, filter.py, models.py, serializers.py, tests.py, urls.py, views.py, migrations/）
6. **生成 apps.py**：删除模板自带的 apps.py，调用 `create_project_apps_py(apps_path, 'greaterwms', folder)` 生成正确的 AppConfig

### extends 模板包含

```
extends/
├── __init__.py
├── admin.py
├── apps.py            (会被覆盖)
├── filter.py
├── migrations/
│   └── __init__.py
├── models.py
├── serializers.py
├── tests.py
├── urls.py
└── views.py
```

这些模板使用的是 bomiot 内置的 `Example` 模型引用（`from bomiot.server.core import models`），创建后需要你手动修改为自己的模型定义。

## 示例

```bash
# 在 greaterwms 下创建一个名为 myapp 的子 APP
bomiot app myapp
```

输出：
```
Create APP success myapp
```

生成的目录结构：
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

## 注意事项

1. **项目名硬编码**：`project_name = 'greaterwms'`，必须在包含 `greaterwms/bomiotconf.ini` 的目录下执行
2. **bomiotconf.ini 必须是 project 模式**：否则提示 "Invalid project mode"
3. **不做代码替换**：与 `api` 命令不同，`app` 命令只复制模板，不自动替换 `Example` → 你的类名，需要手动修改
4. **与 api 命令的区别**：
   - `app`：复制 `extends/` 模板，不替换代码引用，适合快速起骨架
   - `api`：复制 `newapi/` 模板，自动把 `Example` 替换为你的 APP 名，开箱即用
