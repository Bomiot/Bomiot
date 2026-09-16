# bomiot makemigrations Command

## Overview

The `bomiot makemigrations` command generates database migration files for the Django apps in a bomiot project. It sets up the Django environment variables, calls `django.setup()` to initialise Django, and then generates migration scripts via Django's `call_command('makemigrations', ...)`.

The command accepts an optional `appname` argument to generate migrations for a specific app, plus `--empty` and `--dry-run` flags. When no `appname` is given, it auto-discovers all apps that contain models and generates migrations for them.

The command is registered as the `makemigrations` subcommand in `bomiot/cmd/cmd.py`, and the dispatch logic lives in the `makemigrations` branch of the `cmd()` function.

## Usage

```bash
bomiot makemigrations [appname] [--empty] [--dry-run]
```

- `[appname]`: Optional app name. It can be an app label (e.g. `core`) or a full dotted path (e.g. `bomiot.server.core`).
- `--empty`: Create an empty migration file.
- `--dry-run`: Show what would be done without actually writing migration files.

Registration in `cmd.py`:

```python
# makemigrations
parser_makemigrations = subparsers.add_parser(
    'makemigrations', help='Generate migrations for database')
parser_makemigrations.add_argument('appname', nargs='?', type=str, help='App name (e.g., xx or dev.xx)')
parser_makemigrations.add_argument('--empty', action='store_true', help='Create an empty migration')
parser_makemigrations.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
```

## Source Code Analysis

Source file: `bomiot/cmd/cmd.py`, the `makemigrations` branch inside the `cmd()` function.

### Setting Up the Django Environment

On entering the branch, it first sets the `DJANGO_SETTINGS_MODULE` and `RUN_MAIN` environment variables and calls `django.setup()` to initialise the Django app registry:

```python
elif command == 'makemigrations':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    import django
    django.setup()
    from django.core.management import call_command
    from django.apps import apps
```

### Reading the Arguments

It reads `appname`, `empty` and `dry_run` from the parsed arguments and initialises the argument list for `call_command`:

```python
    appname = args.appname
    empty = args.empty
    dry_run = args.dry_run
    cmd_args = ['makemigrations']
```

### App Discovery When appname Is Given

When `appname` is provided, two matching strategies are used depending on whether it contains a `.`:

**Contains a `.` (full dotted path)**: It iterates over all app configs and matches by `app_config.name` exactly; on a hit it appends the app's `label` to the arguments, otherwise it returns immediately:

```python
    if appname:
        if '.' in appname:
            found_app_label = None
            for app_config in apps.get_app_configs():
                if app_config.name == appname:
                    found_app_label = app_config.label
                    break
            if found_app_label:
                cmd_args.append(found_app_label)
            else:
                return
```

**No `.` (app label)**: It iterates over all app configs and matches by `app_config.label` exactly or by `app_config.name` ending with `.` + appname; on a hit it appends the label, otherwise it returns:

```python
        else:
            found_app = None
            for app_config in apps.get_app_configs():
                if app_config.label == appname or app_config.name.endswith('.' + appname):
                    found_app = app_config.label
                    break
            if found_app:
                cmd_args.append(found_app)
            else:
                return
```

### Auto-Discovery When appname Is Omitted

When no `appname` is given, it iterates over all app configs, checks whether each has a `models_module` and whether models can be retrieved, collects the labels of all apps that have models, and appends them to the arguments. If no app has models, it returns immediately:

```python
    else:
        apps_with_models = []
        for app_config in apps.get_app_configs():
            try:
                if app_config.models_module:
                    models = apps.get_app_config(app_config.label).get_models()
                    if models:
                        apps_with_models.append(app_config.label)
            except Exception:
                continue
        if apps_with_models:
            cmd_args.extend(apps_with_models)
        else:
            return
```

### Appending Flags and Executing

Depending on the `empty` and `dry_run` flags it appends `--empty` / `--dry-run` to the arguments, then calls `call_command` to run migration generation, catching exceptions and printing the error:

```python
    if empty:
        cmd_args.append('--empty')
    if dry_run:
        cmd_args.append('--dry-run')
    try:
        call_command(*cmd_args)
    except Exception as e:
        print(f"Error creating migrations: {e}")
```

## Practical Examples

### Auto-generate migrations for all apps

```bash
bomiot makemigrations
```

Without `appname`, the command auto-discovers all apps that contain models and generates migrations for them.

### Generate migrations for a specific app label

```bash
bomiot makemigrations core
```

Matches by app label, equivalent to matching `app_config.label == 'core'` or `app_config.name` ending with `.core`.

### Generate migrations for a full dotted path

```bash
bomiot makemigrations bomiot.server.core
```

Matches `app_config.name` exactly against `bomiot.server.core`, and uses the matched app's label to call `makemigrations`.

### Create an empty migration

```bash
bomiot makemigrations core --empty
```

Creates an empty migration file for the `core` app, typically used for hand-written data migrations.

### Preview migration changes without writing files

```bash
bomiot makemigrations --dry-run
```

Only prints the migration content that would be generated, without writing any migration files.

## Related Commands

- [bomiot migrate](./cli-init.en-US.md): Run `bomiot migrate` to apply migrations to the database
- [bomiot run](./cli-run.en-US.md): Generate migrations, apply them and start the uvicorn server
