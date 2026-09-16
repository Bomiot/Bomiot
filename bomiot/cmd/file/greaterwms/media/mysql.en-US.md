# MySQL Database

## Introduction

- **Bomiot** supports switching to a MySQL database.

---

## Install Library

```bash
pip install mysqlclient
```

---

## Edit setup.ini

```ini
[database]
engine = mysql
name = db_name            # your db name
user = root               # normal is root
password = password       # password
host = 127.0.0.1
port = 3306
```
