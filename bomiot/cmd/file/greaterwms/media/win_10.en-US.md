
#### Windows10 deploy description

#### Download python3.8.10
~~~shell
  #### (Example version X64)
  https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
~~~

- Right click and run the exe file as an administrator to install Python 3.8.10
- Be sure to check Add Python 3.8 To PATH and then click Install Now

#### Download sqlite3
~~~shell
  #### (Example version X64)
  https://www.sqlite.org/2021/sqlite-dll-win64-x64-3350500.zip
~~~

- Unzip the zip file and overwrite the file in the Python path DLL with the address

~~~shell
  C:\Users\{your user name}\AppData\Local\Programs\Python\Python38\DLLs
~~~

#### Download Node.JS 14.19.3
~~~shell
  #### (Example version X64)
  https://nodejs.org/dist/v14.19.3/node-v14.19.3-x64.msi
~~~

#### Download Git
~~~shell
  #### (Example version X64)
  https://git-scm.com/
~~~

- Right click, run the exe file as an administrator, and then continue to the next step
- Choose which directory you want to place GreaterWMS in, right-click, and select Git Bash Here

#### Download GreaterWMS
~~~shell
 git clone https://github.com/GreaterWMS/GreaterWMS.git
~~~

#### Enter GreaterWMS
~~~ shell
  #### cd GreaterWMS
  pip install -r requirements.txt
~~~

#### Back CMD
~~~shell
  #### Create Database
  python manage.py makemigrations
  python manage.py migrate
~~~

#### Run GreaterWMS Again
~~~shell
  daphne -p 8008 greaterwms.asgi:application
~~~

- At this point, open the browser and enter 127.0.0.1:8008
- View the LAN IP, enter 127.0.0.1:8008/myip in the browser
- Save or remember this IP address
- Be sure to note that the internal IP obtained each time Windows starts is different. Either your router sets a fixed internal IP for this computer, or you should not turn off the computer

#### Back CMD
~~~shell
  #### enter templates folder
  cd templates
  npm install -g npm@9
  npm install -g yarn
  npm install -g @quasar/cli
  npm install -g core-js
~~~

#### Yarn Install
~~~shell
  yarn install
~~~

- This process can be a bit slow, sometimes very fast, due to network issues being blocked
- If an error occurs, it is due to network reasons that it has been blocked. We provide a downloaded front-end dependency and download it

##### Internal deploy
~~~shell
  #### templates/public/statics/baseurl.txt change to you internal ip
  http://{your internal ip}:8008
~~~

#### Re Build
~~~shell
  #### cd templates
  quasar build
~~~

#### Restart GreaterWMS
~~~shell
  #### back to GreaterWMS folder
  daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
~~~

- Next, you can use your browser to access { http://{ internal IP }:8008 } to view the project
- Computers on the local area network can also access projects through this IP address
