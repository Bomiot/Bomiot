# bomiot dumpdata

Export application data from the database into standard JSON data files — for backups, data migration, or shipping seed data with the project.

```bash
bomiot dumpdata [appname ...]
```

## Overview

`bomiot dumpdata` reads the database and serializes the data of the specified apps (or all apps) into JSON. The output can be imported as-is on another environment with `bomiot loaddata`, moving data between environments.

The command must be run from the **project root**.

## Basic Usage

| Command | Description |
|---|---|
| `bomiot dumpdata` | Export data of all apps (to standard output) |
| `bomiot dumpdata myapp` | Export only the `myapp` app's data |
| `bomiot dumpdata myapp.mymodel` | Export only one table of the `myapp` app |
| `bomiot dumpdata app1 app2` | Export several apps at once |
| `bomiot dumpdata myapp > backup.json` | Write the export to a file (recommended) |

> When exporting large amounts of data, always redirect to a file — printing to the terminal is slow and hard to keep.

## Common Options

| Option | Description |
|---|---|
| `--output FILE` | Write to the given file (equivalent to `>`); supports compressed formats like `.gz` / `.bz2` |
| `--indent N` | Number of indentation spaces, making the data file readable and version-control friendly, e.g. `--indent 2` |
| `--exclude APP` | Exclude the given app (may be used multiple times) |
| `--exclude APP.MODEL` | Exclude a specific table of an app |
| `--natural-foreign` | Serialize foreign keys as natural keys, avoiding primary-key mismatches across environments |
| `--natural-primary` | Omit primary keys; they are regenerated on import |
| `--pks 1,2,3` | Export only records with the given primary keys (with a single model) |
| `--format json` | Serialization format, defaults to `json` |

## Typical Scenarios

### Back up one app's data

```bash
bomiot dumpdata myapp --indent 2 --output myapp_backup.json
```

### Export a single table, human-readable

```bash
bomiot dumpdata myapp.mymodel --indent 2 > mymodel.json
```

### Full backup excluding transient data

```bash
bomiot dumpdata --exclude sessions --exclude admin.logentry --output full_backup.json
```

### Export a few seed records (for initialization)

```bash
bomiot dumpdata myapp.mymodel --pks 1,2,3 --indent 2 --output seeds.json
```

## Working with bomiot loaddata

Exported data files can be imported directly on another environment:

```bash
# Export on the source environment
bomiot dumpdata myapp --indent 2 --output myapp.json

# Import on the target environment
bomiot loaddata myapp.json
```

For project seed data, place the data file in the app's `fixtures` directory — `loaddata` will find it by filename automatically.

## Notes

- A full export includes every table and can be very large; in production, narrow the scope by naming apps or using `--exclude`
- Data files contain plain-text content — handle sensitive data with care and do not commit them to public repositories
- When importing across environments, mismatched schema versions (pending migrations) can cause failures — run `bomiot migrate` on the target first
- Fields such as user passwords are exported in hashed form and remain usable after import
