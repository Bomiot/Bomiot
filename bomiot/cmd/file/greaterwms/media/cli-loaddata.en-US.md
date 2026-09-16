# bomiot loaddata Command

## Overview

The `bomiot loaddata` command is designed to load data from a config file into a bomiot project. According to the argument definition, `source` is a required positional argument that represents the config file path.

> **Implementation status**: The subcommand parser is registered in `bomiot/cmd/cmd.py`, but the `cmd()` function has **no** corresponding `elif command == 'loaddata'` dispatch branch. This means the command is "declared but not implemented" in the current version — the arguments are parsed correctly, but execution does not perform any actual operation. It is a planned feature that has not been completed yet.

## Usage

```bash
bomiot loaddata <source>
```

- `<source>`: Required config file path (string type).

Registration in `cmd.py`:

```python
# loaddata
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')
```

Note that `source` has neither `nargs='?'` nor a `default` value, so it is a required argument — omitting it causes argparse to error out immediately.

## Source Code Analysis

Source file: `bomiot/cmd/cmd.py`.

### Parser Registration

The `loaddata` subcommand is registered via `subparsers.add_parser('loaddata', ...)` with help text `Load data from configs`, and declares a positional argument named `source`:

```python
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')
```

### Dispatch Logic

In the `cmd()` function, command dispatch is done via an `if/elif` chain. The following shows the branch structure of the `cmd()` function in `cmd.py`, which clearly shows that `loaddata` is missing a corresponding branch:

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

The `if/elif` chain handles `project`, `deploy`, `init`, `initadmin`, `initpwd`, `app`, `api`, `makemigrations`, `migrate` and `run`, but there is no `loaddata` branch. Therefore, when `bomiot loaddata <source>` is executed, argparse parses the arguments successfully, but `command == 'loaddata'` matches no branch, so the function returns without performing any data-loading operation.

### Expected Behaviour (Based on the Argument Definition)

Although not currently implemented, the design intent can be inferred from the argument help text `Configs path`:

- Accept a config file path as `source`.
- Read data from that config and load it into the project database or runtime configuration.
- Act as the inverse of the `bomiot dumpdata` command (dump exports, load imports).

## Practical Examples

### Invoking the command (no actual effect in the current version)

```bash
bomiot loaddata configs/backup.json
```

The command is parsed correctly by argparse (`source` is assigned `configs/backup.json`), but since the `cmd()` function has no corresponding dispatch branch, no data-loading operation is performed.

### Behaviour when source is omitted

```bash
bomiot loaddata
```

Because `source` is a required positional argument with no default, argparse errors out and exits:

```text
error: the following arguments are required: source
```

## Related Commands

- [bomiot dumpdata](./cli-dumpdata.en-US.md): Dump data to a config file (also in a declared-but-unimplemented state)
- [bomiot migrate](./cli-init.en-US.md): Apply database migrations
- [bomiot makemigrations](./cli-makemigrations.en-US.md): Generate database migration files
