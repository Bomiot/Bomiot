# bomiot publish

Publish a built platform artifact to the update server for client incremental updates.

```bash
bomiot publish --os=windows --code=example
```

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `--os` | Yes | Target platform: `windows`, `macos` or `linux` (lowercase) |
| `--code` | Yes | Publish token, verified by the server. Prevents anyone who obtains build.json (the project's unique identifier) from impersonating the project and uploading tampered update files. If forgotten, it can be found in the `verify_code` field of the update app's UpdateModel table |

The command must be run from the **project root** (where `launcher.py` lives).

## Prerequisites

1. The platform has been built with `bomiot build`; the manifest file and output directory exist under `build/`
2. `launcher.py` defines `app_name` and `base_url` (the update server address)
3. A valid publish token (`--code`)

> You can publish an artifact for a different platform than the current machine (e.g. publish a macOS build from Windows), as long as the build output for that platform exists under `build/`.

## Execution Flow

```text
bomiot publish --os=windows --code=example
  │
  ├─ 1. Read launcher.py for app_name and base_url
  ├─ 2. Send --code to the server for publish token verification
  ├─ 3. Locate the manifest and output directory for the platform under build/
  ├─ 4. Ask the server whether this version needs publishing
  ├─ 5. If yes, package the manifest and artifacts and upload them
  └─ 6. Done — clients will pick up this version on next launch
```

Possible outcomes:

- **Publish needed**: artifacts are packaged and uploaded, success is reported
- **Nothing to do**: the same version for this platform already exists on the server; the command exits without uploading
- **Artifacts not found**: no build output for the given platform under `build/`; the command aborts with an error and uploads nothing

## Incremental Updates with launcher.py

The publisher (bomiot publish) and the client (launcher.py) stay in sync through a set of **naming conventions**. The server only stores and serves files by name — it never guesses the client platform.

### Naming Conventions

| Artifact | Format | Example |
|---|---|---|
| Manifest file | `manifest--{app_name}-{os}-{arch}.json` | `manifest--MyApp-windows-x64.json` |
| Build output directory | `{app_name}-{version}-{os}` | `MyApp-1.0.0-windows` |
| Upload archive | `{app_name}--{version}-{os}.tar.xz` | `MyApp--1.0.0-windows.tar.xz` |

`os` and `arch` are baked into the manifest filename at build time. The publisher locates artifacts via `--os`; the client detects its own platform at startup and requests the manifest with exactly the same naming rule — a Windows x64 client only ever receives windows-x64 updates, so platforms never interfere.

### Update Flow

1. **Client startup**: launcher.py reads the local manifest and asks `POST /update/` for the remote version summary of its platform
2. **Compare**: if the summary matches the local manifest, the app starts directly; otherwise an update begins
3. **Fetch manifest**: the full remote manifest (per-file integrity info) is fetched via `POST /update/manifest/`
4. **Diff & download**: only new or changed files are downloaded from `/update/download/...`; large files are fetched in blocks with resume support
5. **Apply**: once downloads complete, an update script is generated; the app exits and the script replaces files and restarts it
6. **Fault tolerance**: if a download is interrupted or fails verification, the update is abandoned and the app starts with the local version, retrying on next launch

User data directories (databases, logs, caches) are never touched by updates.

## Server API

The update service is provided by the `greaterwms.update` app, mounted under `/update/` of `base_url`:

| Endpoint | Method | Purpose |
|---|---|---|
| `/update/` | POST | Client version summary check |
| `/update/manifest/` | POST | Fetch the full manifest for a platform |
| `/update/download/<path>` | GET | Download update files (Range supported) |
| `/update/publish/` | POST | Pre-publish version status check |
| `/update/upload/` | POST | Upload publish artifacts |

## Notes

- `--os` is lowercase and must match the platform label of the build output; a wrong value fails with "manifest not found" and publishes nothing
- A wrong publish token is rejected by the server; nothing is uploaded
- Re-publishing the same version for the same platform is reported as unnecessary and exits without uploading
- To prevent others from POSTing files to your update server, it is recommended to change the auto-update URL and the storage location of update files; if the storage location is changed, the corresponding path in `launcher.py` must be updated as well, otherwise clients cannot download update files
