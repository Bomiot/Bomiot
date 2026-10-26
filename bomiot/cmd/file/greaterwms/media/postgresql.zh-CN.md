# PostgreSQL 数据库

## 介绍

- **Bomiot** 支持切换为 PostgreSQL 数据库，要求 PostgreSQL **12** 及以上版本。

---

## 安装驱动

```bash
pip install psycopg2-binary
```

- `psycopg2-binary` 自带预编译库，开箱即用，适合快速上手。
- 生产环境建议 `pip install psycopg2`（源码编译，链接系统 libpq）。
- 也兼容新一代驱动 `psycopg`（v3），两者任选其一即可。

---

## 准备数据库

建库时指定 UTF8 编码，并把属主设为专用用户：

```sql
CREATE USER bomiot WITH PASSWORD 'your_password';
CREATE DATABASE db_name OWNER bomiot ENCODING 'UTF8';
```

- 用户默认权限即可运行项目和执行迁移。
- 如需运行自动化测试，测试库是动态创建的，需追加建库权限：`ALTER USER bomiot CREATEDB;`

---

## 修改 setup.ini

```ini
[database]
engine = postgresql
name = db_name            # 上面创建的数据库名
user = bomiot
password = your_password
host = 127.0.0.1
port = 5432
```

- `host` 填 `127.0.0.1` 走 TCP 连接；留空则尝试本机 Unix socket（Windows 上请明确填写）。

---

## 初始化数据

```bash
bomiot migrate
bomiot initadmin
```

---

## 注意事项

- **大小写敏感**：PostgreSQL 的 `LIKE` 默认区分大小写，与 MySQL 的默认行为相反，迁移数据后注意核对模糊查询结果。
- **编码**：建库时的 `ENCODING 'UTF8'` 一旦确定不可更改，请勿省略。
- **连接数**：默认 `max_connections = 100`，多 workers 部署时按 worker 数量评估连接占用。
- 修改 `setup.ini` 后需重启服务生效。
