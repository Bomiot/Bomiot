import django
import os


def init_password():
    """
    init superuser password
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bomiot.server.server.settings")
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user_data = User.objects.filter(username='admin', is_superuser=True)
    if user_data.exists:
        user_data.first().set_password('admin')
        print('Reset admin account: admin, initial password: admin, just use it temporarily '
              'and change the password for safety')
    else:
        print('Please init one admin first')
        