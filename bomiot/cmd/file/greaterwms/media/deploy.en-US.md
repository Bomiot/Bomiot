# Deployment & Packaging

## Introduction

Bomiot can package a project into a **single-file executable** (zero-dependency deployment) and provides a Supervisor daemon deployment option. Core Python code can be compiled to binary via Nuitka for source protection.

---

## Single-File Packaging

```bash
bomiot package my-project
```

Output goes to the `dist/` directory — a single executable containing runtime, dependencies, code, and assets. Double-click to run.

---

## Packaging Flow

1. Run `bomiot package <project_name>`
2. Nuitka compiles Python code to native binary
3. Runtime, dependencies, and assets are packed into one executable
4. Output the executable to `dist/`

> During packaging, core modules can be compiled to binary (`.exe` / `.so` / `.pyd`), and critical security paths can be further hardened with PyO3 (Rust). See the Code Protection doc.

---

## Supervisor Deployment

Bomiot provides the `deploy` command to generate a Supervisor config:

```bash
bomiot deploy my-project
```

The generated config can be referenced by `supervisord.conf` for daemon deployment:

```ini
# supervisord.conf example
[include]
files = /path/to/my-project/supervisord.conf
```

---

## Server Options

```bash
bomiot run [options]

Options:
  --host, -b HOST                Host address (default: 127.0.0.1)
  --port, -p PORT                Port (default: 8000)
  --workers, -w WORKERS          Worker processes (default: 1)
  --log-level LEVEL              Log level
  --ssl-keyfile FILE             SSL key file
  --ssl-certfile FILE            SSL cert file
  --proxy-headers                Enable proxy headers
  --limit-concurrency N          Max concurrent requests (default: 1000)
  --timeout-graceful-shutdown S  Graceful shutdown timeout (default: 30s)
```

### Production Example

```bash
bomiot run --host 0.0.0.0 --port 80 --workers 4 --log-level info
```

### SSL Deployment

```bash
bomiot run --ssl-keyfile key.pem --ssl-certfile cert.pem
```

---

## Frontend Deployment

Rebuild after any frontend changes:

```bash
cd templates
quasar build
```

Output goes to `templates/dist/spa/`, served directly by the Django backend.

---

## Multi-Node Collaboration

- **Standalone / LAN**: Local storage on each node, suitable for offline scenarios
- **Multi-node**: Cross-site cloud collaboration via an authorization gateway
- **Data sovereignty**: Data always stays on the local node for compliance

---

## Deployment Checklist

- [ ] Database migrated (`bomiot migrate`)
- [ ] Admin created (`bomiot initadmin`)
- [ ] Database config correct in `setup.ini`
- [ ] Frontend built (`quasar build`)
- [ ] Port not in use
- [ ] SSL certificates (if HTTPS required)
