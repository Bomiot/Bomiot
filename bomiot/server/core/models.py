from email.policy import default

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .field import Md5idField
from django.db.models.signals import post_save, pre_save, post_delete
from .signal import bomiot_signals


class User(AbstractUser):
    type = models.IntegerField(default=1, verbose_name="User Type")
    phone = models.CharField(default='', max_length=255, blank=True, verbose_name="Phone")
    lock = models.IntegerField(default=0, verbose_name="Error Login Time")
    is_delete = models.BooleanField(default=False, verbose_name="Delete Label")
    vip_level = models.IntegerField(default=0, verbose_name="VIP Level")
    md5_id = Md5idField()
    vip_time = models.DateTimeField(auto_now=False, blank=True, null=True, verbose_name="VIP Time")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_user'
        verbose_name = settings.BASE_DB_TABLE + ' User'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class ThrottleModel(models.Model):
    ip = models.CharField(max_length=255, verbose_name="IP")
    method = models.CharField(max_length=18, verbose_name="Method")
    md5_id = Md5idField()
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_throttle'
        verbose_name = settings.BASE_DB_TABLE + ' Throttle'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class JobList(models.Model):
    job_id = models.CharField(max_length=255, verbose_name="Job ID")
    module_name = models.CharField(max_length=255, verbose_name="Module Name")
    func_name = models.CharField(max_length=255, verbose_name="Function Name")
    trigger = models.CharField(max_length=255, verbose_name="Trigger")
    description = models.TextField(default='', null=True, blank=True, verbose_name="Description")
    configuration = models.TextField(null=True, verbose_name="Configuration")
    type = models.BooleanField(default=True, verbose_name="Type")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_job'
        verbose_name = settings.BASE_DB_TABLE + ' Job'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Message(models.Model):
    sender = models.CharField(default='', max_length=255, blank=True, verbose_name="Sender")
    receiver = models.CharField(default='', max_length=255, blank=True, verbose_name="Receiver")
    detail = models.CharField(default='', max_length=255, verbose_name="Detail")
    can_send = models.BooleanField(default=False, verbose_name="Can Send")
    md5_id = models.CharField(default='', max_length=255, verbose_name="MD5 ID")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_message'
        verbose_name = settings.BASE_DB_TABLE + ' Message'
        verbose_name_plural = verbose_name
        ordering = ['-id']


def post_save_user_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(sender=None, msg={
            'models': 'User',
            'type': 'created',
            'data': instance
        })
    else:
        bomiot_signals.send(sender=None, msg={
            'models': 'User',
            'type': 'update',
            'data': instance
        })

def post_save_msg_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(sender=None, msg={
            'models': 'Message',
            'type': 'created',
            'data': instance
        })

post_save.connect(post_save_msg_signals, sender=Message)
post_save.connect(post_save_user_signals, sender=User)