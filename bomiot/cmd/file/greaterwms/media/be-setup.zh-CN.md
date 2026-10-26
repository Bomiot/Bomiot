# 项目配置（setup.ini）

`setup.ini` 位于工作空间根目录（与工程目录同级），由 `bomiot init` 生成。框架在启动时一次性读取它：数据库、限流、JWT、文件上传、邮件、后台服务等运行时行为都集中在此文件。桌面版启动器也会读取其中部分配置（如控制台窗口开关）。修改后需重启服务生效。

## 配置文件全貌

```ini
[project]
name = greaterwms

[debug]
debug = True

[database]
# engine，Accept (sqlite、mysql、oracle、postgresql)
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port

[templates]
name = templates/dist/spa/index.html

[locale]
time_zone = 'UTC'

[throttle]
allocation_seconds = 1
throttle_seconds = 10

[request]
limit = 2

[jwt]
user_jwt_time = 1000000

[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf

[mail]
email_host = email_host
email_port = 465
email_host_user = email_host_user
email_host_password = email_host_password
default_from_email = default_from_email
email_from = email_from
email_use_ssl = True

[system_control]
observer = False
scheduler = True
server_monitor = False
```

## [project]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `name` | `greaterwms` | 工程名，固定为 `greaterwms`，不可修改。框架以它作为模板目录、静态文件目录、媒体目录与动态 app 扫描的根路径，修改后工程将无法启动 |

## [debug]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `debug` | `True` | 调试模式总开关 |

该值影响两处行为：

- **框架调试模式**：框架启动时读取，作为服务的 DEBUG 标志。
- **构建包控制台**：`debug = True` 时，`bomiot build` 构建出的应用包会带 console 控制台。其中 Windows 的控制台由启动器在每次启动时按该值显示 / 隐藏，随启动即时生效；macOS 则在构建时把该值固化进应用包，改动后需重新执行 `bomiot build` 生效（见 CLI 命令 build 文档）。

## [database]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `engine` | `sqlite` | 数据库引擎，可选 `sqlite` / `mysql` / `postgresql` / `oracle` |
| `name` | — | 库名 |
| `user` | — | 用户名 |
| `password` | — | 密码 |
| `host` | — | 主机 |
| `port` | — | 端口 |

- `sqlite`：零配置，自动在工作空间 `dbs/` 目录下创建 `db.sqlite3`，其余字段无需填写。
- 其他引擎：`name` / `user` / `password` / `host` / `port` 全部必填，库需提前建好。

## [templates]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `name` | `templates/dist/spa/index.html` | 前端 SPA 入口 HTML 的相对路径。前端构建产物输出到该位置后即可被服务托管，一般无需修改 |

## [locale]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `time_zone` | `'UTC'` | 服务时区，同时作用于定时任务调度器 |

> 注意：当前框架版本按 `local` 段名读取该值，而随包发布的 `setup.ini` 写作 `[locale]`，因此实际生效的是默认值 `'UTC'`。如需自定义时区，请将段名同步写为 `[local]`。

## [throttle]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `allocation_seconds` | `1` | 同一 IP 两次请求的最小间隔（秒） |
| `throttle_seconds` | `10` | 间隔窗口内允许的最大请求数 |

两者组合构成请求限流：间隔小于 `allocation_seconds` 且窗口内累计请求数达到 `throttle_seconds` 时，后续请求被拒绝。

## [request]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `limit` | `2` | 连续登录失败的最大次数。超过后账号被自动停用，需管理员重新启用 |

## [jwt]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `user_jwt_time` | `1000000` | 登录令牌有效期（秒）。过期后前端需重新登录获取令牌 |

## [file]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `file_size` | `102400000` | 单个上传文件的最大字节数（约 100 MB） |
| `file_extension` | 见配置 | 允许上传的扩展名白名单，逗号分隔，不含点号 |

超出大小或扩展名不在白名单内的上传请求会被拒绝。

## [mail]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `email_host` | — | SMTP 主机 |
| `email_port` | `465` | SMTP 端口 |
| `email_host_user` | — | SMTP 账号 |
| `email_host_password` | — | SMTP 密码 / 授权码 |
| `default_from_email` | — | 默认发件人地址 |
| `email_from` | — | 发件人显示名 |
| `email_use_ssl` | `True` | 是否使用 SSL 连接 |

## [system_control]

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `observer` | `True` | 文件监视进程开关，用于监听工程目录变更 |
| `scheduler` | `True` | 定时任务调度进程开关，关闭后所有计划任务不再执行 |
| `server_monitor` | `True` | 服务器资源监控进程开关（CPU / 内存 / 磁盘等） |

- 三个开关在服务启动时读取；整段缺失或单项缺失时按 `True` 处理。
- 发布配置中 `observer = False`、`server_monitor = False`（关闭以节省运行资源），`scheduler = True` 保持定时任务正常运行。
- 多 workers 部署时，框架通过文件锁保证这些后台进程只启动一次，不会因 worker 数量重复拉起。

## 生效方式

- `setup.ini` 在进程启动时读取一次，**修改后必须重启服务**（桌面版重启应用）才会生效。
- 其中 `debug` 对 macOS 应用是构建期配置，修改后需重新执行 `bomiot build`。
