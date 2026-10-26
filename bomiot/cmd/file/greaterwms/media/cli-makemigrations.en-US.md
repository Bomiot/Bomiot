# bomiot makemigrations

Generate database migration files automatically from model changes.

```bash
bomiot makemigrations [appname ...]
```

## Overview

Table structures in the project are defined by model code. When models change — a new model, added/removed/modified fields, changed field options — those changes must be recorded as **migration files**, which `bomiot migrate` later applies to the database.

`bomiot makemigrations` diffs the current model code against the existing migration files and writes new migration files into the app's `migrations/` directory (auto-named with sequence numbers, e.g. `0002_xxx.py`).

The command must be run from the **project root**.

## Basic Usage

| Command | Description |
|---|---|
| `bomiot makemigrations` | Detect model changes in all apps and generate migrations |
| `bomiot makemigrations myapp` | Detect changes only in `myapp` |

## Common Options

| Option | Description |
|---|---|
| `--name NAME` | Give the migration a name suffix for readability, e.g. `--name add_user_email` |
| `--empty myapp` | Create an empty migration file for hand-written data migrations |
| `--dry-run` | Show what would be generated without writing any files |
| `--check` | Exit with a non-zero code if there are model changes without migrations — ideal for CI |
| `--merge` | Merge branched migration files within one app |

## Typical Scenarios

### A new field was added

```bash
# After editing the model code
bomiot makemigrations myapp
# myapp/migrations/0003_add_score_field.py is created
```

### Give the migration a readable name

```bash
bomiot makemigrations myapp --name add_score_field
# Creates 0003_add_score_field.py
```

### Check for missing migrations before committing

```bash
bomiot makemigrations --check --dry-run
# Non-zero exit code when unrecorded changes exist — great for CI
```

### Migrate data, not just schema

```bash
bomiot makemigrations myapp --empty --name backfill_score
# Creates an empty migration to fill in custom data-migration logic
```

## Standard Workflow

```text
Edit model code
  ↓
bomiot makemigrations [myapp]   ← generate migration files
  ↓
Review the generated migration files
  ↓
bomiot migrate                  ← apply to the database (see migrate doc)
  ↓
Commit migration files together with the model code
```

## Notes

- **Migration files must be committed to version control.** They are the shared record of database changes; teammates run `bomiot migrate` after pulling to sync their schemas
- Review the generated migration **before running migrate**, to confirm it matches your intent
- Applying a migration that drops a field deletes that field's data irreversibly
- Renaming a field may be detected as "drop old field + add new field", losing old data — watch for the confirmation prompt when generating
- Parallel model edits by teammates on the same app can produce migration branches; use `--merge` to reconcile them
- Do not edit a generated migration by hand before it is committed — if adjustments are needed, roll it back or delete it and regenerate
