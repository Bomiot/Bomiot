#### Nginx配置


#### CentOS

##### 安装前置依赖
~~~shell
  yum -y install gcc-c++ zlib-devel openssl openssl-devel gd-devel
~~~

##### 下载nginx-1.14.1源码安装包
~~~shell
  wget https://nginx.org/download/nginx-1.14.1.tar.gz
~~~

##### 解压并开始编译安装
~~~shell
  tar zxvf nginx-1.14.1.tar.gz
  cd nginx-1.14.1
  ./configure --prefix=/usr/local/nginx --user=www --group=www --with-pcre  --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-http_image_filter_module --with-http_slice_module --with-mail --with-threads --with-file-aio --with-stream --with-mail_ssl_module --with-stream_ssl_module
  make && make install
~~~

##### 配置软链接
~~~shell
  ln -s /usr/local/nginx/sbin/nginx /usr/bin/
~~~

##### 检查配置文件是否正常
~~~shell
  nginx -t
~~~

##### 显示结果
~~~shell
  nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
  nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful
~~~

##### 启动服务
~~~shell
  nginx
~~~

#### Ubuntu

##### 安装前置依赖
~~~shell
  sudo apt-get update
  sudo apt-get install build-essential
  sudo apt-get install libtool
  sudo apt-get install libpcre3 libpcre3-dev
  sudo apt-get install zlib1g-dev
  sudo apt-get install libssl-dev
~~~

##### 下载nginx-1.14.1源码安装包
~~~shell
  wget https://nginx.org/download/nginx-1.14.1.tar.gz
~~~

##### 解压并开始编译安装
~~~shell
  tar zxvf nginx-1.14.1.tar.gz
  cd nginx-1.14.1
  ./configure --prefix=/usr/local/nginx --user=www --group=www --with-pcre  --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-http_image_filter_module --with-http_slice_module --with-mail --with-threads --with-file-aio --with-stream --with-mail_ssl_module --with-stream_ssl_module
  make && make install
~~~

##### 配置软链接
~~~shell
  ln -s /usr/local/nginx/sbin/nginx /usr/bin/
~~~

##### 检查配置文件是否正常
~~~shell
  nginx -t
~~~

##### 显示结果
~~~shell
  nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
  nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful
~~~

##### 启动服务
~~~shell
  nginx
~~~

##### 服务状态描述
~~~shell
  #### 检测配置文件是否包含语法错误
    nginx -t
  #### 重新加载配置文件,不会中断服务
    nginx -s reload
  #### 关闭nginx服务
    killall nginx
~~~

#### http部署
~~~shell
  find / -name nginx.conf
  vim /usr/local/nginx/conf/nginx.conf
~~~

- 复制以下内容

```shell
user root;
worker_processes auto;

events {
    worker_connections  1024;
}

http {
    include         mime.types;
    default_type    application/octet-stream;
    sendfile        on;
    gzip            on;
    gzip_min_length 1k;
    gzip_comp_level 4;
    gzip_types      text/plain application/javascript application/x-javascript text/javascript text/xml text/css;
    gzip_disable    "MSIE [1-6]\.";
    gzip_vary       on;
	proxy_redirect off;
	proxy_set_header Host $host;
	proxy_set_header  https $https;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	client_max_body_size 75M;
	client_body_buffer_size 256k;
	client_header_timeout 3m;
	client_body_timeout 3m;
	send_timeout 3m;
	proxy_connect_timeout 300s;
	proxy_read_timeout 300s;
	proxy_send_timeout 300s;
	proxy_buffer_size 64k;
	proxy_buffers 4 32k;
	proxy_busy_buffers_size 64k;
	proxy_temp_file_write_size 64k;
	proxy_ignore_client_abort on;

	server {
		listen      80;
		server_name 127.0.0.1;
		location / {
			#root   html;
			#index  testssl.html index.html index.htm;
			proxy_redirect off;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_pass http://127.0.0.1:8008/;
		}
		location /static/ {
			alias /GreaterWMS/static_new/;
		}
		location /media/ {
			alias /GreaterWMS/media/;
		}
	}
}
```

#### SSL部署
~~~shell
  vim /usr/local/nginx/conf/nginx.conf
~~~

```shell
user root;
worker_processes auto;

events {
    worker_connections  1024;
}

http {
    include         mime.types;
    default_type    application/octet-stream;
    sendfile        on;
    gzip            on;
    gzip_min_length 1k;
    gzip_comp_level 4;
    gzip_types      text/plain application/javascript application/x-javascript text/javascript text/xml text/css;
    gzip_disable    "MSIE [1-6]\.";
    gzip_vary       on;
	proxy_redirect off;
	proxy_set_header Host $host;
	proxy_set_header  https $https;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	client_max_body_size 75M;
	client_body_buffer_size 256k;
	client_header_timeout 3m;
	client_body_timeout 3m;
	send_timeout 3m;
	proxy_connect_timeout 300s;
	proxy_read_timeout 300s;
	proxy_send_timeout 300s;
	proxy_buffer_size 64k;
	proxy_buffers 4 32k;
	proxy_busy_buffers_size 64k;
	proxy_temp_file_write_size 64k;
	proxy_ignore_client_abort on;

	upstream GreaterWMS{
		server 127.0.0.1:8008;
	}
	server {
		listen      80;
		server_name { 你的域名 };
		rewrite ^(.*)$ https://{ 你的域名 }$1;
	}
	server {
		listen      443 ssl;
		server_name  { 你的域名 };
		root /path/to/GreaterWMS;
		charset utf-8;
		add_header X-Frame-Options "SAMEORIGIN";、
		add_header X-XSS-Protection "1; mode=block";
		add_header X-Content-Type-Options "nosniff";
		client_max_body_size 75M;
		ssl_certificate   /path/to/GreaterWMS/cert/GreaterWMS.pem;
		ssl_certificate_key  /path/to/GreaterWMS/cert/GreaterWMS.key;
		ssl_session_timeout 5m;
		ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
		ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
		ssl_prefer_server_ciphers on;
		access_log off;
		error_log  /path/to/GreaterWMS/greaterwms-error.log error;
		location /websocket/ {
			proxy_pass http://GreaterWMS/;
			proxy_read_timeout 60s;
			proxy_set_header Host $host;
			proxy_set_header X-Real_IP $remote_addr;
			proxy_set_header X-Forwarded-for $remote_addr;
			proxy_http_version 1.1;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection 'Upgrade';
		}
		location / {
			#root   html;
			#index  testssl.html index.html index.htm;
			proxy_redirect off;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_pass http://GreaterWMS/;
		}
		location /static/ {
			alias /path/to/GreaterWMS/static_new/;
		}
		location /media/{
			alias /path/to/GreaterWMS/media/;
		}
	}
}
```
