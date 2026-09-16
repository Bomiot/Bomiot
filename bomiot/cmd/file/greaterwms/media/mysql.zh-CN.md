# MySQL 数据库

## 介绍

- **Bomiot** 支持切换为 MySQL 数据库。

---

## 安装支持库

```bash
pip install mysqlclient
```

---

## 修改 setup.ini

```ini
[database]
engine = mysql
name = db_name            # 你的数据库名称
user = root               # 一般为 root
password = password       # 密码
host = 127.0.0.1
port = 3306
```
