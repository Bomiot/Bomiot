# Poetry Usage Guide

## Why Introduction Poetry

- **Bomiot** integrates Poetry and PyPI to implement an application marketplace and plugin modules, simplifying user environment setup and facilitating team collaboration.

---

## What is Poetry

**Poetry** is a modern Python dependency management and packaging tool. It helps you:
- Manage and lock dependencies (automatically generates `pyproject.toml` and `poetry.lock`)
- Create and manage virtual environments
- Build and publish Python packages

Poetry’s goal is to make Python project dependency management, packaging, and distribution simple, reliable, and consistent.

---

## Features of Poetry

- Supports PEP 517/518 (`pyproject.toml`-based)
- Automatic virtual environment management
- Precise dependency version locking
- Multi-Python version isolation
- Convenient package publishing workflow (e.g., PyPI)

---

## Installing Poetry

Recommended installation via the official script:

```bash
# Official recommended method
curl -sSL https://install.python-poetry.org | python3 -

# Or use pip (not recommended)
pip install poetry
```

After installation, verify the version:

```bash
poetry --version
```

---

## Basic Usage

### Creating a New Project

```bash
poetry new myproject
```
- This will create a directory named `myproject` with a standard project structure and an initial `pyproject.toml` file.

### Initializing Poetry in an Existing Project

```bash
cd your_existing_project
poetry init
```
- Interactive prompts will help you set up project metadata and dependencies, generating a `pyproject.toml`.

### Adding Dependencies

```bash
poetry add requests
poetry add flask@2.1.0     # Specify version
poetry add pytest --dev    # Add as a development dependency
```
- This automatically updates `pyproject.toml` and installs the dependencies.

### Removing Dependencies

```bash
poetry remove requests
```
- Removes and uninstalls the specified package from your project.

### Installing Dependencies

```bash
poetry install
```
- Installs all dependencies specified in `pyproject.toml` and `poetry.lock`.

### Updating Dependencies

```bash
poetry update
poetry update requests
```
- Updates all or specific dependencies to the latest compatible versions.

### Managing Virtual Environments

- Poetry automatically creates a virtual environment for each project.
- To activate the shell:

  ```bash
  poetry shell
  ```

- To run commands inside the virtual environment:

  ```bash
  poetry run python script.py
  poetry run pytest
  ```

### Running Your Project

If you have defined scripts in `pyproject.toml`, you can run them directly:

```bash
poetry run my-script
```

### Building and Publishing Packages

- Build your project:

  ```bash
  poetry build
  ```

- Publish to PyPI:

  ```bash
  poetry publish
  # You may need to set your token: poetry config pypi-token.pypi your_token
  ```

---

## Common Commands Cheat Sheet

| Command                          | Description                               |
|-----------------------------------|-------------------------------------------|
| poetry new <project_name>         | Create a new project                      |
| poetry init                      | Initialize Poetry in an existing project  |
| poetry add <package>             | Add a dependency                          |
| poetry add <package> --dev       | Add a development dependency              |
| poetry remove <package>          | Remove a dependency                       |
| poetry install                   | Install dependencies                      |
| poetry update                    | Update dependencies                       |
| poetry shell                     | Activate the virtual environment          |
| poetry run <command>             | Run a command inside the virtual environment |
| poetry build                     | Build the project package                 |
| poetry publish                   | Publish to PyPI                           |

---

## Frequently Asked Questions

**Q1: How do I specify the Python version?**  
A: In the `[tool.poetry.dependencies]` section of `pyproject.toml`, add `python = "^3.9"`. Or use `poetry env use 3.9` to set the Python version for the virtual environment.

**Q2: How do I switch or locate the virtual environment path?**  
A: Use `poetry env list` to see all environments, and `poetry env info` for details on the current one.

**Q3: What if installation is slow or fails?**  
A: You can configure a mirror in `pyproject.toml` or set a repository with `poetry config repositories.xxx https://mirrors.aliyun.com/pypi/simple/`.

**Q4: How do I resolve dependency conflicts?**  
A: Try `poetry update`. If conflicts persist, you may need to manually adjust dependency versions.

---

## References

- [Poetry Official Documentation](https://python-poetry.org/docs/)
- [Poetry GitHub](https://github.com/python-poetry/poetry)
- [pyproject.toml Configuration](https://python-poetry.org/docs/pyproject/)

---

For more advanced usage (such as multi-environment management, plugin extensions, etc.), refer to the official documentation or community resources.