# MySQL Database

## Introduction

- **Bomiot** supports switching to a MySQL database. MySQL **8.0** or later is required.

---

## Install the Driver

```bash
pip install mysqlclient
```

- `mysqlclient` is the recommended Python driver — a C extension with the best performance.
- On Windows, prefer the prebuilt wheel; if the build fails, upgrade pip first: `pip install -U pip`.

---

## Prepare the Database

Create the database with the `utf8mb4` character set, plus a dedicated user:

```sql
CREATE DATABASE db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'bomiot'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON db_name.* TO 'bomiot'@'%';
FLUSH PRIVILEGES;
```

- To allow only local connections, replace `'%'` with `'localhost'`.
- Tables must use the **InnoDB** storage engine (the default in MySQL 8); MyISAM lacks transactions and foreign keys and must not be used.

---

## Edit setup.ini

```ini
[database]
engine = mysql
name = db_name            # the database created above
user = bomiot
password = your_password
host = 127.0.0.1
port = 3306
```

---

## Initialize the Data

```bash
bomiot migrate
bomiot initadmin
```

---

## Notes

- **Character set**: always create the database with `utf8mb4`. The legacy `utf8` in MySQL stores at most 3 bytes per character, so emoji and some rare characters fail to save.
- **sql_mode**: keep `STRICT_TRANS_TABLES` enabled (default in MySQL 8) so invalid data raises errors instead of being silently truncated.
- **Isolation level**: the framework sets every connection to READ COMMITTED automatically — no manual configuration needed.
- **Timezone tables**: for timezone conversions, load the system timezone tables first: `mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql`.
- Restart the service after editing `setup.ini`.
