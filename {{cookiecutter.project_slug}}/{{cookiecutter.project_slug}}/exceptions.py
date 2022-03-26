import logging
from enum import Enum

from rest_framework.exceptions import APIException


log = logging.getLogger(__name__)


class ErrorCodes(Enum):
    """Error codes."""

    ERROR = "error"
    SERVER = "server"
    CLIENT = "client"


class BaseError(Exception):
    """Base class for all project errors (excluding API ones)."""

    default_detail = "There was a server error"
    default_code = ErrorCodes.ERROR.value

    def __init__(self, detail: str = None):
        if detail is None:
            detail = self.default_detail
        self.detail = detail


class BaseAPIError(APIException):
    """Base class for API errors."""
