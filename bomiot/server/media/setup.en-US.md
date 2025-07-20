# setup.ini

---

### Project Control

- Here controls which project directory bomiot points to

```shell
[project]
name = bomiot_example
```

### Database

- Supports multiple databases; the default is the sqlite engine. Supports (sqlite, mysql, oracle, postgresql)

```shell
[database]
engine = sqlite
name = db_name
user = db_user
password = db_pwd
host = db_host
port = db_port
```

### Path to the front-end index.html

- Located under the project directory, pointing to index.html, so it supports React, Angular, Vue, and Django's built-in templates

```shell
[templates]
name = templates/dist/spa/index.html
```

### Time Zone

- Generally not modified

```shell
[locale]
time_zone = 'UTC'
```

### Rate Limiting

- Limits the number of accesses per second, default is 10 times per second

```shell
[throttle]
allocation_seconds = 1
throttle_seconds = 10
```

### Login Restriction

- If the number of incorrect login attempts exceeds 3, the account will be locked

```shell
[request]
limit = 2
```

### JWT Validity Period for Front-end and Back-end Authentication

- Validity period of JWT Token

```shell
[jwt]
user_jwt_time = 1000000
```

### File Restrictions

- file_size is the file size, in bytes
- file_extension refers to file formats; those not in the list are not allowed to be uploaded

```shell
[file]
file_size = 102400000
file_extension = py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf
```

### Email

[mail]
email_host = email_host
email_port = 465
email_host_user = email_host_user
email_host_password = email_host_password
default_from_email = default_from_email
email_from = email_from
email_use_ssl = True

