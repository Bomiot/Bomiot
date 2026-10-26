# bomiot init

Initialize a Bomiot project in the current directory with all base files needed to run, build and ship.

```bash
bomiot init
```

## Overview

`bomiot init` copies the Bomiot project skeleton into the current directory: the launcher entry, global config, workspace templates, platform icons and more. Once it finishes you can start writing business code, run locally with `bomiot run`, and package with `bomiot build`.

> **Idempotent & safe**: the command only fills in missing files — existing files are never overwritten. Re-running it will not clobber your changes.

## Prerequisites

- bomiot installed: `pip install bomiot`
- Run inside an **empty directory or the project root** (the command works on the current working directory)

## Generated Files & Directories

| File / Directory | Description |
|---|---|
| `launcher.py` | Startup entry. Holds the core config — `app_name`, `version`, `base_url` (update server), `port` — read by builds and updates |
| `setup.ini` | Global config (project name, debug switch, etc.). If it already exists it is not overwritten; only `[project] name` is completed when needed |
| `pyproject.toml` | Project configuration (generated when missing, with project name and initial version filled in) |
| `builder.toml` | Build extension config (additional packaging content, see the build doc) |
| `greaterwms/` | Workspace directory holding your business code, including takeover templates and the scheduled-task template `task.py` |
| `discovered_apps.py` | App discovery script (generates the app manifest at `bomiot run` time) |
| `logo.ico` / `logo.icns` / `logo.png` | App icons for Windows / macOS / Linux — replace with your own |
| `splash.png` | Splash image shown while the app starts |
| `sqlite3.def` / `sqlite3.dll` | SQLite support files |
| `README.md` / `LICENSE` / `.gitignore` | Project readme, license and Git ignore rules |
| `logs/` / `dbs/` | Log directory and database directory |

## Execution Flow

```text
bomiot init
  │
  ├─ 1. Generate pyproject.toml (if missing)
  ├─ 2. Copy base files (launcher.py, setup.ini, icons, templates — existing files are skipped)
  ├─ 3. Copy the greaterwms workspace directory (skipped if it already exists)
  ├─ 4. Create the logs/ and dbs/ directories
  └─ 5. Print the welcome message — initialization complete
```

## Standard Flow After init

```text
bomiot init
  ↓
Edit launcher.py (app_name / version / port) and setup.ini as needed
  ↓
Replace the logo icons and splash.png with your own assets
  ↓
bomiot run            ← run locally for development
  ↓
bomiot build          ← local build (see build doc)
  ↓
bomiot deploy + push  ← cloud three-platform build (see deploy doc)
```

## Notes

- `launcher.py` is the project's central config — `app_name`, `version` and `base_url` are all required; build, publish and client updates depend on them
- Replace the icons and splash image right after init, so defaults never make it into a build
- An existing `setup.ini` only gets its project name completed — your other settings are left untouched
- Re-running is safe: every existing file and directory is skipped, your business code is never overwritten
