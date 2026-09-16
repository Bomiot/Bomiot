import os, sys, json, hashlib, fnmatch, platform, subprocess, tempfile, shutil, time
from pathlib import Path
from time import sleep
import urllib.request
import urllib.error
import uvicorn
import socket
import webbrowser
import threading
from os.path import join, exists
from bomiot_token import encrypt_info
from os import getcwd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests

app_name = "GreaterWMS"
version = "3.0.0"
port = 8008

# === Incremental update config (change to your actual address) ===
# Base URL of the remote releases directory; launcher auto-appends manifest and version file paths
# Layout: {UPDATE_URL}manifest-{os}-{arch}.json  and  {UPDATE_URL}GreaterWMS-{version}-{Platform}/
UPDATE_URL = "http://127.0.0.1:8000/media/update/"
# Normalize: ensure UPDATE_URL ends with "/" (keep empty if empty) to avoid 404 from a missing "/" when concatenating
if UPDATE_URL:
    UPDATE_URL = UPDATE_URL.rstrip("/") + "/"


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
    _arch = "arm64" if machine in ("arm64", "aarch64") else "x64"
    return _os, _arch, _display


def _port_available(p: int) -> bool:
    """Check if a TCP port is available for binding (no other process is listening on it)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', p))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def _find_available_port(start_port: int, max_tries: int = 100) -> int:
    """Starting from start_port, return the first port that is not in use (increment by 1 each try)."""
    for candidate in range(start_port, start_port + max_tries):
        if _port_available(candidate):
            if candidate != start_port:
                print(f"Port {start_port} is in use, switched to port {candidate}")
            return candidate
    raise RuntimeError(f"No available port in range [{start_port}, {start_port + max_tries - 1}]")


# === Incremental update ===

def _app_dir():
    """Return the directory where launcher resides (launcher.dist/)"""
    return os.path.dirname(sys.executable)


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
    """Check whether a file matches any .gitignore rule"""
    basename = os.path.basename(rel_path)
    for pat in patterns:
        if fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(basename, pat):
            return True
        if pat.endswith("/"):
            d = pat.rstrip("/")
            if rel_path.startswith(d + "/") or ("/" + d + "/") in rel_path:
                return True
    return False


# Block-level incremental update parameters
# Files larger than BLOCK_THRESHOLD are recorded in block format in the manifest,
# so updates only download blocks whose hash differs (HTTP Range), avoiding re-downloading the whole file.
BLOCK_SIZE = 1024 * 1024          # each block is 1 MiB
BLOCK_THRESHOLD = 8 * 1024 * 1024  # enable block mode for files >= 8 MiB


def _sha256_file(path):
    """Compute the SHA256 of a single file"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_blocks(path, block_size=BLOCK_SIZE):
    """Split a file into blocks of block_size and return the list of per-block SHA256 hashes."""
    hashes = []
    with open(path, "rb") as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            hashes.append(hashlib.sha256(chunk).hexdigest())
    return hashes


def _is_block_entry(val):
    """Whether a manifest entry is in block-level format (a dict containing 'blocks')."""
    return isinstance(val, dict) and isinstance(val.get("blocks"), list) and "sha256" in val


def _entry_sha256(val):
    """Get the overall SHA256 from a manifest entry (a string or a block-level dict)."""
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return val.get("sha256")
    return None


def _scan_local_files(app_dir, ignore_patterns):
    """
    Scan all local files and return {relative_path: SHA256}.
    Skip: .gitignore matches / manifest.json / manifest-*.json / update.bat / update.sh
    -- manifest-*.json must be excluded, otherwise when it is absent from remote files it would be added to to_delete,
       and after the update the local manifest gets deleted, permanently skipping the update check on next startup (issue 2).
    Note: the current check_update diff logic has been changed to "rely only on manifest.files"; this function is no longer called by the main flow, kept as a debugging tool.
    """
    result = {}
    for root, dirs, files in os.walk(app_dir):
        for fn in files:
            if fn in ("manifest.json", "update.bat", "update.sh"):
                continue
            if fn.startswith("manifest-") and fn.endswith(".json"):
                continue  # e.g. manifest-windows-x64.json
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, app_dir).replace(os.sep, "/")
            if _is_ignored(rel, ignore_patterns):
                continue
            try:
                result[rel] = _sha256_file(full)
            except Exception:
                pass
    return result


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
    """
    Download the byte range [byte_start, byte_end] via HTTP Range and write it to dest at the given offset.
    If the server does not support Range (returns 200 full body), fall back to downloading the whole file.
    Returns True if Range succeeded, False if it fell back to the whole file.
    """
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
                    # Range supported: write at the given offset
                    with open(dest, "r+b") as f:
                        f.seek(byte_start)
                        while True:
                            chunk = resp.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                    return True
                else:
                    # Server does not support Range (returns 200), write the whole file
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


def _fetch_manifest(url, max_retries=3):
    """
    Download and parse the remote manifest JSON, with retries and robust error handling.

    Handles:
      - Server returns empty content (0 bytes)
      - HTTP 404/5xx errors
      - Non-JSON response (e.g. HTML error page, blank line, plain text)
      - JSON missing required fields (app_name / version / files)
      - Network timeout / connection failure

    Returns the parsed dict on success; raises on failure (caller handles uniformly).
    """
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GreaterWMS-Updater"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = getattr(resp, "status", 200)
                # 1. HTTP status check (urlopen raises HTTPError on 4xx/5xx; this is extra defense)
                if status < 200 or status >= 300:
                    raise RuntimeError(f"HTTP {status}")
                raw = resp.read()
                # 2. Empty response check
                if not raw or not raw.strip():
                    raise RuntimeError("empty response (0 bytes)")
                # 3. JSON parse (defend against non-JSON content like HTML/404 pages)
                try:
                    data = json.loads(raw.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    snippet = raw[:200].decode("utf-8", errors="replace")
                    raise RuntimeError(f"non-JSON response: {snippet!r}") from e
                # 4. Type check: must be an object
                if not isinstance(data, dict):
                    raise RuntimeError(f"manifest is not an object, got {type(data).__name__}")
                # 5. Required field completeness check
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


def _can_reach_server(update_url, timeout=2.0):
    """
    Quick pre-check: use a raw socket to judge whether the host:port of UPDATE_URL is reachable.
    The goal is to skip the update check within 2 seconds when the network is down / NIC disabled /
    server is fully down, avoiding 3 x 10s = 33s of manifest download retries blocking the splash.
    Returns True meaning "possibly reachable" (only TCP layer works, HTTP layer may still fail),
    returns False meaning definitely unreachable.
    """
    try:
        from urllib.parse import urlparse
        u = urlparse(update_url if update_url.endswith("/") else update_url + "/")
        host = u.hostname
        if not host:
            return True  # invalid URL, let the upper layer decide
        if u.scheme == "https":
            port = u.port or 443
        elif u.scheme == "http":
            port = u.port or 80
        else:
            return True  # unknown protocol, skip pre-check
        # socket.create_connection = DNS + TCP SYN, fails fast within timeout
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.gaierror,         # DNS resolution failed (domain does not exist)
            socket.timeout,          # DNS/TCP timeout
            TimeoutError,            # timeout alias on some platforms
            ConnectionRefusedError,  # host reachable but port not open
            OSError):                # NIC disabled, no route, cable unplugged etc (10051/ENETUNREACH)
        return False
    except Exception:
        return True  # if the pre-check itself errors, do not block; let the upper HTTP request fall back


def _url_head_ok(url, timeout=5.0, max_retries=2):
    """
    Lightweight HTTP HEAD probe to verify whether the remote version directory actually exists before bulk download.
    -- Avoids the case where the server only updated the manifest but forgot to sync the
       GreaterWMS-{version}-{Platform}/ folder, which would trigger _download to retry 3x60s on a 404 file,
       freezing the splash for nearly 3 minutes.
    Returns (ok: bool, reason: str).
    """
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
                return False, last_reason  # 404 needs no retry, immediately judge "folder does not exist"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_reason = f"{type(e).__name__}"
        except Exception as e:
            last_reason = f"{type(e).__name__}: {str(e)[:40]}"
        if attempt < max_retries:
            sleep(1)
    return False, last_reason


def _generate_update_script(app_dir, temp_dir, to_delete, manifest_name=None,
                           new_exe_path=None):
    """
    Generate the update script (update.bat / update.sh) and return its path.

    Args:
      - new_exe_path: absolute path of the new exe corresponding to the remote version
        (e.g. {app_dir}/GreaterWMS-3.0.1-Windows.exe). When a version upgrade changes the
        exe name, this value must be passed; otherwise the bat will still start the old
        version's exe (sys.executable), leaving the built-in version as the old value
        after restart -> update detected again -> infinite loop (user sees "flash exit").
    """
    is_win = sys.platform == "win32"
    exe_name = os.path.basename(sys.executable)
    exe_path = sys.executable
    # Prefer starting the new exe (when version changes the new exe is a different file), otherwise fall back to the current exe
    target_exe_path = new_exe_path if new_exe_path and os.path.isabs(new_exe_path) else exe_path
    target_exe_name = os.path.basename(target_exe_path)

    crash_log = os.path.join(app_dir, "update_crash.log")
    if is_win:
        script_path = os.path.join(app_dir, "update.bat")
        lines = ["@echo off"]
        lines.append(f':wait')
        # Use a temp file as intermediary to avoid the tasklist|find pipe deadlock (find's stdin hangs on EOF under CREATE_NO_WINDOW)
        lines.append(f'tasklist /fi "imagename eq {exe_name}" >"%TEMP%\\_bomiot_wait.tmp" 2>nul')
        lines.append(f'find /i "{exe_name}" "%TEMP%\\_bomiot_wait.tmp" >nul 2>nul')
        lines.append(f'if not errorlevel 1 ( del "%TEMP%\\_bomiot_wait.tmp" >nul 2>nul & ping -n 2 127.0.0.1 >nul 2>nul & goto wait )')
        lines.append(f'del "%TEMP%\\_bomiot_wait.tmp" >nul 2>nul')
        # /H copies hidden+system files (e.g. .gitignore); redirect output to temp log for diagnosis on failure
        lines.append(f'xcopy /Y /S /E /I /H "{temp_dir}" "{app_dir}" >"%TEMP%\\_bomiot_xcopy.log" 2>&1')
        # Bug fix: detect xcopy failure. On error, log and abort — do NOT start the new exe
        # with a half-overwritten app dir (would leave the install in an inconsistent state).
        lines.append(f'if errorlevel 1 goto copyfail')
        lines.append(f'del "%TEMP%\\_bomiot_xcopy.log" >nul 2>nul')
        lines.append(f'goto copyok')
        lines.append(f':copyfail')
        lines.append(f'echo [Update] xcopy failed ^(errorlevel^>^=1^), update aborted. >> "{crash_log}"')
        lines.append(f'type "%TEMP%\\_bomiot_xcopy.log" >> "{crash_log}" 2>nul')
        lines.append(f'del "%TEMP%\\_bomiot_xcopy.log" >nul 2>nul')
        lines.append(f'exit /b 1')
        lines.append(f':copyok')
        # Explicit double insurance: server manifest overwrites local manifest
        if manifest_name:
            lines.append(f'copy /Y "{os.path.join(temp_dir, manifest_name)}" "{os.path.join(app_dir, manifest_name)}" >nul 2>nul')
        lines.append(f'rd /S /Q "{temp_dir}" 2>nul')
        for f in to_delete:
            lines.append(f'del /F /Q "{os.path.join(app_dir, f)}" 2>nul')
        # Start the new exe (target_exe_path) first, then delete the old exe after a 3s ping delay (only needed when new exe name != old exe name)
        #   - do not directly rename the old exe (file lock may fail)
        #   - do not delete before xcopy (old exe is still running)
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
        # Use "{temp_dir}"/. so hidden files (e.g. .gitignore) are also copied; * does not match dotfiles
        lines.append(f'if ! cp -rf "{temp_dir}"/. "{app_dir}"/ 2>> "{crash_log}"; then')
        lines.append(f'    echo "[Update] cp failed, update aborted." >> "{crash_log}"')
        lines.append(f'    exit 1')
        lines.append(f'fi')
        # Explicit double insurance: server manifest overwrites local manifest
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


def check_update(status_label=None, progress_bar=None):
    """
    Check and apply the incremental update.
    Returns True if an update was triggered (caller should exit), False if no update needed.
    """
    app_dir = _app_dir()
    if not UPDATE_URL or not UPDATE_URL.strip():
        print("[Update] UPDATE_URL is empty, update check skipped")
        return False
    _os, _arch, _display = _detect_platform()
    manifest_name = f"manifest-{_os}-{_arch}.json"
    print(f"[Update] Detected platform: {_os} {_arch} ({_display})")
    print(f"[Update] Manifest file name: {manifest_name}")
    print(f"[Update] Manifest URL: {UPDATE_URL}{manifest_name}")

    # Read local manifest (same filename as on the remote server)
    local_manifest_path = os.path.join(app_dir, manifest_name)
    if not os.path.exists(local_manifest_path):
        return False  # no manifest, skip
    try:
        with open(local_manifest_path, encoding="utf-8") as f:
            local_manifest = json.load(f)
    except Exception:
        return False

    # Read .gitignore rules
    ignore_patterns = _read_gitignore(app_dir)

    # ========= Quick network pre-check (2s, avoid 33s hang when offline) =========
    if status_label:
        status_label.config(text="Checking for updates...")
        status_label.update()
    if not _can_reach_server(UPDATE_URL, timeout=2.0):
        err_msg = "Update check failed: network unreachable, skipping"
        print(f"[Update] {err_msg} (server unreachable, pre-check 2s)")
        if status_label:
            status_label.config(text=err_msg)
            status_label.update()
        return False

    # Download remote manifest (same filename as the local artifact)
    manifest_url = f"{UPDATE_URL}{manifest_name}"
    print(f"[Update] Downloading remote manifest: {manifest_url}")
    try:
        import time as _t
        _t0 = _t.time()
        remote_manifest = _fetch_manifest(manifest_url, max_retries=3)
        _size_kb = len(json.dumps(remote_manifest, ensure_ascii=False)) / 1024
        _elapsed = _t.time() - _t0
        print(f"[Update] Remote manifest downloaded: {_size_kb:.1f}KB ({_elapsed:.1f}s)")
    except urllib.error.HTTPError as e:
        # HTTP-level error (404, 500, etc.), server not deployed or temporary failure
        err_msg = f"Update check failed: HTTP {e.code}, skipping"
        print(f"[Update] {err_msg}")
        if status_label:
            status_label.config(text=err_msg)
            status_label.update()
        return False
    except urllib.error.URLError as e:
        # Network-level error (DNS failure, connection timeout, no network, etc.)
        reason = str(e.reason)[:40]
        err_msg = "Update check failed: network error, skipping"
        print(f"[Update] {err_msg} ({reason})")
        if status_label:
            status_label.config(text=err_msg)
            status_label.update()
        return False
    except (TimeoutError, OSError) as e:
        # Directly raised socket-level exceptions (some urllib versions don't wrap them in URLError)
        # e.g. socket.timeout / ConnectionRefusedError / ENETUNREACH(10051)
        reason = f"{type(e).__name__}: {str(e)[:40]}"
        err_msg = "Update check failed: network error, skipping"
        print(f"[Update] {err_msg} ({reason})")
        if status_label:
            status_label.config(text=err_msg)
            status_label.update()
        return False
    except Exception as e:
        # Others: empty response, non-JSON content, missing fields, timeout retries exhausted
        reason = str(e)[:60]
        err_msg = "Update check failed: server unresponsive, skipping"
        print(f"[Update] {err_msg} ({reason})")
        if status_label:
            status_label.config(text=err_msg)
            status_label.update()
        return False

    # Quick version-equality skip (server manifest is the source of truth; no >/< direction check, supports rollback)
    # -- Only when "remote version == hardcoded version compiled into exe" do we treat it as unchanged and skip directly,
    #    avoiding a 1-10s full local SHA256 scan (hits 95% of daily scenarios).
    #    In all other cases (remote higher = upgrade / remote lower = rollback / version matches but files suspected corrupt)
    #    we always enter the hash comparison to align against remote manifest.files.
    if remote_manifest.get("app_name") != app_name:
        return False
    _remote_ver = remote_manifest.get("version", "0")
    if _remote_ver == version:
        print(f"[Update] Version matches (binary {version} == remote {_remote_ver}), skipping hash scan")
        if progress_bar:
            progress_bar["value"] = 0
            progress_bar.update()
        if status_label:
            status_label.config(text="Already up to date")
            status_label.update()
        return False

    remote_version = _remote_ver
    remote_files = remote_manifest.get("files", {})
    # File download base: {UPDATE_URL}GreaterWMS-{version}-{Platform}/
    # Note: in rollback scenarios (remote version < binary version) the concatenated path is the old version directory; the server must keep the corresponding version folder
    file_base_url = f"{UPDATE_URL}{app_name}-{remote_version}-{_display}/"

    _local_ver = local_manifest.get("version", "?")
    if _remote_ver < version:
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

    # ================================================================
    # Diff: dual-manifest intersection model (remote.files = A; local.files = B)
    #   A ∩ B and hash(A) != hash(B)  → download update (intersection)
    #   A − B (declared remotely, absent locally)  → download new (e.g. new version exe)
    #   B − A (declared locally, removed remotely)  → add to to_delete (e.g. old version exe, pyd/dll no longer produced by CI)
    #
    # User data (dbs/ logs/ *.sqlite3 auth_key.py bomiot_ready.lock etc.)
    # is never in local.files (CI applies .gitignore when generating the manifest), so not in B,
    # and never enters to_delete → no extra protect-list needed.
    #
    # Fallback: if local manifest lacks files (old version, malformed), degrade to "remote-only"
    # one-way mode (no deletion) to avoid accidental deletion.
    # ================================================================
    to_download = []
    to_delete = []
    local_files = local_manifest.get("files") if isinstance(local_manifest, dict) else None
    if isinstance(local_files, dict):
        # ==== Standard path: dual-manifest bidirectional diff ====
        A_keys = set(remote_files.keys())
        B_keys = set(local_files.keys())
        # 1) A ∩ B: intersection, compare per file (large files use block-level incremental, small files use full-file hash)
        for rel in A_keys & B_keys:
            remote_entry = remote_files[rel]
            remote_hash = _entry_sha256(remote_entry)
            local_path = os.path.join(app_dir, rel.replace("/", os.sep))
            # Safety lock: a file declared in local manifest but deleted by the user at runtime → re-download as "missing"
            if not os.path.isfile(local_path):
                to_download.append({"path": rel})
                continue
            # Block-level incremental: remote is a block-level entry → compare each block's hash
            if _is_block_entry(remote_entry):
                remote_blocks = remote_entry["blocks"]
                block_size = remote_entry.get("block_size", BLOCK_SIZE)
                try:
                    local_blocks = _hash_blocks(local_path, block_size)
                except Exception:
                    local_blocks = []
                # Same number of blocks and every block hash matches → file unchanged
                if (len(local_blocks) == len(remote_blocks)
                        and all(lb == rb for lb, rb in zip(local_blocks, remote_blocks))):
                    continue
                # Collect changed block indices (blocks absent locally also count as changed)
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
                # Small file: full-file hash comparison
                try:
                    local_hash = _sha256_file(local_path)
                except Exception:
                    local_hash = None
                if local_hash != remote_hash:
                    to_download.append({"path": rel})
        # 2) A − B: remote new files (never declared in local manifest) → full-file download
        for rel in A_keys - B_keys:
            to_download.append({"path": rel})
        # 3) B − A: files declared by CI in the previous version but absent from this remote manifest → treat as removed during upgrade/rollback
        #    Also add a double-insurance layer: these entries must also pass the
        #    .gitignore + manifest-*.json exclusion rules used by _scan_local_files,
        #    to prevent a malicious manifest from using B−A to delete user custom files.
        protected_prefix = ("dbs/", "logs/", "__pycache__/")
        for rel in B_keys - A_keys:
            # Never delete manifest-*.json / update.* / known runtime directory prefixes
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
            # Filter once more with .gitignore (user-added ignore rules are not deleted in B−A)
            if _is_ignored(rel_norm, ignore_patterns):
                continue
            # Final insurance: only delete if the declared path actually exists locally
            local_path = os.path.join(app_dir, rel.replace("/", os.sep))
            if os.path.isfile(local_path):
                to_delete.append(rel)
    else:
        # ==== Fallback path: local manifest has no files → remote-only one-way (no deletion) ====
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
        return False  # no actual change

    # Download changed files into a temp directory
    temp_dir = tempfile.mkdtemp(prefix="bomiot_update_")

    # ========= Pre-probe: does the remote version directory actually exist? =========
    # Prevent the case where the server only updated the manifest but forgot to sync the GreaterWMS-{version}-{Platform}/ folder,
    # which would otherwise trigger 3x60s download retries on the first 404 file and freeze the splash.
    if to_download:
        _probe_path = to_download[0]["path"]
        _probe_url = file_base_url + _probe_path
        _ok, _reason = _url_head_ok(_probe_url, timeout=5.0, max_retries=2)
        if not _ok:
            shutil.rmtree(temp_dir, ignore_errors=True)
            if _reason == "HTTP 404":
                err_msg = f"Server version directory not found ({remote_version}), skipping update"
            else:
                err_msg = f"Update file probe failed ({_reason}), skipping update"
            print(f"[Update] {err_msg} probe={_probe_url}")
            if status_label:
                status_label.config(text=err_msg)
                status_label.update()
            return False
        print(f"[Update] Remote version folder verified via HEAD: {_probe_path} ({_reason})")

    # ========= Progress tracking: compute total download size (block-level known upfront) =========
    # Block-level entries expose changed block count + block_size, so we know the byte budget before downloading.
    # Small files (string-hash entries) have no size in the manifest; their size is added as they are downloaded.
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
                # ===== Block-level incremental: copy local file + download only changed blocks =====
                local_path = os.path.join(app_dir, path.replace("/", os.sep))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                if os.path.isfile(local_path):
                    shutil.copyfile(local_path, dest)
                else:
                    # No local file: create from scratch, download all blocks via Range
                    open(dest, "wb").close()
                block_size = item["block_size"]
                remote_size = item.get("size")
                range_ok = True
                for bi in blocks:
                    byte_start = bi * block_size
                    byte_end = min((bi + 1) * block_size, remote_size) - 1 if remote_size else byte_start + block_size - 1
                    ok = _download_range(url, dest, byte_start, byte_end)
                    if ok:
                        downloaded_bytes += block_size
                    else:
                        # Server does not support Range, the whole file has been written to dest
                        # Adjust accounting: the full file was downloaded, not just this block
                        downloaded_bytes += remote_size if remote_size else block_size
                        range_ok = False
                        break
                    _update_progress(f"Downloading {os.path.basename(path)}")
                # Verify the whole-file SHA256; fall back to full download on mismatch
                if range_ok:
                    try:
                        actual = _sha256_file(dest)
                    except Exception:
                        actual = None
                    if actual != item.get("sha256"):
                        print(f"[Update] block verify mismatch for {path}, falling back to full download")
                        _download(url, dest)
            else:
                _download(url, dest)
                # Small file: add its actual size to both total and downloaded (size unknown before download)
                fsize = os.path.getsize(dest)
                total_bytes += fsize
                downloaded_bytes += fsize
                _update_progress(f"Downloading {os.path.basename(path)}")
        except Exception as e:
            print(f"Download failed: {path} - {e}")
            # Issue ③: clean up the temp directory on download failure to avoid bomiot_update_* garbage piling up in system temp
            shutil.rmtree(temp_dir, ignore_errors=True)
            if progress_bar:
                progress_bar["value"] = 0
                progress_bar.update()
            if status_label:
                status_label.config(text="Update download failed, skipping")
                status_label.update()
            return False

    if progress_bar:
        progress_bar["value"] = 100
        progress_bar.update()
    if status_label:
        status_label.config(text="Update download complete, applying...")
        status_label.update()

    # Also write the new-version manifest into temp_dir, so it gets copied into app_dir along with xcopy/cp.
    # -- Because CI generates the manifest by "scan directory first, then write manifest", remote files does not include the manifest itself.
    #    If we don't write it explicitly here, the local manifest will still be the old version after restart, wasting one check cycle.
    new_manifest_path = os.path.join(temp_dir, manifest_name)
    try:
        with open(new_manifest_path, "w", encoding="utf-8") as f:
            json.dump(remote_manifest, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Failing to write the manifest does not block the update (otherwise the update fails but the old binary remains), just log it
        print(f"[Update] Warning: failed to write new manifest to temp: {e}")

    # Compute the absolute path of the new exe in the client directory (when version or platform display changes,
    # the EXE name is fixed to app_name (e.g. GreaterWMS.exe), no longer carrying the version number.
    # The version number is judged for update via the manifest's sha256/block-level hash comparison;
    # after the same-named EXE is overwritten by xcopy, the new built-in version constant naturally takes effect, no infinite loop.)
    _plat_is_win = sys.platform == "win32"
    if _plat_is_win:
        new_exe_name = f"{app_name}.exe"
    else:
        new_exe_name = app_name
    new_exe_path = os.path.join(app_dir, new_exe_name)

    # Generate update script (pass manifest_name in to generate explicit copy lines, ensuring server manifest overwrites local)
    script_path = _generate_update_script(
        app_dir, temp_dir, to_delete,
        manifest_name=manifest_name,
        new_exe_path=new_exe_path,
    )

    # Start the script (silent: do not pop up any cmd / terminal black window)
    is_win = sys.platform == "win32"
    _started_script = False
    _script_err = ""
    try:
        if is_win:
            CREATE_NO_WINDOW          = int(getattr(subprocess, "CREATE_NO_WINDOW",          0x08000000))
            CREATE_NEW_PROCESS_GROUP  = int(getattr(subprocess, "CREATE_NEW_PROCESS_GROUP",  0x00000200))
            # Note: do NOT add DETACHED_PROCESS. It causes child processes (cmd/xcopy) to run without
            # a console handle, making xcopy return err=4 "The system cannot find the path specified",
            # so update files cannot be copied. CREATE_NO_WINDOW is enough to hide the window.
            flags = CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
            startupinfo = subprocess.STARTUPINFO()
            # STARTF_USESHOWWINDOW = 1, SW_HIDE = 0
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
        # On failure, dump the trace to disk so the user can find the reason for the flash exit
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
        # Script start failed: clean up leftovers + do not exit (continue with Django startup, avoid flash exit + user completely locked out)
        shutil.rmtree(temp_dir, ignore_errors=True)
        try: os.remove(script_path)
        except Exception: pass
        if status_label:
            status_label.config(text="Update script failed to start, skipping (see update_crash.log)")
            status_label.update()
        return False

    # Give the bat child process a 300ms startup buffer (prevent this process from exiting too fast, terminating child processes in the parent process group before bat even starts)
    sleep(0.3)
    return True


if __name__ == "__main__":
    # Top-level safety net: write any uncaught exception to update_crash.log, so the user doesn't just see "the window closed" with no clues
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
    # Image area keeps 329px; bottom panel (status + progress bar) expanded by ~30% for readability
    image_height = 329
    bottom_height = 90
    window_height = image_height + bottom_height
    x = int(splash.winfo_screenwidth() / 2 - window_width / 2)
    y = int(splash.winfo_screenheight() / 2 - window_height / 2)
    canvas = tk.Canvas(splash, width=window_width, height=image_height, bg='white', highlightthickness=0)
    canvas.pack()

    splash.title("Welcome to Bomiot")
    splash.geometry(f'{window_width}x{window_height}+{x}+{y}')
    splash.overrideredirect(True)  # Borderless display
    # Load and scale image (maintain aspect ratio)
    try:
        # Load image using PIL
        image_path = join(getcwd(), 'splash.png')
        pil_img = Image.open(image_path)

        # Get original image dimensions
        img_width, img_height = pil_img.size

        # Calculate scale ratio (maintain aspect ratio)
        scale_width = window_width / img_width
        scale_height = window_height / img_height
        scale = min(scale_width, scale_height)  # Use minimum ratio to ensure image fits entirely within window

        # Calculate scaled dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Scale image
        resized_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # High quality scaling
        img = ImageTk.PhotoImage(resized_img)

        # Calculate center position for image
        x_pos = (window_width - new_width) // 2
        y_pos = (window_height - new_height) // 2

        # Display image on canvas (centered)
        canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=img)
    except Exception as e:
        print(f"Failed to load image: {e}")
        # Display error text
        canvas.create_text(window_width / 2, window_height / 2, text="Failed to load image", font=("Arial", 12))

    # Force window refresh to ensure splash is displayed before subsequent operations
    splash.update()

    # Incremental update status label (larger font for readability)
    status_label = tk.Label(splash, text="Checking for updates...", font=("Arial", 12), bg='white', fg='#555555')
    status_label.pack(side='bottom', pady=4)
    # Dynamic progress bar driven by known total download size
    progress_bar = ttk.Progressbar(splash, orient='horizontal', length=500, mode='determinate', maximum=100)
    progress_bar.pack(side='bottom', pady=2)
    splash.update()

    # Check for updates (if update found, generate script and exit; otherwise continue startup)
    if check_update(status_label, progress_bar):
        splash.destroy()
        sys.exit(0)

    # Set Django environment variables
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault("RUN_MAIN", "true")
    os.environ.setdefault("IS_LAN", "true")
    os.environ.setdefault('WORKERS', '1')
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

    # Prepare makemigrations command arguments
    cmd_args = ["makemigrations"]

    # Auto-detect all apps with models
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

    # Execute makemigrations command
    try:
        call_command(*cmd_args)
        print("Migrations created successfully.")
    except Exception as e:
        print(f"Error creating migrations: {e}")

    # Execute migrate command
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}")

    for app_config in apps.get_app_configs():
        try:
            app_config.ready()
        except Exception:
            pass

    # Execute makemigrations command again
    try:
        call_command(*cmd_args)
        print("Migrations created successfully.")
    except Exception as e:
        print(f"Error creating migrations: {e}")

    # Execute migrate command again
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}")

    # Keep welcome page displayed for a while (original logic: 10 seconds)
    print('System is starting up')

    # Start Django development server
    # ---- port auto-increment: if 8008 is taken, try 8009, 8010, ... up to 100 ports ----
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

    # Manually destroy the welcome page before starting uvicorn
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


