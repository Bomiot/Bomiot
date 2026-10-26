# MySQL 数据库

## 介绍

- **Bomiot** 支持切换为 MySQL 数据库，要求 MySQL **8.0** 及以上版本。

---

## 安装驱动

```bash
pip install mysqlclient
```

- `mysqlclient` 是推荐的 Python 驱动，基于 C 扩展，性能最好。
- Windows 上优先使用预编译 wheel 安装；如编译失败，先升级 pip 再重试：`pip install -U pip`。

---

## 准备数据库

建库时指定 `utf8mb4` 字符集，并创建专用用户：

```sql
CREATE DATABASE db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'bomiot'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON db_name.* TO 'bomiot'@'%';
FLUSH PRIVILEGES;
```

- 只允许本机连接时，把 `'%'` 改为 `'localhost'`。
- 表必须使用 **InnoDB** 存储引擎（MySQL 8 默认即是）；MyISAM 不支持事务和外键，不能使用。

---

## 修改 setup.ini

```ini
[database]
engine = mysql
name = db_name            # 上面创建的数据库名
user = bomiot
password = your_password
host = 127.0.0.1
port = 3306
```

---

## 初始化数据

```bash
bomiot migrate
bomiot initadmin
```

---

## 注意事项

- **字符集**：务必用 `utf8mb4` 建库。旧的 `utf8` 在 MySQL 里最多存 3 字节，emoji 和部分生僻字会写入失败。
- **sql_mode**：建议开启 `STRICT_TRANS_TABLES`（MySQL 8 默认已开启），让非法数据直接报错而不是静默截断。
- **隔离级别**：框架会把每个连接的隔离级别设为 READ COMMITTED，无需手动配置。
- **时区表**：如需按时区转换时间，先导入系统时区表：`mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql`。
- 修改 `setup.ini` 后需重启服务生效。
