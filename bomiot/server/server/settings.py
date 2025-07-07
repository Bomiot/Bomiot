from pathlib import Path
from django.core.management.utils import get_random_secret_key
import os
import sys
from configparser import ConfigParser
import importlib.metadata
import bomiot
from bomiot.server.server.pkgcheck import pkg_check, cwd_check, ignore_pkg, ignore_cwd
import importlib.util
from os import listdir
from os.path import join, isdir, exists, isfile


BASE_DIR = join(Path(bomiot.__file__).resolve().parent, 'server')

WORKING_SPACE_CONFIG = ConfigParser()
WORKING_SPACE_CONFIG.read(join(BASE_DIR, 'workspace.ini'), encoding='utf-8')
WORKING_SPACE = WORKING_SPACE_CONFIG.get('space', 'name', fallback='Create your working space first')
sys.path.insert(0, WORKING_SPACE)

CONFIG = ConfigParser()
setup_ini_path = join(WORKING_SPACE, 'setup.ini')
CONFIG.read(setup_ini_path, encoding='utf-8')
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')

SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
AUTH_USER_MODEL = "core.User"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'django_apscheduler',
    'bomiot.server.core',
]

all_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
res_pkg_list = list(set([name.lower() for name in all_packages]).difference(set(ignore_pkg())))
pkg_squared = list(map(lambda data: pkg_check(data), res_pkg_list))
filtered_pkg_squared = list(filter(lambda x: x is not None, pkg_squared))

current_path = list(set([p for p in listdir(WORKING_SPACE) if isdir(p)]).difference(set(ignore_cwd())))
cur_squared = list(map(lambda data: cwd_check(data), current_path))
filtered_current_path = list(filter(lambda y: y is not None, cur_squared))

def load_dynamic_apps() -> None:
    global INSTALLED_APPS
    load_apps_from_project()
    load_apps_from_working_space()
    load_apps_from_packages()
    

def load_apps_from_packages() -> None:
    global INSTALLED_APPS
    all_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    res_pkg_list = list(set([name.lower() for name in all_packages]).difference(set(ignore_pkg())))
    for module in res_pkg_list:
        spec = importlib.util.find_spec(module)
        if not spec:
            continue
        module_path = spec.origin
        if not module_path:
            continue
        module_dir = Path(module_path).resolve().parent
        config_path = join(module_dir, 'bomiotconf.ini')
        pkg_config = ConfigParser()
        if pkg_config.read(config_path, encoding='utf-8'):
            app_mode = pkg_config.get('mode', 'name', fallback='plugins')
            if app_mode == 'plugins':
                apps_py_path = join(module_dir, 'apps.py')
                if isfile(apps_py_path):
                    app_name = module
                    if app_name not in INSTALLED_APPS:
                        INSTALLED_APPS.append(app_name)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue

def load_apps_from_working_space() -> None:
    global INSTALLED_APPS
    current_path = [
        p for p in listdir(WORKING_SPACE) 
        if isdir(join(WORKING_SPACE, p)) and p not in ignore_cwd()
    ]
    for module_name in current_path:
        module_dir = join(WORKING_SPACE, module_name)
        config_path = join(module_dir, 'bomiotconf.ini')
        app_mode_config = ConfigParser()
        if not app_mode_config.read(config_path, encoding='utf-8'):
            continue
        app_mode = app_mode_config.get('mode', 'name')
        if app_mode == 'plugins':
            apps_py_path = join(module_dir, 'apps.py')
            if isfile(apps_py_path):
                if module_name not in INSTALLED_APPS:
                    INSTALLED_APPS.append(module_name)
                else:
                    continue
            else:
                continue
        else:
            continue

def load_apps_from_project() -> None:
    global INSTALLED_APPS, PROJECT_NAME
    if not PROJECT_NAME or PROJECT_NAME not in [p for p in listdir(WORKING_SPACE) if isdir(p)]:
        return
    project_path = join(WORKING_SPACE, PROJECT_NAME)
    app_dirs = [
        app for app in listdir(project_path) 
        if isdir(join(project_path, app))
    ]
    for app in app_dirs:
        apps_py_path = join(project_path, app, 'apps.py')
        if isfile(apps_py_path):
            app_name = f'{PROJECT_NAME}.{app}'
            if app_name not in INSTALLED_APPS:
                INSTALLED_APPS.append(app_name)
            else:
                continue
        else:
            continue

load_dynamic_apps()

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bomiot.server.server.urls'

TEMPLATES_PATH = join(WORKING_SPACE, PROJECT_NAME)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'bomiot.server.server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
BASE_DB_TABLE = 'bomiot'

DATABASE_MAP = {
    'sqlite': 'django.db.backends.sqlite3',
    'mysql': 'django.db.backends.mysql',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'oracle': 'django.db.backends.oracle',
}

db_engine = CONFIG.get('database', 'engine', fallback='sqlite')
if db_engine == 'sqlite':
    DB_DIR = join(WORKING_SPACE, 'dbs')
    exists(DB_DIR) or os.makedirs(DB_DIR)
    DB_PATH = join(DB_DIR, 'db.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_PATH,
            'CONN_MAX_AGE': 60,
            'OPTIONS': {
                'timeout': 60,
            }
        }
    }
elif db_engine == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': DATABASE_MAP[CONFIG['database']['engine']],
            'NAME': CONFIG['database']['name'],
            'USER': CONFIG['database']['user'],
            'PASSWORD': CONFIG['database']['password'],
            'HOST': CONFIG['database']['host'],
            'PORT': CONFIG['database']['port'],
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DATABASE_MAP[CONFIG['database']['engine']],
            'NAME': CONFIG['database']['name'],
            'USER': CONFIG['database']['user'],
            'PASSWORD': CONFIG['database']['password'],
            'HOST': CONFIG['database']['host'],
            'PORT': CONFIG['database']['port'],
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
if PROJECT_NAME == 'bomiot':
    LANGUAGE_DIR = join(BASE_DIR, 'language').replace('\\', '/')
else:
    LANGUAGE_DIR = join(join(WORKING_SPACE, PROJECT_NAME), 'language').replace('\\', '/')
if exists(join(WORKING_SPACE, PROJECT_NAME)):
    exists(LANGUAGE_DIR) or os.makedirs(LANGUAGE_DIR)

TIME_ZONE = CONFIG.getint('local', 'time_zone', fallback='UTC')

USE_I18N = True

USE_L10N = True  # (localization)

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
if PROJECT_NAME == 'bomiot':
    STATIC_ROOT = join(BASE_DIR, 'bomiot_static').replace('\\', '/')
    STATICFILES_DIRS = [
        join(BASE_DIR, "static").replace('\\', '/'),
    ]
else:
    STATIC_ROOT = join(join(WORKING_SPACE, PROJECT_NAME), 'bomiot_static').replace('\\', '/')
    STATICFILES_DIRS = [
        join(join(WORKING_SPACE, PROJECT_NAME), 'static').replace('\\', '/')
    ]

MEDIA_URL = 'media/'
if PROJECT_NAME == 'bomiot':
    MEDIA_ROOT = join(BASE_DIR, 'media').replace('\\', '/')
else:
    MEDIA_ROOT = join(join(WORKING_SPACE, PROJECT_NAME), 'media').replace('\\', '/')
if exists(join(WORKING_SPACE, PROJECT_NAME)):
    exists(MEDIA_ROOT) or os.makedirs(MEDIA_ROOT)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'language',
    'operator',
    'device',
    'app-id',
    'event-sign'
)

CORS_EXPOSE_HEADERS = [
    "expire"
]

X_FRAME_OPTIONS = 'SAMEORIGIN'


LOG_PATH = join(WORKING_SPACE, 'logs')
exists(LOG_PATH) or os.makedirs(LOG_PATH)
SERVER_LOGS_FILE = join(LOG_PATH, 'server.log')
ERROR_LOGS_FILE = join(LOG_PATH, 'error.log')
STANDARD_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)
CONSOLE_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": STANDARD_LOG_FORMAT},
        "console": {
            "format": CONSOLE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file": {
            "format": CONSOLE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": SERVER_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 3,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },

    },
    "loggers": {
        "": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
        },
        'apscheduler': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        "django": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
            "propagate": False,
        },
        'django.db.backends': {
            'handlers': ["console", "error", "file"],
            'propagate': False,
            'level': "INFO"
        }
    },
}

REST_FRAMEWORK = {
    # AttributeError: 'AutoSchema' object has no attribute 'get_link'
    # DEFAULT SET:
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    # EXCEPTION:
    'EXCEPTION_HANDLER': 'bomiot.server.core.my_exceptions.custom_exception_handler',
    # Base API policies:
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
        #'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': ['bomiot.server.core.auth.CoreAuthentication', ],
    'DEFAULT_PERMISSION_CLASSES': ["bomiot.server.core.permission.CorePermission", ],
    'DEFAULT_THROTTLE_CLASSES': ['bomiot.server.core.throttle.CoreThrottle', ],
    # 'DEFAULT_THROTTLE_RATES': ['utils.throttle.VisitThrottle', ],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': None,
    'DEFAULT_PAGINATION_CLASS': 'bomiot.server.core.page.CorePageNumberPagination',
    # 'PAGE_SIZE': 1,  # 默认 None
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'django_filters.rest_framework.backends.DjangoFilterBackend',
    ],
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'NUM_PROXIES': None,
    # Versioning:
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',
    # Authentication:
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    'UNAUTHENTICATED_TOKEN': None,
    # View configuration:
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
    # Testing
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',
    # Hyperlink settings
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',
    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,
    # Browseable API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",
    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]

USER_JWT_TIME = CONFIG.getint('jwt', 'user_jwt_time', fallback=1000000)
JWT_SALT = 'ds()udsjo@jlsdosjf)wjd_#(#)$'

KEY_PATH = join(WORKING_SPACE, 'auth_key.py')
KEY = ''
if exists(KEY_PATH):
    try:
        with open(KEY_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('KEY') and '=' in line:
                key_value = line.split('=', 1)[1].strip()
                if key_value.startswith("'") and key_value.endswith("'"):
                    key_value = key_value[1:-1]
                elif key_value.startswith('"') and key_value.endswith('"'):
                    key_value = key_value[1:-1]
                KEY = key_value
                break
    except Exception as e:
        print(f"Error reading auth_key.py: {e}")
        KEY = ''

ALLOCATION_SECONDS = CONFIG.getint('throttle', 'allocation_seconds', fallback=1)
THROTTLE_SECONDS = CONFIG.getint('throttle', 'throttle_seconds', fallback=10)

REQUEST_LIMIT = CONFIG.getint('request', 'limit', fallback=2)

DATA_UPLOAD_MAX_MEMORY_SIZE = None

FILE_SIZE = CONFIG.getint('file', 'file_size', fallback=102400000)
FILE_EXTENSION = CONFIG.get('file', 'file_extension', fallback='py,png,jpg,jpeg,gif,bmp,webp,txt,md,html,htm,js,css,json,xml,csv,xlsx,xls,ppt,pptx,doc,docx,pdf').replace(" ", "").split(',')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.get('mail', 'email_host', fallback='')
EMAIL_PORT = CONFIG.getint('mail', 'email_port', fallback=465)
EMAIL_HOST_USER = CONFIG.get('mail', 'email_host_user', fallback='')
EMAIL_HOST_PASSWORD = CONFIG.get('mail', 'email_host_password', fallback='')
DEFAULT_FROM_EMAIL = CONFIG.get('mail', 'default_from_email', fallback='')
EMAIL_FROM = CONFIG.get('mail', 'email_from', fallback='')
EMAIL_USE_SSL = CONFIG.getboolean('mail', 'email_use_ssl', fallback=True)