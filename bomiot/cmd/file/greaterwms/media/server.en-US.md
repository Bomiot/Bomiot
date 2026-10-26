# Server Monitoring

## Introduction

Bomiot ships with a built-in server monitor that periodically collects server metrics (CPU, memory, disk, network, processes) in a background daemon thread. Every sample is written to the database and pushed in real time via a `bomiot_signals` signal to `server.py` in the project root, where you can take over with custom logic.

No collection code is required — uncomment `server.py` and you start receiving data.

---

## How It Works

1. **Startup**: when the server starts, it reads `setup.ini`; with `[system_control] server_monitor = True`, the monitoring daemon thread is launched. Under multi-worker deployments, a file lock guarantees the thread starts exactly once
2. **Readiness wait**: the thread first waits for database migrations to finish (checking for the monitoring table for up to 30 seconds), avoiding write errors during early startup
3. **Collection cycle**: an infinite loop collects the five metric groups in a fixed order, with a 1-second gap between each:

   ```
   CPU → (1s) → Memory → (1s) → Disk → (1s) → Network → (1s) → Processes → sleep 300s → next round
   ```

   A full cycle takes about 5 minutes (4 seconds of gaps + 300 seconds of sleep + collection time; the CPU usage sample itself blocks for 1 second)
4. **Database writes**: each metric is written to its model according to its retention policy (see "Data Retention" below)
5. **Signal dispatch**: every sample emits a `bomiot_signals` signal with `models` set to `CPU` / `Memory` / `Disk` / `Network` / `Pids` and `type` set to `created`
6. **Project takeover**: the framework routes by `models`, parses `server.py` in the project root via AST, dynamically loads it, and calls the matching method:

   | models | server.py method |
   |---|---|
   | `CPU` | `cpu_get(data)` |
   | `Memory` | `memory_get(data)` |
   | `Disk` | `disk_get(data)` |
   | `Network` | `network_get(data)` |
   | `Pids` | `pid_get(data)` |

> **Hot reload**: `server.py` is reloaded on every signal, so changes take effect **without restarting the server**.

---

## File Location

Monitoring signals are handled by `server.py` under the main project directory:

```shell
workspace/                    # workspace
├── setup.ini                 # project configuration
└── greaterwms/               # main project directory
    ├── media/                # files and documents
    └── server.py             # server monitoring signal handling
```

---

## Taking Over Monitoring Signals

The default `server.py` template is commented out. Uncomment to enable:

```python
class ServerClass:
    def pid_get(self, data):        # running process info
        print(data)

    def network_get(self, data):    # network info
        print(data)

    def disk_get(self, data):       # disk info
        print(data)

    def cpu_get(self, data):        # CPU info
        print(data)

    def memory_get(self, data):     # memory info
        print(data)
```

> Note: process collection sends one signal **per process** — `pid_get` is called N times per cycle (N = number of system processes). Keep heavy logic in `pid_get` mindful of this cost.

From here you can run any custom logic: threshold alerts, Webhook pushes, writes to a time-series database, autoscaling hooks, and so on.

---

## Metrics and Data Structures

### CPU

| Field | Description |
| --- | --- |
| `cpu_usage` | CPU usage percentage |
| `physical_cores` | Physical core count |
| `logical_cores` | Logical core count |
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
| `free` | Free memory (bytes) |
| `percent` | Memory usage percentage |
| `swap_total` | Total swap (bytes) |
| `swap_used` | Used swap (bytes) |
| `swap_free` | Free swap (bytes) |
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

One record per mounted partition; partitions without access permission are skipped.

| Field | Description |
| --- | --- |
| `device` | Device name |
| `mountpoint` | Mount point |
| `total` | Total capacity (bytes) |
| `used` | Used space (bytes) |
| `free` | Free space (bytes) |
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

Cumulative values (since system boot); compute deltas between two samples if you need rates.

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

### Processes

One record per live process; PID 0 system processes and processes without access permission are skipped.

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

| Metric | Policy |
|---|---|
| CPU / Memory / Network | Once 10080 rows are reached, the oldest row is deleted for every new one (about 35 days at a 5-minute cycle) |
| Disk / Processes | All old rows are cleared before each cycle; only the latest round is kept |

---

## Enabling the Monitor

Make sure the switch is on in `setup.ini`; it takes effect automatically at server startup:

```ini
[system_control]
server_monitor = True
```
