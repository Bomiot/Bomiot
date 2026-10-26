# bomiot initadmin

Create (or reset) the project's superuser account `admin`.

```bash
bomiot initadmin
```

## Overview

`bomiot initadmin` ensures a superuser named `admin` exists in the database:

- **First run**: creates the `admin` account with an initial password identical to the username (`admin`), granted superuser and admin-site privileges
- **Already exists**: nothing is changed; it simply reports the account is ready
- **Exists but in a broken state** (deactivated, privileges removed): resets the password to the initial value and restores full privileges

The command must be run from the **project root** and operates on the current project's database.

## Prerequisites

Database tables must be ready. For a new project, run first:

```bash
bomiot migrate
bomiot initadmin
```

## Account Details

| Item | Value |
|---|---|
| Username | `admin` |
| Initial password | `admin` |
| Email | `admin@bomiot.com` |
| Privileges | Superuser (with admin-site access) |

> **The initial password is for temporary use only — change it immediately after logging in.** If the password is forgotten, re-run `bomiot initadmin` to reset it to the initial value (this also restores the active state and privileges), or use `bomiot initpwd` to change a password.

## Typical Scenarios

| Scenario | Action |
|---|---|
| First login on a new project | `bomiot migrate` → `bomiot initadmin` → log in with `admin` / `admin` |
| Forgot the admin password | Re-run `bomiot initadmin` — the password is reset to `admin` |
| admin deactivated or demoted by mistake | Re-run `bomiot initadmin` — restores the active state and full privileges |
| Delivering to production | Run it, then **log in and change the password right away** — never keep the initial password online |

## Notes

- The command talks to the database directly; the server does not need to be running
- The initial password is a public default that anyone reaching the login page can try — **do not expose the service to the public internet before changing it**
- Re-running is safe: an account in a healthy state is left untouched
- The command prints the account and initial password — avoid leaving this information in long-lived terminal logs
