#### Supervisor Process Guarded


#### CentOS
~~~shell
  yum install epel-release
  yum install -y supervisor
  pip3 install supervisor
~~~

#### Ubuntu
~~~shell
  apt-get update
  apt-get install supervisor -y
  pip3 install supervisor
~~~

#### Create supervisor config
~~~shell
  mkdir /etc/supervisor
  echo_supervisord_conf > /etc/supervisor/supervisord.conf
~~~

#### Profile
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

#### Run supervisor
~~~shell
  supervisord -c /etc/supervisor/supervisord.conf
~~~

#### Other Command
~~~shell
  supervisorctl -c /etc/supervisor/supervisord.conf status
  supervisorctl -c /etc/supervisor/supervisord.conf reload
  supervisorctl -c /etc/supervisor/supervisord.conf update
~~~

#### System start
~~~shell
  systemctl enable supervisord
~~~
