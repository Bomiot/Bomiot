# Terminal

## Overview

Bomiot manages the entire project lifecycle through the `bomiot` command-line tool. Run `bomiot <command> [options]` in the terminal to invoke the corresponding feature.

> For detailed usage of each command, refer to the corresponding document in the "CLI Commands" tab.

## Optional Arguments

```shell
  -v, --version       Get Bomiot version
  -h, --help          Show help message and exit
```

## Available Commands

```shell
    app               Create a sub-APP for the project
    api               Create a Bomiot API for the project
    project           Create a project workspace
    deploy            Generate GitHub Actions deployment workflow (Sponsor Only)
    init              Initialize bomiot workspace
    initadmin         Create default superuser admin
    initpwd           Reset admin password
    makemigrations    Generate database migrations
    migrate           Apply database migrations
    loaddata          Load data from configs
    dumpdata          Dump data to configs
    run               Start the server
```

## Quick Start

```shell
# 1. Initialize the project
bomiot init

# 2. Create the superuser
bomiot initadmin

# 3. Apply database migrations
bomiot migrate

# 4. Start the server (default 0.0.0.0:8000)
bomiot run
```

## Start the Server

```shell
bomiot run --host 0.0.0.0 --port 8000 --log-level info
```

### Common Start Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--host` / `-b` | `0.0.0.0` | Bind host address |
| `--port` / `-p` | `8000` | Bind port |
| `--log-level` | `info` | Log level: critical / error / warning / info / debug / trace |
| `--ssl-keyfile` | none | SSL key file path |
| `--ssl-certfile` | none | SSL certificate file path |
