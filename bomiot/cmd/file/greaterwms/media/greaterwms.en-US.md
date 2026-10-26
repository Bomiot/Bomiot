﻿#### GreaterWMS Open Source Inventory Management System


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

![YouTube](https://img.shields.io/youtube/channel/subscribers/UCPW1wciGMIEh7CYOdLnsloA?color=red&label=YouTube&logo=youtube&style=for-the-badge){ loading=lazy }

[//]: # (Some Link)
#### :rocket: Link US
<h6>
    Home Page
</h6>
<h6>
    Demo
</h6>
<h6>
  Video Tutorials
</h6>
<h6>
  Report Bug
</h6>
<h6>
  Request Feature
</h6>
<h6>
  中文文档
</h6>

[//]: # (About the Project)
#### :star2: About the Project

This Inventory management system is the currently Ford Asia Pacific after-sales logistics warehousing supply chain process.
After I leave Ford, I start this project in order to help some who need it.
OneAPP Type. Support scanner PDA, mobile APP, desktop exe, website as well.

[//]: # (Function)
#### :dart: Function

* [x] Multiple Warehouses
* [x] Supplier Management
* [x] Customer Management
* [x] Scanner PDA
* [x] Cycle Count
* [x] Order Management
* [x] Stock Control
* [x] Safety Stock Show
* [x] API Documents
* [x] IOS APP Support
* [x] Android APP Support
* [x] Electron APP Support
* [x] Auto Update
* [x] i18n Support
* [x] API Documents

[//]: # (Install)
#### :compass: Install
Python install
- python 3.8.10

Nodejs install
- nodejs 14.19.3

Clone Project
~~~shell
git clone https://github.com/GreaterWMS/GreaterWMS.git
~~~

Backend Environment
~~~shell
cd GreaterWMS/
pip install -r requirements.txt
~~~

Frontend Environment
~~~shell
npm install -g @quasar/cli
npm install -g yarn
cd templates/
yarn install
~~~

DataBase Migrate
~~~shell
cd GreaterWMS/
python manage.py makemigrations
python manage.py migrate
~~~

##### docker(Optional)
~~~shell
cd GreaterWMS/
docker-compose up -d
# Change Baseurl
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
#### :hammer_and_wrench: How To Run Development Server:

- Run Backend:
~~~shell
cd GreaterWMS
daphne -b 8008 greaterwms.asgi:application
or
daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application # Lan
~~~

- Run Frontend:
~~~shell
cd templates
quasar d # http://localhost:8080
or
quasar dev # http://localhost:8080
~~~

- Change Request Baseurl
~~~shell
templates/public/statics/baseurl.txt
~~~

- Companion Mobile APP

GreaterWMS is supported by a companion mobile app which allows users access to run the business well.
It can scan the goods by your camera or your PDA scanner.

IOS

Android

#### Download Android installer tools

!!! info "Android"

    App store search

    Split APKs Installer

#### Directly download installer tools

Sai

- Open Sai APP, choose GWMS.apks then install

[//]: # (publish)
#### :trumpet: How To Publish:

- Web Build:

~~~shell
cd templates
quasar build # /templates/dist/spa
~~~

[//]: # (deploy)
#### :computer: How To Deploy Server:

<h6>
  Supervisor Process Guarded
</h6>
<h6>
  Nginx Config
</h6>

If the server has SSL enabled, please use HTTPS and WSS, if SSL is not enabled, use HTTP and WS

The front-end code needs to be rebuilt after modification.

<!-- Sponsor -->
#### :money_with_wings: Sponsor

If you use GreaterWMS and find it to be useful, please consider making a donation toward its continued development.

Donate via PayPal

#### Show
<div align="left">
    <img src="/media/img/GreaterWMS_en.png" alt="GreaterWMS home" width="" height="400" />
</div>
<div align="left">
    <img src="/media/img/mobile_splash.jpg" alt="GreaterWMS splash" width="200" height="400" />
    <img src="/media/img/mobile_dn_en.jpg" alt="GreaterWMS dn" width="200" height="400" />
    <img src="/media/img/mobile_equ_en.jpg" alt="GreaterWMS goods" width="200" height="400" />
</div>
