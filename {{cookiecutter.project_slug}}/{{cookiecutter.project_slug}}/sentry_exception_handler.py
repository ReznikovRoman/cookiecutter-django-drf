from typing import Any

import sentry_sdk
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def sentry_exception_handler(exc: APIException, context: dict[str, Any]) -> Response | None:
    """Log all DRF exceptions to Sentry (including ValidationErrors)."""
    sentry_sdk.capture_exception(exc)

    response = exception_handler(exc, context)

    if response is None:
        return response

    return _process_exception(response, exc, context)


def _process_exception(response: Response, exc: APIException, context: dict[str, Any]) -> Response:
    if 'detail' in response.data:
        response.data = {
            "detail": None,
            "errors": [
                {"message": exc.detail, "code": exc.default_code},
            ],
        }
    else:
        errors = response.data.copy()
        response.data = []
        for field, exceptions in errors.items():
            error_dict = {
                "detail": field,
                "errors": [],
            }
            for exception in exceptions:
                error_code = getattr(exception, "default_code", exception.code)
                error_dict['errors'].append({"message": exception, "code": error_code})
            response.data.append(error_dict)
    return response
