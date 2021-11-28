from .base import *  # noqa: F401, F403


DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres_db'),
        'USER': os.environ.get('POSTGRES_DEFAULT_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_DEFAULT_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    },
}


# MEDIA
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = BASE_DIR / '{{cookiecutter.django_app_slug}}/media/'
