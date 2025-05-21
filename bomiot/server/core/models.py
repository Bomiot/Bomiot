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
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Updated Time")

    class Meta:
        ordering = ['-id']
        abstract = True


class User(AbstractUser, CoreModel):
    type = models.IntegerField(default=1, verbose_name="User Type")
    phone = models.CharField(default='', max_length=255, blank=True, verbose_name="Phone")
    permission = models.JSONField(default=dict, null=True, verbose_name="Permission")
    request_limit = models.IntegerField(default=0, verbose_name="Request Limit")
    team = models.IntegerField(default=0, blank=True, verbose_name="Team")
    department = models.IntegerField(default=0, blank=True, verbose_name="Department")

    class Meta(AbstractUser.Meta):
        db_table = settings.BASE_DB_TABLE + '_user'
        verbose_name = settings.BASE_DB_TABLE + ' User'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['permission'], name="user_permission_gin_index")
        ]


class Permission(CoreModel):
    api = models.CharField(max_length=255, verbose_name="Permission API")
    name = models.CharField(max_length=255, verbose_name="Permission Name")

    class Meta:
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

    class Meta:
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

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_files'
        verbose_name = settings.BASE_DB_TABLE + ' Files'
        verbose_name_plural = verbose_name
        ordering = ['-updated_time']


class Message(CoreModel):
    sender = models.CharField(default='', max_length=255, blank=True, verbose_name="Sender")
    receiver = models.CharField(default='', max_length=255, blank=True, verbose_name="Receiver")
    detail = models.CharField(default='', max_length=255, verbose_name="Detail")
    can_send = models.BooleanField(default=False, verbose_name="Can Send")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_message'
        verbose_name = settings.BASE_DB_TABLE + ' Message'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Pids(CoreModel):
    pid = models.IntegerField(primary_key=True, editable=False, verbose_name="PID")
    name = models.CharField(default='', max_length=255, blank=True, verbose_name="PID Name")
    memory = models.IntegerField(default=0, verbose_name="Memory")
    create_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, verbose_name="Create Time")
    memory_usage = models.FloatField(default=0, verbose_name="Memory Usage")
    cpu_usage = models.FloatField(default=0, verbose_name="CPU Usage")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_pids'
        verbose_name = settings.BASE_DB_TABLE + ' Pids'
        verbose_name_plural = verbose_name
        ordering = ['-cpu_usage']


class CPU(CoreModel):
    cpu_usage = models.FloatField(default=0, verbose_name="CPU Usage")
    physical_cores = models.IntegerField(default=0, verbose_name="Physical Cores")
    logical_cores = models.IntegerField(default=0, verbose_name="Logical Cores")
    cpu_frequency = models.CharField(default='', max_length=255, verbose_name="CPU Frequency")
    min_cpu_frequency = models.CharField(default='', max_length=255, verbose_name="Min CPU Frequency")
    max_cpu_frequency = models.CharField(default='', max_length=255, verbose_name="Max CPU Frequency")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_cpu'
        verbose_name = settings.BASE_DB_TABLE + ' CPU'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Memory(CoreModel):
    total = models.IntegerField(default=0, verbose_name="Total Memory")
    used = models.IntegerField(default=0, verbose_name="Used Memory")
    free = models.IntegerField(default=0, verbose_name="Free Memory")
    percent = models.FloatField(default=0, verbose_name="Percent")
    swap_total = models.IntegerField(default=0, verbose_name="Swap Total Memory")
    swap_used = models.IntegerField(default=0, verbose_name="Swap Used Memory")
    swap_free = models.IntegerField(default=0, verbose_name="Swap Free Memory")
    swap_percent = models.FloatField(default=0, verbose_name="Swap Percent")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_memory'
        verbose_name = settings.BASE_DB_TABLE + ' Memory'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Disk(CoreModel):
    device = models.CharField(default='', max_length=255, verbose_name="Device")
    mountpoint = models.CharField(default='', max_length=255, verbose_name="Mountpoint")
    total = models.IntegerField(default=0, verbose_name="Total")
    used = models.IntegerField(default=0, verbose_name="Used")
    free = models.IntegerField(default=0, verbose_name="Free")
    percent = models.FloatField(default=0, verbose_name="Percent")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_disk'
        verbose_name = settings.BASE_DB_TABLE + ' Disk'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Network(CoreModel):
    bytes_sent = models.IntegerField(default=0, verbose_name="Bytes Sent")
    bytes_recv = models.IntegerField(default=0, verbose_name="Bytes Received")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_network'
        verbose_name = settings.BASE_DB_TABLE + ' Network'
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
            GinIndex(fields=['data'], name="goods_data_gin_index")
        ]


class Department(CoreModel):
    name = models.CharField(default='', max_length=255, verbose_name="Department Name")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_department'
        verbose_name = settings.BASE_DB_TABLE + ' Department'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Team(CoreModel):
    name = models.CharField(default='', max_length=255, verbose_name="Team Name")
    permission = models.JSONField(default=dict, null=True, verbose_name="Permission")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_team'
        verbose_name = settings.BASE_DB_TABLE + ' Team'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['permission'], name="team_permission_gin_index")
        ]


class Bin(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_bin'
        verbose_name = settings.BASE_DB_TABLE + ' Bin'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="bin_data_gin_index")
        ]


class Stock(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_stock'
        verbose_name = settings.BASE_DB_TABLE + ' Stock'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="stock_data_gin_index")
        ]


class Supplier(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_supplier'
        verbose_name = settings.BASE_DB_TABLE + ' Supplier'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="supplier_data_gin_index")
        ]


class Customer(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_customer'
        verbose_name = settings.BASE_DB_TABLE + ' Customer'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="customer_data_gin_index")
        ]


class ASN(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_asn'
        verbose_name = settings.BASE_DB_TABLE + ' ASN'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="asn_data_gin_index")
        ]


class DN(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_dn'
        verbose_name = settings.BASE_DB_TABLE + ' DN'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="dn_data_gin_index")
        ]


class Purchase(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_purchase'
        verbose_name = settings.BASE_DB_TABLE + ' Purchase'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="purchase_data_gin_index")
        ]


class Bar(CoreModel):
    data = models.JSONField()

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_bar'
        verbose_name = settings.BASE_DB_TABLE + ' Bar'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['data'], name="bar_data_gin_index")
        ]

class PyPi(CoreModel):
    category = models.CharField(max_length=255, verbose_name="Category")
    date = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, verbose_name="PyPi Date")
    percent = models.FloatField(default=0, verbose_name="Percent")
    downloads = models.IntegerField(default=0, verbose_name="Downloads")

    class Meta:
        db_table = settings.BASE_DB_TABLE + '_pypi'
        verbose_name = settings.BASE_DB_TABLE + ' PyPi'
        verbose_name_plural = verbose_name
        ordering = ['-id']


def post_save_user_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'User',
            'type': 'created',
            'data': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
                'phone': instance.phone,
                'type': instance.type,
                'permission': instance.permission,
                'request_limit': instance.request_limit,
                'team': instance.team,
                'department': instance.department,
                'is_active': instance.is_active
            }
        })

def post_save_team_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Team',
            'type': 'created',
            'data': {
                'id': instance.id,
                'name': instance.name,
                'permission': instance.permission
            }
        })

def post_save_department_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Department',
            'type': 'created',
            'data': {
                'id': instance.id,
                'name': instance.name
            }
        })

def post_save_msg_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Message',
            'type': 'created',
            'data': {
                'id': instance.id,
                'sender': instance.sender,
                'receiver': instance.receiver,
                'detail': instance.detail,
                'can_send': instance.can_send,
                'created_time': instance.created_time
            }
        })

def post_save_file_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Files',
            'type': 'created',
            'data': {
                'id': instance.id,
                'name': instance.name,
                'type': instance.type,
                'size': instance.size,
                'owner': instance.owner,
                'shared_to': instance.shared_to
            }
        })

def post_save_cpu_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'CPU',
            'type': 'created',
            'data': {
                'id': instance.id,
                'cpu_usage': instance.cpu_usage,
                'physical_cores': instance.physical_cores,
                'logical_cores': instance.logical_cores,
                'cpu_frequency': instance.cpu_frequency,
                'min_cpu_frequency': instance.min_cpu_frequency,
                'max_cpu_frequency': instance.max_cpu_frequency
            }
        })

def post_save_memory_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Memory',
            'type': 'created',
            'data': {
                'id': instance.id,
                'total': instance.total,
                'used': instance.used,
                'free': instance.free,
                'percent': instance.percent,
                'swap_total': instance.swap_total,
                'swap_used': instance.swap_used,
                'swap_free': instance.swap_free,
                'swap_percent': instance.swap_percent
            }
        })

def post_save_disk_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Disk',
            'type': 'created',
            'data': {
                'id': instance.id,
                'device': instance.device,
                'mountpoint': instance.mountpoint,
                'total': instance.total,
                'used': instance.used,
                'free': instance.free,
                'percent': instance.percent
            }
        })

def post_save_network_signals(sender, instance, created, **kwargs):
    if created:
        bomiot_signals.send(msg={
            'models': 'Network',
            'type': 'created',
            'data': {
                'id': instance.id,
                'bytes_sent': instance.bytes_sent,
                'bytes_recv': instance.bytes_recv
            }
        })

post_save.connect(post_save_user_signals, sender=User)
post_save.connect(post_save_team_signals, sender=Team)
post_save.connect(post_save_department_signals, sender=Department)
post_save.connect(post_save_msg_signals, sender=Message)
post_save.connect(post_save_file_signals, sender=Files)
post_save.connect(post_save_cpu_signals, sender=CPU)
post_save.connect(post_save_memory_signals, sender=Memory)
post_save.connect(post_save_disk_signals, sender=Disk)
post_save.connect(post_save_network_signals, sender=Network)