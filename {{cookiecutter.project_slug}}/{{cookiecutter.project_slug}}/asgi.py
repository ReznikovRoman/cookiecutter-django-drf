import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.project_slug}}.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

from configurations.asgi import get_asgi_application


application = get_asgi_application()
