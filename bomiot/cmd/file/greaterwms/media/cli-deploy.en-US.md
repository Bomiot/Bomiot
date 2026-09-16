# bomiot deploy

> **Sponsor Only**: This command is available to sponsors only.

## Overview

`bomiot deploy` generates a GitHub Actions CI/CD workflow configuration for the project. It creates the `.github/workflows/` directory and copies the `greaterwms.yaml` workflow file.

## Usage

```bash
bomiot deploy [folder]
```

- `folder`: Project name (optional, not used in the current implementation)

**Registration and dispatch in cmd.py:**

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

## Source Code Analysis

`bomiot/cmd/deploy.py`:

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

### Execution Flow

1. **Create `.github/` directory**: if it doesn't exist
2. **Create `.github/workflows/` directory**: if it doesn't exist
3. **Copy `greaterwms.yaml`**: copies from `bomiot/cmd/file/greaterwms.yaml` to `.github/workflows/greaterwms.yaml` (skips if target already exists)
4. **Print success message**

### Generated Directory Structure

```
.github/
└── workflows/
    └── greaterwms.yaml
```

## Example

```bash
bomiot deploy
```

Output:
```
Deploy project success
```

## Notes

1. **No supervisor config**: the old version generated a supervisor `.conf` file; the current version uses a GitHub Actions workflow instead
2. **No arguments**: although `deploy()` accepts `folder` in its signature, it is completely unused internally
3. **Idempotent**: if `greaterwms.yaml` already exists, it will not be overwritten
