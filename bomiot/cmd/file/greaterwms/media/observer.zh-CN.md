# 实时文件

## 介绍

- **Bomiot** 会实时监控 `media` 文件夹下的文件变化，包括创建、修改、删除和移动。
- 文件的任何变化都会自动写入数据库（`Files` 模型），记录文件名、类型、大小和所属用户。
- **Bomiot** 会在后台实时广播 `bomiot_signals` 信号，信号会转发到 `files.py` 供自定义处理。

---

## 工作原理

1. `ObserverManager` 使用 `watchdog` 递归监控 `MEDIA_ROOT` 目录。
2. 当文件被创建或修改时，在数据库中创建/更新 `Files` 记录。
3. 发送 `bomiot_signals` 信号，`models` 为 `'Files'`。
4. 信号处理器调用 `greaterwms/files.py` 中的 `file_get` 方法，传入文件数据。

> 注意：信号仅在 **创建** 和 **修改** 事件时发送。删除和移动事件仅更新数据库。

---

## 获取文件信息

使用命令 `bomiot project <your_project>` 后，你会得到以下文件结构：

```shell
your-project/                  # 项目目录
├── media/                     # 静态文件
│   ├── img/                   # 公用图片
│   └── ***.md                 # 各种文档
├── __version__.py             # 项目版本
├── bomiotconf.ini             # Bomiot 项目标识文件
└── files.py                   # 文件信号处理
setup.ini                      # 项目配置文件
...
```

所有文件信息变化都会实时传送到 `files.py` 中。默认模板是注释状态，取消注释即可启用：

```python
class FileClass:
    def file_get(self, data):
        print(data)
```

你会得到一组实时的 JSON 数据：

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

可以在数据变化后，通过 `files.py` 获取信息并做任何事情。

---

## 文件所属用户识别

文件所属用户由父目录名称决定。`media/` 下的目录名必须与已存在的用户名匹配，文件才会被登记：

```
media/
├── admin/          # 此处的文件属于用户 "admin"
│   └── icon.png
└── alice/          # 此处的文件属于用户 "alice"
    └── report.pdf
```

---

## 分享

- 用户可以将自己的文件分享给其他用户。
- 当用户更新文件后，被分享的用户也会实时获得更新的文件。

---

## 存放位置

- 文件存放在 `media/<user>/<file_name>`。

`注意:`

- 前后端全部文件都存放在 `media` 目录下。

---

## 限制

在 `setup.ini` 中，可以自定义文件的尺寸和格式限制。

- `file_size` 是文件大小，单位为字节。
- `file_extension` 是允许的文件格式，不在列表内的文件不被允许上传。

```ini
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

---

## 启用文件监控

确保 `setup.ini` 中 `[system_control]` 的 `observer = True`，服务启动后自动启用文件监控。

```ini
[system_control]
observer = True
```
