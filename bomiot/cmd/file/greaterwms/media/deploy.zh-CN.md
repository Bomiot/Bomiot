# 部署打包

## 简介

Bomiot 支持将项目打包为**单文件可执行程序**（零依赖部署），并提供 Supervisor 守护进程部署方案。核心 Python 代码可通过 Nuitka 编译为二进制以保护源码。

---

## 单文件打包

```bash
bomiot package my-project
```

打包产物输出在 `dist/` 目录，包含运行时、依赖、代码与资源，双击即可运行。

---

## 打包流程

1. 执行 `bomiot package <project_name>`
2. Nuitka 将 Python 代码编译为本地二进制
3. 运行时、依赖、资源文件被打包进单个可执行文件
4. 输出可执行文件到 `dist/`

> 打包过程中，核心模块可被编译为二进制（`.exe` / `.so` / `.pyd`），关键安全路径可使用 PyO3（Rust）进一步加固。详见「代码保护」文档。

---

## Supervisor 部署

Bomiot 提供 `deploy` 命令生成 Supervisor 配置：

```bash
bomiot deploy my-project
```

生成的配置文件可直接被 `supervisord.conf` 引用，实现守护进程部署：

```ini
# supervisord.conf 示例
[include]
files = /path/to/my-project/supervisord.conf
```

---

## 服务启动参数

```bash
bomiot run [选项]

选项:
  --host, -b HOST                主机地址 (默认: 127.0.0.1)
  --port, -p PORT                端口 (默认: 8000)
  --workers, -w WORKERS          工作进程数 (默认: 1)
  --log-level LEVEL              日志级别
  --ssl-keyfile FILE             SSL 密钥文件
  --ssl-certfile FILE            SSL 证书文件
  --proxy-headers                启用代理头
  --limit-concurrency N          最大并发请求数 (默认: 1000)
  --timeout-graceful-shutdown S  优雅关闭超时 (默认: 30s)
```

### 生产环境示例

```bash
bomiot run --host 0.0.0.0 --port 80 --workers 4 --log-level info
```

### SSL 部署

```bash
bomiot run --ssl-keyfile key.pem --ssl-certfile cert.pem
```

---

## 前端部署

前端修改后需重新构建：

```bash
cd templates
quasar build
```

产物输出到 `templates/dist/spa/`，由 Django 后端直接服务。

---

## 多节点协同

- **单机/局域网**：节点本地存储，适合离线场景
- **多节点协同**：通过授权网关实现跨站云协同
- **数据主权**：数据始终存储在本地节点，满足合规要求

---

## 部署检查清单

- [ ] 数据库已迁移（`bomiot migrate`）
- [ ] 管理员已创建（`bomiot initadmin`）
- [ ] `setup.ini` 中数据库配置正确
- [ ] 前端已构建（`quasar build`）
- [ ] 端口未被占用
- [ ] SSL 证书（如需 HTTPS）
