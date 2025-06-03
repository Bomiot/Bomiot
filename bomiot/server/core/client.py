import psutil

from rest_framework import viewsets

from . import serializers, models, filter
from .page import CorePageNumberPagination
from .permission import NormalPermission
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from .message import others_message_return

from django.db.models import Sum


class PIDList(viewsets.ModelViewSet):
    """
        list:
            Response a PID data list（all）
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.PidsFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {}
            query_data['is_delete'] = False
            query_data['name__icontains'] = self.request.query_params.get('search')
            return models.Pids.objects.filter(**query_data).order_by('-memory_usage', '-cpu_usage')
        else:
            return models.Pids.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.PidsSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class CPUList(viewsets.ModelViewSet):
    """
        list:
            Response a CPU data list（all）
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.CPUFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {}
            query_data['is_delete'] = False
            return models.CPU.objects.filter(**query_data).order_by('-id')
        else:
            return models.CPU.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.CPUSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class MemoryList(viewsets.ModelViewSet):
    """
        list:
            Response a Memory data list（all）
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.MemoryFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {}
            query_data['is_delete'] = False
            return models.Memory.objects.filter(**query_data).order_by('-id')
        else:
            return models.Memory.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.MemorySerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class DiskList(viewsets.ModelViewSet):
    """
        list:
            Response a Disk data list（all）
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.DiskFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {}
            query_data['is_delete'] = False
            return models.Disk.objects.filter(**query_data).order_by('-id')
        else:
            return models.Disk.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.DiskSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class NetworkList(viewsets.ModelViewSet):
    """
        list:
            Response a Network data list（all）
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.NetworkFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {}
            query_data['is_delete'] = False
            return models.Network.objects.filter(**query_data).order_by('-id')
        else:
            return models.Network.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.NetworkSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ServerChartsPage(CorePageNumberPagination):
    def __init__(self, *args, **kwargs):
        self.cpu_data = {}
        self.cpu_data['xAxis_list'] = []
        self.cpu_usage_list = []

        self.memory_data = {}
        self.memory_data['xAxis_list'] = []
        self.memory_used_list = []
        self.memory_free_list = []

        self.disk_data = {}
        self.disk_data['xAxis_list'] = []
        self.disk_used_list = []
        self.disk_free_list = []

        self.network_data = {}
        self.network_data['xAxis_list'] = []
        self.bytes_sent_list = []
        self.bytes_recv_list = []
        super(ServerChartsPage, self).__init__(*args, **kwargs)


    def get_cpu_return_data(self, data) -> dict:
        self.cpu_data['xAxis_list'].append(data.created_time.strftime("%H:%M"))
        self.cpu_usage_list.append(data.cpu_usage)
        return data
    
    def get_memory_return_data(self, data) -> dict:
        self.memory_data['xAxis_list'].append(data.created_time.strftime("%H:%M"))
        self.memory_used_list.append(data.used)
        self.memory_free_list.append(data.free)
        return data

    def get_network_return_data(self, data) -> dict:
        self.network_data['xAxis_list'].append(data.created_time.strftime("%H:%M"))
        self.bytes_sent_list.append(data.bytes_sent)
        self.bytes_recv_list.append(data.bytes_recv)
        return data
    
    def query_data_add(self) -> list:
        cpu_list = models.CPU.objects.filter().order_by('-id')[:30]
        cpu_data_list = list(map(lambda data: self.get_cpu_return_data(data), cpu_list))
        
        memory_list = models.Memory.objects.filter().order_by('-id')[:30]
        memory_data_list = list(map(lambda data: self.get_memory_return_data(data), memory_list))

        partitions = psutil.disk_partitions()
        for i in range(len(partitions)):
            try:
                disk_usage = psutil.disk_usage(partitions[i].mountpoint)
                self.disk_data['xAxis_list'].append(partitions[i].mountpoint)
                self.disk_used_list.append(float(disk_usage.used))
                self.disk_free_list.append(float(disk_usage.free))
            except PermissionError:
                print(f"{partitions[i].mountpoint}")

        network_list = models.Network.objects.filter().order_by('-id')[:30]
        network_data_list = list(map(lambda data: self.get_network_return_data(data), network_list))
        
        self.cpu_data['xAxis_list'] = list(reversed(self.cpu_data['xAxis_list']))
        self.cpu_data['title'] = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "CPU Info")
        self.cpu_data['series_list'] = [
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "CPU Usage"), 'data': list(reversed(self.cpu_usage_list)) }
        ]

        self.memory_data['xAxis_list'] = list(reversed(self.memory_data['xAxis_list']))
        self.memory_data['title'] = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Memory Info")
        self.memory_data['series_list'] = [
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Memory Usad"), 'data': list(reversed(self.memory_used_list)) },
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Memory Free"), 'data': list(reversed(self.memory_free_list)) },
        ]

        self.disk_data['title'] = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Disk Info")
        self.disk_data['series_list'] = [
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Disk Used"), 'data': self.disk_used_list },
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Disk Free"), 'data': self.disk_free_list },
        ]

        self.network_data['xAxis_list'] = list(reversed(self.network_data['xAxis_list']))
        self.network_data['title'] = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Network Info")
        self.network_data['series_list'] = [
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Bytes Sent"), 'data': list(reversed(self.bytes_sent_list)) },
            { 'name': others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Bytes Received"), 'data': list(reversed(self.bytes_recv_list)) },
        ]
        return [
            ("cpu_data", self.cpu_data),
            ("memory_data", self.memory_data),
            ("disk_data", self.disk_data),
            ("network_data", self.network_data)
        ]

class ServerCharts(viewsets.ModelViewSet):
    """
        list:
            Response a Server Charts data list（all）
    """
    pagination_class = ServerChartsPage
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.NetworkFilter

    def get_queryset(self):
        return models.Network.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.NetworkSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class PIDChartsPage(CorePageNumberPagination):
    def __init__(self, *args, **kwargs):
        self.pid_data = {}
        self.pid_data['title'] = 'PID Tree Map'
        self.pid_series_list = []
        super(PIDChartsPage, self).__init__(*args, **kwargs)
    
    def get_pid_return_data(self, data) -> dict:
        pid_append_data = {}
        pid_append_data['name'] = data.get('name')
        pid_append_data['value'] = data.get('total_memory')
        self.pid_series_list.append(pid_append_data)
        return data

    def query_data_add(self) -> list:
        pid_list = models.Pids.objects.values('name').annotate(total_memory=Sum('memory')).order_by('-total_memory')
        pid_data_list = list(map(lambda data: self.get_pid_return_data(data), pid_list))
        self.pid_data['series_list'] = self.pid_series_list

        return [
            ("pid_data", self.pid_data),
        ]

class PIDCharts(viewsets.ModelViewSet):
    """
        list:
            Response a PID Charts data list（all）
    """
    pagination_class = PIDChartsPage
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.PidsFilter

    def get_queryset(self):
        return models.Pids.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.PidsSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)