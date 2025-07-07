# PostgreSQL Database

## Introduction

- **Bomiot** Support change to PostgreSQL database

---

## Install Libery

```bash
pip install psycopg2
```

## Edit setup.ini

```bash
[database]
engine = postgresql
name = db_name            # your db name
user = root               # normal is root
password = password       # password
host = localhost
port = 5432
```