from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, required=False)
    email = serializers.CharField(read_only=True, required=False)
    phone = serializers.CharField(read_only=True, required=False)
    permission = serializers.JSONField(read_only=True, required=False)
    request_limit = serializers.IntegerField(read_only=True, required=False)
    team = serializers.IntegerField(read_only=True, required=False)
    department = serializers.IntegerField(read_only=True, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    last_login = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_active', 'request_limit', 'team', 'department', 'permission', 'date_joined', 'last_login', 'updated_time']
        read_only_fields = ['id']


class PermissionSerializer(serializers.ModelSerializer):
    """
    Permission Serializer
    """
    api = serializers.CharField(read_only=True, required=False)
    name = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = models.Permission
        fields = ['api', 'name']
        read_only_fields = ['api']


class TeamSerializer(serializers.ModelSerializer):
    """
    Team Serializer
    """
    name = serializers.CharField(read_only=True, required=False)
    permission = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Team
        fields = ['id', 'name', 'permission', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Department Serializer
    """
    name = serializers.CharField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Team
        fields = ['id', 'name', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class FileSerializer(serializers.ModelSerializer):
    """
    File Serializer
    """
    name = serializers.CharField(read_only=True, required=False)
    type = serializers.CharField(read_only=True, required=False)
    size = serializers.CharField(read_only=True, required=False)
    owner = serializers.CharField(read_only=True, required=False)
    shared_to = serializers.CharField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Files
        fields = ['id', 'name', 'type', 'size', 'owner', 'shared_to', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class APISerializer(serializers.ModelSerializer):
    """
    API Serializer
    """
    method = serializers.CharField(read_only=True, required=False)
    api = serializers.CharField(read_only=True, required=False)
    func_name = serializers.CharField(read_only=True, required=False)
    name = serializers.CharField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Example
        fields = ['id', 'method', 'api', 'func_name', 'name', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class ExampleSerializer(serializers.ModelSerializer):
    """
    Example Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Example
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class PidsSerializer(serializers.ModelSerializer):
    """
    Pid Serializer
    """
    pid = serializers.IntegerField(read_only=True, required=False)
    name = serializers.CharField(read_only=True, required=False)
    memory = serializers.IntegerField(read_only=True, required=False)
    memory_usage = serializers.FloatField(read_only=True, required=False)
    cpu_usage = serializers.FloatField(read_only=True, required=False)
    create_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Pids
        fields = ['pid', 'name', 'memory', 'create_time', 'memory_usage', 'cpu_usage', 'created_time', 'updated_time']
        read_only_fields = ['pid']


class PyPiSerializer(serializers.ModelSerializer):
    """
    PyPi Serializer
    """
    category = serializers.CharField(read_only=True, required=False)
    date = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d')
    percent = serializers.FloatField(read_only=True, required=False)
    downloads = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = models.PyPi
        fields = ['id', 'category', 'date', 'percent', 'downloads']
        read_only_fields = ['id']


class CPUSerializer(serializers.ModelSerializer):
    """
    CPU Serializer
    """
    cpu_usage = serializers.FloatField(read_only=True, required=False)
    physical_cores = serializers.IntegerField(read_only=True, required=False)
    logical_cores = serializers.IntegerField(read_only=True, required=False)
    cpu_frequency = serializers.CharField(read_only=True, required=False)
    min_cpu_frequency = serializers.CharField(read_only=True, required=False)
    max_cpu_frequency = serializers.CharField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.CPU
        fields = ['id', 'cpu_usage', 'physical_cores', 'logical_cores', 'cpu_frequency', 'min_cpu_frequency', 'max_cpu_frequency', 'created_time', 'updated_time']
        read_only_fields = ['id']


class MemorySerializer(serializers.ModelSerializer):
    """
    Memory Serializer
    """
    total = serializers.IntegerField(read_only=True, required=False)
    used = serializers.IntegerField(read_only=True, required=False)
    free = serializers.IntegerField(read_only=True, required=False)
    percent = serializers.FloatField(read_only=True, required=False)
    swap_total = serializers.IntegerField(read_only=True, required=False)
    swap_used = serializers.IntegerField(read_only=True, required=False)
    swap_free = serializers.IntegerField(read_only=True, required=False)
    swap_percent = serializers.FloatField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Memory
        fields = ['id', 'total', 'used', 'free', 'percent', 'swap_total', 'swap_used', 'swap_free', 'swap_percent', 'created_time', 'updated_time']
        read_only_fields = ['id']


class DiskSerializer(serializers.ModelSerializer):
    """
    Disk Serializer
    """
    device = serializers.CharField(read_only=True, required=False)
    mountpoint = serializers.CharField(read_only=True, required=False)
    total = serializers.IntegerField(read_only=True, required=False)
    used = serializers.IntegerField(read_only=True, required=False)
    free = serializers.IntegerField(read_only=True, required=False)
    percent = serializers.FloatField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Disk
        fields = ['id', 'device', 'mountpoint', 'total', 'used', 'free', 'percent', 'created_time', 'updated_time']
        read_only_fields = ['id']


class NetworkSerializer(serializers.ModelSerializer):
    """
    Network Serializer
    """
    bytes_sent = serializers.IntegerField(read_only=True, required=False)
    bytes_recv = serializers.IntegerField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Network
        fields = ['id', 'bytes_sent', 'bytes_recv', 'created_time', 'updated_time']
        read_only_fields = ['id']


class GoodsSerializer(serializers.ModelSerializer):
    """
    Goods Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Goods
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class BinSerializer(serializers.ModelSerializer):
    """
    Bin Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Bin
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class StockSerializer(serializers.ModelSerializer):
    """
    Stock Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Stock
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class CapitalSerializer(serializers.ModelSerializer):
    """
    Capital Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Capital
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class SupplierSerializer(serializers.ModelSerializer):
    """
    Supplier Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Supplier
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Customer
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class ASNSerializer(serializers.ModelSerializer):
    """
    ASN Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.ASN
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class DNSerializer(serializers.ModelSerializer):
    """
    DN Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.DN
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class PurchaseSerializer(serializers.ModelSerializer):
    """
    Purchase Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Purchase
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class BarSerializer(serializers.ModelSerializer):
    """
    Bar Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Bar
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class FeeSerializer(serializers.ModelSerializer):
    """
    Fee Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Fee
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']


class DriverSerializer(serializers.ModelSerializer):
    """
    Fee Serializer
    """
    data = serializers.JSONField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = models.Fee
        fields = ['id', 'data', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']