# Server monitoring

## Introduction

- **Bomiot** will monitor the server status every minute in real time
- The monitoring data will be saved to the database and send a signal to `server.py`
- Receive real-time signals through `server.py` to achieve server management, which will become very efficient

---

## Get server information

- After using the command `bomiot project <your_project>`, you will get a file structure

```shell
your-project/                 # Project directory
├── media/                    # Static files
│ ├── img/                    # Public images
│ └── ***.md                  # Various documents of md
├── __version__.py            # your_project version
├── bomiotconf.ini            # Bomiot project identification file
└── server.py                 # Server monitoring signal
setup.ini                     # Project configuration file
...

```

---

## `server.py`

```python
class ServerClass:
    def pid_get(self, data): # Running pid information
        print(data)

    def network_get(self, data): # Network information
        print(data)

    def disk_get(self, data): # Hard disk information
        print(data)

    def cpu_get(self, data): # CPU monitoring
        print(data)

    def memory_get(self, data): # Memory information
        print(data)
```