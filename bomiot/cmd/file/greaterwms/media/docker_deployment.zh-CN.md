#### 使用Docker 部署

- Docker下使用GreaterWMS（本文档适用于具备Docker基础的用户使用）

#### 安装或升级Docker客户端

``` shell
#### 如果提示没有curl再执行sudo apt install curl 或 yum -y install curl
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

#### 配置加速器（国内）

``` shell
sudo mkdir -p /etc/docker
sudo vim /etc/docker/daemon.json
{
  "registry-mirrors": ["https://w61q8mf4.mirror.aliyuncs.com"]
}
sudo systemctl daemon-reload
sudo systemctl enable docker
sudo systemctl restart docker
```

#### 安装Docker-compose
```shell
curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 安装git
``` shell
#### Ubuntu下安装git
apt-get install git

#### CentOS下安装git
yum install git
```

#### 开始部署
```shell
#### 拉取代码
git clone https://github.com/GreaterWMS/GreaterWMS.git

#### 修改Dockerfile
#### 说明1：如果您是在国内，希望由自己构建镜像而非从官方仓库中拉取镜像请
#### 打开Dockerfile里第10，11，16，17，35，37行的注释，将依赖的下载源配置为国内源
#### 说明2：如果您修改了相应代码，需要重新构建镜像，请先删除本地镜像，见特别说明
```

![image-02](/media/img/1685295993775.jpg){ loading=lazy style="max-width: 100%" }
![image-04](/media/img/1685296149228.jpg){ loading=lazy style="max-width: 100%" }


##### 如果希望直接下载官方仓库的镜像，请修改docker-compose.yml,将6至9的代码和23至26行代码注释掉

![image-03](/media/img/docker.jpg){ loading=lazy style="max-width: 100%" }

#### 开始运行前的准备工作

``` shell
#### 修改baseurl,将127.0.0.1修改为服务器的IP地址，如果是本地就不用修改
vim templates/public/statics/baseurl.js

#### 为前后端启动脚本赋执行权限
chmod +x web_start.sh
chmod +x backend_start.sh

#### 构建容器
docker-compose build

#### 启动项目
docker-compose up -d

#### 特别备注：执行启动命令后可能会花十分钟左右的时间来进行启动，请耐心等待
#### 特别备注：用户也可以在settings.py中改成mysql或者其他数据库，具体配置可自行研究
```

#### 发布前端代码

``` shell
#### 进入前端容器
docker exec -it greaterwms_front /bin/bash

#### 容器内进入templates目录
cd templates

#### 编译前端代码
quasar build

#### 此时退出容器，再重启后端镜像即可，命令如下
docker restart greaterwms_backend
```

#### 查看supervisord访问日志
``` shell
#### 即后端访问日志,项目目录下的greaterwms_server_access.log
#### 即时输出此文件最新的内容
tail -f greaterwms_server_access.log
```
![image-01](/media/img/jishi.jpg){ loading=lazy style="max-width: 100%" }

#### 访问入口
``` shell
前端：http://127.0.0.1:8080 或者 http://服务器IP:8080

后端：http://127.0.0.1:8008 或者 http://服务器IP:8008
```

#### 特别说明
``` shell
#### 查看前端启动日志
docker logs -f greaterwms_front

#### 查看后端启动日志
docker logs -f greaterwms_backend

#### 进入前端容器
docker exec -it greaterwms_front /bin/bash

#### 进入后端容器
docker exec -it greaterwms_backend /bin/bash

#### 删除本地镜像
docker rmi -f greaterwms:front
docker rmi -f greaterwms:backend

#### 项目目录下的web_start.sh和backend_start.sh为前后端启动脚本
#### 首次运行建议不要修改，后续可根据自身需要进行修改
```
