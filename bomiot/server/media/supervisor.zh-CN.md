# Supervisor 使用指南

## 简介

**Supervisor** 是一款专为类 UNIX 操作系统设计的强大进程控制系统。它允许您监视和控制类 UNIX 系统上的多个进程，尤其适用于管理长时间运行的服务，例如 Web 服务器、后台作业等。

---

## Supervisor 的功能

- 轻松的进程管理（启动、停止、重启、监控）
- 进程失败时自动重启
- 集中式日志记录和日志轮换
- 基于 Web 的监控界面
- 分组进程进行批量控制
- 事件通知和可扩展性

---

## 安装

您可以使用 pip 安装 Supervisor：

```bash
pip install supervisor
```

或者使用您系统的包管理器安装（可能不是最新版本）：

```bash
# Ubuntu/Debian
sudo apt-get install supervisor

# CentOS/RHEL
sudo yum install supervisor
```

检查版本：

```bash
supervisord --version
```

---

## 快速入门

1. **生成默认配置文件**（如果不存在）：

```bash
echo_supervisord_conf > supervisord.conf
```

2. **编辑`supervisord.conf`** 定义你的托管程序。

3. **启动 Supervisor：**

```bash
supervisord -c supervisord.conf
```

4. **控制进程：**

```bash
supervisorctl -c supervisord.conf status
supervisorctl -c supervisord.conf start <program>
supervisorctl -c supervisord.conf stop <program>
```

---

## 配置文件说明

配置文件通常名为 `supervisord.conf`，并遵循 INI 格式。关键部分：

### `[supervisord]`

- 主要 Supervisor 进程设置（日志文件、pid 文件等）

### `[program:<name>]`

- 定义要管理的进程

示例：

```ini
[program:myapp]
command=/home/user/venv/bin/python /home/user/myapp/app.py
directory=/home/user/myapp
autostart=true
autorestart=true
stderr_logfile=/var/log/myapp.err.log
stdout_logfile=/var/log/myapp.out.log
user=myuser
```

### `[group:<name>]`

- 将多个程序分组

### `[inet_http_server]`（可选）

- 启用 Web 界面

---

## 基本操作

- **启动 Supervisor**
```bash
supervisord -c supervisord.conf
```
- **停止 Supervisor：**
```bash
supervisorctl -c supervisord.conf shutdown
```
- **重新加载配置：**
```bash
supervisorctl -c supervisord.conf reload
```
- **查看所有管理程序：**
```bash
supervisorctl -c supervisord.conf status
```

---

## 管理程序

- **启动程序：**
```bash
supervisorctl start myapp
```
- **停止程序：**
```bash
supervisorctl stop myapp
```
- **重启程序：**
```bash
supervisorctl restart myapp
```
- **启动/停止所有程序：**
```bash
supervisorctl start all
supervisorctl stop all
```

---

## 常用配置选项

| 选项 | 说明 |
|-------------------------|------------------------------------------------------------------------|
| `command` | 要运行的命令 |
| `directory` | 工作目录 |
| `autostart` | 是否自动启动 (true/false) |
| `autorestart` | 退出时重新启动 (true/false/意外) |
| `startretries` | 失败时的重试次数 |
| `user` | 运行用户 |
| `environment` | 设置环境变量（例如 `ENV=production`）|
| `stdout_logfile` | 标准输出日志文件 |
| `stderr_logfile` | 标准错误日志文件 |
| `redirect_stderr` | 将 stderr 重定向到 stdout (true/false) |
| `stopasgroup`, `killasgroup` | 停止时终止子进程 |

---

## Web 界面

您可以通过添加以下命令启用 Web 界面：

```ini
[inet_http_server]
port=127.0.0.1:9001
username=您的用户名
password=您的密码
```

- 通过 `http://127.0.0.1:9001/` 访问
- 通过浏览器查看和控制进程

---

## 日志管理

- 每个程序都可以拥有自己的 `stdout_logfile` 和 `stderr_logfile`。
- 使用 `stdout_logfile_maxbytes` 和 `stdout_logfile_backups` 进行日志轮转：

```ini
stdout_logfile_maxbytes=20MB
stdout_logfile_backups=10
```

---

## 进程组

- 将多个程序分组进行批量控制：

```ini
[group:webapps]
programs=myapp,anotherapp
```

- 使用 `supervisorctl start webapps:all` 进行控制

---

## Supervisorctl 命令用法

- 以交互方式使用 `supervisorctl`：

```bash
supervisorctl
```

然后输入 `status`、`start myapp`、`stop all` 等命令。

- 或者以单次模式使用：

```bash
supervisorctl restart myapp
```

---

## 最佳实践与技巧

- 除非必要，否则切勿以 root 身份运行；请使用 `user` 参数。
- 在 `/etc/supervisor/conf.d/` 中为每个服务使用一个配置文件，并将其包含在主配置中。
- 监控日志文件大小以避免磁盘问题。
- 使用 `stopasgroup` 和 `killasgroup` 进行正确的进程树清理。
- 使用强密码保护 Web 界面或仅绑定到本地主机。
- 对于生产环境，请使用 `systemd` 或操作系统的 init 系统管理 Supervisor。

---

## 常见问题

**问题 1：Supervisor 可以管理非 Python 进程吗？**
答：可以。它可以管理任何进程（Node.js、Java、Shell 脚本等），只要它们在前台运行。

**问题 2：如何在不停止正在运行的程序的情况下重新加载配置？**
答：使用 `supervisorctl reread` 和 `supervisorctl update` 添加/删除程序。

**问题 3：日志存储在哪里？**
答：由配置中的 `stdout_logfile` 和 `stderr_logfile` 指定。

**问题 4：如何在系统启动时自动启动 Supervisor？**
答：使用操作系统的初始化系统（systemd、upstart 等）将 Supervisor 启用为服务。

---

## 参考资料

- [Supervisor 官方文档](http://supervisord.org/)
- [Supervisor GitHub 仓库](https://github.com/Supervisor/supervisor)
- [Supervisorctl 文档](http://supervisord.org/running.html#supervisorctl-command-line-interface)
- [Supervisor 配置指南](http://supervisord.org/configuration.html)

---