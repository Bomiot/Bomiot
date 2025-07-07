# MySQL Database

## Introduction

- **Bomiot** Support change to MySQL database

---

## Install Libery

```bash
pip install mysqlclient
```

## Edit setup.ini

```bash
[database]
engine = mysql
name = db_name            # your db name
user = root               # normal is root
password = password       # password
host = 127.0.0.1
port = 3306
```