﻿#### GreaterWMS 开源仓库管理系统

![logo](/media/img/logo.png){ loading=lazy }

![License: AGPLv2](https://img.shields.io/github/license/GreaterWMS/GreaterWMS){ loading=lazy }
![Release Version (latest Version)](https://img.shields.io/github/v/release/GreaterWMS/GreaterWMS?color=orange&include_prereleases){ loading=lazy }
![QR Code Support](https://img.shields.io/badge/QR--Code-Support-orange.svg){ loading=lazy }
![Docker Support](https://img.shields.io/badge/Docker-Support-orange.svg){ loading=lazy }
![i18n Support](https://img.shields.io/badge/i18n-Support-orange.svg){ loading=lazy }

![repo size](https://img.shields.io/github/repo-size/GreaterWMS/GreaterWMS){ loading=lazy }
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/GreaterWMS/GreaterWMS){ loading=lazy }
![Contributors](https://img.shields.io/github/contributors/GreaterWMS/GreaterWMS?color=blue){ loading=lazy }

![GitHub Org's stars](https://img.shields.io/github/stars/GreaterWMS?style=social){ loading=lazy }
![GitHub Follows](https://img.shields.io/github/followers/Singosgu?style=social){ loading=lazy }
![GitHub Forks](https://img.shields.io/github/forks/GreaterWMS/GreaterWMS?style=social){ loading=lazy }
![GitHub Watch](https://img.shields.io/github/watchers/GreaterWMS/GreaterWMS?style=social){ loading=lazy }

![Python](https://img.shields.io/badge/Python-3.8.10-yellowgreen){ loading=lazy }
![Django](https://img.shields.io/badge/Django-4.1.2-yellowgreen){ loading=lazy }
![Quasar Cli](https://img.shields.io/badge/Quasar/cli-1.2.1-yellowgreen){ loading=lazy }
![Vue](https://img.shields.io/badge/Vue-2.6.0-yellowgreen){ loading=lazy }
![NodeJS](https://img.shields.io/badge/NodeJS-14.19.3-yellowgreen){ loading=lazy }

![Bilibili](https://img.shields.io/badge/BiliBili-4987-red){ loading=lazy }

[//]: # (Some Link)
#### :rocket: 找到我们
<h6>
    官网首页
</h6>
<h6>
    演示地址
</h6>
<h6>
  相关视频
</h6>
<h6>
  提交一个Bug
</h6>
<h6>
  提交一个建议
</h6>
<h6>
  英文文档
</h6>

[//]: # (About the Project)
##### :star2: 关于此项目

该库存管理系统是，目前福特亚太区售后物流仓储供应链流程。
离开福特后，我开始了这个项目。 为了帮助一些有需要的人。
OneAPP 理念。 支持扫描设备PDA、手机APP、桌面exe、网站等。

[//]: # (Function)
#### :dart: 模块

* [x] 多仓
* [x] 供应商管理
* [x] 客户管理
* [x] 扫描设备PDA
* [x] 盘点
* [x] 订单管理
* [x] 库存管理
* [x] 安全库存
* [x] API文档
* [x] IOS APP支持
* [x] Android APP支持
* [x] Electron APP支持
* [x] 自动更新
* [x] i18n国际化

[//]: # (Install)
#### :compass: 安装
python安装
- python 3.8.10

nodejs安装
- nodejs 14.19.3

Twisted install
- Please google how to install Twisted , if you have some problem on install it .

克隆代码
~~~shell
git clone https://github.com/GreaterWMS/GreaterWMS.git
~~~

后端环境
~~~shell
cd GreaterWMS/
pip install -r requirements.txt
~~~

后端环境
~~~shell
npm install -g @quasar/cli
npm install -g yarn
cd templates/
yarn install
~~~

数据初始化
~~~shell
cd GreaterWMS/
python manage.py makemigrations
python manage.py migrate
~~~

##### docker(可选择)
~~~shell
cd GreaterWMS/
docker-compose up -d
# 修改请求地址
# baseurl GreaterWMS/templates/public/statics/baseurl.txt
docker-compose restart
~~~

<h6>
  Windows X64
</h6>
<h6>
  Centos 7
</h6>
<h6>
  Ubuntu 20
</h6>

[//]: # (development)
#### :hammer_and_wrench: 怎么启动开发环境:

- 启动后端环境:
~~~shell
cd GreaterWMS
daphne -p 8008 greaterwms.asgi:application
or
daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application # 局域网
~~~

- 启动前端环境:
~~~shell
cd templates
quasar d # http://localhost:8080
or
quasar dev # http://localhost:8080
~~~

- 请求地址修改
~~~shell
templates/public/statics/baseurl.txt
~~~

- 配套的手机APP

IOS

Android

GreaterWMS有配套的APP，支持手机扫描，和PDA扫描，配置下服务器请求地址即可

#### 下载apks安装工具

!!! info "Android"

    应用商店搜索

    Split APKs Installer

#### 或直接下载apks安装工具

Sai

- 打开Sai APP，选择下载的GWMS.apks，即可完成安装

[//]: # (publish)
#### :trumpet: 怎么构建你的app:

- 网页版构建:

~~~shell
cd templates
quasar build # /templates/dist/spa
~~~

[//]: # (deploy)
#### :computer: 怎么部署到服务器:

<h6>
  Supervisor教程
</h6>
<h6>
  Nginx配置
</h6>

记得启用ssl的话，需要额外配置
在前端代码中进行编辑

#### Show
<div align="left">
    <img src="/media/img/GreaterWMS.png" alt="GreaterWMS home" width="" height="400" />
</div>
<div align="left">
    <img src="/media/img/mobile_splash.jpg" alt="GreaterWMS splash" width="200" height="400" />
    <img src="/media/img/mobile_dn.jpg" alt="GreaterWMS dn" width="200" height="400" />
    <img src="/media/img/mobile_equ.jpg" alt="GreaterWMS goods" width="200" height="400" />
</div>

<!-- ABOUT AUTHOR -->
#### :bowing_man: 关于作者

Elvis.Shi
