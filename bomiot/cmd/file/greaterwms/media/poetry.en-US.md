# Poetry in Depth

## Why Poetry Is Covered Here

- **Bomiot** combines Poetry with PyPI to power its app marketplace and plugin modules, making environment setup and team collaboration easier.

## What Is Poetry

**Poetry** is a Python dependency-management and packaging tool that drives a project's metadata, dependencies, and build from a single `pyproject.toml`:

- Declare and lock dependencies (auto-generated `poetry.lock` guarantees identical installs on every machine)
- Create and manage virtual environments automatically
- Build and publish Python packages with one command

---

## Installation

A standalone install is recommended (isolated from your project environments and global pip):

```bash
# macOS / Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Verify the installation:

```bash
poetry --version
```

Avoid `pip install poetry` — it dumps Poetry's own dependencies into the global environment, where they can conflict with your projects.

---

## Project Setup

```bash
# New project: generates the standard layout and pyproject.toml
poetry new myproject

# Existing project: fill in pyproject.toml interactively
cd myproject
poetry init
```

Key fields of the generated `pyproject.toml`:

```toml
[tool.poetry]
name = "myproject"
version = "0.1.0"
description = ""
authors = ["your name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Managing Dependencies

```bash
poetry add requests            # add a runtime dependency
poetry add "flask>=2.0,<3.0"   # with a version range
poetry add pytest --group dev  # add a dev-only dependency
poetry remove requests         # remove a dependency
poetry install                 # install everything per the lock file
poetry install --without dev   # runtime dependencies only (for deployment)
poetry update                  # upgrade all dependencies within constraints, refresh lock
poetry update requests         # upgrade one dependency
poetry show --tree             # inspect the dependency tree
```

Version constraint syntax:

| Syntax | Meaning |
|---|---|
| `^2.31` | Allow upgrades within 2.x (>=2.31, <3.0) |
| `~2.31` | Patch upgrades only (>=2.31, <2.32) |
| `2.31.*` | Wildcard, equivalent to ~2.31 |
| `==2.31.0` | Pin to an exact version |
| `>=2.0,<3.0` | Range expression |

## Virtual Environments

Poetry creates an isolated environment per project automatically. Common operations:

```bash
poetry run python main.py   # run a command inside the project environment
poetry run pytest
poetry env info             # show the current environment's path and details
poetry env list             # list all environments for the project
poetry env use 3.11         # switch the environment's Python version
poetry env remove 3.11      # delete an environment
```

Two useful settings:

```bash
# Create .venv inside the project directory (IDE-friendly, recommended)
poetry config virtualenvs.in-project true

# Inspect / change global configuration
poetry config --list
```

> Since Poetry 2.0, `poetry shell` has moved to the separate `poetry-plugin-shell` plugin. Prefer `poetry run <command>` for daily use — no need to enter the environment at all.

## Build and Publish

```bash
poetry build                              # build sdist and wheel (output to dist/)
poetry config pypi-token.pypi <token>     # configure the PyPI token (once)
poetry publish                            # publish to PyPI
poetry publish --build                    # build and publish in one step
```

## Command Cheat Sheet

| Command | Purpose |
|---|---|
| `poetry new <name>` | Create a new project |
| `poetry init` | Initialize an existing project |
| `poetry add <pkg>` | Add a dependency |
| `poetry add <pkg> --group dev` | Add a dev dependency |
| `poetry remove <pkg>` | Remove a dependency |
| `poetry install` | Install dependencies (per lock) |
| `poetry update` | Upgrade dependencies, refresh lock |
| `poetry lock` | Regenerate the lock file |
| `poetry run <cmd>` | Run inside the project environment |
| `poetry env use <version>` | Switch the environment's Python |
| `poetry build` / `publish` | Build / publish the package |

## Notes

- Always commit `poetry.lock` — it is what keeps teammates and servers on identical versions.
- After pulling someone else's project, the first command is always `poetry install`, which reproduces the environment exactly from the lock file.
- Add new dependencies with `poetry add`; if you edit `pyproject.toml` by hand, don't forget to run `poetry lock` afterwards.
