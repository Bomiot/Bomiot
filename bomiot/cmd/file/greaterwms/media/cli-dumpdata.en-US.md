# bomiot dumpdata Command

## Overview

The `bomiot dumpdata` command is designed to dump data from a bomiot project into a config file. According to the argument definition, `appname` is an optional positional argument that defaults to `core` and specifies the app whose data should be exported.

> **Implementation status**: The subcommand parser is registered in `bomiot/cmd/cmd.py`, but the `cmd()` function has **no** corresponding `elif command == 'dumpdata'` dispatch branch. This means the command is "declared but not implemented" in the current version — the arguments are parsed correctly (including using the default `core`), but execution does not perform any actual operation. It is a planned feature that has not been completed yet.

## Usage

```bash
bomiot dumpdata [appname]
```

- `[appname]`: Optional app name, string type, defaults to `core`. When omitted, `core` is used automatically.

Registration in `cmd.py`:

```python
# dumpdata
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')
```

Note that `appname` has `nargs='?'` and `default='core'`, so it is optional — when omitted it falls back to `core` without error.

## Source Code Analysis

Source file: `bomiot/cmd/cmd.py`.

### Parser Registration

The `dumpdata` subcommand is registered via `subparsers.add_parser('dumpdata', ...)` with help text `Dump data to configs`, and declares an optional positional argument named `appname`:

```python
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')
```

Key argument attributes:

- `default='core'`: When `appname` is not provided, it defaults to dumping the `core` app's data.
- `nargs='?'`: Allows the positional argument to be omitted, making it optional.
- `type=str`: The value type is string.

### Dispatch Logic

In the `cmd()` function, command dispatch is done via an `if/elif` chain. The following shows the branch structure of the `cmd()` function in `cmd.py`, which clearly shows that `dumpdata` is missing a corresponding branch:

```python
def cmd():
    """
    run from cmd
    :return:
    """
    args = parser.parse_args()
    command = args.command
    if command == 'project':
        ...
    elif command == 'deploy':
        ...
    elif command == 'init':
        ...
    elif command == 'initadmin':
        ...
    elif command == 'initpwd':
        ...
    elif command == 'app':
        ...
    elif command == 'api':
        ...
    # marketplace
    # elif command == 'market':
    #     ...
    # # init auth keys
    # elif command == 'keys':
    #     ...
    # makemigrations
    elif command == 'makemigrations':
        ...
    # migrate
    elif command == 'migrate':
        from bomiot.cmd.migrate import migrate
        migrate()
    # run server
    elif command == 'run':
        ...
```

The `if/elif` chain handles `project`, `deploy`, `init`, `initadmin`, `initpwd`, `app`, `api`, `makemigrations`, `migrate` and `run`, but there is no `dumpdata` branch. Therefore, when `bomiot dumpdata` or `bomiot dumpdata someapp` is executed, argparse parses the arguments successfully, but `command == 'dumpdata'` matches no branch, so the function returns without performing any data-export operation.

### Expected Behaviour (Based on the Argument Definition)

Although not currently implemented, the design intent can be inferred from the argument help text `Appname` and the default value `core`:

- Accept an app name `appname`, defaulting to `core`.
- Export that app's data to a config file (dump).
- Act as the inverse of the `bomiot loaddata` command (dump exports, load imports).

## Practical Examples

### Invoking the command (no actual effect in the current version)

```bash
bomiot dumpdata
```

Without `appname`, argparse uses the default value `core`. Since the `cmd()` function has no corresponding dispatch branch, no data-export operation is performed.

### Invoking with an explicit app name

```bash
bomiot dumpdata goods
```

`appname` is assigned `goods`, but again no actual operation is performed.

## Related Commands

- [bomiot loaddata](./cli-loaddata.en-US.md): Load data from a config file (also in a declared-but-unimplemented state)
- [bomiot migrate](./cli-init.en-US.md): Apply database migrations
- [bomiot makemigrations](./cli-makemigrations.en-US.md): Generate database migration files
