# MySQL 数据库

## 介绍

- **Bomiot**支持修改为MySQL数据库

---

## 安装支持库

```bash
pip install mysqlclient
```

## 修改setup.ini

```bash
[database]
engine = mysql
name = db_name            # 你的db设置的name
user = root               # 一般为root
password = password       # 密码
host = 127.0.0.1
port = 3306
```