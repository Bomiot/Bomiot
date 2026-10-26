# bomiot app

Create a new **business app** in the current workspace, with the app skeleton generated and registration done for you.

```bash
bomiot app <name>
```

## Overview

An app is the smallest business unit in Bomiot: a project is composed of apps, and each app carries a related set of features (models, APIs, pages, etc.). `bomiot app <name>` creates the app folder in the workspace, copies the standard app skeleton and completes app registration — you can start writing business code right away.

The command must be run from the **workspace root**.

## Parameters

| Parameter | Description |
|---|---|
| `<name>` | App name (required). Used as the app folder name; must be a valid directory name |

## Naming Rules

| Situation | Result |
|---|---|
| No name provided | `Please enter your app name` |
| Name is `bomiot` (reserved) | `Invalid app name` — creation rejected |
| An app directory with the same name exists | `App directory already exists` — creation rejected |

## Prerequisites

The workspace must be in **project mode** (`[mode] name = project` in `greaterwms/bomiotconf.ini`). Workspaces created by `bomiot init` default to project mode; if you see `Invalid project mode`, check that config or switch mode per the multi-project documentation.

## After Creation

The app skeleton ships with the standard directory and file structure (models, routes, config, etc.) and the app is registered. Then:

1. Write models and business code in the app
2. `bomiot makemigrations` to generate database migrations
3. `bomiot migrate` to apply them
4. `bomiot run` to start and verify

## Typical Flow

```bash
bomiot init              # initialize the workspace
bomiot app goods         # create the goods app
bomiot app orders        # create the orders app
# write model code...
bomiot makemigrations    # generate migrations
bomiot migrate           # apply migrations
bomiot run               # start
```

## Notes

- The name becomes both the folder name and the module identifier — stick to lowercase letters, digits and underscores; avoid spaces and non-ASCII characters
- A failed creation (duplicate/reserved/wrong mode) writes nothing, so retrying is safe
- There is no delete command — removing an app means deleting its folder and cleaning up related registrations and migration records manually
