# Quick Start

Get through the minimal Bomiot loop in 5 minutes: **install → initialize → run → package**.

## Prerequisites

- Python 3.11 or later, with pip
- Any of the three platforms: Windows / macOS / Linux

## Step 1: Install

```bash
pip install bomiot
```

Verify the installation:

```bash
bomiot --version
```

## Step 2: Initialize a Project

```bash
mkdir myapp
cd myapp
bomiot init
```

`init` generates the full project skeleton in the current directory: `launcher.py` (startup and update config), `setup.ini` (global config), the workspace directory, platform icons, and more. Existing files are never overwritten, so it is safe to re-run.

> Replace `logo.ico / logo.icns / logo.png` and `splash.png` with your own assets right after initialization, so the defaults don't end up in your builds.

## Step 3: Initialize the Database

```bash
bomiot migrate      # create tables
bomiot initadmin    # create the admin account; the command prints the initial password
```

SQLite is the default and needs no configuration. To switch to MySQL / PostgreSQL / Oracle, see the corresponding docs under the Database tab.

## Step 4: Run

```bash
bomiot run
```

Open `http://127.0.0.1:8000` in a browser and log in with the admin account from the previous step.

- Binds to `0.0.0.0:8000` by default; adjust with options like `--port 9000`
- **On Windows, run with a single worker** (multi-worker support is poor there) — see CLI Commands → run

## Step 5: Package for Delivery

```bash
bomiot build        # build an app bundle for the current platform locally
```

The output lands in `dist/` and runs with a double-click — no Python required on the user's machine.

To produce Windows / macOS / Linux packages at once, use cloud builds:

```bash
bomiot deploy       # generate the deployment workflow
git push            # pushing triggers the three-platform build
```

## Command Overview

| Command | Purpose |
|---|---|
| `bomiot init` | Initialize the project skeleton |
| `bomiot run` | Start the server |
| `bomiot migrate` / `makemigrations` | Apply / generate database migrations |
| `bomiot initadmin` / `initpwd` | Create admin / reset password |
| `bomiot project` / `app` / `api` | New project / sub-app / API |
| `bomiot loaddata` / `dumpdata` | Import / export data |
| `bomiot build` | Build an app bundle locally |
| `bomiot deploy` / `publish` | Cloud three-platform builds / publish incremental updates |

Full documentation for each command lives under the CLI Commands tab.

## What's Next

- "Basics → setup.ini": global configuration reference
- "Database": switching to a production database
- "CLI Commands → build / deploy / publish": the complete delivery and update pipeline
