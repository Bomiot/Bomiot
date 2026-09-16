# 命令行工具

## 简介

Bomiot 提供强大的命令行工具（CLI），涵盖项目创建、应用管理、数据库、用户、服务、打包等全流程操作。

```bash
bomiot [命令] [选项]
```

---

## 帮助与版本

```bash
# 查看帮助
bomiot -h

# 查看版本
bomiot -v
```

---

## 项目管理

| 命令 | 说明 |
|------|------|
| `bomiot init` | 初始化工作空间 |
| `bomiot project <name>` | 创建新项目 |
| `bomiot new <app>` | 创建应用（默认 Django） |
| `bomiot new <app> --framework django` | 指定框架创建应用 |
| `bomiot plugins <name>` | 创建插件 |
| `bomiot market <project>` | 应用市场 |

### 创建应用时指定框架

```bash
bomiot new my-app --framework django
bomiot new my-app --framework fastapi
bomiot new my-app --framework flask
```

---

## 数据库管理

| 命令 | 说明 |
|------|------|
| `bomiot makemigrations` | 生成数据库迁移文件 |
| `bomiot migrate` | 执行数据库迁移 |
| `bomiot loaddata <source>` | 加载初始数据 |
| `bomiot dumpdata [appname]` | 导出数据 |

---

## 用户管理

| 命令 | 说明 |
|------|------|
| `bomiot initadmin` | 创建管理员账户 |
| `bomiot initpwd` | 重置管理员密码 |

---

## 服务管理

### 启动服务

```bash
bomiot run [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--host, -b` | 主机地址 | 127.0.0.1 |
| `--port, -p` | 端口 | 8000 |
| `--workers, -w` | 工作进程数 | 1 |
| `--log-level` | 日志级别 | info |
| `--ssl-keyfile` | SSL 密钥文件 | - |
| `--ssl-certfile` | SSL 证书文件 | - |
| `--proxy-headers` | 启用代理头 | - |
| `--limit-concurrency` | 最大并发数 | 1000 |
| `--timeout-graceful-shutdown` | 优雅关闭超时(秒) | 30 |

### 部署

```bash
bomiot deploy <project_name>
```

生成 Supervisor 配置文件，用于守护进程部署。

---

## 打包与发布

```bash
bomiot package <project_name>
```

将项目打包为单文件可执行程序，核心模块可编译为二进制。

---

## 系统校验

```bash
bomiot keys
```

初始化校验 Keys，用于数据库等敏感配置的加密验证。

---

## 使用示例

```bash
# 1. 初始化
bomiot init

# 2. 创建项目
bomiot project warehouse

# 3. 进入项目，创建应用
cd warehouse
bomiot new inbound

# 4. 数据库
bomiot makemigrations
bomiot migrate

# 5. 创建管理员
bomiot initadmin

# 6. 启动服务
bomiot run --host 0.0.0.0 --port 8000

# 7. 打包
bomiot package warehouse
```

---

## 日志级别

`--log-level` 可选值：`critical` / `error` / `warning` / `info` / `debug` / `trace`

```bash
bomiot run --log-level debug
```
