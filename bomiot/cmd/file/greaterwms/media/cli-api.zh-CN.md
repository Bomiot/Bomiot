# bomiot api

## 概述

`bomiot api` 命令在当前项目（greaterwms）下创建一个新的子 APP，与 `app` 命令不同的是，它会**自动把模板中的 `Example` 替换为你的 APP 名**，生成开箱即用的完整 API 骨架。

## 用法

```bash
bomiot api <folder>
```

- `folder`：要创建的 APP 名称（必选，且不能为 `bomiot`）

**cmd.py 中的注册与分发：**

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

## 源码分析

`bomiot/cmd/createapi.py`：

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
                    # ... 代码替换 ...
                    print(f'Create APP success {sys.argv[2]}')
            else:
                print('Invalid project mode. Please create a new project or switch to project mode.')
```

### 执行流程

1. **参数校验**：`folder` 不能为空且不能为 `bomiot`
2. **定位项目**：硬编码 `project_name = 'greaterwms'`
3. **模式校验**：`[mode] name = project`
4. **复制 newapi 模板**：从 `bomiot/cmd/newapi/` 复制一套完整文件
5. **生成 apps.py**：调用 `create_project_apps_py(apps_path, 'greaterwms', folder)`
6. **代码替换**：遍历 `filter.py`、`models.py`、`serializers.py`、`urls.py`、`views.py`，执行替换

### 代码替换逻辑

```python
# filter.py
'from bomiot.server.core import models' → f'from {project_name}.{app_name} import models'

# serializers.py
'from bomiot.server.core import models' → f'from {project_name}.{app_name} import models'

# urls.py
'from bomiot.server.function import example' → f'from {project_name}.{app_name} import views'

# views.py
'from bomiot.server.core import models, serializers, filter' → f'from {project_name}.{app_name} import models, serializers, filter'

# 所有文件
'Example' → app_name.capitalize()   # 类名替换
'example' → app_name.lower()        # 变量/路径名替换
```

## 示例

```bash
# 创建一个名为 order 的 API 子 APP
bomiot api order
```

生成后 `order/views.py` 中的导入变为：
```python
from greaterwms.order import models, serializers, filter
```

模型类名从 `Example` 变为 `Order`，模型路径中 `example` 变为 `order`。

## app vs api 对比

| 特性 | `bomiot app` | `bomiot api` |
|------|-------------|--------------|
| 模板来源 | `extends/` | `newapi/` |
| 代码替换 | 无，需手动改 | 自动替换 Example/import 路径 |
| 适用场景 | 自定义骨架，灵活修改 | 快速生成可用 CRUD API |

## 注意事项

1. **项目名硬编码**：必须在包含 `greaterwms/bomiotconf.ini` 的目录下执行
2. **bomiotconf.ini 必须是 project 模式**
3. **替换是全局的**：`Example` → `Order`、`example` → `order`，如果模板中有其他含 example 字符串的注释也会被替换
4. **生成后需运行迁移**：`bomiot makemigrations order` + `bomiot migrate`
