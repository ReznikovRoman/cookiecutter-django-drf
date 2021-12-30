from typing import TypeVar

from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage

from {{cookiecutter.django_app_slug}}.storage_backends import YandexObjectMediaStorage


BaseStorageType = TypeVar('BaseStorageType', bound=Storage)


def select_file_storage() -> BaseStorageType:
    if settings.USE_S3_BUCKET and not settings.DEBUG:
        return YandexObjectMediaStorage()
    return FileSystemStorage()


def parse_bool_query_param(query_param: str) -> bool:
    return not(
            query_param == "false" or
            query_param == "0" or
            query_param == "" or
            query_param is None
    )
