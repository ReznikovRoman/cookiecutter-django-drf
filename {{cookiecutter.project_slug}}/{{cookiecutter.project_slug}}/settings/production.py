from datetime import timedelta

from .base import Base
from .values import from_environ


class Production(Base):
    DEBUG = False
    ALLOWED_HOSTS = from_environ(type=list)
    CSRF_TRUSTED_ORIGINS = from_environ(type=list)

    # Django CORS Headers
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = from_environ(type=list)

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
