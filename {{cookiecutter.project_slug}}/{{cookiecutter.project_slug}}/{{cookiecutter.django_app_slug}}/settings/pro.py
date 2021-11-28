from .base import *  # noqa: F401, F403

{% if cookiecutter.use_sentry == 'y' -%}
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
{%- endif %}


DEBUG = False

ALLOWED_HOSTS = os.environ.get('PROJECT_ALLOWED_HOSTS', '').split(',')

CORS_ALLOWED_ORIGINS = os.environ.get('PROJECT_ALLOWED_CORS_ORIGINS', '').split(',')


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_PROD_DB'),
        'USER': os.environ.get('POSTGRES_PROD_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PROD_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_PROD_HOST'),
        'PORT': os.environ.get('POSTGRES_PROD_PORT'),
    },
}


# MEDIA
if USE_S3_BUCKET:
    # Yandex Object Storage settings
    YANDEX_STORAGE_CUSTOM_DOMAIN = f'{YANDEX_STORAGE_BUCKET_NAME}.storage.yandexcloud.net'
    DEFAULT_FILE_STORAGE = 'storage_backends.YandexObjectMediaStorage'
    AWS_ACCESS_KEY_ID = os.environ.get('YANDEX_STORAGE_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('YANDEX_STORAGE_SECRET_ACCESS_KEY')
    AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
    AWS_S3_REGION_NAME = 'ru-central1'

    # Media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{YANDEX_STORAGE_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
else:
    # MEDIA
    MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
    MEDIA_ROOT = BASE_DIR / '{{cookiecutter.django_app_slug}}/media/'


{% if cookiecutter.use_sentry == 'y' -%}
# SENTRY
SENTRY_CONF = sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
    ],
    send_default_pii=True,
)
{%- endif %}
