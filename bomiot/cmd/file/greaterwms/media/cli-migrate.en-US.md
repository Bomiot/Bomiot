# bomiot migrate

Apply migration files to the database, bringing the schema in line with the model code.

```bash
bomiot migrate [appname] [migration_name]
```

## Overview

After `bomiot makemigrations` generates migration files, the database itself has not changed yet. `bomiot migrate` **actually executes** those changes: it applies every unapplied migration in dependency order and records each one's status, so a migration never runs twice on the same database.

The command must be run from the **project root**.

## Basic Usage

| Command | Description |
|---|---|
| `bomiot migrate` | Apply all pending migrations of all apps (most common) |
| `bomiot migrate myapp` | Apply pending migrations of `myapp` only |
| `bomiot migrate myapp 0003` | Move `myapp` to the given migration (forwards or backwards) |
| `bomiot migrate myapp zero` | Reverse all migrations of `myapp` (back to before its tables existed) |

## Common Options

| Option | Description |
|---|---|
| `--plan` | List which migrations would run, without executing them |
| `--fake` | Update the migration records only, without touching the schema — for special cases where the schema was adjusted manually |
| `--fake-initial` | Skip actually running initial migrations when the tables already exist |
| `--run-syncdb` | Create tables for apps without migration files (not recommended for regular use) |

## Typical Scenarios

### Sync the schema after pulling code

```bash
git pull
bomiot migrate
```

The standard team move: migrations committed by others are applied locally, and both databases match.

### First-time initialization of a new project

```bash
bomiot migrate
```

All built-in and business tables are created, giving you a usable empty database.

### Preview what will run

```bash
bomiot migrate --plan
```

Lists the pending migrations so you can verify before executing for real.

### Roll back the latest change

```bash
bomiot migrate myapp 0002
```

Moves `myapp` back to `0002` (`0003` and later are reversed).

### Adopt migrations on a legacy database

Tables already exist, but migrations were never run:

```bash
bomiot migrate --fake-initial
```

Existing tables are detected; migration status is recorded without re-creating them.

## Working with makemigrations

| Command | Responsibility | When |
|---|---|---|
| `bomiot makemigrations` | **Generate** migration files (code → files) | After editing models |
| `bomiot migrate` | **Apply** migration files (files → database) | After generating migrations / after pulling code / at deploy time |

## Notes

- In production, preview with `--plan` first and back up the database
- Reversing migrations undoes their changes (dropping fields, dropping tables) — the corresponding data is deleted, confirm before running
- Migrations are ordered automatically by dependency, including cross-app dependencies (foreign keys) — no manual ordering needed
- A migration runs only once per database; already-applied migrations are skipped on subsequent runs
- Never delete a migration file that has been applied — records correspond to files one-to-one, and deleting files corrupts the state
- Standard deploy sequence: pull code → `bomiot migrate` → restart the service
