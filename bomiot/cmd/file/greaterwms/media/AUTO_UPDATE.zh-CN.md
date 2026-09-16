# Bomiot Launcher 自动增量更新流程

## 概述

Bomiot 的打包发布采用**绿色版 + manifest.json 增量更新**机制。打包完成后生成绿色版压缩包，解压后与 `manifest.json` 一起部署到更新服务器。本地客户端启动时比对本地与服务器的 `manifest.json`，只下载有变化的文件，实现增量更新。

---

## 完整流程

```
CI 打包 (Nuitka standalone)
  ↓
生成绿色版压缩包
  ↓
解压绿色版 → 生成 manifest.json（文件列表 + 哈希值）
  ↓
manifest.json + 文件一起部署到更新服务器
  ↓
本地客户端启动 → 比对本地与服务器 manifest.json
  ↓
只下载变化的文件 → 替换本地文件 → 启动应用
```

---

## 一、打包阶段

### CI 构建

GitHub Actions（`greaterwms.yaml`）在三个平台构建：

| 平台 | 构建工具 | 产物 |
| --- | --- | --- |
| Windows | Nuitka standalone | `build/*.dist/` 目录 + `.exe` |
| macOS | Nuitka standalone | `build/*.app/` 应用包 |
| Linux | Nuitka standalone | `build/*.dist/` 目录 |

```yaml
- uses: Nuitka/Nuitka-Action@main
  with:
    script-name: launcher.py
    mode: standalone          # 绿色版，非单文件
    enable-plugins: tk-inter
    include-data-files: |
      setup.ini=setup.ini
      splash.png=splash.png
      apps.json=apps.json
      greaterwms/server.py=greaterwms/server.py
      greaterwms/receiver.py=greaterwms/receiver.py
      greaterwms/files.py=greaterwms/files.py
      greaterwms/task.py=greaterwms/task.py
```

- `mode: standalone` 生成独立目录（绿色版），包含 exe + 所有依赖 DLL/库文件
- `include-data-files` 将 `setup.ini`、`splash.png`、`apps.json` 及热更新文件（`server.py`、`receiver.py`、`files.py`、`task.py`）打包进去
- `include-package-data` / `include-package` 包含 bomiot、django、fastapi、flask 等所有依赖

### 关键：热更新文件单独打包

以下文件作为数据文件单独打包，不编译进二进制，便于后续增量更新：

| 文件 | 作用 |
| --- | --- |
| `setup.ini` | 全局配置 |
| `splash.png` | 启动页图片 |
| `apps.json` | 已发现应用列表 |
| `greaterwms/server.py` | 系统监控接管 |
| `greaterwms/receiver.py` | 业务数据接管 |
| `greaterwms/files.py` | 文件监控接管 |
| `greaterwms/task.py` | 定时任务函数 |

这些文件以 `.py` 原始格式存在于绿色版目录中，可直接替换更新。

---

## 二、绿色版生成与 manifest.json

### 打包后处理

Nuitka 构建完成后，CI 执行以下步骤：

```
build/GreaterWMS.dist/        ← Nuitka 产物目录
  ├── GreaterWMS.exe
  ├── setup.ini
  ├── splash.png
  ├── apps.json
  ├── bomiot/                  ← 编译后的 Python 包
  ├── django/
  ├── greaterwms/
  │   ├── server.py
  │   ├── receiver.py
  │   ├── files.py
  │   └── task.py
  ├── *.dll / *.so             ← 依赖库
  └── manifest.json            ← 生成的文件清单
```

### manifest.json 结构

```json
{
  "version": "3.0.0",
  "platform": "windows",
  "files": {
    "GreaterWMS.exe": {
      "size": 134217728,
      "hash": "sha256:a1b2c3d4e5f6..."
    },
    "setup.ini": {
      "size": 1024,
      "hash": "sha256:b2c3d4e5f6a1..."
    },
    "splash.png": {
      "size": 2048576,
      "hash": "sha256:c3d4e5f6a1b2..."
    },
    "greaterwms/server.py": {
      "size": 4096,
      "hash": "sha256:d4e5f6a1b2c3..."
    },
    "greaterwms/receiver.py": {
      "size": 8192,
      "hash": "sha256:e5f6a1b2c3d4..."
    }
  }
}
```

| 字段 | 说明 |
| --- | --- |
| `version` | 当前版本号，与 `launcher.py` 中 `version` 一致 |
| `platform` | 平台标识（windows / macos / linux） |
| `files` | 文件路径 → 元数据映射 |
| `files[path].size` | 文件大小（字节） |
| `files[path].hash` | 文件 SHA-256 哈希值 |

### 生成流程

```
1. 遍历绿色版目录所有文件
2. 计算每个文件的 SHA-256 哈希值
3. 记录文件相对路径、大小、哈希值
4. 写入 manifest.json
5. 将绿色版目录 + manifest.json 一起压缩为 zip
6. 上传到更新服务器
```

---

## 三、更新服务器部署

更新服务器目录结构：

```
update-server/
  ├── manifest.json              ← 最新版本的文件清单
  ├── GreaterWMS-3.0.0-windows.zip   ← 绿色版压缩包
  └── files/                     ← 增量文件目录（按路径组织）
      ├── setup.ini
      ├── greaterwms/
      │   ├── server.py
      │   ├── receiver.py
      │   └── files.py
      └── splash.png
```

- `manifest.json` 始终指向最新版本
- `files/` 目录存放所有可增量更新的文件
- 客户端只需访问 `manifest.json` 的 URL 即可获取版本信息

---

## 四、客户端增量更新流程

### 配置更新服务器地址

在 `launcher.py` 中设置 `update_url`，指向更新服务器的 `manifest.json` 地址：

```python
app_name = "GreaterWMS"
version = "3.0.0"
port = 8008
update_url = "https://your-update-server.com/manifest.json"
```

- `update_url` 指向更新服务器上的 `manifest.json` 文件
- 如果不需要自动更新，设为空字符串即可跳过更新检查
- 首次安装时本地没有 `manifest.json`，会直接下载完整绿色版

### 启动时检查更新

```
launcher.py 启动
  ↓
0. 读取 update_url，为空则跳过更新检查
  ↓
1. 读取本地 manifest.json（如果存在）
  ↓
2. 请求服务器 manifest.json
  ↓
3. 比对 version：
   - 版本相同 → 直接启动，跳过更新
   - 版本不同 → 进入增量更新流程
  ↓
4. 逐文件比对 hash：
   - hash 相同 → 跳过该文件
   - hash 不同或本地不存在 → 下载该文件
  ↓
5. 下载完成后替换本地文件
  ↓
6. 更新本地 manifest.json
  ↓
7. 启动应用（launcher 初始化流程）
```

### 比对逻辑

```python
import hashlib, requests, json

def check_update(server_manifest_url, local_manifest_path):
    # 读取本地 manifest
    with open(local_manifest_path, 'r') as f:
        local_manifest = json.load(f)

    # 拉取服务器 manifest
    response = requests.get(server_manifest_url)
    server_manifest = response.json()

    # 版本相同，无需更新
    if local_manifest['version'] == server_manifest['version']:
        return None  # No update needed

    # 逐文件比对
    files_to_update = []
    for file_path, server_info in server_manifest['files'].items():
        local_info = local_manifest['files'].get(file_path)
        if local_info is None:
            # 本地不存在，需要下载
            files_to_update.append(file_path)
        elif local_info['hash'] != server_info['hash']:
            # 哈希不同，需要下载
            files_to_update.append(file_path)

    return files_to_update
```

### 下载与替换

```python
def download_and_replace(file_path, server_base_url, local_base_dir):
    # 下载文件
    url = f"{server_base_url}/files/{file_path}"
    response = requests.get(url)
    local_path = os.path.join(local_base_dir, file_path)

    # 确保目录存在
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # 替换本地文件
    with open(local_path, 'wb') as f:
        f.write(response.content)

    # 验证哈希
    file_hash = hashlib.sha256(response.content).hexdigest()
    return file_hash
```

### 更新完成后

- 更新本地 `manifest.json` 为服务器版本
- 启动应用进入正常 `launcher.py` 初始化流程

---

## 五、launcher.py 启动流程

增量更新完成后，进入正常启动流程：

```
launcher.py 启动
  ↓
1. 显示启动页（splash.png）
  ↓
2. 设置环境变量 + 清理锁文件
  ↓
3. Django setup()
  ↓
4. 生成加密密钥（auth_key.py）
  ↓
5. 应用发现（apps.json）
  ↓
6. 第一次 makemigrations + migrate
  ↓
7. 调用所有 AppConfig.ready()
  ↓
8. 第二次 makemigrations + migrate
  ↓
9. 端口自增（8008 → 8009 → ... → 8107）
  ↓
10. 启动 uvicorn + 打开浏览器
```

| 环境变量 | 值 | 作用 |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | `bomiot.server.server.settings` | Django 配置入口 |
| `RUN_MAIN` | `true` | 标记主进程，触发 `apps.py ready()` |
| `IS_LAN` | `true` | 桌面端模式，`WORKING_SPACE` 取 exe 所在目录 |
| `WORKERS` | `1` | 单进程模式 |

---

## 六、CI 构建配置

`greaterwms.yaml` 关键配置：

| 配置项 | 值 | 说明 |
| --- | --- | --- |
| `mode` | `standalone` | 生成独立目录（绿色版） |
| `script-name` | `launcher.py` | 入口脚本 |
| `nuitka-version` | `4.1.3` | Nuitka 版本 |
| `lto` | `yes` | 链接时优化 |
| `enable-plugins` | `tk-inter` | 启用 Tkinter 插件 |
| `windows-console-mode` | `disable` | 隐藏控制台窗口 |
| `module-parameter` | `django-settings-module=...` | Django 设置模块 |

### 产物上传

```yaml
- name: Upload Artifact
  uses: actions/upload-artifact@v4
  with:
    name: GreaterWMS-3.0.0-${{ runner.os }}
    path: |
      build/*.exe
      build/*.bin
      build/*.app/**/*
      build/*.dist/**/*
    include-hidden-files: true
```

---

## 文件索引

| 文件 | 职责 |
| --- | --- |
| `bomiot/cmd/file/launcher.py` | 启动入口，splash 页 + 初始化 + uvicorn |
| `bomiot/cmd/file/greaterwms.yaml` | CI 构建配置（Nuitka 打包） |
| `bomiot/cmd/file/discovered_apps.py` | 扫描 `greaterwms/` 下含 `apps.py` 的子目录 |
| `bomiot/server/server/settings.py` | Django 配置，加载 `apps.json`、`setup.ini` |
| `bomiot/server/server/views.py` | `IndexTemplateView` 模板同步、`init_permission`、`init_bomiot` |
| `bomiot/server/core/apps.py` | `CoreConfig.ready()` 启动三个后台线程 |
| `bomiot/cmd/file/setup.ini` | 配置文件模板 |
| `manifest.json` | 文件清单（路径 + 大小 + SHA-256 哈希） |
