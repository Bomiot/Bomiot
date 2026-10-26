# 实时文件

## 介绍

Bomiot 内置文件监控器，在后台实时监听 `media` 目录的创建、修改、删除和移动事件：

- 文件变化自动写入数据库（`Files` 模型），记录文件名、类型、大小和所属用户
- 创建与修改事件会广播 `bomiot_signals` 信号，信号自动转发到项目根目录的 `files.py`，供你接管自定义逻辑

整个过程无需编写任何监听代码，取消 `files.py` 中的注释即可接收数据。

---

## 工作流程

1. **启动**：服务启动时读取 `setup.ini`，`[system_control] observer = True` 时拉起一个守护线程，递归监听 `media` 目录
2. **事件聚合**：文件系统事件触发后做 0.2 秒防抖，短暂间隔内的连续变化（如一次保存产生的多个事件）会合并为一次处理，避免重复通知
3. **快照比对**：对目录做前后快照差异比对，得出本次的创建、修改、删除、移动文件清单
4. **写入数据库**：按清单更新 `Files` 模型记录（详见下方事件行为表）
5. **信号分发**：创建与修改事件发送 `bomiot_signals` 信号，框架按 `models: 'Files'` 路由
6. **项目接管**：框架用 AST 解析项目根目录 `files.py`，若定义了 `file_get` 方法则动态加载并调用，传入文件数据

### 各事件行为

| 事件 | 数据库行为 | 是否发送信号 |
|---|---|---|
| 创建 | 新建 `Files` 记录 | ✅ |
| 修改 | 更新记录（大小、恢复 `is_delete`） | ✅ |
| 删除 | 删除记录 | ❌ |
| 移动 | 原位置删除记录，新位置新建记录 | ❌ |

> 删除与移动只同步数据库，不触发 `files.py`。

---

## 文件位置

文件信号统一由主工程目录下的 `files.py` 接管：

```shell
workspace/                    # 工作区
├── setup.ini                 # 项目配置文件
└── greaterwms/               # 主工程目录
    ├── media/                # 文件与文档目录
    └── files.py              # 文件信号处理
```

## 接管文件信号

`files.py` 默认模板为注释状态，取消注释即可启用：

```python
class FileClass:
    def file_get(self, data):
        print(data)
```

每次文件创建或修改，`file_get` 会收到一组实时 JSON 数据：

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

拿到数据后可以执行任何自定义逻辑：内容扫描、格式转换、第三方同步、通知推送等。

---

## 文件所属用户识别

文件所属用户由**父目录名称**决定：`media/` 下一级目录名必须与已存在的用户名匹配，文件才会被登记并触发信号：

```
media/
├── admin/          # 此目录下的文件属于用户 "admin"
│   └── icon.png
└── alice/          # 此目录下的文件属于用户 "alice"
    └── report.pdf
```

不在用户目录下的文件变化会被忽略。

---

## 分享

- 用户可以将自己的文件分享给其他用户（`shared_to` 字段）
- 文件更新后，被分享的用户会实时获得更新后的文件

---

## 存放位置

- 文件统一存放在 `media/<用户名>/<文件名>`
- 前后端全部文件都在 `media` 目录下

---

## 上传限制

`setup.ini` 的 `[file]` 段控制上传文件的尺寸与格式：

```ini
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

- `file_size`：单文件大小上限，单位字节
- `file_extension`：允许的文件格式，不在列表内的文件禁止上传

---

## 启用文件监控

确保 `setup.ini` 中开启监控开关，服务启动后自动生效：

```ini
[system_control]
observer = True
```

多 workers 部署时框架通过文件锁保证监控线程只启动一次，不会因多进程而重复通知。
