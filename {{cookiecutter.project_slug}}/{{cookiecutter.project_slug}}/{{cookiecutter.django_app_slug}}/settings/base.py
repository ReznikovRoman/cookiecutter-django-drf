import os
from datetime import timedelta
from pathlib import Path
from typing import List

from django.contrib.messages import constants as messages_constants


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "{{ random_ascii_string(50) }}")


ALLOWED_HOSTS: List[str] = []


# Application definition
INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',

    # drf
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',

    # django 3rd party
    'debug_toolbar',
    'django_extensions',
    'django_filters',
    'django_celery_beat',
    'sorl.thumbnail',
    'storages',

    # cleanup
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = '{{cookiecutter.django_app_slug}}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{cookiecutter.django_app_slug}}.wsgi.application'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# FIXME: AUTH_USER_MODEL


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = '{{cookiecutter.timezone}}'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SITES
SITE_ID = 1
DEFAULT_PROTOCOL = os.environ.get("SITE_DEFAULT_PROTOCOL", "http")
PROJECT_FULL_DOMAIN = os.environ.get("PROJECT_FULL_DOMAIN", "http://localhost:8000")


# Static files (CSS, JavaScript, Images)
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = BASE_DIR / '{{cookiecutter.django_app_slug}}/static/'


# S3 Bucket
USE_S3_BUCKET = bool(os.environ.get("USE_S3_BUCKET", False))
YANDEX_STORAGE_BUCKET_NAME = os.environ.get("YANDEX_STORAGE_BUCKET_NAME")


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USERNAME')
DEFAULT_FROM_EMAIL = 'support@{{cookiecutter.django_app_slug}}.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# CHARSET
DEFAULT_CHARSET = "utf-8"


# MESSAGES
MESSAGE_TAGS = {
    messages_constants.DEBUG: 'alert-secondary',
    messages_constants.INFO: 'alert-info',
    messages_constants.SUCCESS: 'alert-success',
    messages_constants.WARNING: 'alert-warning',
    messages_constants.ERROR: 'alert-danger',
}


# DRF SPECTACULAR
SPECTACULAR_SETTINGS = {
    'TITLE': '{{cookiecutter.project_name}} API',
    'VERSION': None,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]+/',
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'SERVE_AUTHENTICATION': ['rest_framework.authentication.SessionAuthentication'],
    'SERVE_PERMISSIONS': ['api.permissions.IsSuperUser'],
    'SERVERS': [
        {'url': f'{PROJECT_FULL_DOMAIN}:8000/api/v1'},
    ],
}


# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# SIMPLE JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# REDIS
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB = os.environ.get('REDIS_MAIN_DB', 1)
REDIS_DECODE_RESPONSES = os.environ.get('REDIS_DECODE_RESPONSES', True)


# CACHES
REDIS_CACHE_DB = os.environ.get('REDIS_CACHE_DB', 2)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}


# SESSIONS
REDIS_SESSION_DB = os.environ.get('REDIS_SESSION_DB', 3)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': REDIS_SESSION_DB,
    'prefix': 'session',
    'socket_timeout': 1,
    'retry_on_timeout': False,
}


# CELERY
CELERY_TIMEZONE = '{{cookiecutter.timezone}}'
CELERY_BROKER_TRANSPORT = os.environ.get('CELERY_BROKER_HOST', "redis")
CELERY_BROKER_HOST = os.environ.get('CELERY_BROKER_HOST', "redis")
CELERY_BROKER_PORT = os.environ.get('CELERY_BROKER_PORT', '6379')
CELERY_BROKER_VHOST = os.environ.get("CELERY_REDIS_DB", 4)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis")

CELERY_REDIS_HOST = REDIS_HOST
CELERY_REDIS_PORT = REDIS_PORT
CELERY_REDIS_DB = CELERY_BROKER_VHOST

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
