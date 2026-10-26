# bomiot project

在当前项目的工作空间中创建一个新的**业务项目**（项目文件夹），包含运行所需的基础配置与模板。

```bash
bomiot project <name>
```

## 概述

Bomiot 采用"工作空间 + 业务项目"的多项目结构：`bomiot init` 初始化工作空间后，可以在其中创建多个相互独立的业务项目，每个项目有自己的配置、数据与代码。`bomiot project <name>` 在当前目录创建这样一个项目文件夹，并补齐运行所需的基础文件。

命令必须在**工作空间根目录**下执行。

## 参数

| 参数 | 说明 |
|---|---|
| `<name>` | 项目名称（必填）。作为项目文件夹名，需为合法的目录名 |

## 命名约束

以下情况会拒绝创建并提示原因：

| 情况 | 提示 |
|---|---|
| 未提供名称 | `Please enter your project name` |
| 名称为 `greaterwms`（保留名，与工作空间目录冲突） | `Project name "greaterwms" is reserved and cannot be used` |
| 同名目录已存在 | `Project directory already exists` |
| 与当前环境中已安装的 Python 包同名 | 拒绝创建（避免导入冲突） |

## 生成的内容

| 文件 / 目录 | 说明 |
|---|---|
| `<name>/` | 项目文件夹 |
| `<name>/__init__.py` | Python 包标识 |
| `<name>/bomiotconf.ini` | 项目级基础配置 |
| `<name>/templates/` | 项目模板目录（前端页面模板等） |
| 项目运行所需的其余基础文件 | 由模板自动补齐 |

## 典型流程

```bash
bomiot init              # 初始化工作空间
bomiot project erp       # 创建第一个业务项目
bomiot project oa        # 再创建一个，互不影响
bomiot run               # 启动（工作空间统一对外提供服务）
```

## 注意事项

- 项目名创建后即为文件夹名与项目标识，建议用小写字母、数字、下划线，避免空格与中文
- 创建失败（重名/保留名/包名冲突）不会写入任何文件，可放心重试
- 多个业务项目共用同一套运行服务，通过切换机制选择当前操作的项目（见"多项目切换"相关文档）
