"""
Scan WORKING_SPACE/greaterwms/<subpkg> for apps.py and emit apps.json.
WORKING_SPACE aligns with bomiot settings.py logic.
Run before `bomiot run` (dev) or before Nuitka packaging (CI).

Usage:
    python discovered_apps.py [--out apps.json]
"""
import argparse
import os
import sys
import orjson
from pathlib import Path

def discover(working_space):
    apps = []
    p = Path(working_space) / "greaterwms"
    if not p.is_dir():
        return apps
    for entry in sorted(p.iterdir()):
        if entry.is_dir() and (entry / "apps.py").exists():
            apps.append(f"greaterwms.{entry.name}")
    return apps

def main(working_space, argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="apps.json")
    # argv=None falls back to sys.argv for standalone use; callers inside the
    # CLI must pass [] to avoid parsing the outer command line.
    args, _ = ap.parse_known_args(argv)

    apps = discover(working_space)
    out_path = Path(working_space) / args.out
    out_path.write_bytes(orjson.dumps(apps, option=orjson.OPT_INDENT_2))