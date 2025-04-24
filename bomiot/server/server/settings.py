from pathlib import Path
from django.core.management.utils import get_random_secret_key
import os
import sys
from configparser import ConfigParser
import pkg_resources
from .pkgcheck import pkg_check, cwd_check, ignore_pkg, ignore_cwd
import importlib.util
from os import listdir
from os.path import join, isdir, exists, isfile


BASE_DIR = Path(__file__).resolve().parent.parent


CONFIG = ConfigParser()
WORKING_SPACE_CONFIG = ConfigParser()
WORKING_SPACE_CONFIG.read(join(BASE_DIR, 'workspace.ini'), encoding='utf-8')
WORKING_SPACE = WORKING_SPACE_CONFIG.get('space', 'name', fallback='Create your working space first')
sys.path.insert(0, WORKING_SPACE)
CONFIG.read(join(WORKING_SPACE, 'setup.ini'), encoding='utf-8')
PROJECT_NAME = CONFIG.get('project', 'name', fallback='bomiot')

SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = ['*']
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


res_pkg_list = list(set([pkg.key for pkg in pkg_resources.working_set]).difference(set(ignore_pkg())))
pkg_squared = list(map(lambda data: pkg_check(data), res_pkg_list))
filtered_pkg_squared = list(filter(lambda x: x is not None, pkg_squared))

current_path = list(set([p for p in listdir(WORKING_SPACE) if isdir(p)]).difference(set(ignore_cwd())))
cur_squared = list(map(lambda data: cwd_check(data), current_path))
filtered_current_path = list(filter(lambda y: y is not None, cur_squared))

LOCALE_PATHS = []

if len(filtered_pkg_squared) > 0:
    for module in filtered_pkg_squared:
        module_path = importlib.util.find_spec(PROJECT_NAME).origin
        list_module_path = Path(module_path).resolve().parent
        pkg_config_check = ConfigParser()
        pkg_config_check.read(join(list_module_path), 'bomiotconf.ini', encoding='utf-8')
        LOCALE_PATHS.append(join(list_module_path, 'locale'))
        app_mode = pkg_config_check.get('mode', 'name', fallback='plugins')
        if app_mode == 'plugins':
            try:
                if isfile(join(list_module_path, 'apps.py')):
                    if module not in INSTALLED_APPS:
                        INSTALLED_APPS.append(f'{module}')
            except:
                continue
        elif app_mode == 'project':
            if module == PROJECT_NAME:
                for app in listdir(list_module_path):
                    try:
                        if isfile(join(join(list_module_path, app), 'apps.py')):
                            if app not in INSTALLED_APPS:
                                INSTALLED_APPS.append(f'{app}')
                    except:
                        pass

if len(filtered_current_path) > 0:
    for module_name in filtered_current_path:
        app_mode_config = ConfigParser()
        app_mode_config.read(join(join(WORKING_SPACE, module_name), 'bomiotconf.ini'), encoding='utf-8')
        LOCALE_PATHS.append(join(join(WORKING_SPACE, module_name), 'locale'))
        app_mode = app_mode_config.get('mode', 'name')
        if app_mode == 'plugins':
            try:
                if isfile(join(join(WORKING_SPACE, module_name), 'apps.py')):
                    if module_name not in INSTALLED_APPS:
                        INSTALLED_APPS.append(module_name)
            except:
                continue
        elif app_mode == 'project':
            if module_name == PROJECT_NAME:
                project_path = join(WORKING_SPACE, PROJECT_NAME)
                for app in listdir(project_path):
                    try:
                        if isfile(join(join(project_path, app), 'apps.py')):
                            if f'{PROJECT_NAME}.{app}' not in INSTALLED_APPS:
                                INSTALLED_APPS.append(f'{PROJECT_NAME}.{app}')
                    except:
                        pass


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bomiot.server.core.middlewares.JwtAuthorizationMiddleware'
]

ROOT_URLCONF = 'bomiot.server.server.urls'

TEMPLATES_PATH = join(BASE_DIR.parent, 'templates')

if PROJECT_NAME in [p for p in listdir(WORKING_SPACE) if isdir(p)]:
    TEMPLATES_PATH = join(join(WORKING_SPACE, PROJECT_NAME), 'templates')


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
            'OPTIONS': {
                'timeout': 20,
            }
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
exists(LANGUAGE_DIR) or os.makedirs(LANGUAGE_DIR)

TIME_ZONE = CONFIG.getint('local', 'time_zone', fallback='UTC')

USE_I18N = True

USE_L10N = True  # 开启本地化(localization)

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
            "backupCount": 5,  # 最多备份5个
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 3,  # 最多备份3个
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
        "django": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
            "propagate": False,
        },
        'django.db.backends': {
            'handlers': ["console", "error", "file"],
            'propagate': False,
            'level': "INFO"
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console", "error", "file"],
        },
        "uvicorn.access": {
            "handlers": ["console", "error", "file"],
            "level": "INFO"
        },
    },
}

REST_FRAMEWORK = {
    # AttributeError: ‘AutoSchema’ object has no attribute ‘get_link’
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

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]

USER_JWT_TIME = CONFIG.getint('jwt', 'user_jwt_time', fallback=1000000)

ALLOCATION_SECONDS = CONFIG.getint('throttle', 'allocation_seconds', fallback=1)
THROTTLE_SECONDS = CONFIG.getint('throttle', 'throttle_seconds', fallback=10)

DATA_UPLOAD_MAX_MEMORY_SIZE = None