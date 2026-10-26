import os, sys, json, hashlib, fnmatch, platform, subprocess, tempfile, shutil, time
from pathlib import Path
from time import sleep
import urllib.request
import urllib.error
import uvicorn
import socket
import webbrowser
import threading
import requests
from os.path import join
from bomiot_token import encrypt_info
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


app_name = "GreaterWMS"
version = "3.0.0"
port = 8008
base_url = "http://127.0.0.1:8000/"
update_url = f"{base_url.rstrip('/')}/update/"


def _find_available_port(start_port, max_tries=100):
    """Find available port starting from start_port, try at most max_tries times"""
    for p in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', p))
                return p
            except OSError:
                continue
    return start_port


# === Incremental auto-update logic (merged from auto_update.py) ===

# Block-level incremental update parameters
BLOCK_SIZE = 0.25 * 1024 * 1024          # each block is 0.25 MiB
BLOCK_THRESHOLD = 1 * 1024 * 1024  # enable block mode for files >= 1 MiB


def _detect_platform():
    """Detect the current platform, return (os_str, arch_str, platform_display)"""
    if sys.platform == "win32":
        _os = "windows"
        _display = "Windows"
    elif sys.platform == "darwin":
        _os = "macos"
        _display = "macOS"
    else:
        _os = "linux"
        _display = "Linux"
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        _arch = "arm64"
    elif machine.startswith("armv"):
        _arch = "armv7"
    else:
        _arch = "x64"
    return _os, _arch, _display


def _app_dir():
    """Return the directory where launcher resides (launcher.dist/)"""
    return os.path.dirname(sys.executable)


def _apply_console_mode():
    """Show or hide the console window based on setup.ini [debug] debug.
    debug=True  -> keep the console visible (force)
    debug=False -> hide the console window (disable)
    """
    if sys.platform != "win32":
        return
    try:
        import configparser
        base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
        parser = configparser.ConfigParser()
        parser.read(os.path.join(base_dir, "setup.ini"), encoding="utf-8")
        if parser.getboolean("debug", "debug", fallback=True):
            return
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            # SW_HIDE = 0
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except Exception:
        pass



def _read_gitignore(app_dir):
    """Read the .gitignore rule list"""
    patterns = []
    gi = os.path.join(app_dir, ".gitignore")
    if not os.path.exists(gi):
        return patterns
    with open(gi, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def _is_ignored(rel_path, patterns):
    """Check whether a file matches any .gitignore rule."""
    if "node_modules" in rel_path.split("/"):
        return True
    basename = os.path.basename(rel_path)
    for pat in patterns:
        if fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(basename, pat):
            return True
        if pat.endswith("/"):
            d = pat.rstrip("/")
            if rel_path.startswith(d + "/") or ("/" + d + "/") in rel_path:
                return True
    return False


def _sha256_file(path):
    """Compute the SHA256 of a single file"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_blocks(path, block_size=BLOCK_SIZE):
    """Split a file into blocks and return per-block SHA256 hashes."""
    hashes = []
    with open(path, "rb") as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            hashes.append(hashlib.sha256(chunk).hexdigest())
    return hashes


def _is_block_entry(val):
    """Whether a manifest entry is in block-level format."""
    return isinstance(val, dict) and isinstance(val.get("blocks"), list) and "sha256" in val


def _entry_sha256(val):
    """Get the overall SHA256 from a manifest entry."""
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return val.get("sha256")
    return None


def _download(url, dest, max_retries=3):
    """Download a file to the given path, with retries"""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GreaterWMS-Updater"})
            with urllib.request.urlopen(req, timeout=60) as resp, open(dest, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            return
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                sleep(1 * attempt)
    raise last_err


def _download_range(url, dest, byte_start, byte_end, max_retries=3):
    """Download byte range via HTTP Range, write to dest at given offset."""
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "GreaterWMS-Updater",
                    "Range": f"bytes={byte_start}-{byte_end}",
                },
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                status = getattr(resp, "status", 200)
                if status == 206:
                    with open(dest, "r+b") as f:
                        f.seek(byte_start)
                        while True:
                            chunk = resp.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                    return True
                else:
                    with open(dest, "wb") as f:
                        while True:
                            chunk = resp.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                    return False
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                sleep(1 * attempt)
    raise last_err


def _fetch_manifest(base_url, app_name, manifest_name, max_retries=3):
    """POST to /update/manifest/ and parse the manifest JSON, with retries."""
    endpoint = f"{base_url.rstrip('/')}/update/manifest/"
    payload = json.dumps({"app_name": app_name, "manifest": manifest_name}).encode("utf-8")
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers={
                    "User-Agent": "GreaterWMS-Updater",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = getattr(resp, "status", 200)
                if status < 200 or status >= 300:
                    raise RuntimeError(f"HTTP {status}")
                raw = resp.read()
                if not raw or not raw.strip():
                    raise RuntimeError("empty response (0 bytes)")
                try:
                    data = json.loads(raw.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    snippet = raw[:200].decode("utf-8", errors="replace")
                    raise RuntimeError(f"non-JSON response: {snippet!r}") from e
                if not isinstance(data, dict):
                    raise RuntimeError(f"manifest is not an object, got {type(data).__name__}")
                missing = [k for k in ("app_name", "version", "files") if k not in data]
                if missing:
                    raise RuntimeError(f"missing required fields: {missing}")
                if not isinstance(data["files"], dict):
                    raise RuntimeError(f"'files' field is not an object, got {type(data['files']).__name__}")
                return data
        except Exception as e:
            last_err = e
            print(f"[Update] Fetch manifest attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                sleep(1 * attempt)
    raise last_err


def _can_reach_server(update_url, timeout=16.0):
    """Quick pre-check: use raw socket to judge whether host:port is reachable."""
    try:
        from urllib.parse import urlparse
        u = urlparse(update_url if update_url.endswith("/") else update_url + "/")
        host = u.hostname
        if not host:
            return True
        if u.scheme == "https":
            port = u.port or 443
        elif u.scheme == "http":
            port = u.port or 80
        else:
            return True
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.gaierror, socket.timeout, TimeoutError,
            ConnectionRefusedError, OSError):
        return False
    except Exception:
        return True


def _url_head_ok(url, timeout=5.0, max_retries=2):
    """Lightweight HTTP HEAD probe to verify remote version directory exists."""
    last_reason = ""
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                url, method="HEAD", headers={"User-Agent": "GreaterWMS-Updater"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = getattr(resp, "status", 200)
                if 200 <= status < 300:
                    return True, f"HTTP {status}"
                last_reason = f"HTTP {status}"
        except urllib.error.HTTPError as e:
            last_reason = f"HTTP {e.code}"
            if e.code == 404:
                return False, last_reason
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_reason = f"{type(e).__name__}"
        except Exception as e:
            last_reason = f"{type(e).__name__}: {str(e)[:40]}"
        if attempt < max_retries:
            sleep(1)
    return False, last_reason


def _generate_update_script(app_dir, temp_dir, to_delete, manifest_name=None,
                           new_exe_path=None):
    """Generate the update script (update.bat / update.sh) and return its path."""
    is_win = sys.platform == "win32"
    exe_name = os.path.basename(sys.executable)
    exe_path = sys.executable
    target_exe_path = new_exe_path if new_exe_path and os.path.isabs(new_exe_path) else exe_path
    target_exe_name = os.path.basename(target_exe_path)

    crash_log = os.path.join(app_dir, "update_crash.log")
    if is_win:
        script_path = os.path.join(app_dir, "update.bat")
        lines = ["@echo off"]
        lines.append(f':wait')
        lines.append(f'tasklist /fi "imagename eq {exe_name}" >"%TEMP%\\_bomiot_wait.tmp" 2>nul')
        lines.append(f'find /i "{exe_name}" "%TEMP%\\_bomiot_wait.tmp" >nul 2>nul')
        lines.append(f'if not errorlevel 1 ( del "%TEMP%\\_bomiot_wait.tmp" >nul 2>nul & ping -n 2 127.0.0.1 >nul 2>nul & goto wait )')
        lines.append(f'del "%TEMP%\\_bomiot_wait.tmp" >nul 2>nul')
        lines.append(f'xcopy /Y /S /E /I /H "{temp_dir}" "{app_dir}" >"%TEMP%\\_bomiot_xcopy.log" 2>&1')
        lines.append(f'if errorlevel 1 goto copyfail')
        lines.append(f'del "%TEMP%\\_bomiot_xcopy.log" >nul 2>nul')
        lines.append(f'goto copyok')
        lines.append(f':copyfail')
        lines.append(f'echo [Update] xcopy failed ^(errorlevel^>^=1^), update aborted. >> "{crash_log}"')
        lines.append(f'type "%TEMP%\\_bomiot_xcopy.log" >> "{crash_log}" 2>nul')
        lines.append(f'del "%TEMP%\\_bomiot_xcopy.log" >nul 2>nul')
        lines.append(f'exit /b 1')
        lines.append(f':copyok')
        if manifest_name:
            lines.append(f'copy /Y "{os.path.join(temp_dir, manifest_name)}" "{os.path.join(app_dir, manifest_name)}" >nul 2>nul')
        lines.append(f'rd /S /Q "{temp_dir}" 2>nul')
        for f in to_delete:
            lines.append(f'del /F /Q "{os.path.join(app_dir, f)}" 2>nul')
        lines.append(f'start "" /MIN "{target_exe_path}"')
        if target_exe_name.lower() != exe_name.lower():
            lines.append(f'ping -n 4 127.0.0.1 >nul 2>nul')
            lines.append(f'del /F /Q "{exe_path}" 2>nul')
        lines.append(f'del "%~f0"')
        with open(script_path, "w", encoding="utf-8") as f:
            f.write("\r\n".join(lines))
    else:
        script_path = os.path.join(app_dir, "update.sh")
        lines = ["#!/bin/bash"]
        lines.append(f'while pgrep -f "{exe_path}" > /dev/null 2>&1; do sleep 1; done')
        lines.append(f'if ! cp -rf "{temp_dir}"/. "{app_dir}"/ 2>> "{crash_log}"; then')
        lines.append(f'    echo "[Update] cp failed, update aborted." >> "{crash_log}"')
        lines.append(f'    exit 1')
        lines.append(f'fi')
        if manifest_name:
            lines.append(f'cp -f "{os.path.join(temp_dir, manifest_name)}" "{os.path.join(app_dir, manifest_name)}" 2>/dev/null')
        lines.append(f'rm -rf "{temp_dir}"')
        for f in to_delete:
            lines.append(f'rm -f "{os.path.join(app_dir, f)}"')
        lines.append(f'nohup "{target_exe_path}" > /dev/null 2>&1 &')
        if target_exe_name.lower() != exe_name.lower():
            lines.append(f'sleep 3')
            lines.append(f'rm -f "{exe_path}" 2>/dev/null')
        lines.append(f'rm -- "$0"')
        with open(script_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        os.chmod(script_path, 0o755)

    return script_path


def check_update(app_name, version, status_label=None, progress_bar=None):
    """
    Check and apply the incremental update.

    Returns True if an update was triggered (caller should exit), False if no update needed.
    """
    app_dir = _app_dir()
    if not update_url or not update_url.strip():
        print("[Update] update_url is empty, update check skipped")
        return False
    _os, _arch, _display = _detect_platform()
    manifest_name = f"manifest--{app_name}-{_os}-{_arch}.json"
    print(f"[Update] Detected platform: {_os} {_arch} ({_display})")
    print(f"[Update] Manifest file name: {manifest_name}")
    print(f"[Update] Manifest URL: {update_url}{manifest_name}")

    # Read local manifest
    local_manifest_path = os.path.join(app_dir, manifest_name)
    if not os.path.exists(local_manifest_path):
        return False
    try:
        with open(local_manifest_path, encoding="utf-8") as f:
            local_manifest = json.load(f)
    except Exception:
        return False

    ignore_patterns = _read_gitignore(app_dir)

    # Quick network pre-check
    if status_label:
        status_label.config(text="Checking for updates...")
        status_label.update()
    if not _can_reach_server(update_url, timeout=16.0):
        err_msg = "Update check failed: network unreachable, skipping"
        print(f"[Update] {err_msg} (server unreachable, pre-check 2s)")
        if status_label:
            status_label.config(text=err_msg)
            status_label.update()
        return False

    # POST to update_url to get manifest summary {app_name, version, os, arch}
    print(f"[Update] Fetching manifest summary: POST {update_url}")
    try:
        _payload = json.dumps({"app_name": app_name, "manifest": manifest_name}).encode("utf-8")
        _req = urllib.request.Request(
            update_url,
            data=_payload,
            headers={
                "User-Agent": "GreaterWMS-Updater",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(_req, timeout=5) as _resp:
            _raw = _resp.read()
            if not _raw or not _raw.strip():
                print("[Update] Empty summary response, skipping update")
                return False
            remote_summary = json.loads(_raw.decode("utf-8"))
    except Exception as e:
        print(f"[Update] Failed to fetch manifest summary: {e}")
        if status_label:
            status_label.config(text="Update check failed, skipping")
            status_label.update()
        return False

    # Compare local vs remote summary
    local_summary = {
        "app_name": local_manifest.get("app_name", ""),
        "version": local_manifest.get("version", ""),
        "os": local_manifest.get("os", ""),
        "arch": local_manifest.get("arch", ""),
    }
    if local_summary == remote_summary:
        print(f"[Update] Summary matches (version {local_summary['version']}), skipping update")
        # Clean up leftover temp dir from a previous interrupted download
        _old_temp = os.path.join(tempfile.gettempdir(), f"bomiot_update_{app_name}")
        if os.path.isdir(_old_temp):
            shutil.rmtree(_old_temp, ignore_errors=True)
            print(f"[Update] cleaned up leftover temp dir: {_old_temp}")
        if progress_bar:
            progress_bar["value"] = 0
            progress_bar.update()
        if status_label:
            status_label.config(text="Already up to date")
            status_label.update()
        return False

    # Summary differs, fetch full manifest via POST /update/manifest/
    manifest_endpoint = f"{base_url.rstrip('/')}/update/manifest/"
    print(f"[Update] Summary differs, fetching full manifest: POST {manifest_endpoint}")
    try:
        _t0 = time.time()
        remote_manifest = _fetch_manifest(base_url, app_name, manifest_name, max_retries=3)
        _size_kb = len(json.dumps(remote_manifest, ensure_ascii=False)) / 1024
        _elapsed = time.time() - _t0
        print(f"[Update] Remote manifest downloaded: {_size_kb:.1f}KB ({_elapsed:.1f}s)")
    except Exception as e:
        print(f"[Update] Failed to fetch full manifest: {e}")
        if status_label:
            status_label.config(text="Update check failed, skipping")
            status_label.update()
        return False

    remote_version = remote_manifest.get("version", "0")
    remote_files = remote_manifest.get("files", {})
    file_base_url = f"{base_url.rstrip('/')}/update/download/{app_name}/{app_name}--{remote_version}-{_os}/"

    # Pre-probe: verify remote version directory exists
    if remote_files:
        _probe_path = next(iter(remote_files))
        _probe_url = file_base_url + _probe_path
        _ok, _reason = _url_head_ok(_probe_url, timeout=5.0, max_retries=2)
        if not _ok:
            if _reason == "HTTP 404":
                err_msg = f"Server version directory not found ({remote_version}), skipping update"
            else:
                err_msg = f"Update probe failed ({_reason}), skipping update"
            print(f"[Update] {err_msg} probe={_probe_url}")
            if status_label:
                status_label.config(text=err_msg)
                status_label.update()
            return False
        print(f"[Update] Remote version folder verified via HEAD: {_probe_path} ({_reason})")

    _local_ver = local_manifest.get("version", "?")
    if remote_version < version:
        _direction = "rollback"
    else:
        _direction = "upgrade"
    if status_label:
        status_label.config(text=f"New version {remote_version} found ({_direction}), updating...")
        status_label.update()
    if progress_bar:
        progress_bar["value"] = 0
        progress_bar.update()

    print(f"[Update] {_direction} needed: binary={version} local_manifest={_local_ver} remote={remote_version}")

    # Diff: dual-manifest intersection model
    to_download = []
    to_delete = []
    local_files = local_manifest.get("files") if isinstance(local_manifest, dict) else None
    if isinstance(local_files, dict):
        A_keys = set(remote_files.keys())
        B_keys = set(local_files.keys())
        # 1) A �?B: intersection, compare per file
        for rel in A_keys & B_keys:
            remote_entry = remote_files[rel]
            remote_hash = _entry_sha256(remote_entry)
            local_path = os.path.join(app_dir, rel.replace("/", os.sep))
            if not os.path.isfile(local_path):
                to_download.append({"path": rel})
                continue
            if _is_block_entry(remote_entry):
                remote_blocks = remote_entry["blocks"]
                block_size = remote_entry.get("block_size", BLOCK_SIZE)
                try:
                    local_blocks = _hash_blocks(local_path, block_size)
                except Exception:
                    local_blocks = []
                if (len(local_blocks) == len(remote_blocks)
                        and all(lb == rb for lb, rb in zip(local_blocks, remote_blocks))):
                    continue
                changed = [
                    i for i in range(len(remote_blocks))
                    if i >= len(local_blocks) or local_blocks[i] != remote_blocks[i]
                ]
                to_download.append({
                    "path": rel,
                    "blocks": changed,
                    "block_size": block_size,
                    "size": remote_entry.get("size"),
                    "sha256": remote_hash,
                })
            else:
                try:
                    local_hash = _sha256_file(local_path)
                except Exception:
                    local_hash = None
                if local_hash != remote_hash:
                    to_download.append({"path": rel})
        # 2) A �?B: remote new files
        for rel in A_keys - B_keys:
            to_download.append({"path": rel})
        # 3) B �?A: removed remotely �?to_delete
        protected_prefix = ("dbs/", "logs/", "__pycache__/")
        for rel in B_keys - A_keys:
            basename = os.path.basename(rel)
            if basename in ("update.bat", "update.sh", "manifest.json"):
                continue
            if basename.startswith("manifest-") and basename.endswith(".json"):
                continue
            rel_norm = rel.replace("\\", "/")
            skip_prefix = False
            for p in protected_prefix:
                if rel_norm.startswith(p) or ("/" + p).rstrip("/") + "/" in "/" + rel_norm:
                    skip_prefix = True
                    break
            if skip_prefix:
                continue
            if _is_ignored(rel_norm, ignore_patterns):
                continue
            local_path = os.path.join(app_dir, rel.replace("/", os.sep))
            if os.path.isfile(local_path):
                to_delete.append(rel)
    else:
        # Fallback: local manifest has no files �?one-way compare
        print("[Update] local manifest missing 'files', falling back to one-way compare (no delete)")
        for rel, remote_entry in remote_files.items():
            remote_hash = _entry_sha256(remote_entry)
            local_path = os.path.join(app_dir, rel.replace("/", os.sep))
            if not os.path.isfile(local_path):
                to_download.append({"path": rel})
                continue
            try:
                local_hash = _sha256_file(local_path)
            except Exception:
                local_hash = None
            if local_hash != remote_hash:
                to_download.append({"path": rel})

    print(f"[Update] diff stats: to_download={len(to_download)}  to_delete(B−A)={len(to_delete)}  "
          f"(remote.files={len(remote_files)}  local.files={len(local_files) if isinstance(local_files, dict) else 'N/A'})")

    if not to_download and not to_delete:
        return False

    # Download changed files into a fixed temp directory (supports resume)
    temp_dir = os.path.join(tempfile.gettempdir(), f"bomiot_update_{app_name}")
    os.makedirs(temp_dir, exist_ok=True)

    total_bytes = 0
    for item in to_download:
        blks = item.get("blocks")
        if blks:
            total_bytes += len(blks) * item.get("block_size", BLOCK_SIZE)
    downloaded_bytes = 0

    def _update_progress(extra_text=""):
        if not progress_bar:
            return
        pct = (downloaded_bytes / total_bytes * 100) if total_bytes > 0 else 0
        progress_bar["value"] = min(pct, 100)
        mb_done = downloaded_bytes / 1024 / 1024
        mb_total = total_bytes / 1024 / 1024
        if status_label:
            if extra_text:
                status_label.config(text=f"{extra_text}  {mb_done:.1f}MB / {mb_total:.1f}MB ({pct:.0f}%)")
            else:
                status_label.config(text=f"Downloading  {mb_done:.1f}MB / {mb_total:.1f}MB ({pct:.0f}%)")
            status_label.update()
        progress_bar.update()

    if progress_bar:
        progress_bar["value"] = 0
        progress_bar.update()
        _update_progress(f"Preparing to download {len(to_download)} files")

    for item in to_download:
        path = item["path"]
        url = file_base_url + path
        dest = os.path.join(temp_dir, path.replace("/", os.sep))
        try:
            blocks = item.get("blocks")
            if blocks:
                # Block-level incremental download with resume support
                block_size = item["block_size"]
                remote_size = item.get("size")
                remote_sha256 = item.get("sha256")

                # Check if file already fully downloaded (resume: skip)
                if os.path.isfile(dest):
                    try:
                        actual = _sha256_file(dest)
                    except Exception:
                        actual = None
                    if actual == remote_sha256:
                        print(f"[Update] resume skip (already complete): {path}")
                        downloaded_bytes += len(blocks) * block_size
                        _update_progress(f"Verifying {os.path.basename(path)}")
                        continue

                # Need to download: start from local copy (base file)
                local_path = os.path.join(app_dir, path.replace("/", os.sep))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                if not os.path.isfile(dest):
                    if os.path.isfile(local_path):
                        shutil.copyfile(local_path, dest)
                    else:
                        open(dest, "wb").close()

                # Download only changed blocks, skip already-correct ones
                range_ok = True
                for bi in blocks:
                    byte_start = bi * block_size
                    byte_end = min((bi + 1) * block_size, remote_size) - 1 if remote_size else byte_start + block_size - 1
                    ok = _download_range(url, dest, byte_start, byte_end)
                    if ok:
                        downloaded_bytes += block_size
                    else:
                        downloaded_bytes += remote_size if remote_size else block_size
                        range_ok = False
                        break
                    _update_progress(f"Downloading {os.path.basename(path)}")
                if range_ok:
                    try:
                        actual = _sha256_file(dest)
                    except Exception:
                        actual = None
                    if actual != remote_sha256:
                        print(f"[Update] block verify mismatch for {path}, falling back to full download")
                        _download(url, dest)
            else:
                # Full file download with resume support
                remote_sha256 = _entry_sha256(item)

                # Check if file already downloaded (resume: skip)
                if remote_sha256 and os.path.isfile(dest):
                    try:
                        actual = _sha256_file(dest)
                    except Exception:
                        actual = None
                    if actual == remote_sha256:
                        print(f"[Update] resume skip (already complete): {path}")
                        fsize = os.path.getsize(dest)
                        total_bytes += fsize
                        downloaded_bytes += fsize
                        _update_progress(f"Verifying {os.path.basename(path)}")
                        continue

                _download(url, dest)
                fsize = os.path.getsize(dest)
                total_bytes += fsize
                downloaded_bytes += fsize
                _update_progress(f"Downloading {os.path.basename(path)}")
        except Exception as e:
            print(f"Download failed: {path} - {e}")
            # Keep temp_dir for resume on next run (do NOT delete)
            if progress_bar:
                progress_bar["value"] = 0
                progress_bar.update()
            if status_label:
                status_label.config(text="Update download interrupted, will resume on next launch")
                status_label.update()
            return False

    if progress_bar:
        progress_bar["value"] = 100
        progress_bar.update()
    if status_label:
        status_label.config(text="Update download complete, applying...")
        status_label.update()

    # Write new-version manifest into temp_dir
    new_manifest_path = os.path.join(temp_dir, manifest_name)
    try:
        with open(new_manifest_path, "w", encoding="utf-8") as f:
            json.dump(remote_manifest, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Update] Warning: failed to write new manifest to temp: {e}")

    # Compute the absolute path of the new exe
    _plat_is_win = sys.platform == "win32"
    if _plat_is_win:
        new_exe_name = f"{app_name}.exe"
    else:
        new_exe_name = app_name
    new_exe_path = os.path.join(app_dir, new_exe_name)

    # Generate update script
    script_path = _generate_update_script(
        app_dir, temp_dir, to_delete,
        manifest_name=manifest_name,
        new_exe_path=new_exe_path,
    )

    # Start the script (silent)
    is_win = sys.platform == "win32"
    _started_script = False
    _script_err = ""
    try:
        if is_win:
            CREATE_NO_WINDOW          = int(getattr(subprocess, "CREATE_NO_WINDOW",          0x08000000))
            CREATE_NEW_PROCESS_GROUP  = int(getattr(subprocess, "CREATE_NEW_PROCESS_GROUP",  0x00000200))
            flags = CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
            startupinfo = subprocess.STARTUPINFO()
            try:
                startupinfo.dwFlags = int(getattr(subprocess, "STARTF_USESHOWWINDOW", 1))
            except Exception:
                startupinfo.dwFlags = 1
            startupinfo.wShowWindow = 0
            subprocess.Popen(
                ["cmd.exe", "/c", script_path],
                cwd=app_dir,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                shell=False,
                startupinfo=startupinfo,
                creationflags=flags,
            )
        else:
            subprocess.Popen(
                ["bash", script_path],
                cwd=app_dir,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                shell=False,
                start_new_session=True,
            )
        _started_script = True
    except Exception as e:
        import traceback as _tb
        _script_err = f"{type(e).__name__}: {e}\n{_tb.format_exc()}"
        print(f"[Update] FATAL: failed to start update script.\n{_script_err}")
        try:
            crash_log = os.path.join(app_dir, "update_crash.log")
            with open(crash_log, "a", encoding="utf-8") as f:
                f.write(f"===== {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
                f.write(f"script_path={script_path}\n")
                f.write(_script_err)
                f.write("\n")
        except Exception:
            pass

    if not _started_script:
        shutil.rmtree(temp_dir, ignore_errors=True)
        try:
            os.remove(script_path)
        except Exception:
            pass
        if status_label:
            status_label.config(text="Update script failed to start, skipping (see update_crash.log)")
            status_label.update()
        return False

    sleep(0.3)
    return True


if __name__ == "__main__":
    # Apply console visibility before anything else (reads setup.ini [debug] debug)
    _apply_console_mode()

    # Top-level safety net: write any uncaught exception to update_crash.log
    _app_dir_root = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    _crash_log = os.path.join(_app_dir_root, "update_crash.log")
    import traceback as _tb_main

    def _write_crash(exc_type, exc_val, tb):
        try:
            with open(_crash_log, "a", encoding="utf-8") as f:
                f.write(f"===== UNHANDLED EXCEPTION {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
                f.write(f"frozen={getattr(sys, 'frozen', False)} executable={sys.executable}\n")
                f.write("".join(_tb_main.format_exception(exc_type, exc_val, tb)))
                f.write("\n")
        except Exception:
            pass

    sys.excepthook = _write_crash

    # Welcome page
    splash = tk.Tk()
    window_width = 675
    image_height = 329
    bottom_height = 90
    window_height = image_height + bottom_height
    x = int(splash.winfo_screenwidth() / 2 - window_width / 2)
    y = int(splash.winfo_screenheight() / 2 - window_height / 2)
    canvas = tk.Canvas(splash, width=window_width, height=image_height, bg='white', highlightthickness=0)
    canvas.pack()

    splash.title("Welcome to Bomiot")
    splash.geometry(f'{window_width}x{window_height}+{x}+{y}')
    splash.overrideredirect(True)
    try:
        image_path = join(os.path.dirname(sys.executable), 'splash.png')
        pil_img = Image.open(image_path)
        img_width, img_height = pil_img.size
        scale_width = window_width / img_width
        scale_height = window_height / img_height
        scale = min(scale_width, scale_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(resized_img)
        x_pos = (window_width - new_width) // 2
        y_pos = (window_height - new_height) // 2
        canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=img)
    except Exception as e:
        print(f"Failed to load image: {e}")
        canvas.create_text(window_width / 2, window_height / 2, text="Failed to load image", font=("Arial", 12))

    splash.update()

    status_label = tk.Label(splash, text="Checking for updates...", font=("Arial", 12), bg='white', fg='#555555')
    status_label.pack(side='bottom', pady=4)
    progress_bar = ttk.Progressbar(splash, orient='horizontal', length=500, mode='determinate', maximum=100)
    progress_bar.pack(side='bottom', pady=2)
    splash.update()

    # Check for updates
    if check_update(app_name, version, status_label, progress_bar):
        splash.destroy()
        sys.exit(0)

    # Set Django environment variables
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault("RUN_MAIN", "true")
    os.environ.setdefault("IS_LAN", "true")
    os.environ.setdefault("WORKERS", "1")
    lockfile = Path(join(os.path.dirname(sys.executable), 'bomiot_ready.lock'))
    if lockfile.exists():
        lockfile.unlink()
    import django

    django.setup()

    auth_key_path = Path(join(os.path.dirname(sys.executable), 'auth_key.py'))
    if auth_key_path.exists():
        auth_key_path.unlink()
    while True:
        community_key, sponsor_key = encrypt_info()
        if '/' in community_key or '/' in sponsor_key:
            continue
        else:
            break
    with open(auth_key_path, "w", encoding="utf-8") as f:
        f.write(f'COMMUNITY_KEY = "{community_key}"\n')
        f.write(f'SPONSOR_KEY = "{sponsor_key}"\n')

    from django.core.management import call_command
    from django.apps import apps
    from django.contrib.auth import get_user_model

    cmd_args = ["makemigrations"]

    apps_with_models = []
    for app_config in apps.get_app_configs():
        try:
            if app_config.models_module:
                models = apps.get_app_config(app_config.label).get_models()
                if models:
                    apps_with_models.append(app_config.label)
        except Exception:
            continue

    if apps_with_models:
        cmd_args.extend(apps_with_models)

    try:
        call_command(*cmd_args)
        print("Migrations created successfully.")
    except Exception as e:
        print(f"Error creating migrations: {e}")

    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}")

    for app_config in apps.get_app_configs():
        try:
            app_config.ready()
        except Exception:
            pass

    try:
        call_command(*cmd_args)
        print("Migrations created successfully.")
    except Exception as e:
        print(f"Error creating migrations: {e}")

    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}")

    print('System is starting up')

    port = _find_available_port(port)

    print('System started successfully')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    print('Local IP address:', ip)
    s.close()
    baseurl = "http://" + ip + ":" + str(port)
    print('Opening browser at:', baseurl)


    def run_server():
        while True:
            try:
                response = requests.get(url=baseurl, timeout=2)
                print(response.status_code)
                sleep(2)
                webbrowser.open(baseurl)
                break
            except:
                print("Server not ready yet, retrying...")
                sleep(0.5)
                continue


    run_server_thread = threading.Thread(target=run_server, daemon=True)
    run_server_thread.start()

    splash.destroy()

    uvicorn.run(
        "bomiot_asgi:application",
        host='0.0.0.0',
        port=port,
        workers=1,
        log_level="info",
        uds=None,
        ssl_keyfile=None,
        ssl_certfile=None,
        proxy_headers=True,
        http="httptools",
        server_header=False,
        limit_concurrency=1000,
        backlog=128,
        timeout_keep_alive=5,
        timeout_graceful_shutdown=30,
        loop="auto",
    )
