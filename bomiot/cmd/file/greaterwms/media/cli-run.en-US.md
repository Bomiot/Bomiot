# bomiot run Command

## Overview

The `bomiot run` command starts the uvicorn ASGI server for a bomiot project. It scans registered apps, frees the occupied port on Windows, removes the `bomiot_ready.lock` lock file, sets the Django environment variables, and then calls `uvicorn.run()` to start the server.

The command is registered as the `run` subcommand in `bomiot/cmd/cmd.py`, and the dispatch logic lives in the `run` branch of the `cmd()` function.

## Usage

```bash
bomiot run [options]
```

Common example:

```bash
bomiot run -b 0.0.0.0 -p 8000 -w 4
```

Registration in `cmd.py`:

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

### Argument List (with Defaults)

| Argument | Short | Type | Default | Choices / Notes |
| --- | --- | --- | --- | --- |
| `--host` | `-b` | str | `0.0.0.0` | Listen address |
| `--port` | `-p` | int | `8000` | Listen port |
| `--workers` | `-w` | int | `1` | Number of worker processes |
| `--log-level` | - | str | `info` | `critical` / `error` / `warning` / `info` / `debug` / `trace` |
| `--uds` | - | str | `None` | UNIX domain socket |
| `--ssl-keyfile` | - | str | `None` | SSL key file |
| `--ssl-certfile` | - | str | `None` | SSL certificate file |
| `--proxy-headers` | - | flag | `False` | Enable X-Forwarded-* headers |
| `--http` | - | str | `httptools` | `auto` / `h11` / `httptools` |
| `--loop` | `-l` | str | `auto` | `auto` / `asyncio` / `uvloop` |
| `--limit-concurrency` | - | str | `1000` | Concurrency limit |
| `--backlog` | - | int | `128` | Backlog queue length |
| `--timeout-keep-alive` | - | str | `5` | keep-alive timeout (seconds) |
| `--timeout-graceful-shutdown` | - | str | `30` | Graceful shutdown timeout (seconds) |
| `--server-header` | - | bool | `False` | Whether to send a server header |
| `--app` | - | str | `bomiot_asgi:application` | ASGI application entry |

## Source Code Analysis

Source file: `bomiot/cmd/cmd.py`, the `run` branch inside the `cmd()` function.

### Scanning Registered Apps

On entering the `run` branch, it first calls `bomiot.cmd.file.discovered_apps.main()` to scan the current working space for apps and emit `apps.json`. To prevent `main()` from reading the current command-line arguments via `sys.argv`, `sys.argv` is temporarily replaced and then restored:

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

### Freeing the Port on Windows

When the operating system is Windows, it calls `kill_process_on_port(args.port)` to free the occupied port and avoid conflicts. `kill_process_on_port` is defined in `bomiot/cmd/killport.py` and uses `netstat` to find the PID holding the port and `taskkill` to force-terminate it:

```python
    if platform.system() == 'Windows':
        from bomiot.cmd.killport import kill_process_on_port
        kill_process_on_port(args.port)
```

The `killport.py` implementation:

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

### Cleaning Up the Lock File

It removes the `bomiot_ready.lock` lock file if it exists, which marks the server's ready state:

```python
    lockfile = Path(join(WORKING_SPACE, 'bomiot_ready.lock'))
    if lockfile.exists():
        lockfile.unlink()
```

### Setting Django Environment Variables

It sets the `DJANGO_SETTINGS_MODULE`, `RUN_MAIN` and `WORKERS` environment variables:

```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    os.environ.setdefault('WORKERS', str(args.workers))
```

### Starting uvicorn

Finally it calls `uvicorn.run()` to start the ASGI server with all the parameters:

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

Note: `server_header` is hardcoded to `False` in the `uvicorn.run()` call and does not use the value of `args.server_header`.

## Practical Examples

### Start with default arguments

```bash
bomiot run
```

Uses all defaults: listen on `0.0.0.0:8000`, 1 worker, `info` log level, `httptools` HTTP implementation, `auto` event loop.

### Listen on all interfaces with multiple workers

```bash
bomiot run -b 0.0.0.0 -p 8000 -w 4
```

Listens on `0.0.0.0:8000` with 4 worker processes.

### Enable debug logging

```bash
bomiot run --log-level debug
```

Outputs debug-level logs for troubleshooting.

### Start an HTTPS server with SSL

```bash
bomiot run --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem
```

### Enable proxy headers (reverse-proxy scenario)

```bash
bomiot run --proxy-headers
```

Lets uvicorn honour `X-Forwarded-For`, `X-Forwarded-Proto` and other headers passed by a reverse proxy.

### Custom ASGI application entry

```bash
bomiot run --app my_asgi:application
```

Changes the ASGI application entry from the default `bomiot_asgi:application` to `my_asgi:application`.

## Related Commands

- [bomiot makemigrations](./cli-makemigrations.en-US.md): Generate database migrations before starting
- [bomiot migrate](./cli-init.en-US.md): Apply database migrations before starting
- [bomiot init](./cli-init.en-US.md): Initialise project base files
