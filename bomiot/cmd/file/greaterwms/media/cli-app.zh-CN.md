# bomiot app

在当前工作空间中创建一个新的**业务应用**（app），自动生成应用骨架与注册配置。

```bash
bomiot app <name>
```

## 概述

应用是 Bomiot 中的最小业务单元：一个项目由多个应用组成，每个应用承载一组相关的功能（模型、接口、页面等）。`bomiot app <name>` 在工作空间下创建应用文件夹，复制标准应用骨架，并完成应用注册，创建后即可开始编写业务代码。

命令必须在**工作空间根目录**下执行。

## 参数

| 参数 | 说明 |
|---|---|
| `<name>` | 应用名称（必填）。作为应用文件夹名，需为合法的目录名 |

## 命名约束

| 情况 | 结果 |
|---|---|
| 未提供名称 | 提示 `Please enter your app name` |
| 名称为 `bomiot`（保留名） | 提示 `Invalid app name`，拒绝创建 |
| 同名应用目录已存在 | 提示 `App directory already exists`，拒绝创建 |

## 使用前提

当前工作空间处于**项目模式**（`greaterwms/bomiotconf.ini` 中 `[mode] name = project`）。通常 `bomiot init` 初始化的工作空间默认即为项目模式；若提示 `Invalid project mode`，请检查该配置或参考多项目切换文档切换模式。

## 创建后

应用骨架包含标准的目录与文件结构（模型、路由、配置等），并完成应用注册。随后即可：

1. 在应用中编写模型（Models）与业务代码
2. `bomiot makemigrations` 生成数据库迁移
3. `bomiot migrate` 应用迁移
4. `bomiot run` 启动查看效果

## 典型流程

```bash
bomiot init              # 初始化工作空间
bomiot app goods         # 创建商品应用
bomiot app orders        # 创建订单应用
# 编写模型代码……
bomiot makemigrations    # 生成迁移
bomiot migrate           # 应用迁移
bomiot run               # 启动
```

## 注意事项

- 应用名创建后即为文件夹名与模块标识，建议用小写字母、数字、下划线，避免空格与中文
- 创建失败（重名/保留名/模式不对）不会写入任何文件，可放心重试
- 删除应用需手动移除文件夹并清理相关注册与迁移记录，没有对应的删除命令
