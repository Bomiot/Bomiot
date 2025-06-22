import mimetypes, os, django, shutil, sys
from os.path import join
from os import getcwd
from configparser import ConfigParser
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)

if os.path.exists(join(getcwd(), 'setup.ini')) is False:
    current_path = Path(__file__).resolve()
    shutil.copy2(join(join(join(current_path.parent.parent.parent, 'cmd'), 'file'), 'setup.ini'), join(getcwd()))
    config = ConfigParser()
    config.read(join(getcwd(), 'setup.ini'))
    config.set('project', 'name', 'bomiot')
    with open(join(getcwd(), 'setup.ini'), 'w') as setup_file:
        config.write(setup_file)
