# PostgreSQL Database

## Introduction

- **Bomiot** supports switching to a PostgreSQL database.

---

## Install Library

```bash
pip install psycopg2
```

---

## Edit setup.ini

```ini
[database]
engine = postgresql
name = db_name            # your db name
user = root               # normal is root
password = password       # password
host = localhost
port = 5432
```
