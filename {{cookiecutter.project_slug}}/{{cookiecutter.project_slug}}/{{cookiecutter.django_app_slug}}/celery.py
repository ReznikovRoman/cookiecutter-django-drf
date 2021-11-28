import os

from celery import Celery


settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', '{{cookiecutter.django_app_slug}}.settings.local')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

app = Celery('{{cookiecutter.django_app_slug}}')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# CELERY PERIODIC TASKS
# https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
