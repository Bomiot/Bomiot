import django
import os
from configparser import ConfigParser


def init_admin():
    """
    create superuser
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        User.objects.get(username='admin', is_superuser=True)
        print('Admin user already exists, you can use admin to login:')
    except:
        username = 'admin'
        email = f'{username}@bomiot.com'
        password = username
        admin, created = User.objects.update_or_create(email=email, username=username)
        admin.set_password(password)
        admin.is_active = True
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        print('%s admin account: %s(%s), initial password: %s, just use it temporarily '
              'and change the password for safety' % \
              ('Created' if created else 'Reset', username, email, password))