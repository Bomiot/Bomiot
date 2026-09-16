
#### IOS Environment


#### Xcode
~~~shell
  #### Login your app developer account first
  https://developer.apple.com/download/all/?q=xcode
~~~

#### Xcode.app
~~~shell
  #### after unzip , change the app name to Xcode.app and copy it to /Application folder
  mv Xcode.app /Users/{your mac name}/Applications
~~~

#### Download plugin
~~~shell
  #### enter templates/src-cordovan
  cordova requirements
~~~
![image-20211030133647439](/media/img/20230429060925.png)

#### Install ios-deploy
~~~shell
  brew install ios-deploy
~~~

#### Install CocoaPods
~~~shell
  sudo gem install cocoapods
~~~

#### Build IOS Platform
~~~shell
    #### src-cordova ios platform
cordova platform ios
~~~

![image-20211030125105616](/media/img/20230429061517.png)

- Use Xcode to open templates/src-cordova/platforms/ios
- add your apple developer ID in

##### Register your apple device to apple developer web
~~~shell
  https://developer.apple.com/account/resources/devices/list
~~~
![image-20211030151000631](/media/img/20230429061759.png)

!!! info "Attention"
    The device added here refers to the tested Apple phone, and the Mac will automatically add it after using XCode to bind the device. Binding the device requires knowing the device's UDID in advance


##### ADD Apple ID

![image-20211030143927297](/media/img/20230429062138.png)

!!! info "Attention"
    If the team on this interface does not have a certificate at this time, you can click on the Download Manual Profile below to download it

##### Developer Certificate Download

![image-20211030145757012](/media/img/20230429062834.png)

- Select the developer certificate we just downloaded from the team in the project, and select a similar certificate from Apple Development for the Signing Certificate

##### Build
- After all the above preparations are ready, enter Xcode and select our testing equipment from Devices

![image-20211030153050463](/media/img/20230429063105.png)

#### Complete All
- There is a play like button above Xcode, click it to complete the installation of IOS package into the current testing Apple phone

![image-20211030153439683](/media/img/20230429063643.png)

Note: When the terminal displays the following information, it indicates that the IOS application is running on the Apple phone:

!!! success "Results"
    **2021-10-30 10:02:31.694411+0800 GreaterWMS--Open Source Warehouse Management System[436:12140] [Snapshotting] Snapshotting a view (0x10702d600, UIKeyboardImpl) that has not been rendered at least once requires afterScreenUpdates:YES.**

- Finshed running XXXXXX on device name will also be displayed above Xcode
