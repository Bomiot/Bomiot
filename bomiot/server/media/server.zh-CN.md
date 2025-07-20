# 服务器监控

## 介绍

- **Bomiot** 会实时每分钟，对服务器状态进行一次监控
- 监控数据会被保存到数据库，并向`server.py`发送信号
- 通过`server.py`接收实时信号，从而实现服务器管理，这将变得非常高效

---

## 获取服务器信息

- 使用命令 `bomiot project <your_project>` 后，你会得到一个文件结构

```shell
your-project/                  # 项目目录
├── media/                     # 静态文件
│   ├── img/                   # 公用图片       
│   └── ***.md                 # md的各种文档
├── __version__.py             # your_project版本
├── bomiotconf.ini             # Bomiot项目标识文件
└── server.py                  # 服务器监控信号
setup.ini                      # 项目配置文件
...

```

---

## `server.py`

```python
class ServerClass:
    def pid_get(self, data):        # 运行中的pid信息
        print(data)
    
    def network_get(self, data):    # 网络信息
        print(data)

    def disk_get(self, data):       # 硬盘信息
        print(data)

    def cpu_get(self, data):        # CPU监控
        print(data)

    def memory_get(self, data):     # 内存信息
        print(data)
```
