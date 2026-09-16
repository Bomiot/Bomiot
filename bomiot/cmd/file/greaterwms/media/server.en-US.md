# Server Monitoring

## Introduction

- **Bomiot** collects server status metrics in a background thread and saves them to the database.
- Each metric sends a `bomiot_signals` signal, which is forwarded to `server.py` for custom handling.
- By receiving real-time signals through `server.py`, you can build your own server management logic.

---

## How It Works

1. `start_monitoring()` launches a background thread running `ServerManager.monitor_server()`.
2. The loop collects metrics in order: CPU → Memory → Disk → Network → PIDs, then sleeps 300 seconds.
3. Each metric is saved to the database and a `bomiot_signals` signal is sent.
4. The signal handler calls the corresponding method in `greaterwms/server.py` (`cpu_get`, `memory_get`, `disk_get`, `network_get`, `pid_get`).

> Note: A full collection cycle takes approximately 5 minutes (300s sleep + collection time).

---

## Get Server Information

After running `bomiot project <your_project>`, you will get the following file structure:

```shell
your-project/                 # Project directory
├── media/                    # Static files
│   ├── img/                  # Public images
│   └── ***.md                # Various documents
├── __version__.py            # your_project version
├── bomiotconf.ini            # Bomiot project identification file
└── server.py                 # Server monitoring signal handler
setup.ini                     # Project configuration file
...
```

---

## `server.py`

`server.py` defines five methods that receive real-time monitoring data. The default template is commented out — uncomment it to enable:

```python
class ServerClass:
    def pid_get(self, data):        # Running process information
        print(data)

    def network_get(self, data):    # Network information
        print(data)

    def disk_get(self, data):       # Hard disk information
        print(data)

    def cpu_get(self, data):        # CPU monitoring
        print(data)

    def memory_get(self, data):     # Memory information
        print(data)
```

---

## Monitoring Metrics and Data Structure

### CPU

| Field | Description |
| --- | --- |
| `cpu_usage` | CPU usage percentage |
| `physical_cores` | Number of physical CPU cores |
| `logical_cores` | Number of logical CPU cores |
| `cpu_frequency` | Current CPU frequency (MHz) |
| `min_cpu_frequency` | Minimum CPU frequency (MHz) |
| `max_cpu_frequency` | Maximum CPU frequency (MHz) |

```json
{
    "id": 1,
    "cpu_usage": 12.5,
    "physical_cores": 4,
    "logical_cores": 8,
    "cpu_frequency": "2400.00 MHz",
    "min_cpu_frequency": "0.00 MHz",
    "max_cpu_frequency": "2400.00 MHz"
}
```

### Memory

| Field | Description |
| --- | --- |
| `total` | Total physical memory (bytes) |
| `used` | Used memory (bytes) |
| `free` | Available memory (bytes) |
| `percent` | Memory usage percentage |
| `swap_total` | Total swap space (bytes) |
| `swap_used` | Used swap space (bytes) |
| `swap_free` | Available swap space (bytes) |
| `swap_percent` | Swap usage percentage |

```json
{
    "id": 1,
    "total": 16777216000,
    "used": 8589934592,
    "free": 8187281408,
    "percent": 51.2,
    "swap_total": 4294967296,
    "swap_used": 1073741824,
    "swap_free": 3221225472,
    "swap_percent": 25.0
}
```

### Disk

| Field | Description |
| --- | --- |
| `device` | Device name |
| `mountpoint` | Mount point |
| `total` | Total capacity (bytes) |
| `used` | Used space (bytes) |
| `free` | Available space (bytes) |
| `percent` | Usage percentage |

```json
{
    "device": "C:\\",
    "mountpoint": "C:\\",
    "total": 512110190592,
    "used": 256055095296,
    "free": 256055095296,
    "percent": 50.0
}
```

### Network

| Field | Description |
| --- | --- |
| `bytes_sent` | Total bytes sent |
| `bytes_recv` | Total bytes received |

```json
{
    "id": 1,
    "bytes_sent": 104857600,
    "bytes_recv": 52428800
}
```

### Process (PIDs)

| Field | Description |
| --- | --- |
| `pid` | Process ID |
| `name` | Process name |
| `memory` | Memory usage (bytes, RSS) |
| `create_time` | Process creation time |
| `memory_usage` | Memory usage percentage |
| `cpu_usage` | CPU usage percentage |

```json
{
    "pid": 1234,
    "name": "python.exe",
    "memory": 104857600,
    "create_time": "2026-09-06T10:00:00",
    "memory_usage": 2.5,
    "cpu_usage": 1.0
}
```

---

## Data Retention

- **CPU, Memory, Network**: Automatically cleaned when the record count reaches 10080 (approximately 7 days), oldest records deleted first.
- **Disk, PIDs**: Fully refreshed on every collection cycle (all previous records deleted, only the latest kept).

---

## Enable Server Monitoring

Make sure `server_monitor = True` under `[system_control]` in `setup.ini`. The monitor starts automatically in a background thread when the service launches.

```ini
[system_control]
server_monitor = True
```
