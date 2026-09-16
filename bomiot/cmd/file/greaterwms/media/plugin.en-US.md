# Plugin Development

## Introduction

Bomiot supports a plugin architecture. Developers can package functionality as standalone plugins that are auto hot-imported after `pip` installation — no changes to the main project required. Plugins can be published to the app marketplace with revenue sharing.

---

## Create a Plugin

```bash
bomiot plugins my-plugin
```

This generates the basic plugin directory structure.

---

## Plugin Structure

```
my-plugin/
├── my_plugin/           # Plugin package
│   ├── __init__.py
│   ├── apps.py          # App config
│   ├── models.py        # Models (optional)
│   ├── views.py         # Views (optional)
│   ├── urls.py          # Routes (optional)
│   └── ...
├── setup.py             # Packaging config
└── README.md
```

---

## Install a Plugin

Plugins are installed via `pip`; Bomiot auto-discovers and hot-imports them:

```bash
pip install my-plugin
# or
poetry add my-plugin
```

> Plugins are auto hot-imported — no service restart needed, just refresh the page.

---

## App Marketplace

Browse and install plugins through the marketplace:

```bash
bomiot market <project_name>
```

---

## Development Guidelines

1. **Auto route mounting**: A plugin's `urls.py` is scanned and mounted under the `/<plugin_name>/` prefix
2. **Model migrations**: Run `bomiot makemigrations` and `bomiot migrate` for plugin models
3. **Signal integration**: Plugins can interact with the main project via `bomiot_signals`
4. **Frontend extension**: Plugins can include frontend pages injected into the main app

---

## Publish a Plugin

1. Fill in package name, version, dependencies in `setup.py`
2. Build and upload to PyPI or a private repository
3. List in the marketplace with a revenue share (up to 70%)

```bash
# Build
python setup.py sdist bdist_wheel

# Upload
twine upload dist/*
```

---

## Notes

- Avoid plugin names that conflict with existing apps in the main project
- Declare all dependencies in `setup.py`
- Provide i18n support (`language/` directory)
- Use code protection for sensitive modules (see Code Protection doc)
