from .base import Base
from .production import Production
from .test import Test


try:
    from .local import Local
except ImportError:
    LOCAL_CONFIGURATION_EXISTS = False
else:
    LOCAL_CONFIGURATION_EXISTS = True

__all__ = [
    'Base',
    'Production',
    'Test',
]

if LOCAL_CONFIGURATION_EXISTS:
    __all__ += ['Local']
