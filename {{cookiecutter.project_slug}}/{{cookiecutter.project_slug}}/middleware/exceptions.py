import sentry_sdk

from django.http import HttpRequest, JsonResponse

from {{cookiecutter.project_slug}}.exceptions import ErrorCodes, TBContentError


class ExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        sentry_sdk.capture_exception(exception)

        error = {
            "detail": None,
            "errors": [
                {"message": str(exception), "code": ErrorCodes.ERROR.value},
            ],
        }
        if isinstance(exception, TBContentError):
            error = {
                "detail": None,
                "errors": [
                    {"message": exception.detail, "code": exception.default_code},
                ],
            }
        return JsonResponse(error)
