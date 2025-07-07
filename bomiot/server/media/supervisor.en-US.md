# Supervisor Usage Guide

## Introduction

**Supervisor** is a powerful process control system designed for UNIX-like operating systems. It allows you to monitor and control a number of processes on UNIX-like systems, especially useful for managing long-running services such as web servers, background jobs, and more.

---

## Features of Supervisor

- Easy process management (start, stop, restart, monitor)
- Automatic process restarts on failure
- Centralized logging and log rotation
- Web-based monitoring interface
- Group processes for batch control
- Event notification and extensibility

---

## Installation

You can install Supervisor with pip:

```bash
pip install supervisor
```

Or install using your system’s package manager (may not be the latest version):

```bash
# Ubuntu/Debian
sudo apt-get install supervisor

# CentOS/RHEL
sudo yum install supervisor
```

Check version:

```bash
supervisord --version
```

---

## Quick Start

1. **Generate a default config file** (if not present):

   ```bash
   echo_supervisord_conf > supervisord.conf
   ```

2. **Edit `supervisord.conf`** to define your managed programs.

3. **Start Supervisor:**

   ```bash
   supervisord -c supervisord.conf
   ```

4. **Control processes:**

   ```bash
   supervisorctl -c supervisord.conf status
   supervisorctl -c supervisord.conf start <program>
   supervisorctl -c supervisord.conf stop <program>
   ```

---

## Configuration File Explained

The configuration file is typically named `supervisord.conf` and follows the INI format. Key sections:

### `[supervisord]`

- Main supervisor process settings (log file, pid file, etc.)

### `[program:<name>]`

- Define a process to manage

Example:

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

- Group multiple programs together

### `[inet_http_server]` (optional)

- Enable web interface

---

## Basic Operations

- **Start Supervisor:**
  ```bash
  supervisord -c supervisord.conf
  ```
- **Stop Supervisor:**
  ```bash
  supervisorctl -c supervisord.conf shutdown
  ```
- **Reload config:**
  ```bash
  supervisorctl -c supervisord.conf reload
  ```
- **View all managed programs:**
  ```bash
  supervisorctl -c supervisord.conf status
  ```

---

## Managing Programs

- **Start a program:**
  ```bash
  supervisorctl start myapp
  ```
- **Stop a program:**
  ```bash
  supervisorctl stop myapp
  ```
- **Restart a program:**
  ```bash
  supervisorctl restart myapp
  ```
- **Start/stop all:**
  ```bash
  supervisorctl start all
  supervisorctl stop all
  ```

---

## Common Configuration Options

| Option                  | Description                                                 |
|-------------------------|------------------------------------------------------------|
| `command`               | Command to run                                             |
| `directory`             | Working directory                                          |
| `autostart`             | Whether to start automatically (true/false)                |
| `autorestart`           | Restart on exit (true/false/unexpected)                    |
| `startretries`          | Number of retries on failure                               |
| `user`                  | User to run as                                             |
| `environment`           | Set environment variables (e.g. `ENV=production`)          |
| `stdout_logfile`        | Standard output log file                                   |
| `stderr_logfile`        | Standard error log file                                    |
| `redirect_stderr`       | Redirect stderr to stdout (true/false)                     |
| `stopasgroup`, `killasgroup` | Kill child processes on stop                          |

---

## Web Interface

You can enable a web interface by adding:

```ini
[inet_http_server]
port=127.0.0.1:9001
username=youruser
password=yourpassword
```

- Access via `http://127.0.0.1:9001/`
- View and control processes via browser

---

## Log Management

- Each program can have its own `stdout_logfile` and `stderr_logfile`.
- Use `stdout_logfile_maxbytes` and `stdout_logfile_backups` for log rotation:

  ```ini
  stdout_logfile_maxbytes=20MB
  stdout_logfile_backups=10
  ```

---

## Process Groups

- Group multiple programs for batch control:

  ```ini
  [group:webapps]
  programs=myapp,anotherapp
  ```

  - Control with `supervisorctl start webapps:all`

---

## Supervisorctl Command Usage

- Use `supervisorctl` interactively:

  ```bash
  supervisorctl
  ```

  Then type commands like `status`, `start myapp`, `stop all`, etc.

- Or use it in one-shot mode:

  ```bash
  supervisorctl restart myapp
  ```

---

## Best Practices & Tips

- Never run as root unless necessary; use the `user` parameter.
- Use one config file per service in `/etc/supervisor/conf.d/` and include them in the main config.
- Monitor log file sizes to avoid disk issues.
- Use `stopasgroup` and `killasgroup` for proper process tree cleanup.
- Secure the web interface with strong passwords or bind only to localhost.
- For production, manage Supervisor with `systemd` or your OS init system.

---

## FAQ

**Q1: Can Supervisor manage non-Python processes?**  
A: Yes. It can manage any process (Node.js, Java, shell scripts, etc.) as long as they run in the foreground.

**Q2: How do I reload configuration without stopping running programs?**  
A: Use `supervisorctl reread` then `supervisorctl update` to add/remove programs.

**Q3: Where are logs stored?**  
A: As specified by `stdout_logfile` and `stderr_logfile` in your config.

**Q4: How to auto-start Supervisor on system boot?**  
A: Use your OS’s init system (systemd, upstart, etc.) to enable Supervisor as a service.

---

## References

- [Supervisor Official Documentation](http://supervisord.org/)
- [Supervisor GitHub Repository](https://github.com/Supervisor/supervisor)
- [Supervisorctl Docs](http://supervisord.org/running.html#supervisorctl-command-line-interface)
- [Supervisor Configuration Guide](http://supervisord.org/configuration.html)

---