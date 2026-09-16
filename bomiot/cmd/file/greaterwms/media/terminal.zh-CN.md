# 终端

## 概述

Bomiot 通过命令行工具 `bomiot` 管理项目的整个生命周期。在终端中执行 `bomiot <command> [options]` 即可调用对应功能。

> 每个命令的详细用法请参考「CLI 命令」Tab 中的对应文档。

## 可选参数

```shell
  -v, --version       获取 Bomiot 版本
  -h, --help          显示帮助信息并退出
```

## 可用命令

```shell
    app               为项目创建子 APP
    api               为项目创建 Bomiot API
    project           创建项目工作空间
    deploy            生成 GitHub Actions 部署工作流（赞助专享）
    init              初始化 bomiot 工作空间
    initadmin         创建默认超级用户 admin
    initpwd           重置 admin 密码
    makemigrations    生成数据库迁移文件
    migrate           执行数据库迁移
    loaddata          从配置加载数据
    dumpdata          将数据导出到配置
    run               启动服务器
```

## 快速上手

```shell
# 1. 初始化项目
bomiot init

# 2. 创建超级管理员
bomiot initadmin

# 3. 执行数据库迁移
bomiot migrate

# 4. 启动服务（默认 0.0.0.0:8000）
bomiot run
```

## 启动服务

```shell
bomiot run --host 0.0.0.0 --port 8000 --log-level info
```

### 常用启动参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--host` / `-b` | `0.0.0.0` | 绑定主机地址 |
| `--port` / `-p` | `8000` | 绑定端口 |
| `--log-level` | `info` | 日志级别：critical / error / warning / info / debug / trace |
| `--ssl-keyfile` | 无 | SSL 密钥文件路径 |
| `--ssl-certfile` | 无 | SSL 证书文件路径 |
