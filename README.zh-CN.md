<div align="center">
  <img src="bomiot/templates/dist/spa/icons/logo.png" alt="Bomiot logo" width="200" height="auto" />
  <h1>Bomiot</h1>
  <p>一个APP，你可以做任何事</p>

<!-- Badges -->
![License: APLv2](https://img.shields.io/github/license/Bomiot/Bomiot)
![Release Version (latest Version)](https://img.shields.io/github/v/release/Bomiot/Bomiot?color=orange&include_prereleases)
![i18n Support](https://img.shields.io/badge/i18n-Support-orange.svg)

![repo size](https://img.shields.io/github/repo-size/Bomiot/Bomiot)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Bomiot/Bomiot)
![Contributors](https://img.shields.io/github/contributors/Bomiot/Bomiot?color=blue)

![GitHub Org's stars](https://img.shields.io/github/stars/Bomiot?style=social)
![GitHub Follows](https://img.shields.io/github/followers/Singosgu?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Bomiot/Bomiot?style=social)
![GitHub Watch](https://img.shields.io/github/watchers/Bomiot/Bomiot?style=social)

![Python](https://img.shields.io/badge/Python-3.9-yellowgreen)
![Django](https://img.shields.io/badge/Django-4.2-yellowgreen)
![Quasar Cli](https://img.shields.io/badge/Quasar/cli-2.4.1-yellowgreen)
![Vue](https://img.shields.io/badge/Vue-3.4.18-yellowgreen)
![NodeJS](https://img.shields.io/badge/NodeJS-18.19.1-yellowgreen)

[![BiliBili](https://img.shields.io/badge/BiliBili-4987-red)](https://space.bilibili.com/407321291/channel/seriesdetail?sid=776320)
</div>

## :rocket: 找到我们

<h4>
  <a href="https://space.bilibili.com/407321291?spm_id_from=333.1007.0.0">教程视频</a>
</h4>
<h4>
  <a href="https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md&title=[BUG]">提交一个Bug</a>
</h4>
<h4>   
  <a href="https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md&title=[FR]">提交一个建议</a>
</h4>


QQ技术交流群：289548524

[//]: # (About the Project)
### :star2: 关于此项目

很多开源项目专注于软件层，各种炫技和封装，而忽略了开发者的易用性，以及开发团队交互的效率，大多数项目的上线，让最终用户从0到1，直接使用无过渡，对于最终用户也是非常难受的
Bomiot的设计初衷，就是解决这些问题

[//]: # (Function)
## :dart: 模块

* [x] 定时任务
* [x] 项目管理
* [x] 插件系统
* [x] 文档管理
* [x] 实时文件监控
* [x] 权限控制
* [x] 多语言

[//]: # (Install)
## :compass: 安装
~~~shell
pip install bomiot
~~~

或者

~~~shell
poetry add bomiot
~~~

### 初始化
初始化工作台
~~~shell
bomiot init
~~~

新建项目
~~~shell
bomiot project test
~~~

新建一个项目中的app
~~~shell
bomiot new app_test
~~~

新建插件
~~~shell
bomiot plugin plugin_test
~~~

建立数据库
~~~shell
bomiot migrate
~~~

建立admin账号
~~~shell
bomiot initadmin
~~~

[//]: # (start)
## :hammer_and_wrench: 怎么启动:

~~~shell
daphne -p 8008 bomiot.server.server.asgi:application

or

daphne -b 0.0.0.0 -p 8008 bomiot.server.server.asgi:application # 局域网
~~~


- 前端开发模式
安装好Quasar环境，进入templates文件夹
在boot/axios.js中，把baseUrl打开
~~~shell
yarn install
~~~

- 启动前端
~~~shell
quasar d
~~~

前端开发修改完，需要重新关闭baseUrl，然后quasar build重新打包前端

<!-- ABOUT AUTHOR -->
## :bowing_man: 关于作者

[Elvis.Shi](https://gitee.com/GreaterWMS/GreaterWMS/wikis/%E6%88%91%E6%98%AF%E5%A6%82%E4%BD%95%E4%BB%8E%E4%B8%80%E4%B8%AA%E7%89%A9%E6%B5%81%E8%8F%9C%E9%B8%9F%EF%BC%8C%E4%B8%80%E7%9B%B4%E5%81%9A%E5%88%B0500%E5%BC%BA%E4%BA%9A%E5%A4%AA%E5%8C%BAChina%20PDC%20Manager%E7%9A%84)
