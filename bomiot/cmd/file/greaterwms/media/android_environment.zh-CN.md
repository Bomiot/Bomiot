#### 安卓APP环境搭建


#### node版本要求

> node v14.19.3

#### app源码目录

> cd app

#### 安装JDK1.8

> 下载地址：https://www.56yhz.com/media/windows/jdk-8u281-windows-x64.exe

- 一直next即可

#### 安装Cordova插件

- app目录下运行

~~~shell
  npm install -g cordova
~~~

#### 安装Android Studio软件

> 下载地址为：https://developer.android.google.cn/studio/

- 一直next,第一次运行，需要安装SDK,全部选是即可

> ![](https://po.56yhz.com/media/windows/1.jpeg){ loading=lazy style="max-width: 100%" }

- 打开Android Studio,点击右边的project——More Actions——SDK Manager——SDK Platforms,选中下边的Hide Obsolete Packages

> ![](https://po.56yhz.com/media/windows/2.jpeg){ loading=lazy style="max-width: 100%" }

(切换到SDK-TOOLS)

- 切换到SDK-TOOLS,选中图中所示

> ![](https://po.56yhz.com/media/windows/3.jpeg){ loading=lazy style="max-width: 100%" }

- 再选中右方的Show Package Details，必须选择30版本的，点击Apply,等下载完成，再点确定

#### 下载Gradle

- 下载完成后解压到其他路径即可

>下载路径为https://downloads.gradle-dn.com/distributions/gradle-4.10.3-all.zip

#### 环境变量配置

- 创建系统环境变量JAVA_HOME:为JDK安装路径

- 创建系统环境变量Gradle:为上一一步中gradle-4.10.3-all.zip解压后的路径

> ![](https://po.56yhz.com/media/windows/4.jpeg){ loading=lazy style="max-width: 100%" }

- 创建系统环境变量ANDROID_HOME和ANDROID_SDK_ROOT:为Android SDK的安装路径

> ![](https://po.56yhz.com/media/windows/5.jpeg){ loading=lazy style="max-width: 100%" }

- 编辑环境变量PATH，添加如图所示

![](https://po.56yhz.com/media/windows/6.jpeg){ loading=lazy style="max-width: 100%" }

#### 验证安卓环境是否配置完成

- app目录下的src-cordova下输入

~~~shell
    cordova requirements
~~~

- 检查环境，如果成功的话如下所示

![](https://po.56yhz.com/media/windows/7.jpeg){ loading=lazy style="max-width: 100%" }

#### 安装前端环境

> yarn install

#### 手机连接调试

> 用手机或者PDA，通过USB连接你的电脑，并打开调试模式

#### 修改请求地址

- 修改项目目录下的app/src/store/settings/state.js

> 修改server的值为http://{ 你的域名或者请求地址 }

#### 调试

- 项目目录下的app下执行

~~~shell
  quasar d -m cordova -T android
~~~

> ![](https://po.56yhz.com/media/windows/9.jpeg){ loading=lazy style="max-width: 100%" }

#### Android Http 请求

- 如果你希望使用Http请求，而不是Https请求

- 添加以下代码到如图所示位置

~~~shell
  android:usesCleartextTraffic="true"
~~~

![image-01](/media/img/android_http.png){ loading=lazy style="max-width: 100%" }
