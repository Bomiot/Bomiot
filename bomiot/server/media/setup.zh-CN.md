# setup.ini

---

### 控制项目

- 这里控制bomiot指向哪个项目的目录

```shell
[project]
name = bomiot_example
```

### 数据库

- 支持多种数据库，默认是sqlite  engine，Accept (sqlite、mysql、oracle、postgresql)

```shell
[database]
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port
```

### 前端的index.html地址

- 在project下面的目录指向index.html，所以支持React,Angular,Vue和Django自带的templates

```shell
[templates]
name = templates/dist/spa/index.html
```

### 时区

- 一般不修改

```shell
[locale]
time_zone = 'UTC'
```

### 限流

- 限制每秒访问次数，默认1秒10次

```shell
[throttle]
allocation_seconds = 1
throttle_seconds = 10
```

### 登入限制

- 登入次数错误，超过3次就锁定

```shell
[request]
limit = 2
```

### 前后端鉴权JWT时效

- JWT Token的时效

```shell
[jwt]
user_jwt_time = 1000000
```

### 文件限制

- file_size是文件大小，byte单位
- file_extension是文件格式，不在文件列表内的，不被允许上传

```shell
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

### 邮箱

[mail]
email_host = email_host
email_port = 465
email_host_user = email_host_user
email_host_password = email_host_password
default_from_email = default_from_email
email_from = email_from
email_use_ssl = True

