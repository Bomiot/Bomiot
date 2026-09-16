# 插件开发

## 简介

Bomiot 支持插件化架构，开发者可以将功能封装为独立插件，通过 `pip` 安装后自动热导入，无需修改主项目代码。插件可上架应用市场并实现收益分成。

---

## 创建插件

```bash
bomiot plugins my-plugin
```

该命令会生成插件的基础目录结构。

---

## 插件结构

```
my-plugin/
├── my_plugin/           # 插件包
│   ├── __init__.py
│   ├── apps.py          # 应用配置
│   ├── models.py        # 数据模型（可选）
│   ├── views.py         # 视图（可选）
│   ├── urls.py          # 路由（可选）
│   └── ...
├── setup.py             # 打包配置
└── README.md
```

---

## 安装插件

插件通过 `pip` 安装，安装后 Bomiot 会自动发现并热导入：

```bash
pip install my-plugin
# 或
poetry add my-plugin
```

> 插件是自动热导入的，安装后无需重启服务，刷新页面即可生效。

---

## 应用市场

通过应用市场命令浏览和安装插件：

```bash
bomiot market <project_name>
```

---

## 插件开发规范

1. **路由自动挂载**：插件的 `urls.py` 会被自动扫描并挂载到 `/<插件名>/` 前缀下
2. **模型迁移**：插件中的模型需要执行 `bomiot makemigrations` 和 `bomiot migrate`
3. **信号集成**：插件可通过 `bomiot_signals` 与主项目交互
4. **前端扩展**：插件可包含前端页面，通过路由注入到主前端

---

## 发布插件

1. 完善 `setup.py` 中的包名、版本、依赖等信息
2. 打包并上传到 PyPI 或私有仓库
3. 在应用市场中上架，设置分成比例（最高可达 70%）

```bash
# 打包
python setup.py sdist bdist_wheel

# 上传
twine upload dist/*
```

---

## 注意事项

- 插件名应避免与主项目已有应用冲突
- 插件依赖需在 `setup.py` 中明确声明
- 建议为插件提供多语言支持（`language/` 目录）
- 敏感模块建议使用代码保护（见「代码保护」文档）
