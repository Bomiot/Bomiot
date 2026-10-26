# build

`bomiot build` is Bomiot's one-command build tool. It compiles the current project into a **standalone, distributable application** — the output runs on target machines with no Python installation required — and generates the manifest file needed for incremental updates.

## Prerequisites

Run the command from the **project root directory**, and make sure these files exist:

| File | Required | Description |
|---|---|---|
| `launcher.py` | Yes | Project entry point. Must define the variables `app_name`, `version` and `base_url` |
| `setup.ini` | Yes | Project config file. The `debug` value in its `[debug]` section affects macOS build output (see "Platform Differences") |
| `builder.toml` | No | Extra build configuration to append additional packages, modules or data files beyond the default scope |

## Usage

```bash
bomiot build
```

No arguments are needed. The command automatically detects the current operating system and CPU architecture, then runs the full build pipeline.

## Build Pipeline

The build proceeds through the following stages, each logging with a `[builder]` prefix in the terminal:

1. **Key preparation** — prepares the authorization keys for this build and embeds them into the output
2. **Project metadata** — reads the app name, version and update URL from `launcher.py`
3. **Runtime normalization** — pins the worker process count to 1 so packaged builds behave consistently
4. **App manifest** — scans the project and generates `apps.json`
5. **Platform detection** — determines the OS (Windows / macOS / Linux) and architecture (x64 / arm64)
6. **Compilation** — invokes the compiler for standalone packaging, streaming logs in real time
7. **Output finalization** — stops leftover background processes, renames the output directory to the standard format, and writes the authorization file
8. **Update manifest** — hashes all output files into a manifest for incremental updates

When finished, the terminal prints the output directory and total elapsed time.

## Build Output

All artifacts are placed under `build/` in the project root:

| Output | Description |
|---|---|
| `build/{app_name}-{version}-{OS}/` | Complete distributable directory — copy it to a target machine and run |
| `build/manifest-{os}-{arch}.json` | Incremental update manifest; the update service uses it to decide which files to download |

## CI Environments

When running in CI such as GitHub Actions, the command automatically switches to CI mode and reads build information from environment variables:

| Variable | Required | Description |
|---|---|---|
| `COMMUNITY_KEY` | Yes | Authorization key, injected by the CI pipeline |
| `SPONSOR_KEY` | Yes | Authorization key, injected by the CI pipeline |
| `APP_NAME` / `BASE_VERSION` | No | When both are set, they override the app name and version from `launcher.py` |
| `BASE_URL` | No | Update URL injected alongside the two variables above |

If the required key variables are missing in CI, the build **fails immediately** so the pipeline turns red right away.

## Platform Differences

| Behavior | Windows | macOS |
|---|---|---|
| Console window | The build always ships console capability; at runtime the console is shown or hidden based on the `debug` value in `setup.ini` — **config changes take effect immediately** | Determined at build time by the `debug` value in `setup.ini`: `True` shows a console window on launch, `False` builds without one. **A rebuild is required after changing it** |
| Parallel compilation | Automatically scaled to the local CPU count | Same locally; CI runners use a higher fixed parallelism to speed up builds |

## builder.toml (Optional)

The build includes everything the project needs at runtime by default. When your project pulls in extra third-party packages or data files, or you need to exclude certain files, create `builder.toml` in the project root and configure it under the `[build]` section. Every option is **merged on top of the defaults** (entries duplicating the defaults are ignored) — there is no need to restate the default scope.

### Options

```toml
[build]
# Extra Python packages to bundle (whole packages)
include_packages = ["my_package"]

# Extra in-package data files to bundle (templates, static assets, locales, etc.)
include_package_data = ["my_package"]

# Extra single Python modules to bundle
include_modules = ["my_module"]

# Packages whose imports are not followed during analysis — trims size and avoids false bundling
nofollow_import_to = ["some_package.tests"]

# Extra single files to copy, in "source=destination" format
# Source is relative to the project root; destination is relative to the output directory
include_data_files = ["logo.png=logo.png"]

# Extra directories to copy, same "source=destination" format
include_data_dirs = ["assets=assets"]

# Files to exclude from the output; wildcards supported
noinclude_data_files = ["*.map", "docs/**/*"]
```

### Notes

- All options are arrays; omitting or leaving them empty means only the default scope is used
- `include_data_files` and `include_data_dirs` must use the `source=destination` format
- In exclusion patterns, `*` does not match directory separators — write each level explicitly (e.g. `docs/*` and `docs/**/*`)
- A bad entry (e.g. a missing path) does not abort the build, but the content will be absent from the output — check the output directory after building
