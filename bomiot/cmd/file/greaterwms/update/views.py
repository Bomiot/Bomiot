import os
import json
import logging
from django.http import JsonResponse, FileResponse
from django.conf import settings
from greaterwms.update.models import UpdateModel

logger = logging.getLogger(__name__)

def update_check(request):
    """
    POST /update/ -> Read manifest from media/update/{app_name}/{manifest}
        JSON body: {"app_name": "...", "manifest": "manifest--*.json"}
        Returns: {"app_name": "...", "version": "...", "os": "...", "arch": "..."}
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = request.body
    try:
        payload = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    app_name = payload.get("app_name", "GreaterWMS")
    manifest_name = payload.get("manifest", "")
    if not app_name or not manifest_name:
        return JsonResponse({"error": "app_name and manifest are required"}, status=400)

    manifest_path = os.path.join(settings.MEDIA_ROOT, 'update', app_name, manifest_name)
    if not os.path.isfile(manifest_path):
        return JsonResponse({"error": "Manifest not found"}, status=404)

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
    except Exception:
        return JsonResponse({"error": "Failed to read manifest"}, status=500)

    return JsonResponse({
        "app_name": manifest_data.get("app_name", ""),
        "version": manifest_data.get("version", ""),
        "os": manifest_data.get("os", ""),
        "arch": manifest_data.get("arch", ""),
    })


def manifest(request):
    """
    POST /update/manifest/ -> Return full manifest JSON content.
        JSON body: {"app_name": "...", "manifest": "manifest--*.json"}
        Returns: the full manifest JSON object
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = request.body
    try:
        payload = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    app_name = payload.get("app_name", "")
    manifest_name = payload.get("manifest", "")
    if not app_name or not manifest_name:
        return JsonResponse({"error": "app_name and manifest are required"}, status=400)

    manifest_path = os.path.join(settings.MEDIA_ROOT, 'update', app_name, manifest_name)
    if not os.path.isfile(manifest_path):
        return JsonResponse({"error": "Manifest not found"}, status=404)

    # Stream the file directly (no JSON parse/serialize overhead)
    f = open(manifest_path, 'rb')
    response = FileResponse(f, content_type='application/json')
    return response


def download(request, file_path):
    """
    GET/HEAD /update/download/<path:file_path> -> Stream file from media/update/{file_path}
    Supports HTTP Range requests for incremental block downloads.
    """
    # Security: prevent directory traversal
    safe_path = os.path.normpath(file_path).replace('\\', '/')
    if safe_path.startswith('..') or '..' in safe_path.split('/'):
        return JsonResponse({"error": "Invalid path"}, status=400)

    full_path = os.path.join(settings.MEDIA_ROOT, 'update', safe_path)
    if not os.path.isfile(full_path):
        return JsonResponse({"error": "File not found"}, status=404)

    f = open(full_path, 'rb')
    response = FileResponse(f, content_type='application/octet-stream')
    return response


def app_info(request):
    """
    POST /update/publish/ -> Check if upload is needed.
        JSON body: {app_name, version, os, arch, verify_code}
        Returns: {"msg": true} if upload needed, {"msg": false} if version already exists
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = request.body
    try:
        payload = json.loads(body) if body else {}
    except json.JSONDecodeError:
        payload = {}

    app_name = payload.get("app_name", "")
    version = payload.get("version", "")
    os_name = payload.get("os", "")
    arch = payload.get("arch", "")
    verify_code = payload.get("verify_code", "") or payload.get("code", "")

    if not all([app_name, version, os_name, arch]):
        return JsonResponse({"msg": False, "detail": "missing fields"})

    # Ensure media/update/{app_name} exists
    from django.conf import settings
    app_dir = os.path.join(settings.MEDIA_ROOT, 'update', app_name)
    os.makedirs(app_dir, exist_ok=True)

    record = UpdateModel.objects.using('default').filter(
        app_name=app_name,
        os=os_name,
        arch=arch,
        verify_code=verify_code,
    ).first()

    if record is not None and record.version == version:
        return JsonResponse({"msg": False})

    return JsonResponse({"msg": True})


def upload(request):
    """
    POST /update/upload/ -> Receive manifest.json and zip file,
        save to media/update/{app_name}/, create or update UpdateModel record.
        verify_code is passed via form-data field.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    from django.conf import settings
    import tarfile
    import io

    files = request.FILES
    logger.info(f"[upload] Received files: {[(k, files[k].name) for k in files]}")
    if not files:
        return JsonResponse({"error": "No files uploaded"}, status=400)

    # Derive app_name from the first non-manifest file's name (first segment before '-')
    app_name = ""
    for key in files:
        fname = files[key].name
        if fname.lower().startswith("manifest"):
            continue
        app_name = fname.split('-')[0]
        break

    # 1) Try to find manifest directly in uploaded files
    manifest_data = None
    for key in files:
        name = files[key].name.lower()
        if name.startswith("manifest") and name.endswith(".json"):
            try:
                raw = files[key].read().decode('utf-8')
                manifest_data = json.loads(raw)
                files[key].seek(0)
            except Exception:
                return JsonResponse({"error": "manifest.json invalid JSON"}, status=400)
            break

    # 2) If not found directly, look inside uploaded tar files
    if manifest_data is None:
        for key in files:
            name = files[key].name.lower()
            if ".tar" in name:
                try:
                    tar_bytes = files[key].read()
                    files[key].seek(0)
                    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode='r:*') as tf:
                        for member in tf.getmembers():
                            base = os.path.basename(member.name).lower()
                            if base.startswith("manifest") and base.endswith(".json"):
                                raw = tf.extractfile(member).read().decode('utf-8')
                                manifest_data = json.loads(raw)
                                break
                except Exception as e:
                    logger.error(f"[upload] Failed to read tar {files[key].name}: {e}")
                if manifest_data is not None:
                    break

    if manifest_data is None:
        return JsonResponse({"error": "manifest.json not found"}, status=400)

    # Fallback to manifest's app_name if filename-based detection failed
    if not app_name:
        app_name = manifest_data.get("app_name", "")

    version = manifest_data.get("version", "")
    os_name = manifest_data.get("os", "")
    arch = manifest_data.get("arch", "")
    verify_code = request.POST.get("verify_code", "") or request.POST.get("code", "")

    # Save all files into media/update/{app_name}/
    save_dir = os.path.join(settings.MEDIA_ROOT, 'update', app_name)
    os.makedirs(save_dir, exist_ok=True)

    saved = []
    for key in files:
        upload_file = files[key]
        dest = os.path.join(save_dir, upload_file.name)
        with open(dest, 'wb') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)
        saved.append(upload_file.name)

    # Extract uploaded tar files directly into save_dir (keep internal folder structure),
    # then delete the tar. Use \\?\ prefix on Windows to bypass MAX_PATH (260 char) limit.
    def _lp(p):
        p = os.path.abspath(p)
        if os.name == 'nt' and not p.startswith('\\\\?\\'):
            return '\\\\?\\' + p
        return p

    save_dir_lp = _lp(save_dir)
    for fname in list(saved):
        if ".tar" not in fname.lower():
            continue
        tar_path = os.path.join(save_dir, fname)
        tar_path_lp = _lp(tar_path)
        try:
            with tarfile.open(tar_path, 'r:*') as tf:
                tf.extractall(save_dir_lp)
            os.remove(tar_path_lp)
        except Exception as e:
            logger.error(f"[upload] Failed to extract {fname}: {e}", exc_info=True)

    record = UpdateModel.objects.using('default').filter(
        app_name=app_name,
        os=os_name,
        arch=arch,
        verify_code=verify_code,
    ).first()

    if record is None:
        UpdateModel.objects.using('default').create(
            app_name=app_name,
            version=version,
            os=os_name,
            arch=arch,
            verify_code=verify_code,
        )
    else:
        record.version = version
        record.save(using='default')

    return JsonResponse({"message": "Upload succeeded", "saved_files": saved})