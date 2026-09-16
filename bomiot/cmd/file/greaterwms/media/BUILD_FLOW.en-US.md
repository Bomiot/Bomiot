# Bomiot Complete Build & Delivery Flow

## Overview

With GitHub Actions + Nuitka, pushing a Bomiot project to GitHub automatically builds portable green builds for Windows / macOS / Linux — no Python environment required to run. Full automation from development to delivery.

---

## Complete Flow

```
1. Register a GitHub account
  ↓
2. Create a new repository
  ↓
3. pip install bomiot
  ↓
4. Create virtual env, pip freeze > requirements.txt
  ↓
5. bomiot init to initialize project
  ↓
6. Modify business code
  ↓
7. bomiot deploy to generate greaterwms.yaml (GitHub Actions workflow)
  ↓
8. Push to GitHub
  ↓
9. GitHub Actions auto-builds three-platform green builds
  ↓
10. Download Artifact → cross-platform portable deliverable
```

---

## 1. Register a GitHub Account

- Go to [github.com](https://github.com) and sign up
- Skip if you already have an account

---

## 2. Create a New Repository

- Click **New repository**
- Fill in the repository name
- Choose Public or Private
- Click **Create repository**

---

## 3. Install Bomiot

```bash
pip install bomiot
```

---

## 4. Generate requirements.txt

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install bomiot and other dependencies
pip install bomiot

# Generate dependency manifest
pip freeze > requirements.txt
```

> GitHub Actions reads this file to install the same dependencies in the CI environment.

---

## 5. bomiot init to Initialize Project

```bash
bomiot init
```

Generates the following files in the current directory.

You can set the app name and version in `launcher.py`:

```python
app_name = "GreaterWMS"
version = "3.0.0"
port = 8008
```

- `app_name` — Application name
- `version` — Version number
- `port` — Default port

| File / Directory | Description |
| --- | --- |
| `launcher.py` | Entry point |
| `setup.ini` | Global config |
| `splash.png` | Splash screen image (transitional screen shown during app startup, replace with your own image) |
| `apps.json` | Discovered app list (generated at runtime) |
| `discovered_apps.py` | App discovery script |
| `logo.ico` | Windows app icon (.ico format) |
| `logo.icns` | macOS app icon (.icns format) |
| `logo.png` | Linux app icon (.png format) |

> The three icon files correspond to the executable icons on each platform. They are automatically injected during the Nuitka build via `windows-icon-from-ico`, `macos-app-icon`, and `linux-icon` config options. Replace with your own icon files as needed.
| `.gitignore` | Git ignore rules |
| `LICENSE` | Open source license |
| `README.md` | Project readme |
| `pyproject.toml` | Project config |
| `sqlite3.def` / `sqlite3.dll` | SQLite database |
| `greaterwms/` | Workspace directory |
| `greaterwms/server.py` | System monitor takeover (template) |
| `greaterwms/receiver.py` | Business data takeover (template) |
| `greaterwms/files.py` | File watcher takeover (template) |
| `greaterwms/task.py` | Scheduled task functions (template) |
| `bomiot_test/` | Test module |
| `logs/` | Log directory |
| `dbs/` | Database directory |

---

## 6. Modify as Needed

Modify project files as needed. When done, push to GitHub.

---

## 7. Push to GitHub

Place `greaterwms.yaml` in the `.github/workflows/` directory:

```
.github/
  └── workflows/
      └── greaterwms.yaml
```

Then commit and push:

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

Pushing to the `main` branch triggers the build automatically.

---

## 8. GitHub Actions Auto-Build

Key settings in `greaterwms.yaml`:

| Setting | Value | Description |
| --- | --- | --- |
| `APP_NAME` | `GreaterWMS` | Application name |
| `BASE_VERSION` | `3.0.0` | Version number |
| `matrix.os` | `windows-latest, macos-latest, ubuntu-22.04` | Parallel builds on three platforms |
| `python-version` | `3.11` | Python version |
| `mode` | `standalone` | Portable green build directory |
| `script-name` | `launcher.py` | Entry script |
| `nuitka-version` | `4.1.3` | Nuitka version |
| `lto` | `yes` | Link-time optimization |
| `windows-console-mode` | `disable` | Hide console |
| `enable-plugins` | `tk-inter` | Tkinter plugin |

### Build Flow

```
Checkout repo → Setup Python 3.11 → pip install -r requirements.txt
  ↓
discovered_apps.py scans greaterwms/ for apps.py → generates apps.json
  ↓
Nuitka standalone build (three platforms in parallel)
  ↓
Upload Artifact
```

### Three-Platform Outputs

| Platform | Icon | Output |
| --- | --- | --- |
| Windows | `logo.ico` | `build/*.dist/` + `build/*.exe` |
| macOS | `logo.icns` | `build/*.app/` |
| Linux | `logo.png` | `build/*.dist/` + `build/*.bin` |

### Data Files (copied directly, not compiled)

| File | Description |
| --- | --- |
| `setup.ini` | Global config |
| `splash.png` | Splash screen |
| `apps.json` | App list |
| `greaterwms/server.py` | System monitor takeover |
| `greaterwms/receiver.py` | Business data takeover |
| `greaterwms/files.py` | File watcher takeover |
| `greaterwms/task.py` | Scheduled tasks |

---

## 9. Download Artifacts

1. Go to the GitHub repo → **Actions** tab
2. Select the latest build run
3. Download from the **Artifacts** section

Artifact names:

```
GreaterWMS-3.0.0-Windows
GreaterWMS-3.0.0-macOS
GreaterWMS-3.0.0-Linux
```

Extract and run directly — no need to install Python or any dependencies.
