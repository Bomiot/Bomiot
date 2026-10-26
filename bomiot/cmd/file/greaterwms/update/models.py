from django.db import models
from bomiot.server.core.models import CoreModel
from django.conf import settings

class UpdateModel(CoreModel):
    app_name = models.CharField(max_length=255, blank=True, default="", verbose_name="App Name")
    version = models.CharField(max_length=255, blank=True, default="", verbose_name="Version")
    os = models.CharField(max_length=255, blank=True, default="", verbose_name="OS")
    arch = models.CharField(max_length=255, blank=True, default="", verbose_name="Arch")
    verify_code = models.CharField(max_length=255, blank=True, default="", verbose_name="Verify Code")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_updatemodel'
        verbose_name = settings.BASE_DB_TABLE + ' UpdateModel'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = (('app_name', 'os', 'arch', 'version', 'verify_code'),)