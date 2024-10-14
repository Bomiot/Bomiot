import mimetypes, os, django, shutil, sys
from configparser import ConfigParser
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)

if os.path.exists(os.path.join(os.getcwd(), 'setup.ini')) is False:
    current_path = Path(__file__).resolve()
    shutil.copy2(os.path.join(current_path.parent.parent.parent, 'cmd/file/setup.ini'), os.path.join(os.getcwd()))
    config = ConfigParser()
    config.read(os.path.join(os.getcwd(), 'setup.ini'))
    config.set('site', 'name', 'bomiot')
    config.set('db_name', 'name', 'bomiot')
    with open(os.path.join(os.getcwd(), 'setup.ini'), 'w') as setupfile:
        config.write(setupfile)