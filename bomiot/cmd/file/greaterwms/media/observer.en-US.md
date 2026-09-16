# Real-time Files

## Introduction

- **Bomiot** monitors file changes in the `media` folder in real time, including creation, modification, deletion, and movement.
- Any file change is automatically written to the database (`Files` model), recording file name, type, size, and owner.
- **Bomiot** broadcasts `bomiot_signals` in real time, and the signal is forwarded to `files.py` for custom handling.

---

## How It Works

1. `ObserverManager` watches `MEDIA_ROOT` recursively using `watchdog`.
2. When a file is created or modified, a `Files` record is created/updated in the database.
3. A `bomiot_signals` signal is sent with `models: 'Files'`.
4. The signal handler calls `file_get` in `greaterwms/files.py`, passing the file data.

> Note: Signals are only sent for **create** and **update** events. Delete and move events only update the database.

---

## Get File Information

After running `bomiot project <your_project>`, you will get the following file structure:

```shell
your-project/                  # Project directory
├── media/                     # Static files
│   ├── img/                   # Public images
│   └── ***.md                 # Various documents
├── __version__.py             # your_project version
├── bomiotconf.ini             # Bomiot project identification file
└── files.py                   # File signal handler
setup.ini                      # Project configuration file
...
```

All file information changes are transmitted to `files.py` in real time. The default template is commented out — uncomment it to enable:

```python
class FileClass:
    def file_get(self, data):
        print(data)
```

You will receive a set of real-time JSON data:

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

You can obtain information through `files.py` after data changes and do anything you need.

---

## File Owner Detection

The file owner is determined by the parent directory name. The directory name under `media/` must match an existing username for the file to be registered:

```
media/
├── admin/          # Files here belong to user "admin"
│   └── icon.png
└── alice/          # Files here belong to user "alice"
    └── report.pdf
```

---

## Sharing

- Users can share their files with other users.
- When a user updates a file, the shared user will also receive the updated file in real time.

---

## Storage Location

- Files are stored at `media/<user>/<file_name>`.

`Note:`

- All front-end and back-end files are stored under the `media` directory.

---

## Restrictions

In `setup.ini`, you can customize file size and format restrictions.

- `file_size` is the file size in bytes.
- `file_extension` is the allowed file formats; files not in the list are not allowed to be uploaded.

```ini
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

---

## Enable File Monitoring

Make sure `observer = True` under `[system_control]` in `setup.ini`. The file monitor starts automatically when the service launches.

```ini
[system_control]
observer = True
```
