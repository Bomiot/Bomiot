# PostgreSQL Database

## Introduction

- **Bomiot** supports switching to a PostgreSQL database. PostgreSQL **12** or later is required.

---

## Install the Driver

```bash
pip install psycopg2-binary
```

- `psycopg2-binary` ships prebuilt libraries and works out of the box — good for getting started.
- For production, prefer `pip install psycopg2` (compiled from source against the system libpq).
- The next-generation driver `psycopg` (v3) is also supported; either one works.

---

## Prepare the Database

Create the database with UTF8 encoding, owned by a dedicated user:

```sql
CREATE USER bomiot WITH PASSWORD 'your_password';
CREATE DATABASE db_name OWNER bomiot ENCODING 'UTF8';
```

- Default privileges are enough to run the project and its migrations.
- To run automated tests, the test database is created on the fly, so the user needs the create-database privilege: `ALTER USER bomiot CREATEDB;`

---

## Edit setup.ini

```ini
[database]
engine = postgresql
name = db_name            # the database created above
user = bomiot
password = your_password
host = 127.0.0.1
port = 5432
```

- `host = 127.0.0.1` uses a TCP connection; leaving it empty attempts a local Unix socket (always set it explicitly on Windows).

---

## Initialize the Data

```bash
bomiot migrate
bomiot initadmin
```

---

## Notes

- **Case sensitivity**: PostgreSQL's `LIKE` is case-sensitive by default — the opposite of MySQL's default. Verify fuzzy-search results after migrating data.
- **Encoding**: the `ENCODING 'UTF8'` set at database creation cannot be changed later — do not omit it.
- **Connections**: the default `max_connections = 100`; estimate usage by worker count when running multiple workers.
- Restart the service after editing `setup.ini`.
