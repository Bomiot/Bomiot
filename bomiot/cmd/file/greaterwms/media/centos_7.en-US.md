#### Centos7 deploy description


#### Update Version
~~~shell
  yum update
  yum upgrade
~~~

#### Install system dependencies
~~~shell
  yum -y install gcc-c++
~~~

#### Install Python dependencies
~~~shell
  yum install zlib-devel xz-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make
~~~

#### Install Node
~~~shell
  wget https://nodejs.org/dist/v14.19.3/node-v14.19.3-linux-x64.tar.gz
  tar zvxf node-v14.19.3-linux-x64.tar.gz -C /usr/local
~~~

#### Environment variable settings
~~~shell
  echo '''export NODE_HOME=/usr/local/node-v14.19.3-linux-x64 export PATH=$PATH:$NODE_HOME/bin export NODE_PATH=$NODE_HOME/lib/node_modules''' /etc/profile
~~~

#### Make environment variables take effect immediately
~~~shell
  source /etc/profile
~~~

#### Soft connection Node and NPM
~~~shell
  ln -sf /usr/local/node-v14.19.3-linux-x64/bin/node /usr/bin/node
  ln -s /usr/local/node-v14.19.3-linux-x64/bin/npm /usr/bin/npm
~~~

#### Verify that node is installed successfully
~~~shell
  node -v
~~~

#### Verify that npm is installed successfully
~~~shell
  npm -v
~~~

#### Upgrade npm
~~~shell
  npm install npm@9 -g
~~~

#### Install yarn
~~~shell
  npm install yarn -g
  ln -s /usr/local/node-v14.19.3-linux-x64/bin/yarn /usr/bin/yarn
~~~

#### Install quasar
~~~shell
  npm install @quasar/cli@1.2.1 -g
  ln -s /usr/local/node-v14.19.3-linux-x64/bin/quasar /usr/bin/quasar
~~~

#### Check quasar version
~~~shell
  quasar -v
~~~

#### Upgrade sqlite3 version
- It is recommended to do this step before installing python3.8.10

##### Download the source code
~~~shell
  wget https://www.sqlite.org/2019/sqlite-autoconf-3300100.tar.gz
~~~

##### unzip, compile
~~~shell
  tar zxvf sqlite-autoconf-3300100.tar.gz
  cd sqlite-autoconf-3300100/
  ./configure --prefix=/usr/local
  make && make install
~~~

##### Replace system low version sqlite3
~~~shell
  mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
  ln -s /usr/local/bin/sqlite3 /usr/bin/sqlite3
  echo "/usr/local/lib" > /etc/ld.so.conf.d/sqlite3.conf
  ldconfig
  sqlite3 -version
~~~

#### Check python version
~~~shell
  python3
~~~

- If the python version is not 3.8.10, please execute the following command

~~~shell
  cd /usr/src
  wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
  tar -zxvf Python-3.8.10.tgz
  cd Python-3.8.10/
  ./configure --enable-optimizations --with-ssl-default-suites=openssl
  make & make altinstall
  mv /usr/bin/python3 /usr/bin/python3.bak
  ln -s /usr/local/bin/python3.8 /usr/bin/python3
  mv /usr/bin/pip3 /usr/bin/pip3.bak
  ln -s /usr/local/bin/pip3.8 /usr/bin/pip3
~~~

#### Check pip3 list is installed successfully
~~~shell
  pip3 list
~~~

#### Install git
~~~shell
  yum install git
~~~

#### Download GreaterWMS from GitHub
~~~shell
  git clone https://github.com/GreaterWMS/GreaterWMS.git
~~~

#### Elevate GreaterWMS Folder
~~~shell
  chmod -R 755 GreaterWMS
~~~

#### Go to the GreaterWMS folder
~~~shell
  cd GreaterWMS
  pip3 install -r requirements.txt
~~~

- Sometimes, there will be problems when you install these libraries because of the python3 version, don't worry, pip3 install the wrong library.

#### Database generation
~~~shell
  python3 manage.py makemigrations
  python3 manage.py migrate
~~~

!!! success "Run GreaterWMS"

    daphne -p 8008 greaterwms.asgi:application

- Now open your browser, type "http://127.0.0.1:8008/myip"
- and you will see the your internal ip
- remember it

!!! success "Run GreaterWMS"

    daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application

- Now open your browser, type "http://{your internal ip}:8008"
- and you will see GreaterWMS run well

#### Go back to the GreaterWMS folder
~~~shell
  Ctrl + C
  cd templates
~~~

~~~shell
  yarn install
~~~

- Wait for the Yarn installation to complete. In fact, you can also npm install it, but it will be slower
Change yarn to domestic source

#### Go back to the baseurl folder
~~~shell
  #### Need to edit 'templates/public/statics/baseurl.txt' to your internal ip
  Ctrl + C // go back to templates folder
  #### Example changes before
    http://127.0.0.1:8008

  #### Example changes after
    https://{ your external ip }:8008
~~~

- Press Esc and type ":wq" to save changes
- Now, you know how to deploy and modify the request address

#### Back to templates
~~~shell
  ####you should build it again
    cd templates
    quasar build
~~~

#### Go back to the GreaterWMS folder
~~~shell
  cd ..
  daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
~~~

- Now, open the browser, type "http://{your internal ip}:8008", you can see the project is running
