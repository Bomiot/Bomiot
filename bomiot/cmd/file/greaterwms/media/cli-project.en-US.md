# bomiot project

Create a new **business project** (project folder) inside the current workspace, with the base config and templates it needs to run.

```bash
bomiot project <name>
```

## Overview

Bomiot follows a "workspace + business projects" structure: after `bomiot init` initializes the workspace, you can create multiple independent business projects inside it — each with its own config, data and code. `bomiot project <name>` creates one such project folder in the current directory and fills in its base files.

The command must be run from the **workspace root**.

## Parameters

| Parameter | Description |
|---|---|
| `<name>` | Project name (required). Used as the project folder name; must be a valid directory name |

## Naming Rules

Creation is rejected, with the reason printed, in these cases:

| Situation | Message |
|---|---|
| No name provided | `Please enter your project name` |
| Name is `greaterwms` (reserved, conflicts with the workspace directory) | `Project name "greaterwms" is reserved and cannot be used` |
| A directory with the same name already exists | `Project directory already exists` |
| Name collides with an installed Python package in the environment | Rejected (to avoid import conflicts) |

## Generated Content

| File / Directory | Description |
|---|---|
| `<name>/` | The project folder |
| `<name>/__init__.py` | Python package marker |
| `<name>/bomiotconf.ini` | Project-level base configuration |
| `<name>/templates/` | Project template directory (frontend page templates, etc.) |
| Remaining base files | Filled in automatically from templates |

## Typical Flow

```bash
bomiot init              # initialize the workspace
bomiot project erp       # create the first business project
bomiot project oa        # create another — they do not affect each other
bomiot run               # start (the workspace serves them uniformly)
```

## Notes

- The name becomes both the folder name and the project identifier — stick to lowercase letters, digits and underscores; avoid spaces and non-ASCII characters
- A failed creation (duplicate/reserved/package collision) writes nothing, so retrying is safe
- Multiple business projects share the same runtime; use the project-switch mechanism to choose the active one (see the "Multi-Project" documentation)
