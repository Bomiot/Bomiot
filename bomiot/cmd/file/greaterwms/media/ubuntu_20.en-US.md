#### Ubuntu20 deploy description

#### Update Version
~~~shell
  apt update
  apt upgrade
  apt install build-essential openssl libssl-dev
  apt install vim
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

#### Check python version
~~~shell
  python3
~~~

- Confirm your python version must greater then 3.8

#### Install git
~~~shell
  apt install git
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
  apt install python3-pip
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
