
#### Windows10部署说明


<h4>
  <a href="https://www.bilibili.com/video/BV1Mh411m72v/?share_source=copy_web&vd_source=22a376f853fb151b9c8909e926f7bf0b">视频教程</a>
</h4>

##### 下载python3.8.10
~~~shell
  #### (版本以自己电脑系统为主，我们以64位为例)
  https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
~~~

- 右键，以管理员运行exe文件，安装python3.8.10
- 注意一定要勾选上Add Python3.8 To PATH,然后点选Install Now

##### 下载sqlite3
~~~shell
  #### (版本以自己电脑系统为主，我们以64位为例)
  https://www.sqlite.org/2021/sqlite-dll-win64-x64-3350500.zip
~~~

- 解压zip文件，将解压出来的文件，覆盖python路径dll中的文件，地址为

~~~shell
  C:\Users\{你的用户名}\AppData\Local\Programs\Python\Python38\DLLs
~~~

##### 下载Node.JS14.19.3
~~~shell
  #### (版本以自己电脑系统为主，我们以64位为例)
  https://nodejs.org/dist/v14.19.3/node-v14.19.3-x64.msi
~~~

##### 下载Git
~~~shell
  #### (版本以自己电脑系统为主，我们以64位为例，需要下载64-bit版本的)
  https://git-scm.com/
~~~

- 右键，以管理员运行exe文件，然后一直下一步就可以了
- 选择好你要把GreaterWMS摆在哪个目录中，右键，选择Git Bash Here

##### 下载 GreaterWMS 代码
~~~shell
 git clone https://github.com/GreaterWMS/GreaterWMS.git
~~~

#### 进入GreaterWMS目录
~~~ shell
  pip install -r requirements.txt
~~~

#### 回到CMD界面
~~~shell
  #### 生成数据库
  python manage.py makemigrations
  python manage.py migrate
~~~

#### 再次启动项目
~~~shell
  daphne -b 8008 greaterwms.asgi:application
~~~

- 这时候打开浏览器，输入127.0.0.1:8008
- 查看局域网IP，浏览器输入127.0.0.1:8008/myip
- 保存或者记住这个IP地址
- 一定注意，windows每次启动获得的内网IP是不同的，要么你路由器设置固定内网IP给这台电脑，要么你就不要关电脑

#### 回到CMD界面
~~~shell
  #### 进入templates目录
  cd templates
  npm install -g npm@9
  npm install -g yarn
  npm install -g @quasar/cli
  yarn install
~~~

- 这个过程会有点慢，有时候会很快，是因为网络原因被墙了

#### 局域网部署
~~~shell
  #### 需要修改templates/public/statics/baseurl.txt中的baseurl为你的局域网ip
  #### Example changes before
    http://127.0.0.1:8008

  #### Example changes after
    https://{ your external ip }:8008
~~~

#### 重新编译前端
~~~shell
  #### templates目录下面
  quasar build
~~~

#### 重启GreaterWMS
~~~shell
  daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
~~~

- 接下来就可以使用你的浏览器，访问 http://{ 局域网IP }:8008 来查看该项目了
- 局域网上的电脑也可以通过这个地址来访问项目
