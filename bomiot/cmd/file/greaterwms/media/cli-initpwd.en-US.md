# bomiot initpwd

Reset the `admin` superuser's password to the initial value `admin`.

```bash
bomiot initpwd
```

## Overview

`bomiot initpwd` is the password-recovery command: it resets the `admin` superuser's password straight back to the initial password `admin`. It must be run from the **project root** and operates on the current project's database.

> **Difference from initadmin**: `initadmin` handles "the account is missing or in a broken state" — it creates the account, reactivates it and restores privileges, resetting the password along the way. `initpwd` does exactly one thing — **reset the password** — and requires the `admin` account to already exist. Both reset to the same initial password.

## Prerequisites

The `admin` superuser must already exist (usually created by `bomiot initadmin`). If it does not, the command prints "Please init one admin first" — run this instead:

```bash
bomiot initadmin
```

## Typical Scenarios

| Scenario | Action |
|---|---|
| Forgot the admin password | Run `bomiot initpwd`, log in with `admin` / `admin`, then change the password immediately |
| A former admin left and access must be reclaimed | Run `bomiot initpwd` to reset, then log in and adjust the account |
| Suspected admin password leak | Run `bomiot initpwd` to reset, then set a new password |

## Outcomes

| Situation | Result |
|---|---|
| `admin` superuser exists | Password is reset to `admin`, with a success message |
| `admin` does not exist | Nothing is changed; you are told to run `bomiot initadmin` first |

## Notes

- The command talks to the database directly; the server does not need to be running
- The initial password is a public default — **log in and change it right after resetting**; do not expose the service to the public internet before doing so
- The reset overwrites the current password without any confirmation prompt — make sure you are pointing at the right database first
- The command prints the account and initial password — avoid leaving this information in long-lived terminal logs
