import os


def create_admin_py(path):
    admin_py = os.path.join(path, "admin.py")
    with open(admin_py, "w") as f:
        f.write("from django.contrib import admin\n")
        f.write("\n")
        f.write("# Register your models here.\n")
    f.close()