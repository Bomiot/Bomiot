import os
import django
from django.core.management import call_command


def migrate():
    """
    Execute database migrations
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    os.environ.setdefault('RUN_MAIN', 'true')
    django.setup()
    
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error during migration: {e}") 