# bomiot run 命令

## 概述

`bomiot run` 命令用于启动 bomiot 项目的 uvicorn ASGI 服务。它会先扫描已注册的应用、在 Windows 上释放被占用的端口、清理 `bomiot_ready.lock` 锁文件，设置 Django 环境变量，然后调用 `uvicorn.run()` 启动服务。

该命令在 `bomiot/cmd/cmd.py` 中注册为 `run` 子命令，派发逻辑位于 `cmd()` 函数的 `run` 分支。

## 用法

```bash
bomiot run [options]
```

常用示例：

```bash
bomiot run -b 0.0.0.0 -p 8000 -w 4
```

在 `cmd.py` 中的注册方式：

```python
# run
parser_run = subparsers.add_parser(
    'run', help='Run server')
parser_run.add_argument("--host", "-b", type=str, default="0.0.0.0", help="Default Domin: 0.0.0.0")
parser_run.add_argument("--port", "-p", type=int, default=8000, help="Default Pore: 8000")
parser_run.add_argument("--workers", "-w", type=int, default=1, help="CPU Core")
parser_run.add_argument("--log-level", type=str, default="info", choices=["critical", "error", "warning", "info", "debug", "trace"], help="Log Level")
parser_run.add_argument("--uds", type=str, default=None, help="UNIX domain socket")
parser_run.add_argument("--ssl-keyfile", type=str, default=None, help="SSL Key")
parser_run.add_argument("--ssl-certfile", type=str, default=None, help="SSL PEM")
parser_run.add_argument("--proxy-headers", action="store_true", help="X-Forwarded-*Header")
parser_run.add_argument("--http", type=str, default="httptools", choices=["auto", "h11", "httptools"], help="HTTP")
parser_run.add_argument("--loop", "-l", type=str, default="auto", choices=["auto", "asyncio", "uvloop"], help="Asyncio Loop")
parser_run.add_argument("--limit-concurrency", type=str, default=1000, help="Limit concurrency")
parser_run.add_argument("--backlog", type=int, default=128, help="Backlog")
parser_run.add_argument("--timeout-keep-alive", type=str, default=5, help="Backlog")
parser_run.add_argument("--timeout-graceful-shutdown", type=str, default=30, help="Time out shut down")
parser_run.add_argument("--server-header", type=bool, default=False, help="Server Header")
parser_run.add_argument("--app", type=str, default="bomiot_asgi:application", help="ASGI Application")
```

### 参数列表（含默认值）

| 参数 | 简写 | 类型 | 默认值 | 可选值 / 说明 |
| --- | --- | --- | --- | --- |
| `--host` | `-b` | str | `0.0.0.0` | 监听地址 |
| `--port` | `-p` | int | `8000` | 监听端口 |
| `--workers` | `-w` | int | `1` | worker 进程数 |
| `--log-level` | - | str | `info` | `critical` / `error` / `warning` / `info` / `debug` / `trace` |
| `--uds` | - | str | `None` | UNIX domain socket |
| `--ssl-keyfile` | - | str | `None` | SSL 密钥文件 |
| `--ssl-certfile` | - | str | `None` | SSL 证书文件 |
| `--proxy-headers` | - | flag | `False` | 启用 X-Forwarded-* 头 |
| `--http` | - | str | `httptools` | `auto` / `h11` / `httptools` |
| `--loop` | `-l` | str | `auto` | `auto` / `asyncio` / `uvloop` |
| `--limit-concurrency` | - | str | `1000` | 并发上限 |
| `--backlog` | - | int | `128` | backlog 队列长度 |
| `--timeout-keep-alive` | - | str | `5` | keep-alive 超时（秒） |
| `--timeout-graceful-shutdown` | - | str | `30` | 优雅关停超时（秒） |
| `--server-header` | - | bool | `False` | 是否发送 server header |
| `--app` | - | str | `bomiot_asgi:application` | ASGI 应用入口 |

## 源码分析

源文件：`bomiot/cmd/cmd.py`，`cmd()` 函数中的 `run` 分支。

### 扫描已注册应用

进入 `run` 分支后，首先调用 `bomiot.cmd.file.discovered_apps.main()` 扫描当前工作空间下的应用并生成 `apps.json`。为了避免 `main()` 内部读取 `sys.argv` 受到当前命令行参数干扰，先临时替换 `sys.argv` 再恢复：

```python
elif command == 'run':
    import platform
    import importlib.resources
    from os.path import join
    from pathlib import Path
    from configparser import ConfigParser
    WORKING_SPACE = os.path.join(os.getcwd())
    # Run discovered_apps.py main() to scan and emit apps.json
    from bomiot.cmd.file.discovered_apps import main as _discover_apps_main
    _orig_argv = sys.argv
    sys.argv = [sys.argv[0]]
    _discover_apps_main(WORKING_SPACE)
    sys.argv = _orig_argv
```

### Windows 下释放端口

当操作系统为 Windows 时，调用 `kill_process_on_port(args.port)` 释放被占用的端口，避免端口冲突。`kill_process_on_port` 定义在 `bomiot/cmd/killport.py` 中，通过 `netstat` 查找占用端口的 PID 并用 `taskkill` 强制结束：

```python
    if platform.system() == 'Windows':
        from bomiot.cmd.killport import kill_process_on_port
        kill_process_on_port(args.port)
```

`killport.py` 的实现：

```python
def kill_process_on_port(port: int):
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def kill_process(port):
        try:
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if f':{port}' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            if pid != 0:
                                subprocess.run(f'taskkill /PID {pid} /F', shell=True)
        except Exception as e:
            print(f"Error: {e}")

    if is_port_in_use(port):
        kill_process(port)
```

### 清理锁文件

清理 `bomiot_ready.lock` 锁文件（若存在），用于标记服务就绪状态：

```python
    lockfile = Path(join(WORKING_SPACE, 'bomiot_ready.lock'))
    if lockfile.exists():
        lockfile.unlink()
```

### 设置 Django 环境变量

设置 `DJANGO_SETTINGS_MODULE`、`RUN_MAIN` 和 `WORKERS` 三个环境变量：

```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    os.environ.setdefault('WORKERS', str(args.workers))
```

### 启动 uvicorn

最后调用 `uvicorn.run()` 启动 ASGI 服务，传入全部参数：

```python
    uvicorn.run(
        args.app,
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_level=args.log_level,
        uds=args.uds,
        ssl_keyfile=args.ssl_keyfile,
        ssl_certfile=args.ssl_certfile,
        proxy_headers=args.proxy_headers,
        http=args.http,
        server_header=False,
        limit_concurrency=args.limit_concurrency,
        backlog=args.backlog,
        timeout_keep_alive=args.timeout_keep_alive,
        timeout_graceful_shutdown=args.timeout_graceful_shutdown,
        loop=args.loop
    )
```

注意：`server_header` 在 `uvicorn.run()` 调用中硬编码为 `False`，不使用 `args.server_header` 的值。

## 实战示例

### 使用默认参数启动

```bash
bomiot run
```

使用全部默认值：监听 `0.0.0.0:8000`、1 个 worker、`info` 日志级别、`httptools` HTTP 实现、`auto` 事件循环。

### 监听所有网卡并启用多 worker

```bash
bomiot run -b 0.0.0.0 -p 8000 -w 4
```

监听 `0.0.0.0:8000`，启动 4 个 worker 进程。

### 启用调试日志

```bash
bomiot run --log-level debug
```

输出 debug 级别日志，便于排查问题。

### 使用 SSL 启动 HTTPS 服务

```bash
bomiot run --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem
```

### 启用代理头（反向代理场景）

```bash
bomiot run --proxy-headers
```

让 uvicorn 识别 `X-Forwarded-For`、`X-Forwarded-Proto` 等反向代理传递的头。

### 自定义 ASGI 应用入口

```bash
bomiot run --app my_asgi:application
```

将 ASGI 应用入口从默认的 `bomiot_asgi:application` 改为 `my_asgi:application`。

## 相关命令

- [bomiot makemigrations](./cli-makemigrations.zh-CN.md)：启动前生成数据库迁移
- [bomiot migrate](./cli-init.zh-CN.md)：启动前应用数据库迁移
- [bomiot init](./cli-init.zh-CN.md)：初始化项目基础文件
