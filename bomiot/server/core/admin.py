import orjson

from os.path import join
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.conf import settings
from bomiot.server.core.utils import receiver_callback, dynamic_import_and_call
from bomiot.server.core.signal import bomiot_data_signals
import bomiot_control
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
    project_name = kwargs.get('request').META.get('HTTP_PROJECT', settings.PROJECT_NAME)
    if project_name.lower() == 'bomiot':
        project_name = settings.PROJECT_NAME
    api_obj = dynamic_import_and_call(f'{project_name}.api', 'api_return', f'{path}')
    value = api_obj.get('func_name')
    feedback = receiver_callback(kwargs, value)
    return feedback

bomiot_data_signals.connect(data_callback, weak=False)
bomiot_signals.connect(bomiot_control.server_callback, weak=False)
