
#### Nginx Config


#### CentOS

##### Install Dependencies
~~~shell
  yum -y install gcc-c++ zlib-devel openssl openssl-devel gd-devel
~~~

##### Download Nginx-1.14.1
~~~shell
  wget https://nginx.org/download/nginx-1.14.1.tar.gz
~~~

##### Tar Nginx
~~~shell
  tar zxvf nginx-1.14.1.tar.gz
  cd nginx-1.14.1
  ./configure --prefix=/usr/local/nginx --user=www --group=www --with-pcre  --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-http_image_filter_module --with-http_slice_module --with-mail --with-threads --with-file-aio --with-stream --with-mail_ssl_module --with-stream_ssl_module
  make && make install
~~~

##### Configure soft links
~~~shell
  ln -s /usr/local/nginx/sbin/nginx /usr/bin/
~~~

##### Check if the configuration file is ok
~~~shell
  nginx -t
~~~

##### Show Results
~~~shell
  nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
  nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful
~~~

##### Run Nginx
~~~shell
  nginx
~~~

#### Ubuntu

##### Install Dependencies
~~~shell
  sudo apt-get update
  sudo apt-get install build-essential
  sudo apt-get install libtool
  sudo apt-get install libpcre3 libpcre3-dev
  sudo apt-get install zlib1g-dev
  sudo apt-get install libssl-dev
~~~

##### Download Nginx-1.14.1
~~~shell
  wget https://nginx.org/download/nginx-1.14.1.tar.gz
~~~

##### Tar Nginx
~~~shell
  tar zxvf nginx-1.14.1.tar.gz
  cd nginx-1.14.1
  ./configure --prefix=/usr/local/nginx --user=www --group=www --with-pcre  --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-http_image_filter_module --with-http_slice_module --with-mail --with-threads --with-file-aio --with-stream --with-mail_ssl_module --with-stream_ssl_module
  make && make install
~~~

##### Configure soft links
~~~shell
  ln -s /usr/local/nginx/sbin/nginx /usr/bin/
~~~

##### Check if the configuration file is ok
~~~shell
  nginx -t
~~~

##### Show Results
~~~shell
  nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
  nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful
~~~

##### Run Nginx
~~~shell
  nginx
~~~



##### Nginx Server Status
~~~shell
  #### Check the nginx profile is ok
    nginx -t
  #### Reload the Nginx server
    nginx -s reload
  #### Kill Nginx server
    killall nginx
~~~

#### http Deply
~~~shell
  find / -name nginx.conf
  vim /usr/local/nginx/conf/nginx.conf
~~~

- Copy behind code

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

#### SSL Deply
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
		server_name { your domin };
		rewrite ^(.*)$ https://{ your domin }$1;
	}
	server {
		listen      443 ssl;
		server_name  { your domin };
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
