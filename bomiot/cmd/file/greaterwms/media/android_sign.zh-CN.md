#### 安卓APP签名


#### 安装bundletool工具（建议下载1.14.1）

> 下载地址：https://github.com/google/bundletool/releases

#### app 构建

> quasar build -m android

#### 生成app

- 打包完成以后会在项目目录/app/dist/cordova/android/bundle/release下生成一个aab文件

![image-01](/media/img/build.png){ loading=lazy style="max-width: 100%" }

#### 签名

- 在release目录下执行签名命令并生成一个apks（需要安装bundletool工具）

> java -jar bundletool-all-1.14.1.jar build-apks --bundle=app-release.aab --output=GWMS.apks

#### 安装此apks到你的PDA或者手机

> java -jar bundletool-all-1.14.1.jar install-apks --apks=GWMS.apks
