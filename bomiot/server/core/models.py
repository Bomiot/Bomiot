from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .field import Md5idField


class User(AbstractUser):
    type = models.IntegerField(default=1, verbose_name="User Type")
    phone = models.CharField(default='', max_length=255, blank=True, verbose_name="Phone")
    lock = models.IntegerField(default=0, verbose_name="Error Login Time")
    is_delete = models.BooleanField(default=False, verbose_name="Delete Label")
    vip_level = models.IntegerField(default=0, verbose_name="VIP Level")
    md5_id = Md5idField()
    vip_time = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name="VIP Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_user'
        verbose_name = settings.BASE_DB_TABLE + ' User'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class ThrottleModel(models.Model):
    ip = models.CharField(max_length=255, verbose_name="IP")
    method = models.CharField(max_length=18, verbose_name="Method")
    md5_id = Md5idField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_throttle'
        verbose_name = settings.BASE_DB_TABLE + ' Throttle'
        verbose_name_plural = verbose_name
        ordering = ['-id']