#### Docker deploy

- Using greaterwms under docker (this document is applicable to users with docker Foundation)


#### Install Or upgrade Docker Client
``` shell
sudo wget -qO- https://get.docker.com/ | bash
#### If you are prompted that there is no curl, execute sudo apt install curl or yum -y install curl
```

#### Install Docker Compose
``` shell
curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

#### Install Git
``` shell
#### Install git under Ubuntu
apt-get install git
#### Installing git under CentOS
yum install git
```

#### start deployment
``` shell
#### Pull code
git clone https://github.com/GreaterWMS/GreaterWMS.git

#### If there is no special need, you can directly start building or download the image from the official warehouse
#### If you have modified the corresponding code and need to rebuild the image,
#### please delete the local image first, see special instructions
#### Baseurl needs to be modified before running the project JS content
vim templates/public/statics/baseurl.pjs #### modify 127.0.0.1 to the IP address of the server

#### Granting execution permissions to front-end and back-end startup scripts
chmod +x web_start.sh
chmod +x backend_start.sh

#### Building containers
docker-compose build

#### Start project
#### Special note: After executing the startup command, it may take about 10 minutes to start. Please be patient and wait
docker-compose up -d
```

#### release front-end code
``` shell
#### Enter the front container
docker exec -it greaterwms_front /bin/bash
#### Enter the templates directory in the container
cd templates

#### Compile front-end code
quasar build
```

#### Release front-end code
``` shell
#### Entering the front-end container
docker exec -it greaterwms_front /bin/bash

#### Enter the templates directory inside the container
cd templates

#### Compile front-end code
quasar build

#### At this point, exit the container and restart the backend image. The command is as follows
docker restart greaterwms_backend
```

#### View the  supervisor access log
``` shell
#### The backend access log is the greaterwms in the project directory greaterwms_server_access.log
#### Instantly output the latest content of this file
tail -f greaterwms_server_access.log
```

![image-01](/media/img/jishi.jpg){ loading=lazy style="max-width: 100%" }

#### Access Portal

``` shell
Front end: http://127.0.0.1:8080 Or http://Server IP:8080

Backend: http://127.0.0.1:8008 Or http://Server IP:8008
```

#### Special instructions

``` shell
#### View front-end startup logs
docker logs -f greaterwms_front

#### View backend startup logs
docker logs -f greaterwms_backend

#### Web under project directory backend_start.sh and backend_ It is recommended not to modify the start.sh and front-end and back-end startup scripts for the first time. You can modify them according to your own needs in the future
#### Entering the front-end container
docker exec -it greaterwms_front /bin/bash

#### Entering the backend container
docker exec -it greaterwms_backend /bin/bash

#### Delete Local Images
docker rmi -f greaterwms:front
docker rmi -f greaterwms:backend
```
