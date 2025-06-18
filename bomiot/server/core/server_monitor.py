import time
import psutil
import threading
import pypistats
import orjson
from datetime import datetime, timedelta
from .models import Pids, PyPi, CPU, Memory, Disk, Network
from .utils import readable_file_size
from .signal import bomiot_signals

pypi_stats_list = []

class ServerManager:
    def __init__(self):
        """init server manager"""
        pass
    
    def get_cpu_info(self):
        """CPU"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_info_check = CPU.objects.filter()
        if cpu_info_check.count() >= 10080:
            cpu_info_check.order_by('id').first().delete()
        cpu_data = CPU.objects.create(
                   cpu_usage=float(f"{cpu_percent:.2f}"),
                   physical_cores=int(cpu_count),
                   logical_cores=int(cpu_count_logical),
                   cpu_frequency=f"{cpu_freq.current:.2f} MHz",
                   min_cpu_frequency=f"{cpu_freq.min:.2f} MHz",
                   max_cpu_frequency=f"{cpu_freq.max:.2f} MHz"
                   )
        bomiot_signals.send(msg={
            'models': 'CPU',
            'type': 'created',
            'data': {
                'id': cpu_data.id,
                'cpu_usage': float(f"{cpu_percent:.2f}"),
                'physical_cores': int(cpu_count),
                'logical_cores': int(cpu_count_logical),
                'cpu_frequency': f"{cpu_freq.current:.2f} MHz",
                'min_cpu_frequency': f"{cpu_freq.min:.2f} MHz",
                'max_cpu_frequency': f"{cpu_freq.max:.2f} MHz"
            }
        })

    def get_memory_info(self):
        """Memory"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memory_info_check = Memory.objects.filter()
        if memory_info_check.count() >= 10080:
            memory_info_check.order_by('id').first().delete()
        memory_data = Memory.objects.create(
                      total=int(memory.total),
                      used=int(memory.used),
                      free=int(memory.free),
                      percent=float(f'{memory.percent:.2f}'),
                      swap_total=int(swap.total),
                      swap_used=int(swap.used),
                      swap_free=int(swap.free),
                      swap_percent=float(f'{swap.percent:.2f}'),
                      )
        bomiot_signals.send(msg={
            'models': 'Memory',
            'type': 'created',
            'data': {
                'id': memory_data.id,
                'total': int(memory.total),
                'used': int(memory.used),
                'free': int(memory.free),
                'percent': float(f'{memory.percent:.2f}'),
                'swap_total': int(swap.total),
                'swap_used': int(swap.used),
                'swap_free': int(swap.free),
                'swap_percent': float(f'{swap.percent:.2f}')
            }
        })

    def get_disk_info(self):
        """Disk"""
        Disk.objects.all().delete()  # Clear all previous records
        partitions = psutil.disk_partitions()
        disk_list = []
        for i in range(len(partitions)):
            try:
                disk_usage = psutil.disk_usage(partitions[i].mountpoint)
                disk_detail = Disk(
                    id=i+1,
                    device=partitions[i].device,
                    mountpoint=partitions[i].mountpoint,
                    total=int(disk_usage.total),
                    used=int(disk_usage.used),
                    free=int(disk_usage.free),
                    percent=float(f'{disk_usage.percent:.2f}')
                )
                bomiot_signals.send(msg={
                    'models': 'Disk',
                    'type': 'created',
                    'data': {
                        'id': i+1,
                        'device': partitions[i].device,
                        'mountpoint': partitions[i].mountpoint,
                        'total': int(disk_usage.total),
                        'used': int(disk_usage.used),
                        'free': int(disk_usage.free),
                        'percent': float(f'{disk_usage.percent:.2f}')
                    }
                })
                disk_list.append(disk_detail)
            except PermissionError:
                print(f"{partitions[i].mountpoint}")
                continue
        if len(disk_list) > 0:
            Disk.objects.bulk_create(disk_list, batch_size=100)

    def get_network_info(self):
        """Network"""
        net_io_counters = psutil.net_io_counters()
        bytes_sent = net_io_counters.bytes_sent
        bytes_recv = net_io_counters.bytes_recv
        newtork_info_check = Network.objects.filter()
        if newtork_info_check.count() >= 10080:
            newtork_info_check.order_by('id').first().delete()
        instance = Network.objects.create(
                   bytes_sent=int(bytes_sent),
                   bytes_recv=int(bytes_recv)
                   )
        bomiot_signals.send(msg={
            'models': 'Network',
            'type': 'created',
            'data': {
                'id': instance.id,
                'bytes_sent': int(bytes_sent),
                'bytes_recv': int(bytes_recv)
            }
        })

    def get_pid(self):
        """PIDs"""
        Pids.objects.all().delete()  # Clear all previous records
        pid_add_list = []
        data_list = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time', 'memory_percent', 'cpu_percent']):
            try:
                info = proc.info
                pid = info['pid']
                if pid == 0:
                    continue
                name = info['name']
                mem_rss = info['memory_info'].rss
                create_time = info['create_time']
                mem_percent = info['memory_percent']
                cpu_percent = info['cpu_percent']
                item = {
                    'pid': int(pid),
                    'name': str(name),
                    'memory': int(mem_rss),
                    'create_time': datetime.fromtimestamp(create_time),
                    'memory_usage': round(float(mem_percent), 2),
                    'cpu_usage': round(float(cpu_percent), 2)
                }
                pid_add = Pids(**item)
                pid_add_list.append(pid_add)
                data_list.append(item)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        Pids.objects.bulk_create(pid_add_list, batch_size=200)  # Bulk create PIDs to improve performance
        bomiot_signals.send(msg={
            'models': 'Pids',
            'type': 'created',
            'data': data_list
        })

    def cteate_pypi_database(self, data):
        return PyPi(
            date=data.get('date'),
            downloads=data.get('downloads'),
            percent=data.get('percent'),
            category=data.get('category')
        )

    def res_pypi_data(self, data):
        data["date"] = datetime.strptime(data.get('date'), '%Y-%m-%d')
        data["percent"] = float(data.get('percent').split('%')[0])
        return data

    def get_pypi_stats(self):
        today = datetime.now().date()
        pypi_today_qs = PyPi.objects.filter(created_time__date=today)
        if pypi_today_qs.exists() is False:
            PyPi.objects.exclude(created_time__date=today).delete()
            df = pypistats.overall("bomiot", total='daily', format="pandas")
            res = df.to_dict(orient="records")
            pypi_list = []
            for record in res:
                if record.get('category') == 'Total':
                    continue
                data = self.res_pypi_data(record)
                pypi_obj = self.cteate_pypi_database(data)
                pypi_list.append(pypi_obj)
            pypi_list.sort(key=lambda x: x.date, reverse=True)
            PyPi.objects.bulk_create(pypi_list, batch_size=200)

    def monitor_server(self):
        """Monitor server status"""
        while True:
            self.get_cpu_info()
            self.get_memory_info()
            self.get_disk_info()
            self.get_network_info()
            self.get_pid()
            self.get_pypi_stats()
            time.sleep(60)  # Perform monitoring every 60 seconds


def start_monitoring():
    """Start the server monitoring thread"""
    server_manager = ServerManager()
    monitoring_thread = threading.Thread(target=server_manager.monitor_server, daemon=True)
    monitoring_thread.start()
