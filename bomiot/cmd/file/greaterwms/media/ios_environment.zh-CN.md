
#### IOS 环境搭建


#### Xcode
~~~shell
  #### 你需要先登入你的苹果开发者账号
  https://developer.apple.com/download/all/?q=xcode
~~~

#### Xcode.app
~~~shell
  #### 将解压出来并安装成功后的应用改名为Xcode.app复制到/Application目录下
  mv Xcode.app /Users/{你的mac机器用户名}/Applications
~~~

#### 下载插件
~~~shell
  #### 进入项目目录下的templates下的src-cordovan，执行：
  cordova requirements
~~~
![image-20211030133647439](/media/img/20230429060925.png)

#### 安装ios-deploy
~~~shell
  brew install ios-deploy
~~~

#### 安装CocoaPods
~~~shell
  sudo gem install cocoapods
~~~

#### Build IOS客户端

#### src-cordova ios platform
~~~shell
  cordova platform ios
~~~

![image-20211030125105616](/media/img/20230429061517.png)

- 用Xcode打开项目的ios目录,templates/src-cordova/platforms/ios
- 并添加苹果开发者账号的Apple ID(开发者账号需要自己注册)

##### 在苹果开发者网站上注册自己的测试设备
~~~shell
  https://developer.apple.com/account/resources/devices/list
~~~
![image-20211030151000631](/media/img/20230429061759.png)

!!! info "注意"
    这里添加的设备是指测试的苹果手机，mac会在使用xcode绑定设备以后系统自动添加，绑定设备需要提前知晓自己设备的UDID


##### 添加Apple ID

![image-20211030143927297](/media/img/20230429062138.png)

!!! info "注意"
    如果此时这个界面的Team 没有证书，可以点击 下面的Download Manual Profile进行下载

##### 项目开发者证书下载

![image-20211030145757012](/media/img/20230429062834.png)

- 在项目里的Team处选择我们刚刚下载的开发者证书，Signing Certificate 选择Apple Development的类似证书

##### 正式打包
- 以上准备工作都就绪后，进入Xcode,Devices处选择我们的测试设备

![image-20211030153050463](/media/img/20230429063105.png)

#### 一切设置好以后
- 在Xcode上方有一个类似播放的按钮，点击他，即可完成将IOS安装包打入当前的测试苹果手机中

![image-20211030153439683](/media/img/20230429063643.png)

注：当终端显示以下信息，就表示IOS应用已在苹果手机上运行：

!!! success "结果"
    **2021-10-30 10:02:31.694411+0800 GreaterWMS--Open Source Warehouse Management System[436:12140] [Snapshotting] Snapshotting a view (0x10702d600, UIKeyboardImpl) that has not been rendered at least once requires afterScreenUpdates:YES.**

- 在Xcode上方也会显示“Finshed runing XXXXXX on 设备名称”
