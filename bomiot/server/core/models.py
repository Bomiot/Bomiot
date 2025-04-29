from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.postgres.indexes import GinIndex
from django.forms import model_to_dict
from .utils import compare_dicts
from .signal import bomiot_signals


class CoreModel(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        ordering = ['-id']
        abstract = True


class User(AbstractUser):
    type = models.IntegerField(default=1, verbose_name="User Type")
    phone = models.CharField(default='', max_length=255, blank=True, verbose_name="Phone")
    permission = models.JSONField(default=dict, null=True, verbose_name="Permission")
    request_limit = models.IntegerField(default=0, verbose_name="Request Limit")
    is_delete = models.BooleanField(default=False, verbose_name="Delete Label")
    approve_level = models.IntegerField(default=0, verbose_name="Approve Level")
    openid = models.CharField(default='', max_length=255, blank=True, verbose_name="OpenID")
    appid = models.CharField(default='', max_length=255, blank=True, verbose_name="AppID")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_user'
        verbose_name = settings.BASE_DB_TABLE + ' User'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Permission(CoreModel):
    api = models.CharField(max_length=255, verbose_name="Permission API")
    name = models.CharField(max_length=255, verbose_name="Permission Name")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_permission'
        verbose_name = settings.BASE_DB_TABLE + ' Permission'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class ThrottleModel(CoreModel):
    ip = models.CharField(max_length=255, verbose_name="IP")
    method = models.CharField(max_length=18, verbose_name="Method")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_throttle'
        verbose_name = settings.BASE_DB_TABLE + ' Throttle'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class JobList(CoreModel):
    job_id = models.CharField(max_length=255, verbose_name="Job ID")
    module_name = models.CharField(max_length=255, verbose_name="Module Name")
    func_name = models.CharField(max_length=255, verbose_name="Function Name")
    trigger = models.CharField(max_length=255, verbose_name="Trigger")
    description = models.TextField(default='', null=True, blank=True, verbose_name="Description")
    configuration = models.TextField(null=True, verbose_name="Configuration")
    type = models.BooleanField(default=True, verbose_name="Type")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_job'
        verbose_name = settings.BASE_DB_TABLE + ' Job'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Files(CoreModel):
    name = models.CharField(default='', max_length=255, blank=True, verbose_name="File Name")
    type = models.CharField(default='', max_length=255, blank=True, verbose_name="Type")
    size = models.CharField(default='', max_length=255, blank=True, verbose_name="Size")
    owner = models.CharField(default='', max_length=255, verbose_name="Owner")
    shared_to = models.CharField(default='', max_length=255, verbose_name="Shared To")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_files'
        verbose_name = settings.BASE_DB_TABLE + ' Files'
        verbose_name_plural = verbose_name
        ordering = ['-updated_time']


class Message(CoreModel):
    sender = models.CharField(default='', max_length=255, blank=True, verbose_name="Sender")
    receiver = models.CharField(default='', max_length=255, blank=True, verbose_name="Receiver")
    detail = models.CharField(default='', max_length=255, verbose_name="Detail")
    can_send = models.BooleanField(default=False, verbose_name="Can Send")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_message'
        verbose_name = settings.BASE_DB_TABLE + ' Message'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Goods(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_goods'
        verbose_name = settings.BASE_DB_TABLE + ' Goods'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Goods")
        ]


class Company(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_company'
        verbose_name = settings.BASE_DB_TABLE + ' Company'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Company")
        ]


class Team(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_team'
        verbose_name = settings.BASE_DB_TABLE + ' Team'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Team")
        ]


class Warehouse(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_warehouse'
        verbose_name = settings.BASE_DB_TABLE + ' Warehouse'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Warehouse")
        ]


class Bin(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_bin'
        verbose_name = settings.BASE_DB_TABLE + ' Bin'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Bin")
        ]


class Stock(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_stock'
        verbose_name = settings.BASE_DB_TABLE + ' Stock'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Stock")
        ]


class Supplier(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_supplier'
        verbose_name = settings.BASE_DB_TABLE + ' Supplier'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Supplier")
        ]


class Customer(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_customer'
        verbose_name = settings.BASE_DB_TABLE + ' Customer'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Customer")
        ]


class Approve(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_approve'
        verbose_name = settings.BASE_DB_TABLE + ' Approve'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Approve")
        ]


class ASN(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_asn'
        verbose_name = settings.BASE_DB_TABLE + ' ASN'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_ASN")
        ]


class DN(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_dn'
        verbose_name = settings.BASE_DB_TABLE + ' DN'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_DN")
        ]


class Purchase(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_purchase'
        verbose_name = settings.BASE_DB_TABLE + ' Purchase'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Purchase")
        ]


class Bar(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_bar'
        verbose_name = settings.BASE_DB_TABLE + ' Bar'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="data_Bar")
        ]


def post_save_user_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(sender=User, msg={
            'models': 'User',
            'type': 'created',
            'data': instance
        })
    # else:
    #     old_instance = sender.objects.get(pk=instance.pk)
    #     data_before_update = model_to_dict(old_instance)
    #     data_after_update = model_to_dict(instance)
    #     updated_fields = compare_dicts(data_before_update, data_after_update)
    #     if updated_fields != {}:
    #         bomiot_signals.send(sender=User, msg={
    #             'models': 'User',
    #             'type': 'update',
    #             'updated_fields': updated_fields
    #         })


def post_save_msg_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(sender=Message, msg={
            'models': 'Message',
            'type': 'created',
            'data': instance
        })


def post_save_file_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(sender=Files, msg={
            'models': 'Files',
            'type': 'created',
            'data': instance
        })


post_save.connect(post_save_msg_signals, sender=Message)
post_save.connect(post_save_user_signals, sender=User)
post_save.connect(post_save_file_signals, sender=Files)