# PostgreSQL 数据库

## 介绍

- **Bomiot** 支持切换为 PostgreSQL 数据库。

---

## 安装支持库

```bash
pip install psycopg2
```

---

## 修改 setup.ini

```ini
[database]
engine = postgresql
name = db_name            # 你的数据库名称
user = root               # 一般为 root
password = password       # 密码
host = localhost
port = 5432
```
