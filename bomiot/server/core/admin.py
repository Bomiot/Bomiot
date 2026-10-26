import orjson

from os.path import join
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.conf import settings
from bomiot.server.core.utils import receiver_callback, dynamic_import_and_call, sync_write_file, receiver_server_callback, receiver_file_callback
from bomiot.server.core.signal import bomiot_data_signals
from bomiot.server.core.signal import bomiot_signals

# get user_model
User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    user admin
    """
    # difine the form for creating and updating user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("phone", "email", "type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # define the form for creating and updating user
    list_display = (
        "username",
        "phone",
        "email",
        "type",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    # add the filter for the list view
    list_filter = ("is_staff", "is_superuser", "is_active", "type")

    # add the search fields for the list view
    search_fields = ("username", "email", "phone")

@receiver(bomiot_data_signals)
def data_callback(**kwargs):
    """
    Signal receiver to handle the received signal
    """
    path = kwargs.get('request').path
    api_obj = dynamic_import_and_call('greaterwms.api', 'api_return', f'{path}')
    value = api_obj.get('func_name')
    feedback = receiver_callback(kwargs, value)
    return feedback

@receiver(bomiot_signals)
def file_server_callback(**kwargs):
    """
    Signal receiver to handle the received signal
    """
    data = kwargs.get('msg')
    if data.get('models') == 'FileSave':
        sync_write_file(kwargs.get('file_path'), kwargs.get('file_data'))
    elif data.get('models') == 'Pids':
        receiver_server_callback(data.get('data'), 'pid_get')
    elif data.get('models') == 'Network':
        receiver_server_callback(data.get('data'), 'network_get')
    elif data.get('models') == 'Disk':
        receiver_server_callback(data.get('data'), 'disk_get')
    elif data.get('models') == 'Memory':
        receiver_server_callback(data.get('data'), 'memory_get')
    elif data.get('models') == 'CPU':
        receiver_server_callback(data.get('data'), 'cpu_get')
    elif data.get('models') == 'Files':
        receiver_file_callback(data.get('data'), 'file_get')
    else:
        return
    return

bomiot_data_signals.connect(data_callback, weak=False)
bomiot_signals.connect(file_server_callback, weak=False)
