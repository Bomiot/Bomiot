# 服务器监控

## 介绍

- **Bomiot** 在后台线程中采集服务器状态指标，并保存到数据库。
- 每个指标都会发送 `bomiot_signals` 信号，信号会转发到 `server.py` 供自定义处理。
- 通过 `server.py` 接收实时信号，可以构建自己的服务器管理逻辑。

---

## 工作原理

1. `start_monitoring()` 启动一个后台线程，运行 `ServerManager.monitor_server()`。
2. 循环按顺序采集指标：CPU → 内存 → 磁盘 → 网络 → 进程，然后休眠 300 秒。
3. 每个指标保存到数据库，并发送 `bomiot_signals` 信号。
4. 信号处理器调用 `greaterwms/server.py` 中对应的方法（`cpu_get`、`memory_get`、`disk_get`、`network_get`、`pid_get`）。

> 注意：一次完整采集周期约为 5 分钟（300 秒休眠 + 采集耗时）。

---

## 获取服务器信息

使用命令 `bomiot project <your_project>` 后，你会得到以下文件结构：

```shell
your-project/                 # 项目目录
├── media/                    # 静态文件
│   ├── img/                  # 公用图片
│   └── ***.md                # 各种文档
├── __version__.py            # 项目版本
├── bomiotconf.ini            # Bomiot 项目标识文件
└── server.py                 # 服务器监控信号处理
setup.ini                     # 项目配置文件
...
```

---

## `server.py`

`server.py` 定义了五个方法，用于接收实时监控数据。默认模板是注释状态，取消注释即可启用：

```python
class ServerClass:
    def pid_get(self, data):        # 运行中的进程信息
        print(data)

    def network_get(self, data):    # 网络信息
        print(data)

    def disk_get(self, data):       # 硬盘信息
        print(data)

    def cpu_get(self, data):        # CPU 监控
        print(data)

    def memory_get(self, data):     # 内存信息
        print(data)
```

---

## 监控指标与数据结构

### 处理器（CPU）

| 字段 | 说明 |
| --- | --- |
| `cpu_usage` | CPU 使用率百分比 |
| `physical_cores` | 物理 CPU 核数 |
| `logical_cores` | 逻辑 CPU 核数 |
| `cpu_frequency` | 当前 CPU 频率（MHz） |
| `min_cpu_frequency` | 最小 CPU 频率（MHz） |
| `max_cpu_frequency` | 最大 CPU 频率（MHz） |

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

### 内存（Memory）

| 字段 | 说明 |
| --- | --- |
| `total` | 总物理内存（字节） |
| `used` | 已用内存（字节） |
| `free` | 可用内存（字节） |
| `percent` | 内存使用率百分比 |
| `swap_total` | Swap 总量（字节） |
| `swap_used` | 已用 Swap（字节） |
| `swap_free` | 可用 Swap（字节） |
| `swap_percent` | Swap 使用率百分比 |

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

### 磁盘（Disk）

| 字段 | 说明 |
| --- | --- |
| `device` | 设备名 |
| `mountpoint` | 挂载点 |
| `total` | 总容量（字节） |
| `used` | 已用空间（字节） |
| `free` | 可用空间（字节） |
| `percent` | 使用率百分比 |

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

### 网络（Network）

| 字段 | 说明 |
| --- | --- |
| `bytes_sent` | 总发送字节数 |
| `bytes_recv` | 总接收字节数 |

```json
{
    "id": 1,
    "bytes_sent": 104857600,
    "bytes_recv": 52428800
}
```

### 进程（PIDs）

| 字段 | 说明 |
| --- | --- |
| `pid` | 进程 ID |
| `name` | 进程名称 |
| `memory` | 内存占用（字节，RSS） |
| `create_time` | 进程创建时间 |
| `memory_usage` | 内存占用率百分比 |
| `cpu_usage` | CPU 占用率百分比 |

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

## 数据保留策略

- **CPU、内存、网络**：记录数达到 10080 条（约 7 天）时自动清理，删除最早的记录。
- **磁盘、进程**：每次采集全量刷新（删除所有旧记录，仅保留最新数据）。

---

## 启用系统监控

确保 `setup.ini` 中 `[system_control]` 的 `server_monitor = True`，服务启动后自动在后台线程运行监控。

```ini
[system_control]
server_monitor = True
```
