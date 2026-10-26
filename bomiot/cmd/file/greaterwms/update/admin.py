from django.contrib import admin
from .models import UpdateModel


@admin.register(UpdateModel)
class UpdateModelAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'version', 'os', 'arch', 'verify_code')
    search_fields = ('app_name', 'version')