#### Android APP sign


#### install bundletool（suggest 1.14.1）

> Download Link: https://github.com/google/bundletool/releases

#### APP Build

``` cmd
quasar build -m android
```

#### Create APP

- app/dist/cordova/android/bundle/release

- will auto create one aab file

![image-01](/media/img/build.png){ loading=lazy style="max-width: 100%" }

#### Sign

- in folder app/dist/cordova/android/bundle/release

- Use bundletool to create a apks file

``` java
java -jar bundletool-all-1.14.1.jar build-apks --bundle=app-release.aab --output=GWMS.apks
```

#### install apks to your PDA or Phone

``` java
java -jar bundletool-all-1.14.1.jar install-apks --apks=GWMS.apks
```
