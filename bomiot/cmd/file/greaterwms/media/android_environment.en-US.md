#### Android APP environment

#### Node version requirements

> node v14.19.3

#### App source code folder

> cd app

#### Install JDK1.8

> Download Link: https://po.56yhz.com/media/windows/jdk-8u281-windows-x64.exe

- Just keep on next

#### Installing the Cordova plugin

~~~shell
  npm install - g cordova
~~~

#### Install the Android Studio software

> The download address is: https://developer.android.google.cn/studio/

- Always next, the first time you run it, you need to install the SDK, you can choose all

> ![](https://po.56yhz.com/media/windows/1.jpeg){ loading=lazy style="max-width: 100%" }

- Open Android Studio, click project on the right - More Actions - SDK Manager - SDK Platforms, select Hide Obsolete Packages below

> ![](https://po.56yhz.com/media/windows/2.jpeg){ loading=lazy style="max-width: 100%" }

- Switch to SDK-TOOLS, select the one shown in the picture

> ![](https://po.56yhz.com/media/windows/3.jpeg){ loading=lazy style="max-width: 100%" }

- Then select Show Package Details on the right, must select version 30, click Apply, wait for the download to complete, and then click OK

#### Download Gradle

- and unzip it to another path after the download is complete

> The download link is https://downloads.gradle-dn.com/distributions/gradle-4.10.3-all.zip

#### Environment variable configuration

- Create a system environment variable JAVA_HOME: the JDK installation path, the default path is as shown in the figure

- Create a system environment variable Gradle: the unzipped path of gradle-4.10.3-all.zip in the previous step

> ![](https://po.56yhz.com/media/windows/4.jpeg){ loading=lazy style="max-width: 100%" }

- Create system environment variables ANDROID_HOME and ANDROID_SDK_ROOT: for the installation path of the Android SDK

> ![](https://po.56yhz.com/media/windows/5.jpeg){ loading=lazy style="max-width: 100%" }

#### Edit the environment variable PATH and add as below

![](https://po.56yhz.com/media/windows/6.jpeg){ loading=lazy style="max-width: 100%" }

#### Verify that the Android environment is configured

~~~shell
    cordova requirements
~~~

- Check the environment by typing cordova requirements, if successful as below:

![](https://po.56yhz.com/media/windows/7.jpeg){ loading=lazy style="max-width: 100%" }

#### Installing the front-end environment

> yarn install

#### Initialize environment

> Connect your phone or PDA to your computer via USB

!!! success "Turn USB Debug"

    Turn on USB Debug menu on the mobile phone or pda, and connect to the computer. Select MTP or PTP mode to turn on USB Debug menu on the mobile phone or pda. The method of turning on USB Debug menu can be studied by yourself.

    Each brand is different, and connected to the computer.

- Modify app/src/store/settings/state.js in the project directory

> Modify the value of server to your domain address

~~~shell
  quasar d - m cordova - T android
~~~

![](https://po.56yhz.com/media/windows/9.jpeg){ loading=lazy style="max-width: 100%" }

#### Android Http request

- If you want use http not https

- add follow code to here

~~~shell
  android:usesCleartextTraffic="true"
~~~

![image-01](/media/img/android_http.png){ loading=lazy style="max-width: 100%" }
