# Quick Start

## Introduction

Bomiot is a node-based full-stack development platform for warehousing and supply chains. It supports single-file deployment, multiple backend frameworks (Django / FastAPI / Flask), multiple frontend frameworks (Vue / React / Angular), Python code compilation protection, and a plugin ecosystem.

---

## Requirements

- **Python**: 3.9 or higher
- **Node.js**: 18.19.1 or higher (required for frontend development)
- **OS**: Windows / macOS / Linux

---

## 1. Install Bomiot

```bash
# Install with pip
pip install bomiot

# Or with poetry
poetry add bomiot
```

---

## 2. Initialize Workspace

```bash
bomiot init
```

This creates a Bomiot workspace in the current directory with `setup.ini` and other global config files.

---

## 3. Create a Project

```bash
# Create a new project
bomiot project my-project
```

Enter the project directory and create apps:

```bash
cd my-project

# Create an app (Django by default)
bomiot new my-app

# Specify backend framework
bomiot new my-app --framework django
bomiot new my-app --framework fastapi
bomiot new my-app --framework flask
```

---

## 4. Database

```bash
# Generate migration files
bomiot makemigrations

# Apply migrations
bomiot migrate

# Load initial data
bomiot loaddata <source>

# Export data
bomiot dumpdata [appname]
```

---

## 5. Admin User

```bash
# Create admin account
bomiot initadmin

# Reset admin password
bomiot initpwd
```

---

## 6. Start the Server

```bash
# Start dev server (default 127.0.0.1:8000)
bomiot run

# Specify host and port
bomiot run --host 0.0.0.0 --port 8080

# Production config
bomiot run --host 0.0.0.0 --port 80 --workers 4 --log-level info
```

Open `http://127.0.0.1:8000/` to access the system.

---

## 7. Verify Installation

After starting, test each backend framework:

```
Django:   http://127.0.0.1:8000/test/
FastAPI:  http://127.0.0.1:8000/fastapi/test/
Flask:    http://127.0.0.1:8000/flask/test/
```

---

## 8. Package & Release

```bash
# Package project (core modules can be compiled to binary for source protection)
bomiot package my-project
```

Output goes to the `dist/` directory.

---

## Command Reference

| Command | Description |
|---------|-------------|
| `bomiot init` | Initialize workspace |
| `bomiot project <name>` | Create project |
| `bomiot new <app>` | Create app |
| `bomiot makemigrations` | Generate migrations |
| `bomiot migrate` | Apply migrations |
| `bomiot initadmin` | Create admin |
| `bomiot initpwd` | Reset admin password |
| `bomiot run` | Start server |
| `bomiot package <name>` | Package project |
| `bomiot keys` | Init validation keys |
