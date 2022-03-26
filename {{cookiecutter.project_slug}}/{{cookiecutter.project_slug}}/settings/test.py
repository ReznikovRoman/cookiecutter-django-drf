from .base import Base


class Test(Base):
    PROJECT_ENVIRONMENT = 'test'

    DEBUG = False

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    }
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    CELERY_BROKER_URL = 'memory://'
    SENTRY_DSN = None
