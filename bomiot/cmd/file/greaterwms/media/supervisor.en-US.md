# Supervisor Guide

## Introduction

**Supervisor** is a process control system written in Python that monitors and manages processes on UNIX-like operating systems. It is especially suited for hosting long-running services such as web servers and background jobs.

> Supervisor **does not run on Windows** — it only works on UNIX-like systems such as Linux and macOS.

It consists of four parts:

| Component | Role |
|---|---|
| `supervisord` | The daemon itself; spawns and supervises all child processes |
| `supervisorctl` | The command-line client used to inspect and control processes managed by supervisord |
| Web interface | An optional browser-based management page (enabled via inet_http_server) |
| XML-RPC interface | An API for third-party integration (the web UI is built on it) |

---

## Installation

```bash
pip install supervisor
```

Or via the system package manager (versions may lag behind):

```bash
# Ubuntu / Debian
sudo apt-get install supervisor

# CentOS / RHEL
sudo yum install supervisor
```

Verify:

```bash
supervisord --version
```

---

## Quick Start

1. **Generate a fully commented sample configuration**:

```bash
echo_supervisord_conf > /etc/supervisord.conf
```

2. **Edit the config** and append the programs to manage at the end (see `[program:x]` below).

3. **Start the daemon**:

```bash
supervisord -c /etc/supervisord.conf
```

4. **Control processes with the client**:

```bash
supervisorctl -c /etc/supervisord.conf status
supervisorctl -c /etc/supervisord.conf start myapp
supervisorctl -c /etc/supervisord.conf stop myapp
```

---

## Configuration in Detail

The config file uses INI format. The key sections:

### `[unix_http_server]`

supervisorctl talks to the daemon over a Unix socket by default, so this section **must exist**:

```ini
[unix_http_server]
file=/tmp/supervisor.sock
chmod=0700
```

### `[supervisord]`

Runtime settings of the daemon itself:

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

Client connection settings, matching unix_http_server:

```ini
[supervisorctl]
serverurl=unix:///tmp/supervisor.sock
```

### `[program:x]` — the core section

One section per managed program, where `x` is the program name:

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

Key options:

| Option | Description |
|---|---|
| `command` | The launch command. **The program must run in the foreground** — it must not daemonize itself |
| `autostart` | Start automatically when supervisord starts (true/false) |
| `autorestart` | Restart policy on exit: `false` never; `true` always; `unexpected` only when the exit code is not listed in `exitcodes` |
| `startsecs` | The process must stay up this many seconds to count as "started successfully", otherwise startup is considered failed |
| `startretries` | Max startup attempts before giving up and entering FATAL |
| `exitcodes` | Exit codes considered "expected", default `0` |
| `stopsignal` | Signal used to stop the process (TERM/INT/QUIT/HUP/KILL…) |
| `stopwaitsecs` | Seconds to wait after the stop signal before forcing SIGKILL |
| `stopasgroup` / `killasgroup` | Apply stop/kill to the whole process group, preventing orphaned children |
| `numprocs` + `process_name` | Run multiple instances, e.g. `process_name=%(program_name)s_%(process_num)02d` with `numprocs=4` |
| `priority` | Startup order weight; lower numbers start first and stop last |
| `user` | Run as this user — **avoid root unless necessary** |
| `redirect_stderr` | When true, stderr is merged into the stdout log |

### `[include]` — splitting configuration

With many programs, keep one file per program and include them from the main config:

```ini
[include]
files = /etc/supervisor/conf.d/*.conf
```

### `[inet_http_server]` — web UI (optional)

```ini
[inet_http_server]
port=127.0.0.1:9001
username=admin
password=strong_password
```

Open `http://127.0.0.1:9001/` in a browser to view and control processes. Binding to `127.0.0.1` allows local access only; if you expose it, always set a username and password.

### `[group:x]` — process groups

```ini
[group:webapps]
programs=myapp,anotherapp
priority=999
```

Then operate on the whole group with e.g. `supervisorctl start webapps:*`.

---

## Common supervisorctl Commands

```bash
supervisorctl status                 # status of all processes
supervisorctl start myapp            # start
supervisorctl stop myapp             # stop
supervisorctl restart myapp          # restart
supervisorctl start all              # bulk operations
supervisorctl tail myapp             # live-view a program's stdout
supervisorctl tail myapp stderr      # live-view stderr
supervisorctl signal HUP myapp       # send a signal to the process
supervisorctl reread                 # re-read the config (no effect yet)
supervisorctl update                 # apply config changes (adds/removes processes as needed)
supervisorctl reload                 # restart the supervisord daemon itself
supervisorctl shutdown               # stop supervisord and everything it manages
```

The standard routine after editing the config is `reread` + `update`: new programs get started, removed programs get stopped, and unchanged processes are left alone.

Run `supervisorctl` with no subcommand to enter interactive mode, where you can type `status`, `restart myapp`, etc. repeatedly.

---

## Process States

| State | Meaning |
|---|---|
| `STARTING` | Starting up (waiting for startsecs to elapse) |
| `RUNNING` | Running normally |
| `BACKOFF` | Exited too quickly at startup; waiting to retry |
| `FATAL` | Failed to start after startretries attempts |
| `STOPPING` | Stopping |
| `STOPPED` | Stopped |
| `EXITED` | Exited (what happens next depends on autorestart) |

---

## Notes

- **Managed programs must run in the foreground.** If a program forks itself into the background, supervisord thinks it exited and will keep restarting it.
- Control log rotation with `stdout_logfile_maxbytes` + `stdout_logfile_backups` — always set them, or logs can fill the disk.
- When stopping script-based programs, enable `stopasgroup` and `killasgroup`; otherwise children spawned through a shell may be left behind as orphans.
- Never expose the web UI directly to the public internet; if remote access is required, bind to an internal address and use a strong password.
- Let the operating system's init system (e.g. a systemd unit) start supervisord itself at boot — ready-made scripts for major distributions are available.
