# bomiot loaddata

Load the contents of data files (fixtures) into the database — for restoring backups, loading seed data, or moving data between environments.

```bash
bomiot loaddata <fixture> [fixture ...]
```

## Overview

`bomiot loaddata` reads JSON data files and writes their records into the corresponding database tables. Data files are usually produced by `bomiot dumpdata`, but can also be written by hand — a data file is a repeatable package of "seed data".

The command must be run from the **project root**.

## Basic Usage

| Command | Description |
|---|---|
| `bomiot loaddata myapp.json` | Load the given data file |
| `bomiot loaddata app1.json app2.json` | Load several data files at once |
| `bomiot loaddata seeds` | Omit the extension; the file is located via fixture lookup rules |

## Where Files Are Looked Up

When given a bare filename, files are searched in this order:

| Location | Description |
|---|---|
| Each app's `fixtures/` directory | Seed data shipped with the app, looked up by filename |
| Current directory / given path | Read directly when a relative or absolute path is given |

> For project seed data, place the file in the app's `fixtures/` directory with an app-related name (e.g. `myapp.json`). After pulling the code, teammates simply run `bomiot loaddata myapp` to initialize.

## Common Options

| Option | Description |
|---|---|
| `--app myapp` | Load only the records belonging to the `myapp` app |
| `--ignorenonexistent` | Skip models or fields in the file that no longer exist, instead of failing |
| `--format json` | Data file format, defaults to `json` (usually detected from the extension) |
| `--exclude APP` | Exclude the given app's data while loading (may be used multiple times) |

## Typical Scenarios

### Restore one app's backup

```bash
bomiot loaddata myapp_backup.json
```

### Initialize seed data for a new project

```bash
bomiot loaddata seeds.json
```

### Move data between environments

```bash
# Source environment
bomiot dumpdata myapp --indent 2 --output myapp.json

# Target environment (make sure the schema matches first)
bomiot migrate
bomiot loaddata myapp.json
```

### File contains fields removed from the current code

```bash
bomiot loaddata old_backup.json --ignorenonexistent
```

## Loading Behavior

- Records are keyed by **primary key**: an existing primary key updates the record, a new one inserts it
- Files exported with `--natural-primary` contain no primary keys — all records are inserted with freshly generated keys
- Loading runs in a single transaction; on error it rolls back, leaving no partial data behind

## Notes

- Run `bomiot migrate` on the target database first so the schema matches the data file, otherwise loading may fail
- Fields such as user passwords are stored as hashes in data files and work directly after loading — never rewrite them as plain text
- Re-loading the same file is safe (records are updated by primary key), but files without primary keys create duplicates when loaded twice
- Large files take time to load; avoid writing to the same tables concurrently during the load
