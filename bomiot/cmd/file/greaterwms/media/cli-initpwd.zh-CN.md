# bomiot initpwd

将超级管理员 `admin` 的密码重置为初始值 `admin`。

```bash
bomiot initpwd
```

## 概述

`bomiot initpwd` 用于找回管理员密码：把 `admin` 超级管理员的密码直接重置为初始密码 `admin`。命令必须在**项目根目录**下执行，操作的是当前项目的数据库。

> **与 initadmin 的区别**：`initadmin` 处理的是"账号不存在或状态异常"——创建账号、恢复禁用、恢复权限，顺便重置密码；`initpwd` 只做一件事——**重置密码**，要求 `admin` 账号已经存在。两者重置后的初始密码相同。

## 使用前提

`admin` 超级管理员账号已存在（通常由 `bomiot initadmin` 创建）。若账号尚不存在，命令会提示"Please init one admin first"，请先执行：

```bash
bomiot initadmin
```

## 典型场景

| 场景 | 操作 |
|---|---|
| admin 密码遗忘 | 执行 `bomiot initpwd`，用 `admin` / `admin` 登录后立即改密 |
| 前任管理员离职，需要回收权限 | 执行 `bomiot initpwd` 重置密码，再登录调整账号 |
| 怀疑 admin 密码泄露 | 执行 `bomiot initpwd` 重置，然后设置新密码 |

## 执行结果

| 情况 | 结果 |
|---|---|
| `admin` 超级管理员存在 | 密码重置为 `admin`，输出重置成功提示 |
| `admin` 不存在 | 不做任何改动，提示先执行 `bomiot initadmin` |

## 注意事项

- 该命令直接操作数据库，无需服务处于运行状态
- 初始密码是公开默认值，重置后**必须第一时间登录修改**；未改密前不要将服务暴露到公网
- 重置会覆盖现有密码，且没有任何确认提示——确认目标数据库无误后再执行
- 执行后会打印账号与初始密码提示，注意终端日志中不要长期留存该信息
