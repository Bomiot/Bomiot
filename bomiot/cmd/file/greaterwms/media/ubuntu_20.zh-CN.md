#### Ubuntu20部署说明


<h4>
  <a href="https://www.bilibili.com/video/BV15X4y1g7Ed/?share_source=copy_web&vd_source=22a376f853fb151b9c8909e926f7bf0b">视频教程</a>
</h4>

#### 升级版本
~~~shell
  apt update
  apt upgrade
  apt install build-essential openssl libssl-dev
  apt install vim
~~~

#### 安装Node
~~~shell
  wget https://nodejs.org/dist/v14.19.3/node-v14.19.3-linux-x64.tar.gz
  tar zvxf node-v14.19.3-linux-x64.tar.gz -C /usr/local
~~~

#### 环境变量设置
~~~shell
  echo '''export NODE_HOME=/usr/local/node-v14.19.3-linux-x64 export PATH=$PATH:$NODE_HOME/bin export NODE_PATH=$NODE_HOME/lib/node_modules''' /etc/profile
~~~

#### 使环境变量立即生效
~~~shell
  source /etc/profile
~~~

#### 软连接Node和NPM
~~~shell
  ln -sf /usr/local/node-v14.19.3-linux-x64/bin/node /usr/bin/node
  ln -s /usr/local/node-v14.19.3-linux-x64/bin/npm /usr/bin/npm
~~~

#### 验证node是否安装成功
~~~shell
  node -v
~~~

#### 验证npm是否安装成功
~~~shell
  npm -v
~~~

#### 升级npm
~~~shell
  npm install npm@9 -g
~~~

#### 安装yarn
~~~shell
  npm install yarn -g
  ln -s /usr/local/node-v14.19.3-linux-x64/bin/yarn /usr/bin/yarn
~~~

#### 安装quasar
~~~shell
  npm install @quasar/cli@1.2.1 -g
  ln -s /usr/local/node-v14.19.3-linux-x64/bin/quasar /usr/bin/quasar
~~~

#### 检查quasar版本
~~~shell
  quasar -v
~~~

#### 查看python版本
~~~shell
  python3
~~~

- 确认你的python版本大于3.8

#### 安装git
~~~shell
  apt install git
~~~

#### 下载 GreaterWMS 从 Github
~~~shell
  git clone https://github.com/GreaterWMS/GreaterWMS.git
~~~

#### 提权 GreaterWMS 文件夹
~~~shell
  chmod -R 755 GreaterWMS
~~~

#### 进入GreaterWMS文件夹
~~~shell
  cd GreaterWMS
  apt install python3-pip
  pip3 install -r requirements.txt
~~~

- 有些时候，你安装这些库会出问题，是因为python3版本的问题，不用担心，pip3 install 出错的库就可以了.

#### 回到GreaterWMS文件夹
~~~shell
  Ctrl + C
~~~

#### 数据库生成
~~~shell
  python3 manage.py makemigrations
  python3 manage.py migrate
~~~

!!! info "启动GreaterWMS"

        daphne -p 8008 greaterwms.asgi:application

- 现在打开浏览器，输入"http://127.0.0.1:8008/myip"
- 你会看到你的局域网ip
- 记住他

!!! info "启动GreaterWMS"

        daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application

- 现在打开浏览器，输入"http://{你的局域网IP}:8008"
- 你会看到项目已经启动了

#### 回到GreaterWMS文件夹
~~~shell
  Ctrl + C
  cd templates
~~~

#### 安装Yarn
~~~shell
  yarn install
~~~

- 等待Yarn安装完成，其实你也可以npm install ，就是会慢一点

~~~shell
  yarn install
~~~

- 前端会向 "http://{局域网ip}:8008"发请求, 在这里我们只是看下项目是不是可以运行

~~~shell
  #### 需要修改templates/public/statics/baseurl.txt中的baseurl为你的局域网ip
  #### Example changes before
    http://127.0.0.1:8008

  #### Example changes after
    https://{ your external ip }:8008
~~~

- 按下 Esc 然后输入 ":wq" 去保存修改
- 现在，你已经知道怎么部署和修改请求地址了

#### 重新打包
~~~shell
  #### 你需要回到templates目录下重新打包
  cd templates
  quasar build
~~~

#### 回到GreaterWMS文件夹
~~~shell
  cd ..
  daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
~~~

- 现在，打开浏览器，输入 "http://{你的局域网ip}:8008"，你可以看到项目已经运行了
