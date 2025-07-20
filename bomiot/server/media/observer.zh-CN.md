# 实时文件

## 介绍

- **Bomiot** 会实时监控media文件夹下，用户的文件变化
- 文件的任何变化，都会实时存入数据库
- **Bomiot** 会后台实时释放信号，让程序获取

---

## 获取文件信息

- 使用命令 `bomiot project <your_project>` 后，你会得到一个文件结构

```shell
your-project/                  # 项目目录
├── media/                     # 静态文件
│   ├── img/                   # 公用图片       
│   └── ***.md                 # md的各种文档
├── __version__.py             # your_project版本
├── bomiotconf.ini             # Bomiot项目标识文件
└── files.py                   # 文件信号
setup.ini                      # 项目配置文件
...

```

- 所有的文件信息变化，会实时传送给到`files.py`中

```python
class FileClass:
    def file_get(self, data):
        print(data)
```

- 会得到一组json数据，这组数据是实时的

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

- 可以在数据变化后，通过`files.py`获取信息，并做任何事情

---

## 分享

- 用户可以将自己的文件分享给其他用户
- 当用户更新文件后，被分享的用户也会实时获得更新的文件

---

## 存放位置

- `media/<user>/<file_name>`

`注意:`
- 前后端全部存放在media地址下

## 限制

- 在`setup.ini`中，可以自定义文件的尺寸和格式限制
- file_size是文件大小，byte单位
- file_extension是文件格式，不在文件列表内的，不被允许上传

```ini
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```