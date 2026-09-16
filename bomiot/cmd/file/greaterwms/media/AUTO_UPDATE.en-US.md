# Bomiot Launcher Auto-Incremental Update Flow

## Overview

Bomiot's packaging and distribution uses a **portable green build + manifest.json incremental update** mechanism. After packaging, a portable green build is generated and compressed. Once extracted, it is deployed alongside a `manifest.json` to an update server. The local client compares its local `manifest.json` with the server's on startup, downloading only the files that have changed — enabling incremental updates.

---

## Complete Flow

```
CI Build (Nuitka standalone)
  ↓
Generate portable green build archive
  ↓
Extract green build → Generate manifest.json (file list + hashes)
  ↓
Deploy manifest.json + files to update server
  ↓
Local client starts → Compare local vs. server manifest.json
  ↓
Download only changed files → Replace local files → Launch application
```

---

## 1. Packaging Stage

### CI Build

GitHub Actions (`greaterwms.yaml`) builds on three platforms:

| Platform | Build Tool | Output |
| --- | --- | --- |
| Windows | Nuitka standalone | `build/*.dist/` directory + `.exe` |
| macOS | Nuitka standalone | `build/*.app/` app bundle |
| Linux | Nuitka standalone | `build/*.dist/` directory |

```yaml
- uses: Nuitka/Nuitka-Action@main
  with:
    script-name: launcher.py
    mode: standalone          # Portable green build, not single-file
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

- `mode: standalone` generates a self-contained directory (portable green build) with the exe and all dependency DLLs/libraries
- `include-data-files` packages `setup.ini`, `splash.png`, `apps.json`, and hot-update files (`server.py`, `receiver.py`, `files.py`, `task.py`)
- `include-package-data` / `include-package` includes bomiot, django, fastapi, flask, and all other dependencies

### Key: Hot-Update Files Packaged Separately

The following files are packaged as data files (not compiled into the binary), making them directly replaceable for incremental updates:

| File | Purpose |
| --- | --- |
| `setup.ini` | Global configuration |
| `splash.png` | Splash screen image |
| `apps.json` | Discovered app list |
| `greaterwms/server.py` | System monitor takeover |
| `greaterwms/receiver.py` | Business data takeover |
| `greaterwms/files.py` | File watcher takeover |
| `greaterwms/task.py` | Scheduled task functions |

These files exist as raw `.py` files in the green build directory and can be directly replaced.

---

## 2. Green Build Generation & manifest.json

### Post-Build Processing

After Nuitka completes, the CI performs these steps:

```
build/GreaterWMS.dist/        ← Nuitka output directory
  ├── GreaterWMS.exe
  ├── setup.ini
  ├── splash.png
  ├── apps.json
  ├── bomiot/                  ← Compiled Python packages
  ├── django/
  ├── greaterwms/
  │   ├── server.py
  │   ├── receiver.py
  │   ├── files.py
  │   └── task.py
  ├── *.dll / *.so             ← Dependency libraries
  └── manifest.json            ← Generated file manifest
```

### manifest.json Structure

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

| Field | Description |
| --- | --- |
| `version` | Current version number, matching `version` in `launcher.py` |
| `platform` | Platform identifier (windows / macos / linux) |
| `files` | File path → metadata mapping |
| `files[path].size` | File size in bytes |
| `files[path].hash` | File SHA-256 hash value |

### Generation Flow

```
1. Walk all files in the green build directory
2. Compute SHA-256 hash for each file
3. Record relative path, size, and hash
4. Write manifest.json
5. Compress the green build directory + manifest.json into a zip
6. Upload to the update server
```

---

## 3. Update Server Deployment

Update server directory structure:

```
update-server/
  ├── manifest.json              ← Latest version file manifest
  ├── GreaterWMS-3.0.0-windows.zip   ← Green build archive
  └── files/                     ← Incremental file directory (organized by path)
      ├── setup.ini
      ├── greaterwms/
      │   ├── server.py
      │   ├── receiver.py
      │   └── files.py
      └── splash.png
```

- `manifest.json` always points to the latest version
- `files/` directory contains all incrementally updatable files
- The client only needs to access the `manifest.json` URL to get version info

---

## 4. Client Incremental Update Flow

### Configure Update Server URL

Set `update_url` in `launcher.py` to point to the update server's `manifest.json`:

```python
app_name = "GreaterWMS"
version = "3.0.0"
port = 8008
update_url = "https://your-update-server.com/manifest.json"
```

- `update_url` points to the `manifest.json` file on the update server
- If auto-update is not needed, set it to an empty string to skip update checks
- On first install, there is no local `manifest.json`, so the full green build is downloaded directly

### Update Check on Startup

```
launcher.py starts
  ↓
0. Read update_url; if empty, skip update check
  ↓
1. Read local manifest.json (if it exists)
  ↓
2. Request server manifest.json
  ↓
3. Compare version:
   - Same version → Launch directly, skip update
   - Different version → Enter incremental update flow
  ↓
4. Compare file hashes one by one:
   - Hash matches → Skip this file
   - Hash differs or local file missing → Download this file
  ↓
5. Replace local files after download
  ↓
6. Update local manifest.json
  ↓
7. Launch application (launcher init flow)
```

### Comparison Logic

```python
import hashlib, requests, json

def check_update(server_manifest_url, local_manifest_path):
    # Read local manifest
    with open(local_manifest_path, 'r') as f:
        local_manifest = json.load(f)

    # Fetch server manifest
    response = requests.get(server_manifest_url)
    server_manifest = response.json()

    # Same version, no update needed
    if local_manifest['version'] == server_manifest['version']:
        return None  # No update needed

    # Compare files one by one
    files_to_update = []
    for file_path, server_info in server_manifest['files'].items():
        local_info = local_manifest['files'].get(file_path)
        if local_info is None:
            # Local file missing, need to download
            files_to_update.append(file_path)
        elif local_info['hash'] != server_info['hash']:
            # Hash differs, need to download
            files_to_update.append(file_path)

    return files_to_update
```

### Download & Replace

```python
def download_and_replace(file_path, server_base_url, local_base_dir):
    # Download file
    url = f"{server_base_url}/files/{file_path}"
    response = requests.get(url)
    local_path = os.path.join(local_base_dir, file_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Replace local file
    with open(local_path, 'wb') as f:
        f.write(response.content)

    # Verify hash
    file_hash = hashlib.sha256(response.content).hexdigest()
    return file_hash
```

### After Update Complete

- Update local `manifest.json` to match the server version
- Launch application into the normal `launcher.py` initialization flow

---

## 5. launcher.py Startup Flow

After incremental update completes, the normal startup flow begins:

```
launcher.py starts
  ↓
1. Display splash screen (splash.png)
  ↓
2. Set environment variables + clean lock file
  ↓
3. Django setup()
  ↓
4. Generate encryption keys (auth_key.py)
  ↓
5. App discovery (apps.json)
  ↓
6. First makemigrations + migrate
  ↓
7. Call all AppConfig.ready()
  ↓
8. Second makemigrations + migrate
  ↓
9. Port auto-increment (8008 → 8009 → ... → 8107)
  ↓
10. Start uvicorn + open browser
```

| Environment Variable | Value | Purpose |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | `bomiot.server.server.settings` | Django settings entry |
| `RUN_MAIN` | `true` | Marks main process, triggers `apps.py ready()` |
| `IS_LAN` | `true` | Desktop mode; `WORKING_SPACE` = exe directory |
| `WORKERS` | `1` | Single-process mode |

---

## 6. CI Build Configuration

Key settings in `greaterwms.yaml`:

| Setting | Value | Description |
| --- | --- | --- |
| `mode` | `standalone` | Generate self-contained directory (portable green build) |
| `script-name` | `launcher.py` | Entry script |
| `nuitka-version` | `4.1.3` | Nuitka version |
| `lto` | `yes` | Link-time optimization |
| `enable-plugins` | `tk-inter` | Enable Tkinter plugin |
| `windows-console-mode` | `disable` | Hide console window |
| `module-parameter` | `django-settings-module=...` | Django settings module |

### Artifact Upload

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

## File Index

| File | Responsibility |
| --- | --- |
| `bomiot/cmd/file/launcher.py` | Entry point: splash + init + uvicorn |
| `bomiot/cmd/file/greaterwms.yaml` | CI build config (Nuitka packaging) |
| `bomiot/cmd/file/discovered_apps.py` | Scans `greaterwms/` for subdirs with `apps.py` |
| `bomiot/server/server/settings.py` | Django config: loads `apps.json`, `setup.ini` |
| `bomiot/server/server/views.py` | `IndexTemplateView` template sync, `init_permission`, `init_bomiot` |
| `bomiot/server/core/apps.py` | `CoreConfig.ready()` starts three background threads |
| `bomiot/cmd/file/setup.ini` | Config template |
| `manifest.json` | File manifest (path + size + SHA-256 hash) |
