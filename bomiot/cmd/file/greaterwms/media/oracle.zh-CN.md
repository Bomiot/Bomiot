# Oracle 数据库

## 介绍

- **Bomiot** 支持切换为 Oracle 数据库，要求 Oracle **12.2** 及以上版本。

---

## 安装驱动

```bash
pip install oracledb
```

- `oracledb` 是当前的官方 Python 驱动，默认运行在瘦模式（Thin），**不需要**安装 Oracle Instant Client。
- 只有用到高级特性（如应用连续性、高级队列）时才需要切换到厚模式（Thick）并安装 Instant Client。
- 老项目里的 `cx_Oracle` 已被 `oracledb` 取代，新环境直接装后者。

---

## 准备数据库用户

不要直接用 `system` 等高权限账号运行项目，建议建一个专用用户：

```sql
CREATE USER bomiot IDENTIFIED BY "your_password"
    DEFAULT TABLESPACE users
    TEMPORARY TABLESPACE temp;

GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE,
      CREATE PROCEDURE, CREATE TRIGGER TO bomiot;

ALTER USER bomiot QUOTA UNLIMITED ON users;
```

- `CREATE SESSION` 允许登录，`CREATE TABLE / SEQUENCE / PROCEDURE / TRIGGER` 是执行迁移建表所需的最小权限集。
- `QUOTA UNLIMITED ON users` 授予表空间配额，否则建表会报配额不足。
- 如需运行自动化测试，测试库会单独创建表空间，还需追加 `CREATE TABLESPACE` 和 `DROP TABLESPACE` 权限。

---

## 修改 setup.ini

```ini
[database]
engine = oracle
name = ORCLPDB1           # Oracle 服务名（SERVICE_NAME），不是 SID
user = bomiot
password = your_password
host = localhost
port = 1521
```

- `name` 填**服务名**（可在数据库服务器上执行 `SELECT sys_context('userenv','service_name') FROM dual;` 查询）。
- 如果 `host` 留空，则 `name` 需要填写完整连接串：`host:port/service_name`，或 `tnsnames.ora` 中配置好的别名。

---

## 初始化数据

```bash
bomiot migrate
bomiot initadmin
```

---

## 注意事项

- **空字符串即 NULL**：Oracle 把空字符串 `''` 当作 `NULL` 存储。涉及可能存空串的字段，查询时要按 `NULL` 处理，行为与 sqlite / mysql 不同。
- **标识符大写**：Oracle 默认把未加引号的表名、列名转为大写，框架会自动处理，手写 SQL 时注意。
- **字段长度**：`VARCHAR2` 默认最大 4000 字节；Oracle 12.2+ 可通过 `MAX_STRING_SIZE=EXTENDED` 扩展到 32767，超长文本请用 CLOB 类型字段。
- **字符集**：建库时建议选择 `AL32UTF8`（UTF-8），库创建后再改字符集代价很大。
- 修改 `setup.ini` 后需重启服务生效。
