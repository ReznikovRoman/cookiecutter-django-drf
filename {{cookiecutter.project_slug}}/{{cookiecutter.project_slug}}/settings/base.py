from __future__ import annotations

import datetime
import logging
from datetime import timedelta
from pathlib import Path
from urllib.parse import urljoin

import sentry_sdk
from configurations import Configuration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from django.utils.functional import cached_property

from {{cookiecutter.project_slug}}.logging import LoggerDescriptor

from .values import from_environ


class Base(Configuration):
    log = LoggerDescriptor(__name__)

    PROJECT_NAME = '{{cookiecutter.project_slug}}'
    PROJECT_BASE_URL = from_environ('http://localhost')
    PROJECT_ENVIRONMENT = from_environ('unknown')
    # Fix relative MEDIA_URL и STATIC_URL and create absolute ones with PROJECT_BASE_URL
    FIX_RELATIVE_URLS = from_environ(True)

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    ALLOWED_HOSTS = []
    CSRF_TRUSTED_ORIGINS = []

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = from_environ("{{ random_ascii_string(50) }}")

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
        'storages',
        'tinymce',
        'django_object_actions',

        # cleanup
        'django_cleanup.apps.CleanupConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',

        'corsheaders.middleware.CorsMiddleware',

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        '{{cookiecutter.project_slug}}.middleware.exceptions.ExceptionsMiddleware',
    ]

    ROOT_URLCONF = '{{cookiecutter.project_slug}}.urls'
    WSGI_APPLICATION = '{{cookiecutter.project_slug}}.wsgi.application'
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': from_environ(name='DB_NAME'),
            'USER': from_environ(name='DB_USER'),
            'PASSWORD': from_environ(name='DB_PASSWORD'),
            'HOST': from_environ(name='DB_HOST'),
            'PORT': from_environ(name='DB_PORT', type=int),
        },
    }

    # Cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': from_environ(name='REDIS_CACHE_URL'),
            'KEY_PREFIX': PROJECT_NAME.lower(),
        },
    }

    # Password validation
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
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = '{{cookiecutter.timezone}}'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # STATIC
    STATIC_URL = from_environ('/staticfiles/')
    STATIC_ROOT = PROJECT_ROOT / 'staticfiles'

    # MEDIA
    MEDIA_URL = from_environ('/media/')
    MEDIA_ROOT = PROJECT_ROOT / 'media'

    # TEMPLATES
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

    # AUTHENTICATION
    LOGIN_URL = '/'
    LOGIN_REDIRECT_URL = '/'
    USER_FIELDS = ['email']
    # AUTH_USER_MODEL = 'profiles.User'  # TODO: custom User model
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
    ]

    # EMAIL
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = from_environ(name="EMAIL_HOST_USERNAME")
    DEFAULT_FROM_EMAIL = 'support@{{cookiecutter.project_slug}}.com'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = from_environ()
    DEFAULT_SENDER = f'{PROJECT_NAME} <{DEFAULT_FROM_EMAIL}>'
    DEFAULT_TO_EMAIL = []

    @cached_property
    def LOGGING(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '[ %(levelname)-7s ] %(asctime)s %(name)s: %(message)s',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        }

    # CONFIGURATION
    DISABLE_THROTTLING = from_environ(default=False, type=bool)

    # REST_FRAMEWORK
    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
        'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
        'DEFAULT_AUTHENTICATION_CLASSES': ['{{cookiecutter.project_slug}}.api.authentication.TokenAuthentication'],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
        ],
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'EXCEPTION_HANDLER': '{{cookiecutter.project_slug}}.sentry_exception_handler.sentry_exception_handler',
        'DEFAULT_THROTTLE_CLASSES': [
            'rest_framework.throttling.AnonRateThrottle',
        ],
        'DEFAULT_THROTTLE_RATES': {
            'anon': '100/min',
        },
    }

    # SIMPLE JWT
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
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

    @cached_property
    def SPECTACULAR_SETTINGS(self):
        return {
            'TITLE': f'{self.PROJECT_NAME} API',
            'VERSION': None,
            'SCHEMA_PATH_PREFIX': r'/api/v[0-9]+/',
            'SCHEMA_PATH_PREFIX_TRIM': True,
            'SERVE_AUTHENTICATION': ['rest_framework.authentication.SessionAuthentication'],
            'SERVE_PERMISSIONS': ['{{cookiecutter.project_slug}}.api.permissions.IsSuperUser'],
            'SERVERS': [{'url': f'{self.PROJECT_BASE_URL}/api/v1'}],
        }

    # REDIS
    REDIS_HOST = from_environ("localhost")
    REDIS_PORT = from_environ(6379)
    REDIS_DB = from_environ(1, name="REDIS_MAIN_DB", type=int)
    REDIS_DECODE_RESPONSES = from_environ(True, type=bool)

    # Celery
    CELERY_TIMEZONE = '{{cookiecutter.timezone}}'
    CELERY_BROKER_URL = from_environ(name='REDIS_BROKER_URL')
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TASK_DEFAULT_QUEUE = f'{PROJECT_NAME.lower()}_default'
    CELERY_TASK_RESULT_EXPIRES = datetime.timedelta(hours=1)
    CELERY_RESULT_BACKEND = from_environ("redis")
    CELERY_REDIS_MAX_CONNECTIONS = 20
    CELERYD_MAX_TASKS_PER_CHILD = 100

    {% if cookiecutter.use_sentry == 'y' -%}
    # Sentry settings
    SENTRY_DSN = from_environ(None)
    SENTRY_TRACES_SAMPLE_RATE = from_environ(1.0, type=float)
    {%- endif %}

    # TINYMCE
    TINYMCE_DEFAULT_CONFIG = {
        'plugins': (
            'print preview textcolor importcss searchreplace autolink autosave save directionality visualblocks '
            'visualchars fullscreen image link media codesample table charmap hr pagebreak nonbreaking anchor toc '
            'insertdatetime advlist lists wordcount textpattern noneditable help charmap emoticons'
        ),
        'toolbar': (
            'insert | undo redo | formatselect | bold italic backcolor forecolor | '
            'alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help'
        ),
        'cleanup_on_startup': True,
        'custom_undo_redo_levels': 10,
        'width': 'auto',
        'language': 'ru',
    }

    # SESSIONS
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False

    # FILES
    FILE_UPLOAD_PERMISSIONS = 0o777
    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777
    FILE_UPLOAD_HANDLERS = [
        'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    ]
    DIRECTORY = ''

    # S3 Bucket
    USE_S3_BUCKET = from_environ(False, type=bool)
    YANDEX_STORAGE_BUCKET_NAME = from_environ("", type=str)

    # CHARSET
    DEFAULT_CHARSET = from_environ("utf-8")

    # https://github.com/jazzband/django-configurations/issues/323
    _DEFAULT_AUTO_FIELD = DEFAULT_AUTO_FIELD

    # SITES
    SITE_ID = 1
    DEFAULT_PROTOCOL = from_environ("http", name="SITE_DEFAULT_PROTOCOL")

    @classmethod
    def setup(cls):
        super().setup()
        # https://github.com/jazzband/django-configurations/issues/323
        cls.DEFAULT_AUTO_FIELD = cls._DEFAULT_AUTO_FIELD
        if cls.FIX_RELATIVE_URLS:
            cls._fix_relative_urls()

    @classmethod
    def post_setup(cls):
        super().post_setup()
        logging.basicConfig(level=logging.INFO, format='*** %(message)s')
        cls.log.info(f'Starting {cls.PROJECT_NAME} project using {cls.__name__} configuration')

        {% if cookiecutter.use_sentry == 'y' -%}
        if cls.SENTRY_DSN:
            cls.log.info(f'Sentry is enabled, environment: {cls.PROJECT_ENVIRONMENT}')
            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                environment=cls.PROJECT_ENVIRONMENT,
                integrations=[
                    DjangoIntegration(),
                    CeleryIntegration(),
                    RedisIntegration(),
                ],
                traces_sample_rate=cls.SENTRY_TRACES_SAMPLE_RATE,
                send_default_pii=True,
            )
        else:
            cls.log.info('Sentry is disabled')
        {%- endif %}

    @classmethod
    def _fix_relative_urls(cls):
        for url_attr in ['STATIC_URL', 'MEDIA_URL']:
            url: str = getattr(cls, url_attr)
            if url.startswith('/'):
                url = urljoin(cls.PROJECT_BASE_URL, url)
            if not url.endswith('/'):
                url = f'{url}/'
            setattr(cls, url_attr, url)
