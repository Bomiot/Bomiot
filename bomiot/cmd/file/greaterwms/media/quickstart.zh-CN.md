# 快速开始

## 简介

Bomiot 是面向仓储与供应链的节点化全栈开发平台，支持单文件部署、多后端框架（Django / FastAPI / Flask）与多前端框架（Vue / React / Angular），并提供 Python 代码编译保护与插件生态。

---

## 环境要求

- **Python**：3.9 或更高版本
- **Node.js**：18.19.1 或更高版本（修改前端时需要）
- **操作系统**：Windows / macOS / Linux

---

## 1. 安装 Bomiot

```bash
# 使用 pip 安装
pip install bomiot

# 或使用 poetry 安装
poetry add bomiot
```

---

## 2. 初始化工作空间

```bash
bomiot init
```

该命令会在当前目录创建 Bomiot 工作空间，生成 `setup.ini` 等全局配置文件。

---

## 3. 创建项目

```bash
# 创建新项目
bomiot project my-project
```

进入项目目录后，可以继续创建应用：

```bash
cd my-project

# 创建应用（默认 Django 框架）
bomiot new my-app

# 指定后端框架
bomiot new my-app --framework django
bomiot new my-app --framework fastapi
bomiot new my-app --framework flask
```

---

## 4. 数据库

```bash
# 生成数据库迁移文件
bomiot makemigrations

# 执行数据库迁移
bomiot migrate

# 加载初始数据
bomiot loaddata <source>

# 导出数据
bomiot dumpdata [appname]
```

---

## 5. 管理员

```bash
# 创建管理员账户
bomiot initadmin

# 重置管理员密码
bomiot initpwd
```

---

## 6. 启动服务

```bash
# 启动开发服务器（默认 127.0.0.1:8000）
bomiot run

# 指定主机和端口
bomiot run --host 0.0.0.0 --port 8080

# 生产环境配置
bomiot run --host 0.0.0.0 --port 80 --workers 4 --log-level info
```

启动后访问 `http://127.0.0.1:8000/` 即可进入系统。

---

## 7. 验证安装

启动服务后，可通过以下地址测试各后端框架：

```
Django:   http://127.0.0.1:8000/test/
FastAPI:  http://127.0.0.1:8000/fastapi/test/
Flask:    http://127.0.0.1:8000/flask/test/
```

---

## 8. 打包发布

```bash
# 打包项目（核心模块可编译为二进制以保护源码）
bomiot package my-project
```

打包产物输出在 `dist/` 目录。

---

## 常用命令速览

| 命令 | 说明 |
|------|------|
| `bomiot init` | 初始化工作空间 |
| `bomiot project <name>` | 创建项目 |
| `bomiot new <app>` | 创建应用 |
| `bomiot makemigrations` | 生成迁移 |
| `bomiot migrate` | 执行迁移 |
| `bomiot initadmin` | 创建管理员 |
| `bomiot initpwd` | 重置管理员密码 |
| `bomiot run` | 启动服务 |
| `bomiot package <name>` | 打包项目 |
| `bomiot keys` | 初始化校验 Keys |
