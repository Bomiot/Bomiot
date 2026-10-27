<div align="center"><img src="https://gitee.com/Bomiot/Bomiot/raw/main/bomiot/server/media/img/logo.png" alt="Bomiot logo" width="180" height="auto" />

# 🚀 Bomiot

**AI writes the code, Bomiot packs and ships it**

*Binary · Cross-platform · Incremental updates · Source code protection*

[English](README.md) | [中文](README_CN.md)

[![PyPI Downloads](https://img.shields.io/pypi/dm/bomiot?label=PyPI&color=green)](https://pepy.tech/projects/bomiot)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/vue-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![GitHub Stars](https://img.shields.io/github/stars/bomiot/bomiot?style=social)](https://github.com/bomiot/bomiot)
[![Home](https://img.shields.io/badge/Home-Online-brightgreen)](https://www.bomiot.com)

</div>

---

## 🌟 About Bomiot

> **Bomiot is not some "revolutionary magic framework"** — it turns a real need for Python apps, **no-environment delivery + continuous updates + code protection**, into a complete out-of-the-box pipeline: **letting developers hand their finished apps — no environment, no source code, still continuously updated — to non-technical users.**

AI has compressed coding to minutes, yet delivery stands still. Bomiot fills exactly that gap: `init` → `run` → `build` → `publish`, one chain end to end. The end-user experience rivals a mobile app: double-click to run, silent background updates, automatic fallback on failure.

| Pain Point | Bomiot Solution |
| :--- | :--- |
| 🐢 Hard delivery, environment coupling | ✅ Compiled portable binary — no Python needed, double-click to run |
| 🔄 Users never update | ✅ Incremental auto-update, delta download, fallback on failure, zero awareness |
| 🧩 Endless frontend-backend alignment | ✅ Unified interaction contract, four fixed endpoints, parallel development |
| 🗂️ One person maintaining many systems | ✅ Multi-project isolation via the `project` request header |
| 🛡️ Source code exposed | ✅ Compiled to native binary, effectively improving code protection |

Honest boundaries: protection raises the bar but is not unbreakable; artifacts are larger than native apps; it only fits scenarios where **you actually need to hand your project to someone else**.

---

## ✨ Core Features

| Feature | Description |
| :--- | :--- |
| 📦 No-Environment Delivery | `bomiot build` compiles a portable program — copy and run |
| 🔄 Incremental Auto-Update | Per-file hash manifest comparison — only changes download; chunked large files with resumable transfer; automatic fallback on failure, zero user awareness |
| 🌍 Cross-Platform | Full coverage of Windows / macOS / Linux × x64 / arm64, platform and architecture auto-detected at build time |
| 🦀 Rust ASGI Gateway | Native WebSocket, stable performance, code protection |
| 🧩 Multi-Framework | Django (default) / FastAPI / Flask, sharing one ORM and data layer |
| 📐 Interaction Contract | `bomiot api` generates full CRUD endpoints; business logic lives in `receiver.py`, hot-effective |
| 🗂️ Multi-Project | Multiple projects per workspace, one-click frontend switch, backend data isolation |
| 🔑 Permissions | Declared via `name` in `urls.py`; JWT auth, department isolation, soft delete |
| ⏰ Scheduled Tasks | Functions in `task.py` + `JobList` registration; cron / interval / date triggers |
| 📁 File Monitoring | Watches `media/`, auto-registers to database, `files.py` takeover |
| 📊 System Monitoring | Periodic CPU / memory / disk / network / process collection, `server.py` takeover |

---

## 🌍 Cross-Platform Support

One codebase, runs everywhere. `bomiot build` auto-detects the current OS and CPU architecture with no arguments; to get a package for a platform, run one build on that platform.

| Platform | Architecture | Notes |
| :--- | :--- | :--- |
| Windows | x64 | Windows 7 and above — the most common desktop delivery target |
| macOS | x64 / arm64 (Apple Silicon) | Intel and M-series chips auto-detected |
| Linux | x64 / arm64 | Ubuntu 22.04+ / glibc 2.35+, covering servers and embedded devices |

- 🖥️ **All kinds of devices**: office PCs, cloud servers, industrial PCs, Raspberry Pi, edge gateways — build one package and it runs wherever you copy it
- 🔒 **Local data**: data stays on each node's own machine — suited for intranets, offline sites and data-sovereignty requirements
- 🔁 **Platform-isolated updates**: one manifest `manifest--{app}-{os}-{arch}.json` per platform — a Windows client will never pull a macOS package

---

## 🚀 Quick Start (5 Minutes)

Requirements: Python 3.11+, Windows / macOS / Linux.

```bash
pip install bomiot        # 1. Install
mkdir myapp && cd myapp
bomiot init               # 2. Scaffold the project (idempotent, safe to re-run)
bomiot migrate            # 3. Create tables
bomiot initadmin          # 4. Create admin (command prints the initial password)
bomiot run                # 5. Start the server
bomiot build              # 6. Package: artifacts in build/, double-click to run
```

Open `http://127.0.0.1:8000` and log in with the admin account.

> Replace `logo.ico / logo.icns / logo.png` and `splash.png` with your own assets before building. Need packages for other platforms? Just run `bomiot build` on a machine or CI runner of that platform.

---

## 🛠️ CLI Reference

| Command | Description |
| :--- | :--- |
| `bomiot init` | Initialize the workspace |
| `bomiot project <name>` | Create a business project |
| `bomiot app <name>` | Create a business app (basic skeleton) |
| `bomiot api <name>` | Create an API app (full CRUD template) |
| `bomiot makemigrations` / `migrate` | Generate / apply database migrations |
| `bomiot loaddata` / `dumpdata` | Import / export data |
| `bomiot initadmin` / `initpwd` | Create admin / reset password |
| `bomiot run [-b host] [-p port] [-w workers]` | Start the server (default `0.0.0.0:8000`; keep 1 worker on Windows) |
| `bomiot build` | Build the current platform's package locally |
| `bomiot publish --os=<os> --code=<code>` | Publish an incremental update (`--os`: `windows`/`macos`/`linux`) |

---

## 🔧 Configuration (setup.ini)

`setup.ini` at the workspace root, loaded at startup — **restart after changes**:

| Section | Key | Description |
| :--- | :--- | :--- |
| `[database]` | `engine` | `sqlite` (default, zero-config) / `mysql` / `postgresql` / `oracle` |
| `[debug]` | `debug` | Must be `False` in production |
| `[file]` | `file_size` / `file_extension` | Upload size limit (~100MB default) and allowed extensions |
| `[jwt]` | `user_jwt_time` | Login token validity (seconds) |
| `[throttle]` / `[request]` | - | API rate limiting (per IP + HTTP method) |
| `[mail]` | - | SMTP email configuration |
| `[system_control]` | `observer` / `scheduler` / `server_monitor` | Switches for file monitoring / scheduler / system monitoring — all on by default |

---

## 📦 Build, Publish & Auto-Update

`launcher.py` (generated by `bomiot init`) is the project hub — `app_name` / `version` / `base_url` (update server) are mandatory; build, publish and client updates all read it. To append packaging content, create `builder.toml` in the project root.

```bash
bomiot build                                 # Local build → build/ directory
bomiot publish --os=windows --code=example   # Publish to the update server
```

### Version Control: Every File Has a Fingerprint

- Each build generates a manifest `manifest--{app_name}-{os}-{arch}.json` recording **the hash of every shipped file** — the manifest is this version's complete fingerprint set
- Versions are strictly scoped per platform: one `{app_name}-{version}-{os}` directory per release; manifests for `windows` / `macos` / `linux` and `x64` / `arm64` never interfere — a Windows client only pulls Windows packages
- Republishing the same version for the same platform is skipped after server-side comparison — nothing is uploaded twice
- The `--code` publish passphrase is verified by the server, preventing anyone who learns your project identifier from impersonating you and uploading tampered updates

### Auto-Update: What Happens When a Client Starts

1. **Version check**: the client reads its local manifest and requests the remote version digest from `base_url` — if identical, it starts directly with zero overhead
2. **Fetch manifest**: on mismatch, it pulls the complete remote manifest (per-file hashes)
3. **Incremental download**: files are compared hash by hash — **only new and changed files are downloaded**; untouched files are never transferred
4. **Resumable transfer**: large files download in chunks; a dropped connection resumes from where it stopped, never from scratch
5. **Silent swap**: after download, an update script is generated; the app exits, the script replaces the files and restarts the app — the user notices nothing
6. **Failure fallback**: if the download breaks or checksums fail, the update is abandoned, the app starts with the local version, and retries on next launch

User business data (databases, logs, caches) is outside the update scope — no matter how versions change, data is never touched.

---

## 🌐 Deployment & Distribution

Bomiot offers two deployment approaches — **both completely free**:

| Comparison | `bomiot run` (server deployment) | `bomiot build` + `publish` (node distribution) |
| :--- | :--- | :--- |
| Runtime | Requires Python and dependencies | Portable, double-click to run |
| Incremental updates | Handle it yourself | Built-in silent updates |
| Code protection | Plain source | Compiled binary |
| Device binding | None | Unique binding per device |

### Traditional Server Deployment

```bash
bomiot run --host 0.0.0.0 --port 8000
```

For public-network deployment, configure HTTPS (`--ssl-keyfile` + `--ssl-certfile`); run multiple workers on Linux / macOS.

### Node-Based Distribution

The portable runtime files generated by `bomiot build` can be deployed directly to physical devices (PCs, industrial PCs, Raspberry Pi) or cloud server instances. On first run the program generates a machine-identity file `auth_key.py`; bring it to the official website to exchange for `sponsor.py` and the device binding is complete — all verification is performed **locally**, valid only for the current device; re-binding is required when switching machines.

> **Privacy commitment**: verification works offline, uploads no node information or business data — your code and data stay on the local node.

---

## ⚠️ Security Notice

For production: set `[debug]` to `False`; HTTPS is mandatory on the public network (`--ssl-keyfile` + `--ssl-certfile`); back up the database (`bomiot dumpdata`) and `setup.ini` regularly. Change the auto-update URL and update-file storage path to prevent unauthorized uploads to your update server.

---

## 🤝 Contributing

Website: https://www.bomiot.com

## 📄 License

**Apache License 2.0** — see the LICENSE file.

---

**⭐ If Bomiot helps you, please give it a Star!**

**Ready out of the box, continuously updated.** That is the promise we can give you.

Made with ❤️ by Bomiot Team
