# Oracle Database

## Introduction

- **Bomiot** supports switching to an Oracle database. Oracle **12.2** or later is required.

---

## Install the Driver

```bash
pip install oracledb
```

- `oracledb` is the current official Python driver. It runs in Thin mode by default, so **no Oracle Instant Client is needed**.
- Thick mode (with Instant Client) is only required for advanced features such as Application Continuity or Advanced Queuing.
- The legacy `cx_Oracle` driver has been superseded by `oracledb`; install the latter on new environments.

---

## Prepare a Database User

Do not run the project with a privileged account like `system`. Create a dedicated user instead:

```sql
CREATE USER bomiot IDENTIFIED BY "your_password"
    DEFAULT TABLESPACE users
    TEMPORARY TABLESPACE temp;

GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE,
      CREATE PROCEDURE, CREATE TRIGGER TO bomiot;

ALTER USER bomiot QUOTA UNLIMITED ON users;
```

- `CREATE SESSION` allows login; `CREATE TABLE / SEQUENCE / PROCEDURE / TRIGGER` is the minimal privilege set needed to run migrations.
- `QUOTA UNLIMITED ON users` grants tablespace quota — without it, table creation fails with a quota error.
- If you plan to run automated tests, the test database creates its own tablespaces, which additionally requires `CREATE TABLESPACE` and `DROP TABLESPACE`.

---

## Edit setup.ini

```ini
[database]
engine = oracle
name = ORCLPDB1           # Oracle SERVICE_NAME, not the SID
user = bomiot
password = your_password
host = localhost
port = 1521
```

- `name` takes the **service name** (query it on the database server with `SELECT sys_context('userenv','service_name') FROM dual;`).
- If `host` is left empty, `name` must be a full connect string: `host:port/service_name`, or an alias configured in `tnsnames.ora`.

---

## Initialize the Data

```bash
bomiot migrate
bomiot initadmin
```

---

## Notes

- **Empty string means NULL**: Oracle stores `''` as `NULL`. For fields that may hold empty strings, query them as `NULL` — this differs from sqlite / mysql.
- **Uppercase identifiers**: Oracle uppercases unquoted table and column names by default. The framework handles this automatically, but keep it in mind when writing raw SQL.
- **Field length**: `VARCHAR2` is limited to 4000 bytes by default; Oracle 12.2+ can raise this to 32767 via `MAX_STRING_SIZE=EXTENDED`. Use CLOB-typed fields for longer text.
- **Character set**: choose `AL32UTF8` (UTF-8) when creating the database — changing it afterwards is expensive.
- Restart the service after editing `setup.ini`.
