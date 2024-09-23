import os


def generate(project):
    """
    generate code from configuration
    :param project:
    :return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')
    # os.environ.setdefault('RUN_MAIN', 'true')
    import django
    django.setup()
    from bomiot.server.core.utils import generate_project
    generate_project(project)
