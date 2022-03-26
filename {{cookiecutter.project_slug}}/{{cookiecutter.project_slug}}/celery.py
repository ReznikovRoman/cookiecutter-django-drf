from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, ClassVar

import configurations
from celery import Celery
from celery.app.task import Task as _Task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from django.core.cache import cache
from django.utils import timezone


if TYPE_CHECKING:
    from celery.result import AsyncResult


configurations.setup()


from django.conf import settings  # noqa: E402


app = Celery(settings.PROJECT_NAME, task_cls='{{cookiecutter.project_slug}}.celery:Task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# CELERY PERIODIC TASKS
# https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
app.conf.beat_schedule = {}


class Task(_Task):
    # lock ttl for relaunching tasks, in seconds
    lock_ttl: ClassVar[int | None] = None

    # unique lock suffix: None, tuple or callable[tuple]
    lock_suffix: ClassVar[tuple | Callable | None] = None

    log: logging.Logger = get_task_logger(__name__)

    def __call__(self, *args, **kwargs):
        self.log.info(f'Starting task {self.request.id}')
        return super().__call__(*args, **kwargs)

    def get_lock_key(self, args, kwargs) -> str:
        lock_suffix = self.__class__.lock_suffix
        if lock_suffix:
            if callable(lock_suffix):
                lock_suffix = lock_suffix(*args or (), **kwargs or {})
        else:
            lock_suffix = ()
        return ':'.join(('task', self.name, *map(str, lock_suffix), 'lock'))

    def acquire_lock(self, lock_key: str, *, force: bool = False) -> bool:
        timestamp = timezone.now().timestamp()
        if force:
            self.log.debug(f'force=True, ignoring [{lock_key}]')
            cache.set(lock_key, timestamp, self.lock_ttl)
            return True
        elif not cache.add(lock_key, timestamp, self.lock_ttl):
            self.log.debug(f'[{lock_key}] is locked')
            return False
        self.log.debug(f'[{lock_key}] has been acquired')
        return True

    def delay(self, *args, force: bool = False, **kwargs) -> AsyncResult | None:
        if not self.lock_ttl:
            return super().apply_async(args, kwargs)
        lock_key = self.get_lock_key(args, kwargs)
        if self.acquire_lock(lock_key, force=force):
            return super().apply_async(args, kwargs)
        return None

    def apply_async(self, args=None, kwargs=None, *, force: bool = False, **options) -> AsyncResult | None:
        if not self.lock_ttl:
            return super().apply_async(args=args, kwargs=kwargs, **options)
        lock_key = self.get_lock_key(args, kwargs)
        if self.acquire_lock(lock_key, force=force):
            return super().apply_async(args=args, kwargs=kwargs, **options)
        return None
