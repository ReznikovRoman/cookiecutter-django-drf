# {{cookiecutter.project_name}}
{{cookiecutter.project_short_description}}

## Technologies:
- Django 3
- DRF
- Postgres
- Celery
- Redis


## Configuration
Docker containers:
 1. db
 2. redis
 3. server
 4. celery
 5. celery_beat
 6. flower

docker-compose files:
 1. `docker-compose.yml` - for local development

To run docker containers you have to create a `.env` file in the root directory.

**Example of `.env` file:**

```dotenv
ENV=.env


# Python
PYTHONUNBUFFERED=


# Project
ENVIRONMENT=<local|test|prod>
DJANGO_SETTINGS_MODULE=<{{cookiecutter.django_app_slug}}.settings.local|{{cookiecutter.django_app_slug}}.settings.pro|{{cookiecutter.django_app_slug}}.settings.test>
SECRET_KEY="secure-key-912953fndfjndjkbnf2uhb5138"
PROJECT_ALLOWED_HOSTS=<host1,host2>
PROJECT_ALLOWED_CORS_ORIGINS=<host1,host2>
PROJECT_FULL_DOMAIN=<http://127.0.0.1>
SITE_DEFAULT_PROTOCOL=<http>


# Yandex Object Storage
USE_S3_BUCKET=<0|1>

# Optional
YANDEX_STORAGE_BUCKET_NAME=
YANDEX_STORAGE_ACCESS_KEY_ID=
YANDEX_STORAGE_SECRET_ACCESS_KEY=


# Media & staticfiles
MEDIA_URL=
STATIC_URL=


# Emails
EMAIL_HOST_USERNAME=<email@username>
EMAIL_HOST_PASSWORD=<email.password>


# Postgres
POSTGRES_DEFAULT_USER=
POSTGRES_DEFAULT_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=<db>
POSTGRES_PORT=

# Prod
POSTGRES_PROD_USER=
POSTGRES_PROD_PASSWORD=
POSTGRES_PROD_DB=
POSTGRES_PROD_HOST=
POSTGRES_PROD_PORT=

# Yandex.Cloud Managed PostgreSQL
USE_MANAGED_POSTGRES=<0|1>


# Celery
CELERY_BROKER_TRANSPORT=
CELERY_BROKER_HOST=<redis>
CELERY_BROKER_PORT=
CELERY_BROKER_VHOST=
CELERY_RESULT_BACKEND=<redis>


# Redis
REDIS_DECODE_RESPONSES=1
REDIS_PORT=6379
REDIS_URL=
REDIS_HOST=<redis>

# Redis DBs
REDIS_CACHE_DB=
REDIS_MAIN_DB=
REDIS_SESSION_DB=
CELERY_REDIS_DB=


# Flower
CELERY_BROKER_URL=
FLOWER_PORT=<8888>

{% if cookiecutter.use_sentry == 'y' -%}
# Sentry
SENTRY_DSN=
DJANGO_SENTRY_LOG_LEVEL=<CRITICAL|FATAL|ERROR|WARNING|WARN|INFO|DEBUG|NOTSET>
DJANGO_SENTRY_ENVIRONMENT=<production>
{%- endif %}


```

### Start project:

Local:
```shell
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

Migrations will be applied automatically.


## Code style:

Before pushing a commit run all linters:

```shell
docker-compose -f docker-compose.yml run --rm server sh -c "make check"
```

You also have to add a `makefile.env` file (for pre-commit):
```dotenv
# Your docker-compose file name
DOCKER_COMPOSE_FILENAME=<docker-compose.yml>
```

And then run linters:
```shell
make check-docker
```


### pre-commit:

To configure pre-commit on your local machine:
```shell
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml run --rm server sh -c "pre-commit install"
```

## Project guides

- [Python styleguide](./docs/guides/python_guide.md)
- [Django styleguide](./docs/guides/django_guide.md)
