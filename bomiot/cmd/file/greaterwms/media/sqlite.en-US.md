# SQLite Database

## Introduction

- **Bomiot** uses SQLite by default — zero configuration, nothing to install, all data in a single file.
- The driver is Python's built-in `sqlite3` module, so **no extra dependency is required**. Python installers already bundle a recent SQLite library; a manual upgrade is normally unnecessary.

---

## Edit setup.ini

```ini
[database]
engine = sqlite
```

- This single line is enough; the other keys (name / user / password / host / port) are not needed.
- `db.sqlite3` is created automatically under the workspace `dbs/` directory on first startup.

---

## Initialize the Data

```bash
bomiot migrate
bomiot initadmin
```

---

## Notes

- **Concurrent write locking**: SQLite allows only one writer at a time; heavy concurrent writes produce `database is locked` errors. Fine for development and small deployments — for write-heavy production use, switch to MySQL / PostgreSQL / Oracle.
- **Backup**: backing up means copying the single `dbs/db.sqlite3` file; restore the same way.
- **Case-insensitive matching**: SQLite's `LIKE` is case-insensitive for ASCII characters by default, unlike other databases — verify query results when migrating data.
- **Foreign keys**: the framework enables foreign-key enforcement on every connection automatically; no extra setup needed.
- Restart the service after editing `setup.ini`.
