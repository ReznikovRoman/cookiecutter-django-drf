from enum import Enum
from typing import Dict


class ExtendedEnum(Enum):

    @classmethod
    def names(cls) -> Dict[str, str]:
        return {item.name: item.name for item in cls}

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BaseChoicesEnum(ExtendedEnum):

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]
