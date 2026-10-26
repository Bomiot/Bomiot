# 服务器监控

## 介绍

Bomiot 内置服务器监控器，在后台守护线程中周期性采集服务器指标（CPU、内存、磁盘、网络、进程），采集结果写入数据库，同时通过 `bomiot_signals` 信号实时推送到项目根目录的 `server.py`，供你接管自定义逻辑。

无需编写任何采集代码，取消 `server.py` 中的注释即可接收数据。

---

## 工作流程

1. **启动**：服务启动时读取 `setup.ini`，`[system_control] server_monitor = True` 时启动监控守护线程；多 workers 部署下框架通过文件锁保证监控线程只启动一次
2. **就绪等待**：线程启动后先等待数据库迁移完成（最多 30 秒检测监控表是否就绪），避免启动早期写库报错
3. **周期采集**：进入无限循环，按固定顺序采集五类指标，每类之间间隔 1 秒：

   ```
   CPU → (1s) → 内存 → (1s) → 磁盘 → (1s) → 网络 → (1s) → 进程 → 休眠 300 秒 → 下一轮
   ```

   一个完整周期约 5 分钟（4 秒间隔 + 300 秒休眠 + 采集耗时；其中 CPU 使用率采样本身阻塞 1 秒）
4. **写入数据库**：每个指标按各自的保留策略写入对应模型（见下方"数据保留策略"）
5. **信号分发**：每条采集结果发送 `bomiot_signals` 信号，`models` 为 `CPU` / `Memory` / `Disk` / `Network` / `Pids`，`type` 为 `created`
6. **项目接管**：框架按 `models` 路由，用 AST 解析项目根目录 `server.py`，动态加载并调用对应方法：

   | models | server.py 方法 |
   |---|---|
   | `CPU` | `cpu_get(data)` |
   | `Memory` | `memory_get(data)` |
   | `Disk` | `disk_get(data)` |
   | `Network` | `network_get(data)` |
   | `Pids` | `pid_get(data)` |

> **热更新**：`server.py` 在每次信号触发时重新加载，修改后**无需重启服务**即可生效。

---

## 文件位置

监控信号统一由主工程目录下的 `server.py` 接管：

```shell
workspace/                    # 工作区
├── setup.ini                 # 项目配置文件
└── greaterwms/               # 主工程目录
    ├── media/                # 文件与文档目录
    └── server.py             # 服务器监控信号处理
```

---

## 接管监控信号

`server.py` 默认模板为注释状态，取消注释即可启用：

```python
class ServerClass:
    def pid_get(self, data):        # 运行中的进程信息
        print(data)

    def network_get(self, data):    # 网络信息
        print(data)

    def disk_get(self, data):       # 磁盘信息
        print(data)

    def cpu_get(self, data):        # CPU 信息
        print(data)

    def memory_get(self, data):     # 内存信息
        print(data)
```

> 注意：进程采集是逐个进程发送信号的——`pid_get` 每个周期会被调用 N 次（N 为系统进程数）。在 `pid_get` 中执行重逻辑时注意性能开销。

拿到数据后可以执行任何自定义逻辑：阈值告警、Webhook 推送、写入时序数据库、联动扩缩容等。

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

每个挂载分区产生一条数据；无权限访问的分区自动跳过。

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

累计值（自系统启动起），如需速率请自行计算相邻两次的差值。

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

每个存活进程产生一条数据；PID 为 0 的系统进程与无权限访问的进程自动跳过。

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

| 指标 | 策略 |
|---|---|
| CPU / 内存 / 网络 | 记录数达到 10080 条后，每新增一条删除最早一条（按 5 分钟周期约保留 35 天） |
| 磁盘 / 进程 | 每轮采集前清空旧记录，只保留最新一轮 |

---

## 启用系统监控

确保 `setup.ini` 中开启监控开关，服务启动后自动生效：

```ini
[system_control]
server_monitor = True
```
