# bomiot initpwd Command

## Overview

The `bomiot initpwd` command resets the password of bomiot's default superuser `admin` back to `admin`. It sets the Django environment variables and runs `django.setup()`, obtains the user model via `get_user_model()`, looks up the superuser named `admin`, and if found resets its password to `admin`; if none exists it prompts the user to create an admin first.

The command is implemented by the `init_password()` function in `bomiot/cmd/initpwd.py` and registered as the `initpwd` subcommand in `bomiot/cmd/cmd.py`.

> ⚠️ **Known source bug**: when checking whether the admin exists, the code uses `user_data.exists` (property access) instead of `user_data.exists()` (method call), which makes the condition always truthy, so even when no admin user exists it enters the reset branch and raises an exception. See "Known Issue in the Source" below.

## Usage

```bash
bomiot initpwd
```

- This command takes **no arguments**.

Registration in `cmd.py`:

```python
# init password
parser_initpwd = subparsers.add_parser(
    'initpwd', help='Init admin password')
```

Dispatch logic:

```python
# init admin
elif command == 'initpwd':
    from bomiot.cmd.initpwd import init_password
    init_password()
```

## Source Code Analysis

Source file: `bomiot/cmd/initpwd.py`

The full source is:

```python
import django
import os


def init_password():
    """
    init superuser password
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user_data = User.objects.filter(username='admin', is_superuser=True)
    if user_data.exists:
        user_data.first().set_password('admin')
        print('Reset admin account: admin, initial password: admin, just use it temporarily '
              'and change the password for safety')
    else:
        print('Please init one admin first')
```

### Setting Up the Django Environment

As with `initadmin`, it first sets `DJANGO_SETTINGS_MODULE` and calls `django.setup()`, then dynamically imports `get_user_model()`:

```python
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()
```

### Looking Up the admin Superuser

It uses `filter(username='admin', is_superuser=True)` to obtain a queryset `user_data`:

```python
    user_data = User.objects.filter(username='admin', is_superuser=True)
```

### Checking and Resetting the Password

The source intends to reset the password when the queryset is non-empty, otherwise prompt the user to create an admin first. But it actually writes `if user_data.exists:`:

```python
    if user_data.exists:
        user_data.first().set_password('admin')
        print('Reset admin account: admin, initial password: admin, just use it temporarily '
              'and change the password for safety')
    else:
        print('Please init one admin first')
```

### Known Issue in the Source (Bug)

Django QuerySet's `exists` is a **method**, so the correct call form is `user_data.exists()`. Writing `user_data.exists` (without parentheses) merely obtains a reference to the bound method object, and a bound method object is **always truthy** in a boolean context. Therefore:

- Regardless of whether the admin user exists, `if user_data.exists:` always holds, and the program always enters the reset branch.
- When no admin user exists, `user_data.first()` returns `None`, and the subsequent `None.set_password('admin')` raises `AttributeError`.
- The `else` branch (prompting `Please init one admin first`) is **never executed**.

The correct version should be:

```python
    if user_data.exists():
        user_data.first().set_password('admin')
        ...
    else:
        print('Please init one admin first')
```

## Practical Examples

### Resetting the password when the admin user exists

Prerequisite: an admin user has already been created via `bomiot initadmin`.

```bash
bomiot initpwd
```

Output:

```text
Reset admin account: admin, initial password: admin, just use it temporarily and change the password for safety
```

You can then log in to the backend with `admin` / `admin`.

### When the admin user does not exist (affected by the bug)

Due to the bug above, when no admin user exists the command does not print `Please init one admin first`; instead it raises an exception at `user_data.first().set_password('admin')`:

```text
AttributeError: 'NoneType' object has no attribute 'set_password'
```

So if you have not yet created an admin user, run this first:

```bash
bomiot initadmin
```

## Prerequisites

This command loads Django settings and accesses the database, so make sure before running:

1. You are in the project root.
2. You have already run `bomiot migrate` to create tables.

## Security Notice

- The reset password is the weak value `admin`, intended for temporary use only. After logging in, change it immediately to a strong password.
- This command does not verify the caller's identity; anyone able to run `bomiot initpwd` can reset the admin password to a known value, so control runtime environment permissions carefully.

## Related Commands

- [bomiot initadmin](./cli-initadmin.en-US.md): Create the default admin superuser
- [bomiot migrate](./cli-migrate.en-US.md): Run database migrations (tables must exist before `initpwd`)
- [bomiot init](./cli-init.en-US.md): Initialize base project files
