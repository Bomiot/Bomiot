# Real-time files

## Introduction

- **Bomiot** will monitor the user's file changes in the media folder in real time
- Any changes to the file will be stored in the database in real time
- **Bomiot** will release signals in the background in real time for the program to obtain

---

## Get file information

- After using the command `bomiot project <your_project>`, you will get a file structure

```shell
your-project/       # Project directory
├── media/          # Static files
│ ├── img/          # Public images
│ └── ***.md        # Various documents of md
├── __version__.py  # your_project version
├── bomiotconf.ini  # Bomiot project identification file
└── files.py        # File signal
setup.ini           # Project configuration file
...

```

- All file information changes will be transmitted to `files.py` in real time

```python
class FileClass:
    def file_get(self, data):
        print(data)
```

- You will get a set of json data, which is real-time

```json
{
    'id': 1,
    'name': 'icon.png',
    'type': 'png',
    'size': 1702,
    'owner': 'admin',
    'shared_to': ''
}

```

- You can get information and do anything through `files.py` after the data changes

---

## Sharing

- Users can share their files with other users
- When a user updates a file, the shared user will also get the updated file in real time

---

## Storage location

- `media/<user>/<file_name>`

`Note:`
- All front-end and back-end are stored under the media address

## Restrictions

- In `setup.ini`, you can customize the file size and format restrictions
- file_size is the file size, in bytes
- file_extension is the file format, files not in the file list are not allowed to be uploaded

```ini
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```