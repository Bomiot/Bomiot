# SQLite 数据库

## 介绍

- **Bomiot** 默认使用 SQLite，零配置、免安装，数据存于单个文件。
- 驱动为 Python 自带的 `sqlite3` 模块，**无需安装任何依赖**；Python 安装包已内置较新版本的 SQLite 库，一般不需要手动升级。

---

## 修改 setup.ini

```ini
[database]
engine = sqlite
```

- 仅此一项即可，其余字段（name / user / password / host / port）无需填写。
- 首次启动自动在工作空间 `dbs/` 目录下创建 `db.sqlite3`。

---

## 初始化数据

```bash
bomiot migrate
bomiot initadmin
```

---

## 注意事项

- **并发写锁**：SQLite 同一时刻只允许一个写入者，高并发写入会出现 `database is locked`。开发与中小规模部署足够用；多人同时写入的生产环境建议改用 MySQL / PostgreSQL / Oracle。
- **备份**：备份就是复制 `dbs/db.sqlite3` 这一个文件，恢复同理。
- **大小写匹配**：SQLite 的 `LIKE` 对 ASCII 字符默认不区分大小写，与其他数据库行为不同，迁移数据时注意核对查询结果。
- **外键**：框架连接时已自动开启外键约束，无需额外配置。
- 修改 `setup.ini` 后需重启服务生效。
