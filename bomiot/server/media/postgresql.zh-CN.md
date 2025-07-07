# PostgreSQL 数据库

## 介绍

- **Bomiot**支持修改为PostgreSQL数据库

---

## 安装支持库

```bash
pip install psycopg2
```

## 修改setup.ini

```bash
[database]
engine = postgresql
name = db_name            # 你的db设置的name
user = root               # 一般为root
password = password       # 密码
host = localhost
port = 5432
```