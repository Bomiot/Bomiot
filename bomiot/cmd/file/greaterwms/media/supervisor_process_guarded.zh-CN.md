#### Supervisor守护进程


#### CentOS配置
~~~shell
  yum install epel-release
  yum install -y supervisor
  pip3 install supervisor
~~~

#### Ubuntu配置
~~~shell
  apt-get update
  apt-get install supervisor -y
  pip3 install supervisor
~~~

#### 创建supervisor配置文件
~~~shell
  mkdir /etc/supervisor
  echo_supervisord_conf > /etc/supervisor/supervisord.conf
~~~

#### 配置参数
```shell
[program:greaterwms]
directory=/GreaterWMS/
user=root
command=daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
autostart=true
autorestart=true
startsecs=0
stopwaitsecs=0
stdout_logfile=/GreaterWMS/greaterwms_server_access.log
stderr_logfile=/GreaterWMS/greaterwms_server_err.log
redirect_stderr=true
```

#### 启动supervisor
~~~shell
  supervisord -c /etc/supervisor/supervisord.conf
~~~

#### 其他常用命令
~~~shell
  supervisorctl -c /etc/supervisor/supervisord.conf status
  supervisorctl -c /etc/supervisor/supervisord.conf reload
  supervisorctl -c /etc/supervisor/supervisord.conf update
~~~

#### 开机启动
~~~shell
  systemctl enable supervisord
~~~
