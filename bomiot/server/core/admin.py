import orjson

from os.path import join
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import bomiot_data_control
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

bomiot_data_signals.connect(bomiot_data_control.data_callback, weak=False)
bomiot_signals.connect(bomiot_control.server_callback, weak=False)