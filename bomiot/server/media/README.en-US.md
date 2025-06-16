<div align="center">
  <img src="media/img/logo.png" alt="Bomiot logo" width="200" height="auto" />
  <h1>Bomiot</h1>
  <p>One App you can do everything</p>

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

[![YouTube](https://img.shields.io/youtube/channel/subscribers/UCPW1wciGMIEh7CYOdLnsloA?color=red&label=YouTube&logo=youtube&style=for-the-badge)](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)

</div>


## :rocket: Link US

<h4>
  <a href="https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA">Video Tutorials</a>
</h4>
<h4>
  <a href="https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md&title=[BUG]">Report Bug</a>
</h4>
<h4>   
  <a href="https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md&title=[FR]">Request Feature</a>
</h4>


[//]: # (About the Project)
## :star2: About the Project

Many open source projects focus on the software layer, various tricks and encapsulation, while ignoring the ease of use for developers and the efficiency of interaction between development teams. Most projects are launched online, so that end users can use them directly from 0 to 1 without any transition, which is very uncomfortable for end users.
Bomiot was originally designed to solve these problems.

[//]: # (Function)
## :dart: module

* [x] Scheduled tasks
* [x] Project management
* [x] Plugin system
* [x] Document management
* [x] Real-time file monitoring
* [x] Permission control
* [x] Multi-language

[//]: # (Install)
## :compass: Installation
~~~shell
pip install bomiot
~~~

Or

~~~shell
poetry add bomiot
~~~

### Initialization
Initialize the workbench
~~~shell
bomiot init
~~~

Create a new project
~~~shell
bomiot project test
~~~

Create an app in a new project
~~~shell
bomiot new app_test
~~~

Create a new plugin
~~~shell
bomiot plugin plugin_test
~~~

Create a database
~~~shell
bomiot migrate
~~~

Create an admin account
~~~shell
bomiot initadmin
~~~

[//]: # (start)
## :hammer_and_wrench: How to start:

~~~shell
daphne -p 8008 bomiot.server.server.asgi:application

or

daphne -b 0.0.0.0 -p 8008 bomiot.server.server.asgi:application # LAN
~~~

- Front-end development mode
Install the Quasar environment and enter the templates folder
In boot/axios.js, open baseUrl
~~~shell
yarn install
~~~

- Start the front end
~~~shell
quasar d
~~~

After modifying the front end development, you need to close the baseUrl again, and then quasar build to repackage the front end