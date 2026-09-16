# bomiot deploy

> **赞助专享（Sponsor Only）**：此命令仅对赞助商开放。

## 概述

`bomiot deploy` 命令用于为项目生成 GitHub Actions CI/CD 工作流配置。它会创建 `.github/workflows/` 目录并复制 `greaterwms.yaml` 工作流文件。

## 用法

```bash
bomiot deploy [folder]
```

- `folder`：项目名称（可选，当前实现中未使用此参数）

**cmd.py 中的注册与分发：**

```python
parser_deploy = subparsers.add_parser(
    'deploy', help='Deploy project')
parser_deploy.add_argument('folder', default='',
                         nargs='?', type=str, help='deploy project')
# ...
elif command == 'deploy':
    from bomiot.cmd.deploy import deploy
    deploy(args.folder)
```

## 源码分析

`bomiot/cmd/deploy.py`：

```python
def deploy(folder: str):
    # Create .github folder if it doesn't exist
    github_path = join(getcwd(), '.github')
    if not exists(github_path):
        makedirs(github_path)
    # Create .github/workflows folder if it doesn't exist
    workflows_path = join(github_path, 'workflows')
    if not exists(workflows_path):
        makedirs(workflows_path)
    # Copy greaterwms.yaml to .github/workflows
    current_dir = Path(__file__).parent
    source_yaml = current_dir / 'file' / 'greaterwms.yaml'
    dest_yaml = join(workflows_path, 'greaterwms.yaml')
    if exists(source_yaml) and not exists(dest_yaml):
        shutil.copy2(str(source_yaml), dest_yaml)

    print(f'Deploy project success')
```

### 执行流程

1. **创建 `.github/` 目录**：如果不存在
2. **创建 `.github/workflows/` 目录**：如果不存在
3. **复制 `greaterwms.yaml`**：从 `bomiot/cmd/file/greaterwms.yaml` 复制到 `.github/workflows/greaterwms.yaml`（如果目标已存在则跳过）
4. **打印成功信息**

### 生成的目录结构

```
.github/
└── workflows/
    └── greaterwms.yaml
```

## 示例

```bash
bomiot deploy
```

输出：
```
Deploy project success
```

## 注意事项

1. **不生成 supervisor 配置**：旧版会生成 supervisor `.conf` 文件，当前版本改为 GitHub Actions 工作流
2. **无参数**：`deploy()` 函数签名虽接受 `folder`，但内部完全未使用
3. **幂等操作**：如果 `greaterwms.yaml` 已存在则不会覆盖
