# Real-Time File Monitoring

## Introduction

Bomiot ships with a built-in file monitor that watches the `media` directory in the background for create, modify, delete, and move events:

- File changes are automatically written to the database (`Files` model), recording the name, type, size, and owning user
- Create and modify events broadcast a `bomiot_signals` signal, which is automatically forwarded to `files.py` in the project root for your custom logic

No listening code is required — uncomment `files.py` and you start receiving data.

---

## How It Works

1. **Startup**: when the server starts, it reads `setup.ini`; with `[system_control] observer = True`, a daemon thread is spawned to recursively watch the `media` directory
2. **Event aggregation**: filesystem events are debounced by 0.2 seconds, so a burst of changes (e.g. the multiple events produced by a single save) is merged into one pass, avoiding duplicate notifications
3. **Snapshot diffing**: a before/after snapshot of the directory is diffed to produce the list of created, modified, deleted, and moved files
4. **Database sync**: the `Files` model is updated according to that list (see the event behavior table below)
5. **Signal dispatch**: create and modify events emit a `bomiot_signals` signal, routed by `models: 'Files'`
6. **Project takeover**: the framework parses `files.py` in the project root via AST; if a `file_get` method is defined, the module is dynamically loaded and the method is called with the file data

### Behavior per Event

| Event | Database behavior | Signal sent |
|---|---|---|
| Create | New `Files` record | ✅ |
| Modify | Update record (size, restore `is_delete`) | ✅ |
| Delete | Delete record | ❌ |
| Move | Delete record at old path, create record at new path | ❌ |

> Deletes and moves only sync the database; they do not trigger `files.py`.

---

## File Location

File signals are handled by `files.py` under the main project directory:

```shell
workspace/                    # workspace
├── setup.ini                 # project configuration
└── greaterwms/               # main project directory
    ├── media/                # files and documents
    └── files.py              # file signal handling
```

## Taking Over File Signals

The default `files.py` template is commented out. Uncomment to enable:

```python
class FileClass:
    def file_get(self, data):
        print(data)
```

On every file create or modify, `file_get` receives a real-time JSON payload:

```json
{
    "id": 1,
    "name": "icon.png",
    "type": "png",
    "size": 1702,
    "owner": "admin",
    "shared_to": ""
}
```

From here you can run any custom logic: content scanning, format conversion, third-party sync, push notifications, and so on.

---

## File Ownership

Ownership is determined by the **parent directory name**: a file is registered and its signal fired only when the first-level directory under `media/` matches an existing username:

```
media/
├── admin/          # files here belong to user "admin"
│   └── icon.png
└── alice/          # files here belong to user "alice"
    └── report.pdf
```

Changes outside a user directory are ignored.

---

## Sharing

- Users can share their files with other users (the `shared_to` field)
- When a file is updated, the users it is shared with receive the updated file in real time

---

## Storage Location

- Files are stored at `media/<username>/<filename>`
- All front-end and back-end files live under the `media` directory

---

## Upload Limits

The `[file]` section of `setup.ini` controls upload size and format:

```ini
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

- `file_size`: max size per file, in bytes
- `file_extension`: allowed formats; anything not listed is rejected

---

## Enabling the Monitor

Make sure the switch is on in `setup.ini`; it takes effect automatically at server startup:

```ini
[system_control]
observer = True
```

Under multi-worker deployments, a file lock guarantees the monitor thread starts exactly once, so notifications are never duplicated across processes.
