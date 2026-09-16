# bomiot initadmin Command

## Overview

The `bomiot initadmin` command creates the default superuser account for bomiot. It sets the Django environment variables and runs `django.setup()`, obtains the user model via `get_user_model()`, checks whether a superuser named `admin` already exists, and if not, creates one with username `admin`, email `admin@bomiot.com` and initial password `admin`, setting `is_active`, `is_superuser` and `is_staff` all to `True`, and finally warns the user to change the password promptly.

The command is implemented by the `init_admin()` function in `bomiot/cmd/initadmin.py` and registered as the `initadmin` subcommand in `bomiot/cmd/cmd.py`.

## Usage

```bash
bomiot initadmin
```

- This command takes **no arguments**.

Registration in `cmd.py`:

```python
# init admin
parser_initadmin = subparsers.add_parser(
    'initadmin', help='Create default super user admin')
```

Dispatch logic:

```python
# init admin
elif command == 'initadmin':
    from bomiot.cmd.initadmin import init_admin
    init_admin()
```

## Source Code Analysis

Source file: `bomiot/cmd/initadmin.py`

### Setting Up the Django Environment

It first sets the `DJANGO_SETTINGS_MODULE` environment variable to point at bomiot's server settings module, then calls `django.setup()` to register apps before the Django ORM can be used:

```python
import django
import os
from configparser import ConfigParser


def init_admin():
    """
    create superuser
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model
```

> Note: `os.environ.setdefault` only writes when the environment variable is unset; it does not override an existing value.

### Obtaining the User Model

It uses Django's built-in `get_user_model()` to dynamically obtain the user model configured for the current project (which may be a custom User model):

```python
    User = get_user_model()
```

### Checking Whether the Admin Already Exists

It tries to fetch an existing admin superuser via `User.objects.get(username='admin', is_superuser=True)`. If one exists it tells the user they can log in directly; if an exception is raised (i.e. none exists), it falls into the creation branch:

```python
    try:
        User.objects.get(username='admin', is_superuser=True)
        print('Admin user already exists, you can use admin to login:')
    except:
```

### Creating the Admin Account

Inside the `except` branch it builds the account info and uses `update_or_create` to create or update the record by `email` and `username`, then sets the password and permission flags:

```python
        username = 'admin'
        email = f'{username}@bomiot.com'
        password = username
        admin, created = User.objects.update_or_create(email=email, username=username)
        admin.set_password(password)
        admin.is_active = True
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        print('%s admin account: %s(%s), initial password: %s, just use it temporarily '
              'and change the password for safety' % \
              ('Created' if created else 'Reset', username, email, password))
```

Key points:

- `username = 'admin'`
- `email = 'admin@bomiot.com'` (assembled via `f'{username}@bomiot.com'`)
- `password = 'admin'` (same as the username)
- `update_or_create` looks up by `email` and `username`, updating if found or creating if not, and returns `(object, created_bool)`.
- `set_password(password)` hashes the plaintext password before saving.
- `is_active`, `is_superuser` and `is_staff` are all set to `True`, granting backend login and full permissions.
- The output picks `Created` or `Reset` based on `created` and explicitly reminds: "just use it temporarily and change the password for safety".

## Practical Examples

### Creating the admin for the first time

```bash
bomiot initadmin
```

Output:

```text
Created admin account: admin(admin@bomiot.com), initial password: admin, just use it temporarily and change the password for safety
```

You can then log in to the bomiot backend with `admin` / `admin`.

### Running again when the admin already exists

```bash
bomiot initadmin
```

Output:

```text
Admin user already exists, you can use admin to login:
```

### Prerequisites

Because this command loads Django settings and accesses the database, make sure before running:

1. You are in the project root (containing `setup.ini` or a configured bomiot environment).
2. You have already run `bomiot migrate` to create tables, otherwise the `User` table will be missing and an error will be raised.

## Security Notice

- The initial password is the weak value `admin`, intended only for first login. After logging in, change it immediately to a strong password via the backend or a method other than [bomiot initpwd](./cli-initpwd.en-US.md).
- This account has `is_superuser=True` and `is_staff=True`, granting full backend permissions; keep it safe.

## Related Commands

- [bomiot migrate](./cli-migrate.en-US.md): Run database migrations (tables must exist before `initadmin`)
- [bomiot initpwd](./cli-initpwd.en-US.md): Reset the admin password back to `admin`
- [bomiot init](./cli-init.en-US.md): Initialize base project files
