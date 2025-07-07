# Sqlite3 数据库

## 介绍

- **Bomiot**默认数据库是sqlite，为了保证正常运行，最好升级一下

---

## Windows

- 安装 Chocolatey
- 以管理员身份运行 PowerShell，执行：

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

- 升级 SQLite3

- 运行命令：

```bash
choco upgrade sqlite --version=3.50.1
```

若提示版本不可用，可能需要手动添加第三方源或等待 Chocolatey 更新包

---

## Mac

- 升级 Homebrew 包管理工具

```bash
brew update
```

- 升级 SQLite3

```bash
brew upgrade sqlite
```

---

## Linux

#### 下载最新源码

```bash
wget https://www.sqlite.org/2025/sqlite-autoconf-3500100.tar.gz
tar -xzf sqlite-autoconf-3500100.tar.gz
cd sqlite-autoconf-3500100
```

#### 安装依赖（以 Ubuntu 为例）

```bash
sudo apt install autoconf automake libtool libreadline-dev
```

#### 配置与编译

```bash
./configure --prefix=/usr/local
make
sudo make install
```

#### 替换系统旧版本

```bash
sudo mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
sudo ln -s /usr/local/bin/sqlite3 /usr/bin/sqlite3
```

#### 更新动态链接库缓存

```bash
echo "/usr/local/lib" | sudo tee -a /etc/ld.so.conf.d/sqlite3.conf
sudo ldconfig
```