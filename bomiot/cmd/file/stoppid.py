import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
os.environ.setdefault('RUN_MAIN', 'true')
import django
django.setup()
from bomiot.server.core.models import UvicornProcess
import subprocess
import sys

def kill_uvicorn_processes():
    process = UvicornProcess.objects.filter()
    for pid in process:
        subprocess.run(["kill", "-9", pid.pid])
        pid.delete()
    return 0

if __name__ == "__main__":
    sys.exit(kill_uvicorn_processes())