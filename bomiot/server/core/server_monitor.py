import psutil
import time


def get_cpu_info():
    """获取 CPU 信息"""
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()

    print(f"CPU 使用率: {cpu_percent}%")
    print(f"物理 CPU 核心数: {cpu_count}")
    print(f"逻辑 CPU 核心数: {cpu_count_logical}")
    print(f"CPU 频率:  当前 {cpu_freq.current:.2f} MHz, 最小 {cpu_freq.min:.2f} MHz, 最大 {cpu_freq.max:.2f} MHz")


def get_memory_info():
    """获取内存信息"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    print(f"总内存: {memory.total / (1024 ** 3):.2f} GB")
    print(f"已使用内存: {memory.used / (1024 ** 3):.2f} GB")
    print(f"可用内存: {memory.available / (1024 ** 3):.2f} GB")
    print(f"内存使用率: {memory.percent}%")

    print(f"总交换空间: {swap.total / (1024 ** 3):.2f} GB")
    print(f"已使用交换空间: {swap.used / (1024 ** 3):.2f} GB")
    print(f"可用交换空间: {swap.free / (1024 ** 3):.2f} GB")
    print(f"交换空间使用率: {swap.percent}%")


def get_disk_info():
    """获取磁盘信息"""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"分区: {partition.device}")
        try:
            disk_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  挂载点: {partition.mountpoint}")
            print(f"  总容量: {disk_usage.total / (1024 ** 3):.2f} GB")
            print(f"  已使用容量: {disk_usage.used / (1024 ** 3):.2f} GB")
            print(f"  可用容量: {disk_usage.free / (1024 ** 3):.2f} GB")
            print(f"  使用率: {disk_usage.percent}%")
        except PermissionError:
            print(f"  无法访问 {partition.mountpoint} 的磁盘信息")


def get_network_info():
    """获取网络信息"""
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_recv = net_io_counters.bytes_recv

    print(f"网络发送字节数: {bytes_sent}")
    print(f"网络接收字节数: {bytes_recv}")


def monitor_server():
    """监控服务器状态"""
    while True:
        print("=" * 50)
        print("服务器状态监控信息")
        print("=" * 50)

        get_cpu_info()
        print("-" * 50)
        get_memory_info()
        print("-" * 50)
        get_disk_info()
        print("-" * 50)
        get_network_info()

        print("=" * 50)
        time.sleep(10)  # 每 10 秒监控一次


if __name__ == "__main__":
    monitor_server()