# bomiot api

Create a new **API app** in the current workspace with a ready-to-use, full CRUD interface skeleton.

```bash
bomiot api <name>
```

## Overview

Like `bomiot app`, `bomiot api <name>` creates an app folder and registers it — but the skeleton differs: **api generates a complete CRUD template** with models, serializers, filters, views and routes all wired up, giving you a working set of RESTful endpoints the moment it is created. Use it to stand up data interfaces fast; use `bomiot app` when you prefer a blank skeleton to fill in yourself.

The command must be run from the **workspace root**, and the workspace must be in project mode.

## Parameters

| Parameter | Description |
|---|---|
| `<name>` | App name (required). Used as the app folder name and the endpoint path prefix; must be a valid directory name |

## Naming Rules

| Situation | Result |
|---|---|
| No name provided | `Please enter your app name` |
| Name is `bomiot` (reserved) | `Invalid app name` — creation rejected |
| An app directory with the same name exists | `App directory already exists` — creation rejected |

## Generated Content

| File | Description |
|---|---|
| `models.py` | Example data model |
| `serializers.py` | Serializers |
| `filter.py` | Query filters |
| `views.py` | CRUD views |
| `urls.py` | Route registration (paths prefixed with the app name) |

All example identifiers in the skeleton are automatically replaced with your app name, so the endpoints are callable immediately.

## api vs app

| | `bomiot app` | `bomiot api` |
|---|---|---|
| Skeleton | Basic directory structure | Full CRUD interface template |
| Best for | Building custom features from scratch | Producing callable data endpoints fast |
| After creation | You write models and interfaces yourself | Example endpoints included — adapt the model and go |

## Typical Flow

```bash
bomiot api goods         # create the goods API app
# adapt the example model in models.py
bomiot makemigrations    # generate migrations
bomiot migrate           # apply migrations
bomiot run               # start — the goods endpoints are live
```

## Notes

- The example model is only a starting point — after adapting it to your business, **always run the migrations**, otherwise the endpoints will operate on tables that do not exist
- Same naming advice as `bomiot app`: lowercase letters, digits and underscores
- A failed creation (duplicate/reserved/wrong mode) writes nothing, so retrying is safe
- There is no delete command — removing an app means deleting its folder and cleaning up registrations and migration records manually
