

#### GreaterWMS仓库管理生态系统群晖NAS用docker部署

[原文地址](https://blog.csdn.net/wbsu2004/article/details/128392486)

#### 安装 Git

> 套件中心 → 设置 --> 套件来源 --> 新增

![image-01](/media/img/nas1.png){ loading=lazy style="max-width: 100%" }

~~~shell
  名称：随意
  位置：http://packages.synocommunity.com/
~~~

> 套件中心 --> 社群，找到并安装套件 Git

![image-02](/media/img/nas2.png){ loading=lazy style="max-width: 100%" }

#### 下载代码

> 用 SSH 客户端连到群晖，依次执行下面的命令

~~~shell
  # 进入 docker 目录
  cd /volume2/docker
  # 国内用户使用 gitee 克隆项目到您的本地或服务器
  git clone https://gitee.com/Singosgu/GreaterWMS.git
  # 国外用户还是用 github
  git clone https://github.com/GreaterWMS/GreaterWMS.git
  # 进入目录
  cd GreaterWMS
~~~

![image-03](/media/img/nas3.png){ loading=lazy style="max-width: 100%" }

#### 修改 docker-compose.yml

> 主要就是端口，本地端口不冲突就行，不确定的话可以用命令查一下

~~~shell
  # 查看端口占用
  netstat -tunlp | grep 端口号
~~~

> 在 GreaterWMS 根目录中找到 docker-compose.yml 文件

![image-04](/media/img/nas4.png){ loading=lazy style="max-width: 100%" }

#### 默认 docker-compose.yml 中的端口设置是👇这样的

| 镜像  | 本地端口  |	容器端口 |
|:----| :---------:|--------:|
|   front  | 8080|8080|
|   backend  | 8000|8000|

![image-05](/media/img/nas5.png){ loading=lazy style="max-width: 100%" }

#### 老苏找了两个连续的空闲本地端口做了修改

| 镜像  | 本地端口  |	容器端口 |
|:----| :---------:|--------:|
|   front  | 8285|8080|
|   backend  | 8286|8000|

![image-06](/media/img/nas6.png){ loading=lazy style="max-width: 100%" }

![image-07](/media/img/nas7.png){ loading=lazy style="max-width: 100%" }

#### 修改 baseurl.txt

> 在 File Station 中找到 /docker/GreaterWMS/templates/public/statics/baseurl.txt 文件

> 将 http://127.0.0.1:8000 ，改为本机 IP + 本地端口，老苏群晖 IP 为 192.168.0.197，结合前面修改的端口，所以这里改为 http://192.168.0.197:8286

![image-08](/media/img/nas8.png){ loading=lazy style="max-width: 100%" }

#### 修改 nginx.conf

> 默认 docker-compose.yml 中并没有启用 nginx，所以改不改应该没啥关系；

> 在 GreaterWMS 根目录中找到 nginx.conf 文件

![image-09](/media/img/nas9.png){ loading=lazy style="max-width: 100%" }

> 找到 server 127.0.0.1:8008;

![image-10](/media/img/nas10.png){ loading=lazy style="max-width: 100%" }

> 改为 server 192.168.0.197:8285;

![image-11](/media/img/nas11.png){ loading=lazy style="max-width: 100%" }

#### 启动

> 准备工作完成后，就可以开始启动了

~~~shell
  # 一键启动
  docker-compose up -d
~~~

> 按照官方的特别备注：执行 docker-compose up -d 后会自动下载前端依赖，有时会下载失败，导致前端无法启动，此时先执行 docker-compose down 再docker-compose up -d 重新下载，直至成功为止。

> 第一次运行会拉取镜像，容量不小

![image-12](/media/img/nas12.png){ loading=lazy style="max-width: 100%" }

> 看到两个 done 就完成了

![image-13](/media/img/nas13.png){ loading=lazy style="max-width: 100%" }

#### 可以进群晖的容器看一下状态

> 前端内存占用多，后端CPU占用高，而且一直都比较稳定；

![image-14](/media/img/nas14.png){ loading=lazy style="max-width: 100%" }

> 一般不出意外的话，应该都是能正常工作的

#### 编译前端

> 不编译的话，访问后端地址不能登录，会一直显示网络错误

~~~shell
  # 进入前端容器
  docker exec -it greaterwms_front /bin/bash
  # 编译前端代码
  quasar build
~~~

![image-15](/media/img/nas15.png){ loading=lazy style="max-width: 100%" }

> 编译完成

![image-16](/media/img/nas16.png){ loading=lazy style="max-width: 100%" }

> 我们可以在 /docker/GreaterWMS/templates/dist/spa 中看到生成的前端代码

![image-17](/media/img/nas17.png){ loading=lazy style="max-width: 100%" }

> 然后先删再启动

~~~shell
  # 一键卸载
  docker-compose down
  # 再一键启动
  docker-compose up -d
~~~

![image-18](/media/img/nas18.png){ loading=lazy style="max-width: 100%" }

#### 运行

> 是否可以浏览还需要看日志

> 后端要看到 Starting development server at http://0.0.0.0:8000/

![image-19](/media/img/nas19.png){ loading=lazy style="max-width: 100%" }

> 前端要看到 ℹ ｢wds｣: Project is running at http://0.0.0.0:8080/

![image-20](/media/img/nas20.png){ loading=lazy style="max-width: 100%" }

> 现在可以开始访问了，在浏览器中输入 http://群晖IP:8285 或者 http://群晖IP:8286都是能看到主界面的，所不同的是，从 8285 打开的话，右下角有个绿色的 vConsole 按钮，感觉像是调试用的

![image-21](/media/img/nas21.png){ loading=lazy style="max-width: 100%" }

> 首先注册一个管理员账号，完成后就是主界面了

![image-22](/media/img/nas22.png){ loading=lazy style="max-width: 100%" }

> 功能就留个需要的人自己研究吧

![image-23](/media/img/nas23.png){ loading=lazy style="max-width: 100%" }

[部署视频](https://www.bilibili.com/video/BV1Vo4y1P7yz/)
