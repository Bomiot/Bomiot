# Sqlite3 Database

## Introduction

- **Bomiot** The default database is sqlite. To ensure normal operation, it is best to upgrade it

---

## Windows

- Install Chocolatey
- Run PowerShell as an administrator and execute:

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

- Upgrade SQLite3

- Run the command:

```bash
choco upgrade sqlite --version=3.50.1
```

If the version is not available, you may need to manually add a third-party source or wait for the Chocolatey update package

---

## Mac

- Upgrade Homebrew package management tool

```bash
brew update
```

- Upgrade SQLite3

```bash
brew upgrade sqlite
```

---

## Linux

#### Download the latest source code

```bash
wget https://www.sqlite.org/2025/sqlite-autoconf-3500100.tar.gz
tar -xzf sqlite-autoconf-3500100.tar.gz
cd sqlite-autoconf-3500100
```

#### Install dependencies (taking Ubuntu as an example)

```bash
sudo apt install autoconf automake libtool libreadline-dev
```

#### Configuration and compilation

```bash
./configure --prefix=/usr/local
make
sudo make install
```

#### Replace the old version of the system

```bash
sudo mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
sudo ln -s /usr/local/bin/sqlite3 /usr/bin/sqlite3
```

#### Update the dynamic link library cache

```bash
echo "/usr/local/lib" | sudo tee -a /etc/ld.so.conf.d/sqlite3.conf
sudo ldconfig
```