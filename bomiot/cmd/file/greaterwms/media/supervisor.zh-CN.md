# Supervisor 使用指南

## 简介

**Supervisor** 是一个用 Python 编写的进程控制系统，用于在类 UNIX 系统上监控和管理进程，特别适合托管长时间运行的服务（Web 服务、后台任务等）。

> Supervisor **不支持 Windows**，只能运行在 Linux / macOS 等类 UNIX 系统上。

它由四个部分组成：

| 组件 | 作用 |
|---|---|
| `supervisord` | 守护进程本体，负责拉起并看管所有子进程 |
| `supervisorctl` | 命令行客户端，用来查看和控制 supervisord 托管的进程 |
| Web 界面 | 可选的浏览器管理页（通过 inet_http_server 开启） |
| XML-RPC 接口 | 供第三方程序集成的 API（Web 界面即基于此实现） |

---

## 安装

```bash
pip install supervisor
```

或用系统包管理器（版本可能偏旧）：

```bash
# Ubuntu / Debian
sudo apt-get install supervisor

# CentOS / RHEL
sudo yum install supervisor
```

验证：

```bash
supervisord --version
```

---

## 快速开始

1. **生成一份带完整注释的示例配置**：

```bash
echo_supervisord_conf > /etc/supervisord.conf
```

2. **编辑配置**，在文件末尾追加要托管的程序（见下文 `[program:x]`）。

3. **启动守护进程**：

```bash
supervisord -c /etc/supervisord.conf
```

4. **用客户端控制进程**：

```bash
supervisorctl -c /etc/supervisord.conf status
supervisorctl -c /etc/supervisord.conf start myapp
supervisorctl -c /etc/supervisord.conf stop myapp
```

---

## 配置文件详解

配置文件为 INI 格式，关键段如下。

### `[unix_http_server]`

supervisorctl 默认通过 Unix socket 与守护进程通信，这一段**必须存在**：

```ini
[unix_http_server]
file=/tmp/supervisor.sock
chmod=0700
```

### `[supervisord]`

守护进程自身的运行参数：

```ini
[supervisord]
logfile=/var/log/supervisord.log
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=/var/run/supervisord.pid
nodaemon=false
```

### `[supervisorctl]`

客户端的连接参数，与 unix_http_server 对应：

```ini
[supervisorctl]
serverurl=unix:///tmp/supervisor.sock
```

### `[program:x]` —— 核心段

每个要托管的程序一段，`x` 是程序名：

```ini
[program:myapp]
command=/home/user/venv/bin/python /home/user/myapp/app.py
process_name=%(program_name)s
numprocs=1
directory=/home/user/myapp
umask=022
priority=999
autostart=true
autorestart=unexpected
startsecs=3
startretries=3
exitcodes=0
stopsignal=TERM
stopwaitsecs=10
stopasgroup=false
killasgroup=false
user=myuser
redirect_stderr=false
stdout_logfile=/var/log/myapp.out.log
stdout_logfile_maxbytes=20MB
stdout_logfile_backups=10
stderr_logfile=/var/log/myapp.err.log
environment=LANG=en_US.UTF-8,ENV=production
```

关键选项说明：

| 选项 | 说明 |
|---|---|
| `command` | 启动命令，**程序必须在前台运行**，不能自行 daemonize |
| `autostart` | supervisord 启动时是否自动拉起（true/false） |
| `autorestart` | 退出后是否重启：`false` 不重启；`true` 总是重启；`unexpected` 仅当退出码不在 `exitcodes` 列表时重启 |
| `startsecs` | 启动后存活满 N 秒才算"启动成功"，否则视为启动失败 |
| `startretries` | 启动失败的最大重试次数，超过后进入 FATAL 状态 |
| `exitcodes` | 视为"正常退出"的退出码列表，默认 `0` |
| `stopsignal` | 停止时发送的信号（TERM/INT/QUIT/HUP/KILL…） |
| `stopwaitsecs` | 发信号后等待退出的秒数，超时则强制 SIGKILL |
| `stopasgroup` / `killasgroup` | 停止/强杀时是否作用于整个进程组，防止子进程残留 |
| `numprocs` + `process_name` | 启动多个实例，如 `process_name=%(program_name)s_%(process_num)02d` 配 `numprocs=4` |
| `priority` | 启动顺序权重，数字小先启动，停止时反过来 |
| `user` | 以指定用户身份运行，**不要无必要地用 root** |
| `redirect_stderr` | 为 true 时 stderr 合并进 stdout 日志 |

### `[include]` —— 拆分配置

程序多的时候建议每个程序一个文件，主配置引入即可：

```ini
[include]
files = /etc/supervisor/conf.d/*.conf
```

### `[inet_http_server]` —— Web 管理页（可选）

```ini
[inet_http_server]
port=127.0.0.1:9001
username=admin
password=强密码
```

浏览器访问 `http://127.0.0.1:9001/` 即可查看和控制进程。`port` 绑定到 `127.0.0.1` 仅允许本机访问；对外开放务必设置用户名密码。

### `[group:x]` —— 进程分组

```ini
[group:webapps]
programs=myapp,anotherapp
priority=999
```

之后可用 `supervisorctl start webapps:*` 批量操作整组。

---

## supervisorctl 常用命令

```bash
supervisorctl status                 # 查看所有进程状态
supervisorctl start myapp            # 启动
supervisorctl stop myapp             # 停止
supervisorctl restart myapp          # 重启
supervisorctl start all              # 批量操作
supervisorctl tail myapp             # 实时查看程序 stdout 日志
supervisorctl tail myapp stderr      # 实时查看 stderr
supervisorctl signal HUP myapp       # 向进程发信号
supervisorctl reread                 # 重新读取配置（不生效）
supervisorctl update                 # 让变更的配置生效（按需增删进程）
supervisorctl reload                 # 重启 supervisord 本体
supervisorctl shutdown               # 关闭 supervisord 及其托管的全部进程
```

修改配置后的标准动作是 `reread` + `update`：新增的程序会被启动，被删除的程序会被停止，未变更的进程不受影响。

不带子命令直接运行 `supervisorctl` 进入交互模式，可连续输入 `status`、`restart myapp` 等。

---

## 进程状态说明

| 状态 | 含义 |
|---|---|
| `STARTING` | 启动中（等待满 startsecs） |
| `RUNNING` | 正常运行 |
| `BACKOFF` | 启动过快失败，等待重试 |
| `FATAL` | 超过 startretries 次仍无法启动 |
| `STOPPING` | 停止中 |
| `STOPPED` | 已停止 |
| `EXITED` | 已退出（autorestart 决定后续动作） |

---

## 注意事项

- **托管的程序必须前台运行**。如果程序自己会 fork 到后台，supervisord 会认为它已退出并反复重启。
- 日志轮转用 `stdout_logfile_maxbytes` + `stdout_logfile_backups` 控制，务必设置，避免磁盘被日志写满。
- 停止脚本类程序时建议开启 `stopasgroup` 和 `killasgroup`，否则 shell 启动的子进程可能残留成孤儿。
- Web 管理页不要直接暴露到公网；确需远程访问时绑定内网地址并设置强密码。
- 让 supervisord 自身开机自启，交给系统初始化系统（如 systemd 的 unit 文件）管理，Supervisor 仓库提供了各发行版的现成脚本。
