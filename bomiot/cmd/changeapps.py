import os


def create_project_apps_py(path, app, name):
    with open(path, "w") as f:
        f.write("from django.apps import AppConfig\n")
        f.write("\n")
        f.write(f"class {name.capitalize()}Config(AppConfig):\n")
        f.write(f"    name = '{app}.{name}'\n")
    f.close()


def create_plugins_apps_py(path, name):
    with open(path, "w") as f:
        f.write("from django.apps import AppConfig\n")
        f.write("\n")
        f.write(f"class {name.capitalize()}Config(AppConfig):\n")
        f.write(f"    name = '{name}'\n")
    f.close()