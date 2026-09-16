# bomiot migrate Command

## Overview

The `bomiot migrate` command runs database migrations, applying all pending Django migrations to the database. It sets the `DJANGO_SETTINGS_MODULE` and `RUN_MAIN` environment variables, calls `django.setup()` to register apps, then invokes Django's built-in `call_command('migrate')` to apply all pending migrations.

The command is implemented by the `migrate()` function in `bomiot/cmd/migrate.py` and registered as the `migrate` subcommand in `bomiot/cmd/cmd.py`.

## Usage

```bash
bomiot migrate
```

- This command takes **no arguments**. It applies all unapplied migrations across every app in the project.

Registration in `cmd.py`:

```python
# migrate
parser_migrate = subparsers.add_parser('migrate', help='Migrate database')
```

Dispatch logic:

```python
# migrate
elif command == 'migrate':
    from bomiot.cmd.migrate import migrate
    migrate()
```

## Source Code Analysis

Source file: `bomiot/cmd/migrate.py`

The full source is:

```python
import os
import django
from django.core.management import call_command


def migrate():
    """
    Execute database migrations
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    django.setup()
    
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}") 
```

### Setting Environment Variables

The command sets two environment variables:

- `DJANGO_SETTINGS_MODULE`: points at the bomiot server settings module `bomiot.server.server.settings`.
- `RUN_MAIN`: set to `'true'`. In Django's autoreload mechanism, `RUN_MAIN` marks the "main process" to avoid repeatedly triggering the reloader. Setting it manually here lets the migration run directly in a single process.

```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
```

> `setdefault` only writes when the variable is unset; it does not override an existing value.

### Initializing Django

It calls `django.setup()` to load settings and register apps, making the ORM and migration system available:

```python
    django.setup()
```

### Running the Migration

It invokes Django's built-in `call_command('migrate')`, equivalent to running `python manage.py migrate`, which applies all unapplied migrations:

```python
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}") 
```

If an exception is raised during migration, it is caught by the `try/except` and `Error during migration: <exception message>` is printed, preventing the process from crashing.

## Practical Examples

### Initializing the database for the first time

After creating a new project or pulling the code, run the migration to create database tables:

```bash
bomiot migrate
```

Typical output (excerpt):

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Using together with makemigrations

When you change a model (e.g. adding a field to `models.py` in a plugin), first generate the migration then apply it:

```bash
# 1. Generate migration files
bomiot makemigrations <appname>

# 2. Apply migrations
bomiot migrate
```

### Output on migration failure

If the database connection fails or there is a migration conflict, an error is printed instead of crashing:

```text
Error during migration: <specific exception message>
```

Common causes include: the database service is not running, the connection configuration is wrong, or there are dependency conflicts between migration files. Investigate based on the error message and retry.

## Prerequisites

1. You are in the project root and the bomiot environment is properly configured.
2. The database service is running and the connection configuration is correct.
3. For a new project, it is recommended to run `bomiot init` / `bomiot project` first to initialize the project structure.

## Related Commands

- [bomiot makemigrations](#): Generate migration files (registered as the `makemigrations` subcommand in `cmd.py`)
- [bomiot initadmin](./cli-initadmin.en-US.md): Create the admin user (tables must exist via `migrate` first)
- [bomiot initpwd](./cli-initpwd.en-US.md): Reset the admin password (tables must exist via `migrate` first)
- [bomiot init](./cli-init.en-US.md): Initialize base project files
