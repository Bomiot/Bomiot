# CLI

## Introduction

Bomiot provides a powerful command-line interface (CLI) covering the full workflow: project creation, app management, database, users, server, packaging, and more.

```bash
bomiot [command] [options]
```

---

## Help & Version

```bash
# Show help
bomiot -h

# Show version
bomiot -v
```

---

## Project Management

| Command | Description |
|---------|-------------|
| `bomiot init` | Initialize workspace |
| `bomiot project <name>` | Create a new project |
| `bomiot new <app>` | Create an app (Django default) |
| `bomiot new <app> --framework django` | Create app with specified framework |
| `bomiot plugins <name>` | Create a plugin |
| `bomiot market <project>` | App marketplace |

### Specify Framework When Creating an App

```bash
bomiot new my-app --framework django
bomiot new my-app --framework fastapi
bomiot new my-app --framework flask
```

---

## Database Management

| Command | Description |
|---------|-------------|
| `bomiot makemigrations` | Generate migration files |
| `bomiot migrate` | Apply migrations |
| `bomiot loaddata <source>` | Load initial data |
| `bomiot dumpdata [appname]` | Export data |

---

## User Management

| Command | Description |
|---------|-------------|
| `bomiot initadmin` | Create admin account |
| `bomiot initpwd` | Reset admin password |

---

## Server Management

### Start Server

```bash
bomiot run [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--host, -b` | Host address | 127.0.0.1 |
| `--port, -p` | Port | 8000 |
| `--workers, -w` | Worker processes | 1 |
| `--log-level` | Log level | info |
| `--ssl-keyfile` | SSL key file | - |
| `--ssl-certfile` | SSL cert file | - |
| `--proxy-headers` | Enable proxy headers | - |
| `--limit-concurrency` | Max concurrency | 1000 |
| `--timeout-graceful-shutdown` | Graceful shutdown (s) | 30 |

### Deploy

```bash
bomiot deploy <project_name>
```

Generates a Supervisor config file for daemon deployment.

---

## Packaging & Release

```bash
bomiot package <project_name>
```

Packages the project into a single-file executable; core modules can be compiled to binary.

---

## System Validation

```bash
bomiot keys
```

Initializes validation keys used for encrypting sensitive configs like database settings.

---

## Usage Example

```bash
# 1. Initialize
bomiot init

# 2. Create project
bomiot project warehouse

# 3. Enter project, create app
cd warehouse
bomiot new inbound

# 4. Database
bomiot makemigrations
bomiot migrate

# 5. Create admin
bomiot initadmin

# 6. Start server
bomiot run --host 0.0.0.0 --port 8000

# 7. Package
bomiot package warehouse
```

---

## Log Levels

`--log-level` accepts: `critical` / `error` / `warning` / `info` / `debug` / `trace`

```bash
bomiot run --log-level debug
```
